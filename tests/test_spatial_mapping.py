import csv
import gzip

import pytest

from cortex.spatial import ColumnAssignment
from cortex.spatial_mapping import audit_coordinate_to_column_mapping, load_coordinate_records


def _write(path, rows):
    with gzip.open(path, "wt", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["root_id", "position", "supervoxel_id"])
        writer.writerows(rows)


def _assignments():
    rows = []
    for index in range(1, 31):
        x, y, z = float(index), float(index % 5), float(index % 3)
        p = round(2 * x - y + 3 * z)
        q = round(-x + 2 * y + z)
        rows.append(ColumnAssignment(
            str(index), "left" if index % 2 else "right",
            "Mi1" if index % 3 else "T4a", f"C{index}",
            x, y, p, q,
        ))
    return tuple(rows)


def test_coordinate_loader_parses_three_dimensional_position(tmp_path):
    path = tmp_path / "coordinates.csv.gz"
    _write(path, [["1", "[10 20 30]", "99"]])
    result = load_coordinate_records(path)
    assert (result["1"].x, result["1"].y, result["1"].z) == (10, 20, 30)


def test_coordinate_mapping_audit_reports_holdouts_without_mapping_candidates(tmp_path):
    path = tmp_path / "coordinates.csv.gz"
    assignments = _assignments()
    _write(path, [
        [row.root_id, f"[{int(row.x)} {int(row.y)} {index % 3}]", "99"]
        for index, row in enumerate(assignments, start=1)
    ])
    report = audit_coordinate_to_column_mapping(path, assignments)
    assert report["assignment_rows_with_coordinates"] == 30
    assert report["assignment_rows_missing_coordinates"] == 0
    assert report["candidate_cells_mapped"] is False
    assert report["deterministic_random_holdout"]["status"] == "ok"
    assert report["leave_one_cell_type_out"]


def test_coordinate_loader_rejects_invalid_position(tmp_path):
    path = tmp_path / "coordinates.csv.gz"
    _write(path, [["1", "[10 20]", "99"]])
    with pytest.raises(ValueError, match="expected 3D position"):
        load_coordinate_records(path)


def test_coordinate_loader_aggregates_multiple_supervoxel_positions(tmp_path):
    path = tmp_path / "coordinates.csv.gz"
    _write(path, [["1", "[10 20 30]", "99"], ["1", "[12 24 34]", "98"]])
    result = load_coordinate_records(path)
    assert (result["1"].x, result["1"].y, result["1"].z) == (11, 22, 32)
    assert result["1"].sample_count == 2
    assert result["1"].bbox_diagonal == pytest.approx(6)


def test_coordinate_loader_counts_exact_duplicate_position_rows(tmp_path):
    path = tmp_path / "coordinates.csv.gz"
    _write(path, [["1", "[10 20 30]", "99"], ["1", "[10 20 30]", "99"]])
    result = load_coordinate_records(path)
    assert result["1"].sample_count == 2
    assert result["1"].unique_supervoxel_ids == 1
    assert result["1"].repeated_root_supervoxel_pairs == 1
    assert result["1"].conflicting_root_supervoxel_pairs == 0
    assert result["1"].exact_duplicate_position_rows == 1


def test_coordinate_loader_preserves_conflicting_positions_for_repeated_supervoxel(tmp_path):
    path = tmp_path / "coordinates.csv.gz"
    _write(path, [["1", "[10 20 30]", "99"], ["1", "[12 24 34]", "99"]])
    result = load_coordinate_records(path)
    assert result["1"].sample_count == 2
    assert result["1"].repeated_root_supervoxel_pairs == 1
    assert result["1"].conflicting_root_supervoxel_pairs == 1
    assert result["1"].exact_duplicate_position_rows == 0
