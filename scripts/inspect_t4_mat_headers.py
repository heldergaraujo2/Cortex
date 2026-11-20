"""Inspect MATLAB headers inside Gruntman ZIP without extracting multi-GB payloads."""
from __future__ import annotations
import argparse
import json
import zipfile
from collections import Counter
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",type=Path,default=Path("data/t4/gruntman_manifest.json"))
    p.add_argument("--output",type=Path,default=Path("data/t4/gruntman_mat_headers.json"))
    a=p.parse_args()
    manifest=json.loads(a.manifest.read_text(encoding="utf-8"))
    reports=[]
    for entry in manifest["files"]:
        archive_path=Path(entry["local_file"])
        with zipfile.ZipFile(archive_path) as z:
            for info in z.infolist():
                if info.is_dir() or info.filename.startswith("__MACOSX/") or not info.filename.lower().endswith(".mat"):
                    continue
                with z.open(info) as f:
                    header=f.read(128)
                fmt=("MATLAB-v5" if header.startswith(b"MATLAB 5.0 MAT-file") else
                     "HDF5-v7.3" if header.startswith(b"\\x89HDF\\r\\n\\x1a\\n") or b"MATLAB 7.3 MAT-file" in header else "unknown")
                reports.append({"path":info.filename,"bytes":info.file_size,"mat_format":fmt,"header":header[:116].decode("ascii","replace").strip()})
    result={"source_article_id":manifest["article_id"],"mat_files":len(reports),"formats":dict(Counter(r["mat_format"] for r in reports)),"files":reports,"biologically_validated":False,"note":"Headers only; no subtype or physiological measurement has been validated."}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"mat_files":result["mat_files"],"formats":result["formats"],"examples":reports[:12]},indent=2))
if __name__=="__main__":
    main()
