"""Diagnose real T4 experiment outputs without asserting biological selectivity."""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

TYPES = ("T4a", "T4b", "T4c", "T4d")


def diagnose(data):
    metrics = data["metrics"]
    directions = tuple(sorted(metrics["T4a"]["responses"]))
    raw = {t: {d: float(metrics[t]["responses"][d]) for d in directions} for t in TYPES}
    if any(not math.isfinite(v) or v < 0 for row in raw.values() for v in row.values()):
        raise ValueError("Nonfinite or negative response")
    # Normalize each subtype's response to its own maximum; compare patterns,
    # not raw population sums (subtype sizes differ).
    normalized = {t: {d: raw[t][d] / max(raw[t].values()) if max(raw[t].values()) else 0.0
                      for d in directions} for t in TYPES}
    mean_profile = {d: sum(normalized[t][d] for t in TYPES) / len(TYPES) for d in directions}
    residuals = {t: {d: normalized[t][d] - mean_profile[d] for d in directions} for t in TYPES}
    winners = {t: max(raw[t], key=raw[t].get) for t in TYPES}
    return {"subtype_winners": winners, "all_subtypes_share_winner": len(set(winners.values())) == 1,
            "normalized_subtype_profiles": normalized, "common_mode_profile": mean_profile,
            "subtype_residuals_after_common_mode": residuals,
            "baseline_integrated": data["responses"]["baseline"]["integrated"],
            "warning": "Large responses can reflect unnormalized recurrent amplification; no validated biological direction preference.",
            "biological_direction_selectivity_validated": False}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    result = diagnose(json.loads(a.input.read_text()))
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"all_subtypes_share_winner": result["all_subtypes_share_winner"],
                      "winners": result["subtype_winners"]}))


if __name__ == "__main__":
    main()
