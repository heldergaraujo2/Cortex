"""Run the deterministic FAFB v783 structural rate baseline."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from cortex.connectome import load_pilot_connectome
from cortex.dynamics import RateConfig, run_baseline_experiment


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data/raw/fafb_v783"))
    parser.add_argument("--neuropil", required=True, help="Exact single neuropil label, e.g. ME_L")
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--stimulus-duration", type=int, default=2)
    parser.add_argument("--leak", type=float, default=0.5)
    parser.add_argument("--minimum-synapses", type=int, default=5)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    connectome = load_pilot_connectome(args.data_dir)
    config = RateConfig(
        steps=args.steps, stimulus_duration=args.stimulus_duration,
        leak=args.leak, minimum_synapses=args.minimum_synapses,
    )
    report = run_baseline_experiment(connectome, args.neuropil, config)
    report["source_manifest"] = list(connectome.file_manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "neuropil": args.neuropil,
        "scenarios": {
            name: {
                "edges": item["network"]["edges"],
                "readout_neurons": item["network"]["t4_readout_neurons"],
                "peak_mean_t4_rate": item["metrics"]["peak_mean_t4_rate"],
            }
            for name, item in report["scenarios"].items()
        },
        "direction_selectivity_claimed": report["comparison"]["direction_selectivity_claimed"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
