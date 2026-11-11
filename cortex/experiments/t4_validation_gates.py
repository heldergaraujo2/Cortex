"""Preliminary T4 model quality gates; never equate them with biological validation."""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

OPPOSITES = {"p_positive": "p_negative", "p_negative": "p_positive",
             "q_positive": "q_negative", "q_negative": "q_positive"}
TYPES = ("T4a", "T4b", "T4c", "T4d")


def assess(result):
    metrics = result["metrics"]
    baseline = result["responses"]["baseline"]["integrated"]
    finite = True
    dsi = {}
    winners = {}
    for subtype in TYPES:
        responses = metrics[subtype]["responses"]
        if set(responses) != set(OPPOSITES):
            raise ValueError("Expected exactly four direction conditions")
        if not all(math.isfinite(float(v)) and float(v) >= 0 for v in responses.values()):
            finite = False
            continue
        winner = max(responses, key=responses.get)
        opposite = OPPOSITES[winner]
        a, b = float(responses[winner]), float(responses[opposite])
        winners[subtype] = winner
        dsi[subtype] = (a - b) / (a + b + 1e-12)
    baseline_ok = all(math.isfinite(float(baseline[t])) and abs(float(baseline[t])) <= 1e-9 for t in TYPES)
    return {
        "numerical_finite_integrated": finite,
        "baseline_near_zero": baseline_ok,
        "normalized_graph": bool(result["responses"].get("normalize_outgoing")),
        "preferred_conditions": winners,
        "opposite_direction_dsi": dsi,
        "all_subtypes_share_winner": len(set(winners.values())) == 1 if len(winners) == 4 else None,
        "independent_anatomical_alignment_verified": False,
        "held_out_physiological_reference_verified": False,
        "biological_direction_selectivity_validated": False,
        "note": "Descriptive software gates only; no held-out biological validation."
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assessment = assess(json.loads(args.input.read_text()))
    args.output.write_text(json.dumps(assessment, indent=2, sort_keys=True) + "\n")
    print(json.dumps(assessment, sort_keys=True))
    if not assessment["numerical_finite_integrated"] or not assessment["baseline_near_zero"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
