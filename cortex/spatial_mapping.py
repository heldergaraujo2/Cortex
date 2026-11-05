"""Cross-validated feasibility audit for mapping neuron coordinates to medulla p/q.

This diagnostic tests generalization on already-assigned neurons only. It never
assigns columns to unassigned candidate neurons or interprets coordinates as
visual directions.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, median
from typing import Iterable

from cortex.spatial import ColumnAssignment


@dataclass(frozen=True, slots=True)
class CoordinateRecord:
    root_id: str
    x: float
    y: float
    z: float
    sample_count: int
    bbox_diagonal: float
    unique_supervoxel_ids: int
    repeated_root_supervoxel_pairs: int
    conflicting_root_supervoxel_pairs: int
    exact_duplicate_position_rows: int


@dataclass(frozen=True, slots=True)
class MappingSample:
    root_id: str
    cell_type: str
    hemisphere: str
    coordinates: tuple[float, float, float]
    p: int
    q: int


def load_coordinate_records(path: str | Path) -> dict[str, CoordinateRecord]:
    """Aggregate all supplied positions per root ID; repeated supervoxel pairs are retained."""
    source = Path(path)
    samples_by_root: dict[str, list[tuple[str, tuple[float, float, float]]]] = defaultdict(list)
    with gzip.open(source, "rt", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"root_id", "position", "supervoxel_id"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"{source.name}: expected columns {sorted(required)}")
        for line_number, row in enumerate(reader, start=2):
            root_id = (row.get("root_id") or "").strip()
            supervoxel_id = (row.get("supervoxel_id") or "").strip()
            if not root_id or not supervoxel_id:
                raise ValueError(f"{source.name}:{line_number}: empty root_id/supervoxel_id")
            values = re.findall(
                r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?",
                row.get("position") or "",
            )
            if len(values) != 3:
                raise ValueError(
                    f"{source.name}:{line_number}: expected 3D position, got {row.get('position')!r}"
                )
            xyz = tuple(float(value) for value in values)
            if not all(math.isfinite(value) for value in xyz):
                raise ValueError(f"{source.name}:{line_number}: non-finite position")
            samples_by_root[root_id].append(
                (supervoxel_id, (xyz[0], xyz[1], xyz[2]))
            )

    result: dict[str, CoordinateRecord] = {}
    for root_id, samples in samples_by_root.items():
        points = [point for _, point in samples]
        medians = tuple(median(point[axis] for point in points) for axis in range(3))
        ranges = tuple(
            max(point[axis] for point in points) - min(point[axis] for point in points)
            for axis in range(3)
        )
        by_supervoxel: dict[str, list[tuple[float, float, float]]] = defaultdict(list)
        for supervoxel_id, point in samples:
            by_supervoxel[supervoxel_id].append(point)
        repeated_pairs = sum(len(values) > 1 for values in by_supervoxel.values())
        conflicting_pairs = sum(
            len(set(values)) > 1 for values in by_supervoxel.values()
        )
        exact_duplicate_rows = sum(
            len(values) - len(set(values)) for values in by_supervoxel.values()
        )
        result[root_id] = CoordinateRecord(
            root_id,
            medians[0],
            medians[1],
            medians[2],
            len(points),
            math.sqrt(sum(value * value for value in ranges)),
            len(by_supervoxel),
            repeated_pairs,
            conflicting_pairs,
            exact_duplicate_rows,
        )
    return result


def _solve_linear_system(matrix: list[list[float]], vector: list[float]) -> list[float] | None:
    size = len(vector)
    augmented = [row[:] + [vector[index]] for index, row in enumerate(matrix)]
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1e-12:
            return None
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        augmented[column] = [value / divisor for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor:
                augmented[row] = [
                    augmented[row][index] - factor * augmented[column][index]
                    for index in range(size + 1)
                ]
    return [augmented[index][-1] for index in range(size)]


def _fit_affine(
    samples: list[MappingSample],
    target: str,
) -> tuple[tuple[float, ...], tuple[float, ...], tuple[int, ...], tuple[float, ...]] | None:
    if len(samples) < 4:
        return None
    means = tuple(mean(sample.coordinates[axis] for sample in samples) for axis in range(3))
    scales = []
    for axis in range(3):
        variance = mean((sample.coordinates[axis] - means[axis]) ** 2 for sample in samples)
        scale = math.sqrt(variance)
        scales.append(scale if scale > 1e-9 else 0.0)
    active_axes = tuple(axis for axis, scale in enumerate(scales) if scale > 0)
    feature_count = 1 + len(active_axes)
    if len(samples) < feature_count:
        return None

    design = []
    targets = []
    for sample in samples:
        row = [1.0]
        row.extend(
            (sample.coordinates[axis] - means[axis]) / scales[axis]
            for axis in active_axes
        )
        design.append(row)
        targets.append(float(sample.p if target == "p" else sample.q))

    xtx = [[sum(row[i] * row[j] for row in design) for j in range(feature_count)]
           for i in range(feature_count)]
    xty = [sum(row[i] * value for row, value in zip(design, targets))
           for i in range(feature_count)]
    coefficients = _solve_linear_system(xtx, xty)
    if coefficients is None:
        return None
    return means, tuple(scales), active_axes, tuple(coefficients)


def _predict(
    model: tuple[tuple[float, ...], tuple[float, ...], tuple[int, ...], tuple[float, ...]],
    xyz: tuple[float, float, float],
) -> float:
    means, scales, axes, coefficients = model
    features = [1.0]
    features.extend((xyz[axis] - means[axis]) / scales[axis] for axis in axes)
    return sum(feature * coefficient for feature, coefficient in zip(features, coefficients))


def _mapping_metrics(
    train: list[MappingSample],
    test: list[MappingSample],
) -> dict[str, object]:
    if not train or not test:
        return {"train_rows": len(train), "test_rows": len(test), "status": "insufficient_split"}
    p_model = _fit_affine(train, "p")
    q_model = _fit_affine(train, "q")
    if p_model is None or q_model is None:
        return {"train_rows": len(train), "test_rows": len(test), "status": "rank_deficient"}
    errors = []
    p_errors = []
    q_errors = []
    exact = 0
    within_one = 0
    for sample in test:
        p_value = _predict(p_model, sample.coordinates)
        q_value = _predict(q_model, sample.coordinates)
        p_rounded, q_rounded = round(p_value), round(q_value)
        p_error, q_error = abs(p_value - sample.p), abs(q_value - sample.q)
        p_errors.append(p_error)
        q_errors.append(q_error)
        errors.append(math.sqrt(p_error * p_error + q_error * q_error))
        exact += int(p_rounded == sample.p and q_rounded == sample.q)
        within_one += int(abs(p_rounded - sample.p) <= 1 and abs(q_rounded - sample.q) <= 1)
    return {
        "train_rows": len(train),
        "test_rows": len(test),
        "status": "ok",
        "p_mae": mean(p_errors),
        "q_mae": mean(q_errors),
        "pq_euclidean_rmse": math.sqrt(mean(error * error for error in errors)),
        "exact_integer_pq_match_rate": exact / len(test),
        "within_one_lattice_step_rate": within_one / len(test),
    }


def _hemisphere_accuracy(train: list[MappingSample], test: list[MappingSample]) -> dict[str, object]:
    centroids: dict[str, tuple[float, float, float]] = {}
    for hemisphere in ("left", "right"):
        members = [sample for sample in train if sample.hemisphere == hemisphere]
        if not members:
            return {"status": "insufficient_hemisphere_training"}
        centroids[hemisphere] = tuple(
            mean(sample.coordinates[axis] for sample in members) for axis in range(3)
        )
    if not test:
        return {"status": "empty_test"}
    correct = 0
    for sample in test:
        distances = {
            hemisphere: sum(
                (sample.coordinates[axis] - centroid[axis]) ** 2 for axis in range(3)
            )
            for hemisphere, centroid in centroids.items()
        }
        prediction = min(distances, key=distances.get)
        correct += int(prediction == sample.hemisphere)
    return {"status": "ok", "test_rows": len(test), "accuracy": correct / len(test)}


def audit_coordinate_to_column_mapping(
    coordinates_path: str | Path,
    assignments: Iterable[ColumnAssignment],
) -> dict[str, object]:
    coordinates_file = Path(coordinates_path)
    coordinates = load_coordinate_records(coordinates_file)
    assignment_rows = tuple(assignments)
    samples = []
    missing_coordinate_ids = []
    seen_assignment_ids = set()
    for assignment in assignment_rows:
        if assignment.root_id in seen_assignment_ids:
            raise ValueError(f"duplicate column assignment for root_id {assignment.root_id}")
        seen_assignment_ids.add(assignment.root_id)
        coordinate = coordinates.get(assignment.root_id)
        if coordinate is None:
            missing_coordinate_ids.append(assignment.root_id)
            continue
        samples.append(MappingSample(
            assignment.root_id,
            assignment.cell_type,
            assignment.hemisphere,
            (coordinate.x, coordinate.y, coordinate.z),
            assignment.p,
            assignment.q,
        ))

    test = []
    train = []
    for sample in samples:
        bucket = int(hashlib.sha256(sample.root_id.encode("utf-8")).hexdigest()[:8], 16) % 5
        (test if bucket == 0 else train).append(sample)

    by_type = []
    for cell_type in sorted({sample.cell_type for sample in samples}):
        held_out = [sample for sample in samples if sample.cell_type == cell_type]
        training = [sample for sample in samples if sample.cell_type != cell_type]
        by_type.append({
            "held_out_cell_type": cell_type,
            **_mapping_metrics(training, held_out),
        })

    hemisphere = _hemisphere_accuracy(train, test)
    type_counts = Counter(sample.cell_type for sample in samples)
    return {
        "dataset": "FlyWire FAFB v783",
        "coordinate_source": coordinates_file.name,
        "coordinate_file_sha256": hashlib.sha256(coordinates_file.read_bytes()).hexdigest(),
        "coordinate_rows": sum(
            record.sample_count + record.duplicate_rows_ignored for record in coordinates.values()
        ),
        "unique_supervoxel_ids_by_root_id_sum": sum(
            record.unique_supervoxel_ids for record in coordinates.values()
        ),
        "repeated_root_supervoxel_pairs": sum(
            record.repeated_root_supervoxel_pairs for record in coordinates.values()
        ),
        "root_supervoxel_pairs_with_multiple_positions": sum(
            record.conflicting_root_supervoxel_pairs for record in coordinates.values()
        ),
        "exact_duplicate_position_rows": sum(
            record.exact_duplicate_position_rows for record in coordinates.values()
        ),
        "unique_coordinate_root_ids": len(coordinates),
        "coordinate_root_ids_with_multiple_samples": sum(
            record.sample_count > 1 for record in coordinates.values()
        ),
        "maximum_coordinate_samples_per_root": max(
            (record.sample_count for record in coordinates.values()), default=0
        ),
        "mean_coordinate_samples_per_root": mean(
            record.sample_count for record in coordinates.values()
        ) if coordinates else None,
        "median_coordinate_samples_per_root": median(
            record.sample_count for record in coordinates.values()
        ) if coordinates else None,
        "maximum_coordinate_bbox_diagonal": max(
            (record.bbox_diagonal for record in coordinates.values()), default=0.0
        ),
        "coordinate_aggregation_method": (
            "per-axis median of all supplied position rows sharing the same root_id; "
            "repeated root_id/supervoxel_id rows are retained; not interpreted as soma or arborization centroid"
        ),
        "column_assignment_rows": len(assignment_rows),
        "assignment_rows_with_coordinates": len(samples),
        "assignment_rows_missing_coordinates": len(missing_coordinate_ids),
        "assigned_samples_by_cell_type": dict(sorted(type_counts.items())),
        "deterministic_random_holdout": {
            "method": "SHA-256(root_id) first 32 bits modulo 5; bucket 0 held out",
            **_mapping_metrics(train, test),
        },
        "leave_one_cell_type_out": by_type,
        "hemisphere_nearest_centroid_holdout": hemisphere,
        "candidate_cells_mapped": False,
        "interpretation_limits": [
            "This is a feasibility audit on already-assigned cells only.",
            "No p/q or hemisphere predictions are generated for unassigned candidate neurons.",
            "A good fit would show coordinate predictability, not prove that coordinates encode medulla arborization columns.",
            "A poor leave-one-cell-type-out result blocks cross-type extrapolation.",
            "No retinal/world transform or preferred motion direction is inferred.",
        ],
    }
