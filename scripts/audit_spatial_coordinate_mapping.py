"""Audit whether FAFB 3D coordinates predict known medulla p/q assignments."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from cortex.spatial import load_column_assignments
from cortex.spatial_mapping import audit_coordinate_to_column_mapping
from cortex.t4_inputs import load_primary_types


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data/raw/fafb_v783"))
    parser.add_argument(
        "--column-file", type=Path,
        default=Path("data/raw/fafb_v783/column_assignment.csv.gz"),
    )
    parser.add_argument(
        "--coordinates-file", type=Path,
        default=Path("data/raw/fafb_v783/coordinates.csv.gz"),
    )
    parser.add_argument("--output", type=Path, default=Path("fafb_v783_coordinate_mapping_audit.json"))
    args = parser.parse_args()
    primary_types = load_primary_types(args.data_dir / "consolidated_cell_types.csv.gz")
    assignments = load_column_assignments(args.column_file, primary_types)
    report = audit_coordinate_to_column_mapping(args.coordinates_file, assignments.rows)
    report["column_assignment_source_sha256"] = assignments.sha256
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        key: value for key, value in report.items()
        if key not in {"leave_one_cell_type_out"}
    }, ensure_ascii=False, indent=2))
    print(f"REPORT_PATH: {args.output.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
