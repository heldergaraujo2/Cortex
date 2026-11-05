import csv
import gzip

import pytest

from scripts.audit_t4_inputs import audit_t4_inputs


def _write(path, headers, rows):
    with gzip.open(path, "wt", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(headers)
        writer.writerows(rows)


def _dataset(tmp_path, *, cells=None, edges=None):
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
            ["2", "3", "ME_L", "4", "GABA"],
            ["5", "4", "ME_R", "7", "GABA"],
            ["6", "3", "ME_L", "9", "ACH"],
        ],
    )
    return tmp_path


def test_audit_counts_candidate_t4_inputs_without_assigning_sign(tmp_path):
    report = audit_t4_inputs(_dataset(tmp_path))
    assert report["candidate_and_T4_primary_type_counts"]["Mi4"] == 1
    assert report["candidate_pre_to_T4_connection_rows"] == 3
    assert report["nt_type_row_counts_as_supplied"] == {"ACH": 1, "GABA": 2}
    assert {row["presynaptic_primary_type"] for row in report["candidate_pre_to_T4_pairs_by_type_neuropil_and_nt"]} == {
        "Mi1", "Mi4", "TmY15"
    }
    assert any("not treated as a definitive" in item for item in report["interpretation_limits"])


def test_audit_keeps_neuropils_and_transmitter_labels_separate(tmp_path):
    report = audit_t4_inputs(_dataset(
        tmp_path,
        edges=[
            ["1", "3", "ME_L", "5", "ACH"],
            ["1", "3", "ME_R", "7", "ACH"],
            ["1", "3", "ME_L", "2", "GABA"],
        ],
    ))
    rows = report["candidate_pre_to_T4_pairs_by_type_neuropil_and_nt"]
    assert len(rows) == 3
    assert {row["neuropil"] for row in rows} == {"ME_L", "ME_R"}
    assert {row["nt_type_as_supplied"] for row in rows} == {"ACH", "GABA"}


def test_invalid_synapse_count_is_rejected(tmp_path):
    _dataset(tmp_path, edges=[["1", "3", "ME_L", "bad", "ACH"]])
    with pytest.raises(ValueError, match="invalid syn_count"):
        audit_t4_inputs(tmp_path)


def test_duplicate_primary_type_root_id_is_rejected(tmp_path):
    _dataset(tmp_path, cells=[["1", "Mi1"], ["1", "Mi4"]])
    with pytest.raises(ValueError, match="duplicate root_id"):
        audit_t4_inputs(tmp_path)
