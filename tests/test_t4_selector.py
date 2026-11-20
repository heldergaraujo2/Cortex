import csv
import gzip

import pytest

from cortex.experiments.t4_selector import select_t4_pilot


def test_t4_selection_and_simulation(tmp_path):
    cells = tmp_path / "types.csv.gz"
    with gzip.open(cells, "wt", newline="") as f:
        w = csv.writer(f)
        w.writerows([["root_id", "cell_type"], [101, "L1"], [102, "Mi1"],
                     [103, "Tm3"], [104, "T4"], [105, "other"]])
    edges = tmp_path / "connections.csv"
    with edges.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerows([["pre_root_id", "post_root_id", "syn_count"],
                     [101, 102, 6], [101, 103, 7], [102, 104, 8],
                     [103, 104, 9], [104, 101, 100], [105, 104, 50],
                     [101, 104, 20], [101, 102, 2]])
    result = select_t4_pilot(cells, edges)
    assert result.circuit.root_ids == (101, 102, 103, 104)
    assert len(result.circuit.edges) == 4
    assert result.edge_counts["Mi1->T4"] == 1
    net = result.circuit.simulator()
    assert net.neuron_count == 4
    assert len(net.synapses) == 4


def test_missing_annotations_fail(tmp_path):
    cells = tmp_path / "types.csv"
    cells.write_text("root_id,cell_type\n1,other\n")
    edges = tmp_path / "edges.csv"
    edges.write_text("pre_root_id,post_root_id,syn_count\n1,2,10\n")
    with pytest.raises(ValueError, match="no annotated"):
        select_t4_pilot(cells, edges)


def test_no_matching_connections_fail(tmp_path):
    cells = tmp_path / "types.csv"
    cells.write_text("root_id,cell_type\n1,L1\n2,T4\n")
    edges = tmp_path / "edges.csv"
    edges.write_text("pre_root_id,post_root_id,syn_count\n1,2,10\n")
    with pytest.raises(ValueError, match="no qualifying"):
        select_t4_pilot(cells, edges)
