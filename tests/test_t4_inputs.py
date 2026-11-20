import csv
import gzip

import pytest

from cortex.t4_inputs import load_t4_input_edges, summarize_t4_input_edges


def _write(path, headers, rows):
    with gzip.open(path, "wt", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(headers)
        writer.writerows(rows)


def _data(tmp_path, *, cells=None, edges=None):
    _write(
        tmp_path / "consolidated_cell_types.csv.gz",
        ["root_id", "primary_type"],
        cells if cells is not None else [
            ["1", "Mi1"], ["2", "Mi4"], ["3", "T4a"], ["4", "T4b"],
            ["5", "TmY15"], ["6", "Other"],
        ],
    )
    _write(
        tmp_path / "connections_princeton.csv.gz",
        ["pre_root_id", "post_root_id", "neuropil", "syn_count", "nt_type"],
        edges if edges is not None else [
            ["1", "3", "ME_L", "8", "ACH"],
            ["1", "3", "ME_L", "4", "GLUT"],
            ["2", "3", "ME_L", "4", "GABA"],
            ["5", "4", "ME_R", "7", "GABA"],
            ["6", "3", "ME_L", "10", "ACH"],
            ["1", "6", "ME_L", "10", "ACH"],
            ["2", "3", "ME_R", "6", "GABA"],
        ],
    )
    return tmp_path


def test_loader_preserves_candidate_edges_and_supplied_labels(tmp_path):
    edges = load_t4_input_edges(_data(tmp_path))
    assert len(edges) == 5
    assert [(edge.pre_type, edge.nt_type) for edge in edges[:3]] == [
        ("Mi1", "ACH"), ("Mi1", "GLUT"), ("Mi4", "GABA")
    ]
    assert len({(edge.pre_root_id, edge.post_root_id, edge.neuropil) for edge in edges}) == 4


def test_loader_filters_exact_neuropil_and_minimum_synapse_threshold(tmp_path):
    edges = load_t4_input_edges(_data(tmp_path), neuropil="ME_L", minimum_synapses=5)
    assert len(edges) == 1
    assert edges[0].pre_type == "Mi1"
    assert edges[0].syn_count == 8


def test_summary_keeps_neuropil_and_nt_type_separate(tmp_path):
    edges = load_t4_input_edges(_data(tmp_path))
    report = summarize_t4_input_edges(edges)
    assert report["candidate_input_rows"] == 5
    assert report["synaptic_sign_assigned"] is False
    assert {row["nt_type_as_supplied"] for row in report["rows_by_type_neuropil_nt_type"]} == {
        "ACH", "GLUT", "GABA"
    }
    assert {row["neuropil"] for row in report["rows_by_type_neuropil_nt_type"]} == {
        "ME_L", "ME_R"
    }


def test_duplicate_rows_are_not_silently_merged(tmp_path):
    edges = load_t4_input_edges(_data(
        tmp_path,
        edges=[
            ["1", "3", "ME_L", "8", "ACH"],
            ["1", "3", "ME_L", "8", "ACH"],
        ],
    ))
    assert len(edges) == 2
    report = summarize_t4_input_edges(edges)
    assert report["rows_by_type_neuropil_nt_type"][0]["table_rows"] == 2
    assert report["rows_by_type_neuropil_nt_type"][0]["distinct_pre_post_pairs_within_group"] == 1


def test_invalid_synapse_count_is_rejected(tmp_path):
    _data(tmp_path, edges=[["1", "3", "ME_L", "bad", "ACH"]])
    with pytest.raises(ValueError, match="invalid syn_count"):
        load_t4_input_edges(tmp_path)


def test_negative_synapse_count_is_rejected(tmp_path):
    _data(tmp_path, edges=[["1", "3", "ME_L", "-1", "ACH"]])
    with pytest.raises(ValueError, match="negative syn_count"):
        load_t4_input_edges(tmp_path)


def test_invalid_filter_parameters_are_rejected(tmp_path):
    data = _data(tmp_path)
    with pytest.raises(ValueError, match="neuropil"):
        load_t4_input_edges(data, neuropil=" ")
    with pytest.raises(ValueError, match="minimum_synapses"):
        load_t4_input_edges(data, minimum_synapses=-1)


def test_duplicate_primary_type_ids_are_rejected(tmp_path):
    _data(tmp_path, cells=[["1", "Mi1"], ["1", "Mi4"]])
    with pytest.raises(ValueError, match="duplicate root_id"):
        load_t4_input_edges(tmp_path)
