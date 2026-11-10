import csv
import gzip

import pytest

from cortex.experiments.connectome_adapter import import_connections


def test_import_real_format_from_gzip(tmp_path):
    path = tmp_path / "connections.csv.gz"
    with gzip.open(path, "wt", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["pre_root_id", "post_root_id", "syn_count"])
        writer.writeheader()
        writer.writerows([
            {"pre_root_id": 101, "post_root_id": 102, "syn_count": 8},
            {"pre_root_id": 102, "post_root_id": 103, "syn_count": 4},
            {"pre_root_id": 999, "post_root_id": 101, "syn_count": 9},
        ])
    circuit = import_connections(path, {101, 102, 103})
    assert circuit.root_ids == (101, 102, 103)
    assert circuit.edges == ((101, 102, 8), (102, 103, 4))
    net = circuit.simulator()
    assert len(net.synapses) == 2
    assert net.synapses[0].weight == pytest.approx(0.4)
    assert net.step((1.1, 0, 0)) == (True, False, False)
    assert net.step((0, 0, 0)) == (False, False, False)


def test_missing_columns_rejected(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("from,to,count\\n1,2,3\\n")
    with pytest.raises(ValueError, match="missing columns"):
        import_connections(path, {1, 2})


def test_no_matching_edges_rejected(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("pre_root_id,post_root_id,syn_count\\n1,2,3\\n")
    with pytest.raises(ValueError, match="no matching"):
        import_connections(path, {3, 4})


def test_invalid_root_ids_rejected(tmp_path):
    with pytest.raises(ValueError, match="positive integer"):
        import_connections(tmp_path / "missing.csv", {0})
