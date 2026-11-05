"""Audit per-neuron predicted neurotransmitter labels against T4 edge labels.

Codex's neurons.csv.gz contains predicted nt_type and nt_type_score. These are
not verified physiological signs and must not be converted directly to edge
polarity.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
from collections import Counter, defaultdict
from dataclasses import dataclass
from math import isfinite
from pathlib import Path
from statistics import mean, median

from cortex.t4_inputs import T4InputEdge


@dataclass(frozen=True, slots=True)
class NeuronTransmitterAnnotation:
    root_id: str
    nt_type: str
    nt_type_score: float | None


def load_neuron_transmitter_annotations(
    path: str | Path,
) -> dict[str, NeuronTransmitterAnnotation]:
    source = Path(path)
    result: dict[str, NeuronTransmitterAnnotation] = {}
    with gzip.open(source, "rt", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"root_id", "nt_type", "nt_type_score"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"{source.name}: expected columns {sorted(required)}")
        for line_number, row in enumerate(reader, start=2):
            root_id = (row.get("root_id") or "").strip()
            if not root_id:
                raise ValueError(f"{source.name}:{line_number}: empty root_id")
            if root_id in result:
                raise ValueError(f"{source.name}:{line_number}: duplicate root_id {root_id}")
            label = (row.get("nt_type") or "").strip() or "(empty)"
            raw_score = (row.get("nt_type_score") or "").strip()
            try:
                score = float(raw_score) if raw_score else None
            except ValueError as exc:
                raise ValueError(
                    f"{source.name}:{line_number}: invalid nt_type_score {raw_score!r}"
                ) from exc
            if score is not None and (not isfinite(score) or not 0 <= score <= 1):
                raise ValueError(
                    f"{source.name}:{line_number}: nt_type_score must be within [0, 1]"
                )
            result[root_id] = NeuronTransmitterAnnotation(root_id, label, score)
    return result


def audit_t4_neuron_annotations(
    annotations_path: str | Path,
    edges: tuple[T4InputEdge, ...],
) -> dict[str, object]:
    annotations = load_neuron_transmitter_annotations(annotations_path)
    edge_labels: Counter[str] = Counter()
    predictions_by_type: dict[str, Counter[str]] = defaultdict(Counter)
    scores_by_type: dict[str, list[float]] = defaultdict(list)
    agreements_by_type: dict[str, Counter[str]] = defaultdict(Counter)
    annotated_edge_rows = 0
    missing_edge_rows = 0
    unique_candidate_ids = {edge.pre_root_id for edge in edges}
    for edge in edges:
        edge_labels[edge.nt_type] += 1
        annotation = annotations.get(edge.pre_root_id)
        if annotation is None:
            missing_edge_rows += 1
            continue
        annotated_edge_rows += 1
        predictions_by_type[edge.pre_type][annotation.nt_type] += 1
        if annotation.nt_type_score is not None:
            scores_by_type[edge.pre_type].append(annotation.nt_type_score)
        if annotation.nt_type == edge.nt_type:
            agreements_by_type[edge.pre_type]["match"] += 1
        else:
            agreements_by_type[edge.pre_type]["mismatch"] += 1

    prediction_summary = []
    for cell_type in sorted(predictions_by_type):
        scores = scores_by_type[cell_type]
        prediction_summary.append({
            "presynaptic_primary_type": cell_type,
            "edge_rows_with_neuron_annotation": sum(predictions_by_type[cell_type].values()),
            "neuron_nt_type_prediction_counts": dict(sorted(predictions_by_type[cell_type].items())),
            "edge_vs_neuron_prediction_match_rows": agreements_by_type[cell_type]["match"],
            "edge_vs_neuron_prediction_mismatch_rows": agreements_by_type[cell_type]["mismatch"],
            "nt_type_score_count": len(scores),
            "nt_type_score_mean": mean(scores) if scores else None,
            "nt_type_score_median": median(scores) if scores else None,
        })

    return {
        "dataset": "FlyWire FAFB v783",
        "annotation_product": Path(annotations_path).name,
        "annotation_file_sha256": hashlib.sha256(Path(annotations_path).read_bytes()).hexdigest(),
        "neuron_annotation_rows": len(annotations),
        "candidate_input_edge_rows": len(edges),
        "unique_candidate_presynaptic_root_ids": len(unique_candidate_ids),
        "unique_candidate_presynaptic_root_ids_with_annotation": len(unique_candidate_ids & set(annotations)),
        "edge_rows_with_presynaptic_annotation": annotated_edge_rows,
        "edge_rows_missing_presynaptic_annotation": missing_edge_rows,
        "edge_nt_type_counts_as_supplied": dict(sorted(edge_labels.items())),
        "by_presynaptic_primary_type": prediction_summary,
        "nt_type_verified_available_in_product": False,
        "synaptic_sign_assigned": False,
        "interpretation_limits": [
            "neurons.csv.gz nt_type is a prediction and nt_type_score is its confidence score",
            "connection-row nt_type and neuron-level nt_type are compared but neither is treated as verified",
            "a predicted transmitter label is not by itself a postsynaptic physiological sign",
            "no synaptic efficacy, receptor state, delay, or direction preference is inferred",
        ],
    }
