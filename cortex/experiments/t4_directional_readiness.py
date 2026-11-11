"""Audit real FAFB v783 inputs needed for directional T4 experiments.

This is a feasibility check, NOT evidence of direction selectivity.
"""
from __future__ import annotations
import argparse
import csv
import gzip
import json
from collections import Counter
from pathlib import Path

def rows(path):
    with gzip.open(path, "rt", encoding="utf-8-sig", newline="") as stream:
        yield from csv.DictReader(stream)

def audit(annotations, columns):
    types = {}
    for row in rows(annotations):
        label = (row.get("primary_type") or "").strip()
        if label in {"L1", "Mi1", "Tm3", "T4a", "T4b", "T4c", "T4d"}:
            types[row["root_id"]] = label
    counts = Counter(types.values())
    with gzip.open(columns, "rt", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames or []
        id_field = next((f for f in ("root_id", "pt_root_id") if f in fields), None)
        matched = Counter()
        assigned = set()
        if id_field:
            for row in reader:
                root = row.get(id_field)
                if root in types:
                    matched[types[root]] += 1
                    assigned.add(root)
    return {
        "annotation_counts": dict(sorted(counts.items())),
        "column_assignment_fields": fields,
        "column_assignment_id_field": id_field,
        "column_rows_matched_by_type": dict(sorted(matched.items())),
        "unique_annotated_cells_with_column_rows": len(assigned),
        "has_all_four_t4_subtypes": all(counts[x] > 0 for x in ("T4a","T4b","T4c","T4d")),
        "spatial_stimulus_implemented": False,
        "direction_selectivity_validated": False,
        "note": "Anatomical column metadata must be mapped and tested before moving-bar stimulation."
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--annotations", required=True)
    p.add_argument("--columns", required=True)
    args = p.parse_args()
    print(json.dumps(audit(Path(args.annotations), Path(args.columns)), indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
