"""Generate reproducible four-direction spatial input schedules from FAFB column assignments.

This generates INPUTS, not neural responses or evidence of direction selectivity.
Coordinates p/q are treated as an anatomical grid; their relation to visual
degrees and subtype-preferred directions requires separate validation.
"""
from __future__ import annotations
import argparse
import csv
import gzip
import json
from pathlib import Path

DIRECTIONS = {"p_positive": (1, 0), "p_negative": (-1, 0),
              "q_positive": (0, 1), "q_negative": (0, -1)}

def read_rows(path):
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8-sig", newline="") as stream:
        yield from csv.DictReader(stream)

def balance_schedules(schedules):
    """Deterministically equalize input-event counts, preserving frame order.

    This is an experimental matched-drive control, not a biological calibration.
    Keep original schedules separately for provenance.
    """
    if not schedules or any(not frames for frames in schedules.values()):
        raise ValueError("Nonempty schedules required")
    totals = {name: sum(len(frame["active_l1_root_ids"]) for frame in frames)
              for name, frames in schedules.items()}
    target = min(totals.values())
    if target == 0:
        raise ValueError("Cannot balance schedules with zero input events")
    balanced = {}
    for name, frames in schedules.items():
        copied = [{"step": frame["step"],
                   "active_l1_root_ids": list(frame["active_l1_root_ids"])}
                  for frame in frames]
        excess = totals[name] - target
        while excess:
            # Trim the fullest frame first; deterministic tie-breaking.
            index = max(range(len(copied)),
                        key=lambda i: (len(copied[i]["active_l1_root_ids"]), -i))
            copied[index]["active_l1_root_ids"].pop()
            excess -= 1
        balanced[name] = copied
    return balanced


def generate(annotations, columns, steps=12, stripe_width=1.0):
    if steps < 2 or stripe_width <= 0:
        raise ValueError("steps must be >=2 and stripe_width positive")
    l1 = {row["root_id"] for row in read_rows(annotations)
          if (row.get("primary_type") or "").strip() == "L1"}
    if not l1:
        raise ValueError("No annotated L1 neurons")
    positions = {}
    for row in read_rows(columns):
        root = row.get("root_id") or row.get("pt_root_id")
        if root not in l1:
            continue
        try:
            p, q = float(row["p"]), float(row["q"])
        except (KeyError, ValueError, TypeError):
            continue
        positions.setdefault(root, (p, q))
    if not positions:
        raise ValueError("No L1 neurons with numeric p/q column coordinates")
    schedules = {}
    for name, (dp, dq) in DIRECTIONS.items():
        projection = {root: dp * p + dq * q for root, (p, q) in positions.items()}
        low, high = min(projection.values()), max(projection.values())
        frames = []
        for step in range(steps):
            center = low + (high - low) * step / (steps - 1)
            active = sorted(root for root, value in projection.items()
                            if abs(value - center) <= stripe_width / 2)
            frames.append({"step": step, "active_l1_root_ids": active})
        schedules[name] = frames
    return {"schema": "cortex.fafb_t4_spatial_inputs.v1",
            "source": "FAFB v783 annotations and column assignments",
            "stimulus_type": "moving stripe over p/q column coordinates",
            "steps": steps, "stripe_width_columns": stripe_width,
            "mapped_l1_neurons": len(positions),
            "directions": schedules,
            "neural_simulation_executed": False,
            "direction_selectivity_validated": False}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--columns", type=Path, required=True)
    parser.add_argument("--steps", type=int, default=12)
    parser.add_argument("--stripe-width", type=float, default=1.0)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = generate(args.annotations, args.columns, args.steps, args.stripe_width)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "mapped_l1_neurons": result["mapped_l1_neurons"],
                      "directions": list(result["directions"])}))

if __name__ == "__main__":
    main()
