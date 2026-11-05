"""Join real T4 input edges to T4 column assignments and build structural profiles."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from cortex.spatial import load_column_assignments
from cortex.t4_inputs import load_primary_types, load_t4_input_edges
from cortex.t4_profiles import summarize_t4_target_profiles


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data/raw/fafb_v783"))
    parser.add_argument(
        "--column-file", type=Path,
        default=Path("data/raw/fafb_v783/column_assignment.csv.gz"),
    )
    parser.add_argument("--minimum-synapses", type=int, default=0)
    parser.add_argument("--output", type=Path, default=Path("fafb_v783_t4_target_profiles.json"))
    args = parser.parse_args()
    primary_types = load_primary_types(args.data_dir / "consolidated_cell_types.csv.gz")
    assignments = load_column_assignments(args.column_file, primary_types)
    edges = load_t4_input_edges(args.data_dir, minimum_synapses=args.minimum_synapses)
    report = summarize_t4_target_profiles(edges, assignments.rows)
    report["column_assignment_source"] = {
        "name": args.column_file.name,
        "sha256": assignments.sha256,
        "rows": len(assignments.rows),
    }
    report["filters"] = {"minimum_synapses": args.minimum_synapses}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        key: value for key, value in report.items()
        if key not in {"profiles_by_t4_target", "aggregate_by_t4_type_hemisphere_input_type_neuropil_nt"}
    }, ensure_ascii=False, indent=2))
    print(f"TARGET_PROFILES: {len(report['profiles_by_t4_target'])}")
    print(f"AGGREGATE_GROUPS: {len(report['aggregate_by_t4_type_hemisphere_input_type_neuropil_nt'])}")
    print(f"REPORT_PATH: {args.output.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
