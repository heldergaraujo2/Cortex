import csv
import gzip

import pytest

from cortex.t4_annotations import (
    audit_t4_neuron_annotations,
    load_neuron_transmitter_annotations,
)
from cortex.t4_inputs import T4InputEdge


def _write(path, rows):
    with gzip.open(path, "wt", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow([
            "root_id", "group", "nt_type", "nt_type_score",
            "da_avg", "ser_avg", "gaba_avg", "glut_avg", "ach_avg", "oct_avg",
        ])
        writer.writerows(rows)


def _edges():
    return (
        T4InputEdge("1", "10", "Mi1", "T4a", "ME_L", 8, "ACH"),
        T4InputEdge("1", "11", "Mi1", "T4b", "ME_L", 5, "GLUT"),
        T4InputEdge("2", "10", "Mi4", "T4a", "ME_L", 4, "GABA"),
        T4InputEdge("3", "11", "Mi9", "T4b", "ME_R", 7, "GLUT"),
        T4InputEdge("4", "10", "C3", "T4a", "ME_R", 6, "GABA"),
    )


def test_annotation_loader_reads_prediction_and_score(tmp_path):
    path = tmp_path / "neurons.csv.gz"
    _write(path, [["1", "optic", "ACH", "0.98", "0", "0", "0", "0", "1", "0"]])
    result = load_neuron_transmitter_annotations(path)
    assert result["1"].nt_type == "ACH"
    assert result["1"].nt_type_score == pytest.approx(0.98)


def test_audit_compares_edge_and_neuron_predictions_without_signing(tmp_path):
    path = tmp_path / "neurons.csv.gz"
    _write(path, [
        ["1", "optic", "ACH", "0.98", "0", "0", "0", "0", "1", "0"],
        ["2", "optic", "GABA", "0.91", "0", "0", "1", "0", "0", "0"],
        ["3", "optic", "GLUT", "0.87", "0", "0", "0", "1", "0", "0"],
        ["4", "optic", "GABA", "0.82", "0", "0", "1", "0", "0", "0"],
    ])
    report = audit_t4_neuron_annotations(path, _edges())
    assert report["candidate_input_edge_rows"] == 5
    assert report["edge_rows_with_presynaptic_annotation"] == 5
    assert report["edge_rows_missing_presynaptic_annotation"] == 0
    assert report["by_presynaptic_primary_type"][0]["edge_vs_neuron_prediction_match_rows"] == 1
    assert report["by_presynaptic_primary_type"][0]["edge_vs_neuron_prediction_mismatch_rows"] == 1
    assert report["nt_type_verified_available_in_product"] is False
    assert report["synaptic_sign_assigned"] is False


def test_missing_neuron_annotation_is_counted(tmp_path):
    path = tmp_path / "neurons.csv.gz"
    _write(path, [["1", "optic", "ACH", "0.98", "0", "0", "0", "0", "1", "0"]])
    report = audit_t4_neuron_annotations(path, _edges())
    assert report["edge_rows_missing_presynaptic_annotation"] == 3
    assert report["unique_candidate_presynaptic_root_ids_with_annotation"] == 1


def test_duplicate_neuron_root_id_is_rejected(tmp_path):
    path = tmp_path / "neurons.csv.gz"
    row = ["1", "optic", "ACH", "0.98", "0", "0", "0", "0", "1", "0"]
    _write(path, [row, row])
    with pytest.raises(ValueError, match="duplicate root_id"):
        load_neuron_transmitter_annotations(path)


def test_invalid_neuron_transmitter_score_is_rejected(tmp_path):
    path = tmp_path / "neurons.csv.gz"
    _write(path, [["1", "optic", "ACH", "1.5", "0", "0", "0", "0", "1", "0"]])
    with pytest.raises(ValueError, match="within"):
        load_neuron_transmitter_annotations(path)
