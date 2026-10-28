from cortex.diagnostics import collect_diagnostics


def test_diagnostics_returns_basic_runtime_fields():
    report = collect_diagnostics()
    assert isinstance(report["platform"], str)
    assert isinstance(report["python_version"], str)
    assert isinstance(report["cpu_count_logical"], int)
    assert isinstance(report["working_directory_free_bytes"], int)
    assert isinstance(report["working_directory_total_bytes"], int)
    assert report["working_directory_free_bytes"] <= report["working_directory_total_bytes"]
    assert "No files were written" in report["note"]
