from __future__ import annotations

import csv
import gzip
import hashlib
import json
from pathlib import Path

DATA_DIR = Path("data/raw/fafb_v783")
FILES = (
    "consolidated_cell_types.csv.gz",
    "connections_princeton.csv.gz",
    "coordinates.csv.gz",
)
REPORT_PATH = Path("fafb_v783_validation_report.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_csv(path: Path) -> dict:
    result = {
        "file": path.name,
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "columns": [],
        "data_rows": 0,
        "sample_rows": [],
        "gzip_csv_readable": False,
    }

    with gzip.open(path, "rt", encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream)
        result["columns"] = next(reader, [])
        for row in reader:
            result["data_rows"] += 1
            if len(result["sample_rows"]) < 2:
                result["sample_rows"].append(
                    [cell[:160] for cell in row[:12]]
                )

    result["gzip_csv_readable"] = True
    return result


def main() -> int:
    report = {
        "dataset": "FlyWire FAFB v783",
        "purpose": "Automated structural validation of the three pilot data files",
        "files": [],
        "errors": [],
    }

    for filename in FILES:
        path = DATA_DIR / filename
        if not path.is_file():
            report["errors"].append(f"Missing file: {path.as_posix()}")
            continue

        try:
            item = inspect_csv(path)
            report["files"].append(item)
            print(f"\nFILE: {item['file']}")
            print(f"SIZE_BYTES: {item['size_bytes']}")
            print(f"SHA256: {item['sha256']}")
            print("COLUMNS: " + json.dumps(item["columns"], ensure_ascii=False))
            print(f"DATA_ROWS: {item['data_rows']}")
            print("SAMPLE_ROWS: " + json.dumps(item["sample_rows"], ensure_ascii=False))
            print("GZIP_CSV_READABLE: true")
        except Exception as exc:  # Report corruption/schema problems without hiding them.
            message = f"{filename}: {type(exc).__name__}: {exc}"
            report["errors"].append(message)
            print(f"ERROR: {message}")

    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\nREPORT_PATH: {REPORT_PATH.as_posix()}")
    print(f"FILES_OK: {len(report['files'])}/{len(FILES)}")
    print(f"ERRORS: {len(report['errors'])}")
    return 1 if report["errors"] or len(report["files"]) != len(FILES) else 0


if __name__ == "__main__":
    raise SystemExit(main())
