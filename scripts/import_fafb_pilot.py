"""Build a reproducible summary/manifest for the reduced FAFB v783 pilot."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from cortex.connectome import load_pilot_connectome


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data/raw/fafb_v783"),
        help="Directory containing the three official Codex CSV.gz products.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/fafb_v783_pilot_manifest.json"),
        help="Output JSON path (generated output should remain outside Git).",
    )
    args = parser.parse_args()

    graph = load_pilot_connectome(args.data_dir)
    report = graph.summary()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "output": str(args.output),
        "dataset": report["dataset"],
        "pilot_neuron_ids": report["pilot_neuron_ids"],
        "pilot_neuron_ids_with_coordinates": report["pilot_neuron_ids_with_coordinates"],
        "pilot_connection_rows": report["pilot_connection_rows"],
        "file_manifest": report["file_manifest"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
