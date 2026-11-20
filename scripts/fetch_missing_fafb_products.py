"""Fetch missing public FAFB v783 data products into a local/cache directory.

Sources are official FlyWire Codex static downloads. Do not commit bulk datasets
to Git: record hashes and store large files as workflow artifacts or external data.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import urllib.request
from pathlib import Path

BASE = "https://storage.googleapis.com/flywire-data/codex/data/fafb/783"
PRODUCTS = {
    "connections_princeton_no_threshold": "connections_princeton_no_threshold.csv.gz",
    "synapse_coordinates": "synapse_coordinates.csv.gz",
    "fafb_v783_princeton_synapse_table": "fafb_v783_princeton_synapse_table.csv.gz",
}
def fetch(name: str, destination: Path) -> dict:
    if name not in PRODUCTS:
        raise ValueError(f"unknown data product: {name}")
    destination.mkdir(parents=True, exist_ok=True)
    filename = PRODUCTS[name]
    path = destination / filename
    url = f"{BASE}/{filename}"
    if not path.exists():
        tmp = path.with_suffix(path.suffix + ".partial")
        try:
            with urllib.request.urlopen(url, timeout=120) as source, tmp.open("wb") as out:
                while chunk := source.read(1024 * 1024):
                    out.write(chunk)
            tmp.replace(path)
        finally:
            tmp.unlink(missing_ok=True)
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return {"product": name, "source": url, "path": str(path),
            "bytes": path.stat().st_size, "sha256": digest.hexdigest()}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("products", nargs="+", choices=sorted(PRODUCTS))
    parser.add_argument("--output", default="data/external/fafb_v783")
    args = parser.parse_args()
    print(json.dumps([fetch(name, Path(args.output)) for name in args.products], indent=2))

if __name__ == "__main__":
    main()
