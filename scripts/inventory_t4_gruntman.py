"""Inventory downloaded T4 physiology files without treating them as validated traces."""
from __future__ import annotations
import argparse
import json
import tarfile
import zipfile
from pathlib import Path

def inspect_file(path: Path) -> dict:
    result = {"name": path.name, "bytes": path.stat().st_size, "format": path.suffix.lower(), "entries": []}
    try:
        if zipfile.is_zipfile(path):
            result["format"] = "zip"
            with zipfile.ZipFile(path) as archive:
                entries = archive.infolist()
                result["entry_count"] = len(entries)
                result["entries"] = [{"name": e.filename, "bytes": e.file_size} for e in entries[:200]]
                result["truncated"] = len(entries) > 200
        elif tarfile.is_tarfile(path):
            result["format"] = "tar"
            with tarfile.open(path) as archive:
                entries = archive.getmembers()
                result["entry_count"] = len(entries)
                result["entries"] = [{"name": e.name, "bytes": e.size} for e in entries[:200]]
                result["truncated"] = len(entries) > 200
        elif path.suffix.lower() in {".csv", ".tsv", ".txt"}:
            with path.open("r", encoding="utf-8", errors="replace") as stream:
                result["header_preview"] = [stream.readline().rstrip("\n")[:500] for _ in range(3)]
    except (OSError, ValueError, zipfile.BadZipFile, tarfile.TarError) as exc:
        result["inspection_error"] = str(exc)
    return result

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=Path("data/t4/gruntman_manifest.json"))
    parser.add_argument("--output", type=Path, default=Path("data/t4/gruntman_inventory.json"))
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    records = []
    for entry in manifest.get("files", []):
        local = entry.get("local_file")
        if not local:
            continue
        path = Path(local)
        if not path.is_file():
            raise FileNotFoundError(path)
        if path.stat().st_size != entry.get("size"):
            raise ValueError(f"size mismatch: {path}")
        records.append(inspect_file(path))
    report = {
        "source_article_id": manifest.get("article_id"),
        "source_doi": manifest.get("doi"),
        "source_title": manifest.get("title"),
        "license": manifest.get("license"),
        "download_status": manifest.get("status"),
        "file_count": len(records),
        "files": records,
        "biologically_validated": False,
        "next_gate": "Review actual experimental stimulus metadata, T4 subtype labels and per-animal traces before numerical comparison."
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
