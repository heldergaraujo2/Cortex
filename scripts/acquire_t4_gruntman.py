"""Download and inventory the Gruntman T4 Figshare article without inventing data.

Usage: python scripts/acquire_t4_gruntman.py --manifest data/t4/gruntman_manifest.json
       python scripts/acquire_t4_gruntman.py --manifest data/t4/gruntman_manifest.json --download
By default this retrieves metadata only; --download fetches files into the
manifest's parent directory. Verify license and subtype metadata before analysis.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

ARTICLE_ID = 5576101
API = f"https://api.figshare.com/v2/articles/{ARTICLE_ID}"


def fetch(url: str) -> bytes:
    with urlopen(Request(url, headers={"User-Agent": "Cortex-T4-research/1.0"}), timeout=60) as response:
        return response.read()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=Path("data/t4/gruntman_manifest.json"))
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    metadata = json.loads(fetch(API))
    manifest = {
        "source_api": API,
        "article_id": ARTICLE_ID,
        "doi": metadata.get("doi"),
        "title": metadata.get("title"),
        "license": metadata.get("license"),
        "published_date": metadata.get("published_date"),
        "status": "metadata_only",
        "biologically_validated": False,
        "files": [],
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    for file in metadata.get("files", []):
        entry = {key: file.get(key) for key in ("id", "name", "size", "download_url", "computed_md5", "supplied_md5")}
        if args.download:
            name = Path(str(file["name"])).name
            if name in (".", "..") or not name:
                raise ValueError("unsafe filename")
            target = args.manifest.parent / f"{file['id']}_{name}"
            content = fetch(file["download_url"])
            if len(content) != file["size"]:
                raise ValueError(f"size mismatch for {name}")
            entry["sha256"] = hashlib.sha256(content).hexdigest()
            entry["local_file"] = str(target)
            target.write_bytes(content)
        manifest["files"].append(entry)
    if args.download:
        manifest["status"] = "downloaded_unreviewed"
    args.manifest.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Manifest: {args.manifest}; files: {len(manifest['files'])}; status: {manifest['status']}")


if __name__ == "__main__":
    main()
