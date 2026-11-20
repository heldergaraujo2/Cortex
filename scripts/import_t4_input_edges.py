"""Import and summarize real FAFB v783 candidate input edges into T4."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from cortex.t4_inputs import load_t4_input_edges, summarize_t4_input_edges


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data/raw/fafb_v783"))
    parser.add_argument("--neuropil", choices=("ME_L", "ME_R"))
    parser.add_argument("--minimum-synapses", type=int, default=0)
    parser.add_argument("--output", type=Path, default=Path("fafb_v783_t4_input_edges.json"))
    args = parser.parse_args()
    edges = load_t4_input_edges(args.data_dir, args.neuropil, args.minimum_synapses)
    report = summarize_t4_input_edges(edges)
    report["filters"] = {
        "neuropil": args.neuropil,
        "minimum_synapses": args.minimum_synapses,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"REPORT_PATH: {args.output.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
