import csv
import gzip

import pytest

from cortex.connectome import load_pilot_connectome


def _write_gzip_csv(path, headers, rows):
    with gzip.open(path, "wt", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(headers)
        writer.writerows(rows)


def _make_data_dir(tmp_path, *, cells=None, connections=None, coordinates=None):
    _write_gzip_csv(
        tmp_path / "consolidated_cell_types.csv.gz",
        ["root_id", "primary_type", "additional_type(s)"],
        cells if cells is not None else [
            ["1", "L1", ""],
            ["2", "Mi1", ""],
            ["3", "T4a", ""],
            ["4", "Tm3", ""],
            ["5", "Other", ""],
        ],
    )
    _write_gzip_csv(
        tmp_path / "connections_princeton.csv.gz",
        ["pre_root_id", "post_root_id", "neuropil", "syn_count", "nt_type"],
        connections if connections is not None else [
            ["1", "2", "ME_L", "5", "ACH"],
            ["1", "2", "ME_R", "7", "ACH"],
            ["2", "3", "ME_L", "8", "ACH"],
            ["4", "3", "ME_L", "4", "GABA"],
            ["5", "2", "ME_L", "9", "ACH"],
        ],
    )
    _write_gzip_csv(
        tmp_path / "coordinates.csv.gz",
        ["root_id", "position", "supervoxel_id"],
        coordinates if coordinates is not None else [
            ["1", "[10 20 30]", "101"],
            ["1", "[11 21 31]", "102"],
            ["2", "[40 50 60]", "201"],
            ["3", "[70 80 90]", "301"],
            ["4", "[15 25 35]", "401"],
            ["5", "[99 99 99]", "501"],
        ],
    )
    return tmp_path


def test_imports_pilot_rows_and_preserves_neuropil_separation(tmp_path):
    data_dir = _make_data_dir(tmp_path)
    graph = load_pilot_connectome(data_dir)

    assert graph.dataset == "FlyWire FAFB v783"
    assert graph.total_connection_rows == 5
    assert len(graph.connections) == 4  # non-pilot neuron "Other" is excluded
    assert len(graph.coordinates_by_root_id["1"]) == 2  # never silently pick one coordinate

    summary = graph.summary()
    assert summary["cell_type_counts"] == {"L1": 1, "Mi1": 1, "T4a": 1, "Tm3": 1}
    assert summary["pilot_neuron_ids"] == 4
    assert summary["pilot_neuron_ids_with_coordinates"] == 4
    assert summary["pilot_neuron_ids_without_coordinates"] == 0

    l1_mi1 = next(
        pair for pair in summary["pilot_type_pairs"]
        if pair["pre_type"] == "L1" and pair["post_type"] == "Mi1"
    )
    assert l1_mi1["table_rows_across_neuropils"] == 2
    assert l1_mi1["distinct_pre_post_root_id_pairs"] == 1
    assert {item["neuropil"] for item in l1_mi1["neuropils"]} == {"ME_L", "ME_R"}
    assert {item["syn_count_sum_within_neuropil"] for item in l1_mi1["neuropils"]} == {5, 7}


def test_missing_file_is_reported(tmp_path):
    with pytest.raises(FileNotFoundError, match="coordinates.csv.gz"):
        load_pilot_connectome(tmp_path)


def test_duplicate_cell_root_id_is_rejected(tmp_path):
    _make_data_dir(tmp_path, cells=[
        ["1", "L1", ""], ["1", "L1", ""], ["2", "Mi1", ""],
    ])
    with pytest.raises(ValueError, match="duplicate root_id"):
        load_pilot_connectome(tmp_path)


def test_invalid_coordinate_is_rejected(tmp_path):
    _make_data_dir(tmp_path, coordinates=[
        ["1", "[10 20]", "101"],
    ])
    with pytest.raises(ValueError, match="expected three integer coordinates"):
        load_pilot_connectome(tmp_path)


def test_invalid_synapse_count_is_rejected_for_pilot_connection(tmp_path):
    _make_data_dir(tmp_path, connections=[
        ["1", "2", "ME_L", "not-a-number", "ACH"],
    ])
    with pytest.raises(ValueError, match="invalid syn_count"):
        load_pilot_connectome(tmp_path)


def test_required_headers_are_checked(tmp_path):
    _write_gzip_csv(
        tmp_path / "consolidated_cell_types.csv.gz",
        ["root_id", "wrong_name"],
        [["1", "L1"]],
    )
    _write_gzip_csv(
        tmp_path / "connections_princeton.csv.gz",
        ["pre_root_id", "post_root_id", "neuropil", "syn_count", "nt_type"],
        [],
    )
    _write_gzip_csv(
        tmp_path / "coordinates.csv.gz",
        ["root_id", "position", "supervoxel_id"],
        [],
    )
    with pytest.raises(ValueError, match="missing required columns"):
        load_pilot_connectome(tmp_path)



def test_unmapped_connection_ids_are_counted_not_silently_hidden(tmp_path):
    _make_data_dir(tmp_path, connections=[
        ["999", "2", "ME_L", "5", "ACH"],
        ["1", "2", "ME_L", "6", "ACH"],
    ])
    graph = load_pilot_connectome(tmp_path)
    summary = graph.summary()

    assert summary["connection_table_rows_total"] == 2
    assert summary["connection_rows_with_pre_id_in_cell_type_table"] == 1
    assert summary["connection_rows_with_post_id_in_cell_type_table"] == 2
    assert summary["connection_rows_with_both_ids_in_cell_type_table"] == 1
    assert summary["pilot_connection_rows"] == 1


def test_duplicate_pilot_connection_key_is_reported_and_rows_preserved(tmp_path):
    _make_data_dir(tmp_path, connections=[
        ["1", "2", "ME_L", "5", "ACH"],
        ["1", "2", "ME_L", "5", "ACH"],
    ])
    graph = load_pilot_connectome(tmp_path)
    summary = graph.summary()

    assert len(graph.connections) == 2
    assert summary["duplicate_pilot_pre_post_neuropil_keys"] == 1



def test_corrupted_gzip_is_rejected(tmp_path):
    _make_data_dir(tmp_path)
    (tmp_path / "connections_princeton.csv.gz").write_bytes(b"not a gzip stream")
    with pytest.raises(OSError):
        load_pilot_connectome(tmp_path)
