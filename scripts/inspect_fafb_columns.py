"""Validate the FAFB v783 visual column assignment against the pilot cell types."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from cortex.connectome import load_pilot_connectome
from cortex.spatial import load_column_assignments


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir", type=Path, default=Path("data/raw/fafb_v783"),
        help="Directory containing the three pilot CSV.GZ files.",
    )
    parser.add_argument(
        "--column-file", type=Path,
        default=Path("data/raw/fafb_v783/column_assignment.csv.gz"),
        help="FlyWire Codex column_assignment.csv.gz file.",
    )
    parser.add_argument(
        "--output", type=Path,
        default=Path("fafb_v783_column_assignment_report.json"),
        help="Generated JSON report path.",
    )
    args = parser.parse_args()

    graph = load_pilot_connectome(args.data_dir)
    column_data = load_column_assignments(args.column_file, graph.cell_types)
    report = column_data.summary(graph.cell_types)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "output": str(args.output),
        "rows": report["rows"],
        "unique_root_ids": report["unique_root_ids"],
        "pilot_ids": report["pilot_ids"],
        "pilot_ids_with_column_assignment": report["pilot_ids_with_column_assignment"],
        "pilot_ids_without_column_assignment": report["pilot_ids_without_column_assignment"],
        "coverage_by_primary_type": report["coverage_by_primary_type"],
        "unique_hemisphere_column_pairs": report["unique_hemisphere_column_pairs"],
        "sha256": report["source_file"]["sha256"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
