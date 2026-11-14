"""Independent T4 reference gate: fail closed without verified physiology.

The reference JSON is deliberately supplied by the researcher, never fabricated.
This module does not equate FAFB p/q axes with biological directions.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

SUBTYPES = ("T4a", "T4b", "T4c", "T4d")
DIRECTIONS = ("p_positive", "p_negative", "q_positive", "q_negative")


def validate_reference(payload: dict) -> dict:
    """Validate provenance and held-out independence before any biological claim."""
    errors = []
    if not isinstance(payload, dict):
        return {"valid": False, "errors": ["reference must be an object"]}
    for key in ("doi", "figure", "license", "axis_transform_source", "axis_transform"):
        if not isinstance(payload.get(key), str) or not payload[key].strip():
            errors.append(f"missing {key}")
    transform = payload.get("axis_transform")
    if transform not in (None, "") and not isinstance(transform, str):
        errors.append("axis_transform must be a documented string")
    calibration = payload.get("calibration_sample_ids")
    held_out = payload.get("held_out_sample_ids")
    if not isinstance(calibration, list) or not calibration or not all(isinstance(x, str) and x for x in calibration):
        errors.append("invalid calibration_sample_ids")
    if not isinstance(held_out, list) or not held_out or not all(isinstance(x, str) and x for x in held_out):
        errors.append("invalid held_out_sample_ids")
    if isinstance(calibration, list) and isinstance(held_out, list) and set(calibration) & set(held_out):
        errors.append("calibration and held-out samples overlap")
    observations = payload.get("observations")
    if not isinstance(observations, dict):
        errors.append("missing observations")
    else:
        for subtype in SUBTYPES:
            item = observations.get(subtype)
            if not isinstance(item, dict):
                errors.append(f"missing {subtype}")
                continue
            direction = item.get("preferred_direction")
            if direction not in DIRECTIONS:
                errors.append(f"invalid preferred_direction for {subtype}")
            dsi = item.get("dsi")
            ci = item.get("dsi_ci95")
            if isinstance(dsi, bool) or not isinstance(dsi, (float, int)) or not math.isfinite(dsi) or not -1 <= dsi <= 1:
                errors.append(f"invalid dsi for {subtype}")
            if (not isinstance(ci, list) or len(ci) != 2 or
                    any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in ci) or
                    (len(ci) == 2 and all(isinstance(x, (int, float)) for x in ci) and ci[0] > ci[1])):
                errors.append(f"invalid dsi_ci95 for {subtype}")
    return {"valid": not errors, "errors": errors}


def evaluate(reference: dict, simulated: dict) -> dict:
    """A reference can be structurally valid without proving biological agreement."""
    check = validate_reference(reference)
    if not check["valid"]:
        return {"biological_direction_selectivity_validated": False,
                "held_out_physiological_reference_verified": False,
                "independent_anatomical_alignment_verified": False,
                "errors": check["errors"]}
    # Provenance fields alone cannot establish independent anatomical alignment.
    # Nor can a single set of DSI values establish permutation p or replication.
    return {"biological_direction_selectivity_validated": False,
            "held_out_physiological_reference_verified": False,
            "independent_anatomical_alignment_verified": False,
            "errors": ["manual source verification, frozen axis calibration, "
                       "replicated held-out comparison and permutation test required"]}


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("reference", type=Path)
    parser.add_argument("--simulated", type=Path)
    args = parser.parse_args()
    reference = json.loads(args.reference.read_text(encoding="utf-8"))
    simulated = json.loads(args.simulated.read_text(encoding="utf-8")) if args.simulated else {}
    print(json.dumps(evaluate(reference, simulated), indent=2))


if __name__ == "__main__":
    main()
