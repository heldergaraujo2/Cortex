"""Inspect local FAFB CSV/GZ schemas without loading full datasets into memory.

Reports actual column names and a few redacted-free example field values.
No biological identity or circuit membership is inferred from the sample.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import json
from pathlib import Path


def inspect_csv(path: str | Path, *, sample_rows: int = 3) -> dict[str, object]:
    path = Path(path)
    if sample_rows < 0 or sample_rows > 10:
        raise ValueError("sample_rows must be between 0 and 10")
    opener = gzip.open if path.suffix.lower() == ".gz" else open
    with opener(path, "rt", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames:
            raise ValueError("CSV has no header")
        examples = [row for _, row in zip(range(sample_rows), reader)]
    return {"file": str(path), "columns": reader.fieldnames, "examples": examples}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+")
    parser.add_argument("--sample-rows", type=int, default=2)
    args = parser.parse_args()
    print(json.dumps(
        [inspect_csv(path, sample_rows=args.sample_rows) for path in args.files],
        indent=2, ensure_ascii=False
    ))


if __name__ == "__main__":
    main()
