"""Run the synthetic T4 signed-input mechanism demonstration."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from cortex.t4_mechanism import compare_opposite_sweeps


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extent", type=int, default=2)
    parser.add_argument("--output", type=Path, default=Path("t4_mechanism_demo.json"))
    args = parser.parse_args()
    report = compare_opposite_sweeps(extent=args.extent)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report["comparison"], ensure_ascii=False, indent=2))
    print(f"REPORT_PATH: {args.output.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
