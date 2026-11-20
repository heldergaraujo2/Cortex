import gzip

from cortex.experiments.fafb_inspect import inspect_csv


def test_inspect_gz_header_and_rows(tmp_path):
    path = tmp_path / "annotations.csv.gz"
    with gzip.open(path, "wt", newline="") as f:
        f.write("root_id,cell_type\n123,L1\n456,T4\n")
    result = inspect_csv(path, sample_rows=1)
    assert result["columns"] == ["root_id", "cell_type"]
    assert result["examples"] == [{"root_id": "123", "cell_type": "L1"}]


def test_inspect_zero_rows(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("a,b\n")
    assert inspect_csv(path, sample_rows=0)["examples"] == []
