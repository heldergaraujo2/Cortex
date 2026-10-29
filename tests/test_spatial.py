import csv
import gzip

import pytest

from cortex.spatial import load_column_assignments


def _write_gzip_csv(path, headers, rows):
    with gzip.open(path, "wt", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(headers)
        writer.writerows(rows)
    return path


HEADERS = ["root_id", "hemisphere", "type", "column_id", "x", "y", "p", "q"]


def test_column_assignment_import_and_pilot_coverage(tmp_path):
    path = _write_gzip_csv(tmp_path / "column_assignment.csv.gz", HEADERS, [
        ["1", "left", "L1", "10", "12.5", "14.0", "-2", "3"],
        ["2", "left", "Mi1", "10", "12.5", "14.0", "-2", "3"],
        ["3", "right", "T4a", "10", "15", "18", "1", "2"],
        ["4", "right", "T4d", "11", "17", "20", "2", "2"],
        ["999", "left", "R1-6", "10", "12", "14", "-2", "3"],
    ])
    primary_types = {"1": "L1", "2": "Mi1", "3": "T4a", "4": "T4d", "5": "Tm3"}
    report = load_column_assignments(path, primary_types)
    summary = report.summary(primary_types)

    assert len(report.rows) == 5
    assert report.unmapped_root_ids == 1
    assert summary["pilot_ids"] == 5
    assert summary["pilot_ids_with_column_assignment"] == 4
    assert summary["pilot_ids_without_column_assignment"] == 1
    assert summary["unique_hemisphere_column_pairs"] == 3
    assert summary["unique_columns_by_hemisphere"] == {"left": 1, "right": 2}
    assert summary["coverage_by_primary_type"]["Tm3"]["unassigned_ids"] == 1
    assert len(report.sha256) == 64


def test_same_column_id_is_scoped_by_hemisphere(tmp_path):
    path = _write_gzip_csv(tmp_path / "column_assignment.csv.gz", HEADERS, [
        ["1", "left", "L1", "1", "1", "1", "0", "0"],
        ["2", "right", "L1", "1", "1", "1", "0", "0"],
    ])
    report = load_column_assignments(path, {"1": "L1", "2": "L1"})
    summary = report.summary({"1": "L1", "2": "L1"})
    assert summary["unique_hemisphere_column_pairs"] == 2
    assert summary["unique_columns_by_hemisphere"] == {"left": 1, "right": 1}


def test_missing_file_is_reported(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_column_assignments(tmp_path / "missing.csv.gz", {})


def test_missing_required_column_is_rejected(tmp_path):
    path = _write_gzip_csv(tmp_path / "column_assignment.csv.gz", HEADERS[:-1], [])
    with pytest.raises(ValueError, match="missing required columns"):
        load_column_assignments(path, {})


@pytest.mark.parametrize("bad_p,bad_q", [("x", "0"), ("0", "1.5")])
def test_non_integer_lattice_coordinates_are_rejected(tmp_path, bad_p, bad_q):
    path = _write_gzip_csv(tmp_path / "column_assignment.csv.gz", HEADERS, [
        ["1", "left", "L1", "1", "1", "1", bad_p, bad_q],
    ])
    with pytest.raises(ValueError, match="invalid integer p/q"):
        load_column_assignments(path, {"1": "L1"})


@pytest.mark.parametrize("bad_x", ["NaN", "inf", "not-number"])
def test_invalid_x_coordinate_is_rejected(tmp_path, bad_x):
    path = _write_gzip_csv(tmp_path / "column_assignment.csv.gz", HEADERS, [
        ["1", "left", "L1", "1", bad_x, "1", "0", "0"],
    ])
    with pytest.raises(ValueError, match="invalid x"):
        load_column_assignments(path, {"1": "L1"})


def test_corrupted_gzip_is_rejected(tmp_path):
    path = tmp_path / "column_assignment.csv.gz"
    path.write_bytes(b"not a gzip stream")
    with pytest.raises(OSError):
        load_column_assignments(path, {})
