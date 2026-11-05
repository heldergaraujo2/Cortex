#!/usr/bin/env python3
"""Create a conservative CATMAID skeleton -> FlyWire v783 crosswalk.

Input is the R-generated CSV containing only Mi1 annotations with a verified
local M10 coordinate. This script uses fafbseg's published skid_to_id routine,
which downloads CATMAID skeleton nodes, transforms FAFB14 -> FlyWire space,
looks up the segmentation at each node, and reports the most frequent root ID.

No root ID is accepted/rejected automatically by confidence threshold. Every
result is retained with its confidence score and status for later review.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="mi1_catmaid_skids_for_crosswalk.csv")
    parser.add_argument("--output", required=True, help="Output CSV path")
    parser.add_argument("--catmaid-url", default="https://fafb.catmaid.virtualflybrain.org/")
    parser.add_argument("--project-id", type=int, default=1)
    parser.add_argument("--batch-size", type=int, default=10)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = os.environ.get("FLYWIRE_TOKEN", "").strip()
    if not token:
        raise SystemExit("FLYWIRE_TOKEN is required; provide it as a GitHub Actions secret or environment variable.")

    from fafbseg import flywire
    import pymaid

    flywire.set_chunkedgraph_secret(token, overwrite=True)
    catmaid_token = os.environ.get("CATMAID_API_TOKEN") or None
    catmaid = pymaid.CatmaidInstance(
        args.catmaid_url,
        project_id=args.project_id,
        api_token=catmaid_token,
    )

    source = pd.read_csv(args.input, dtype={"skid": "string"})
    required = {"skid", "anno_Mi1_row", "Mi1_M10_row"}
    missing = required.difference(source.columns)
    if missing:
        raise ValueError(f"Input is missing required columns: {sorted(missing)}")
    if source["skid"].isna().any() or source["skid"].duplicated().any():
        raise ValueError("Input skid values must be present and unique.")
    if not source["Mi1_M10_row"].notna().all():
        raise ValueError("Input must contain only rows with verified M10 coordinates.")

    results: dict[str, dict] = {}

    def map_batch(skids: list[str]) -> None:
        try:
            frame = flywire.skid_to_id(
                [int(s) for s in skids],
                catmaid_instance=catmaid,
                progress=False,
                sample=None,
                dataset="flat_783",
            )
            if frame is not None and len(frame):
                for row in frame.to_dict(orient="records"):
                    sid = str(int(row["skeleton_id"]))
                    fid = row.get("flywire_id")
                    results[sid] = {
                        "flywire_id": "" if pd.isna(fid) else str(int(fid)),
                        "confidence": row.get("confidence"),
                        "crosswalk_status": "mapped_top_candidate",
                        "error": "",
                    }
        except Exception as exc:
            # A batch failure must not discard the entire cohort. Retry each
            # skeleton independently so failures remain attributable.
            batch_error = f"{type(exc).__name__}: {exc}"
            for skid in skids:
                try:
                    frame = flywire.skid_to_id(
                        int(skid),
                        catmaid_instance=catmaid,
                        progress=False,
                        sample=None,
                        dataset="flat_783",
                    )
                    if frame is None or frame.empty:
                        raise RuntimeError("fafbseg returned no mapping row")
                    row = frame.iloc[0]
                    fid = row["flywire_id"]
                    results[skid] = {
                        "flywire_id": "" if pd.isna(fid) else str(int(fid)),
                        "confidence": row.get("confidence"),
                        "crosswalk_status": "mapped_top_candidate",
                        "error": "",
                    }
                except Exception as single_exc:
                    results[skid] = {
                        "flywire_id": "",
                        "confidence": "",
                        "crosswalk_status": "lookup_failed",
                        "error": f"batch={batch_error}; single={type(single_exc).__name__}: {single_exc}"[:1000],
                    }

    skids = source["skid"].astype(str).tolist()
    for start in range(0, len(skids), args.batch_size):
        batch = skids[start : start + args.batch_size]
        map_batch(batch)
        print(f"Processed {min(start + len(batch), len(skids))}/{len(skids)} CATMAID IDs", flush=True)

    mapped_rows = []
    for row in source.to_dict(orient="records"):
        skid = str(row["skid"])
        result = results.get(
            skid,
            {
                "flywire_id": "",
                "confidence": "",
                "crosswalk_status": "no_result",
                "error": "No result returned for this skeleton ID.",
            },
        )
        mapped_rows.append({**row, **result, "target_dataset": "flat_783"})

    output = pd.DataFrame(mapped_rows)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_path, index=False)

    counts = output["crosswalk_status"].value_counts(dropna=False).to_dict()
    print(f"Saved {len(output)} rows to {output_path}")
    print(f"Status counts: {counts}")
    print("Confidence is retained as returned by fafbseg; no automatic acceptance threshold was applied.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
