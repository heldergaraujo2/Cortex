import csv

from cortex.experiments.t4_pilot_runner import run_pilot


def test_pilot_measures_t4_spikes(tmp_path):
    cells = tmp_path / "types.csv"
    edges = tmp_path / "connections.csv"
    with cells.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerows([["root_id", "cell_type"], [1, "L1"], [2, "Mi1"], [3, "T4"]])
    with edges.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerows([["pre_root_id", "post_root_id", "syn_count"],
                     [1, 2, 20], [2, 3, 20]])
    result = run_pilot(cells, edges, steps=12)
    assert result["selected_neurons"] == 3
    assert result["selected_edges"] == 2
    assert result["t4_spikes_no_stimulus"] == 0
    assert result["t4_spikes_l1_current"] > 0
    assert result["spatial_motion_test"] is False
    assert result["plasticity_enabled"] is False
