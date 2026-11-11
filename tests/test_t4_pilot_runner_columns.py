import csv

from cortex.experiments.t4_pilot_runner import run_pilot


def test_custom_real_data_headers(tmp_path):
    cells = tmp_path / "types.csv"
    edges = tmp_path / "connections.csv"
    with cells.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerows([["pt_root_id", "type"], [101, "L1"], [102, "Mi1"], [103, "T4"]])
    with edges.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerows([["pre_pt_root_id", "post_pt_root_id", "synapse_count"],
                     [101, 102, 20], [102, 103, 20]])
    result = run_pilot(
        cells, edges, steps=12, cell_id_column="pt_root_id",
        cell_type_column="type", pre_column="pre_pt_root_id",
        post_column="post_pt_root_id", synapse_column="synapse_count",
    )
    assert result["selected_edges"] == 2
    assert result["t4_spikes_l1_current"] > result["t4_spikes_no_stimulus"]
