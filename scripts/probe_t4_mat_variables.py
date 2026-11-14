"""Extract bounded MATLAB variable metadata, never invent physiological labels.

Usage: python scripts/probe_t4_mat_variables.py --manifest data/t4/gruntman_manifest.json
Requires scipy for MATLAB v5 and h5py for MATLAB v7.3.
"""
from __future__ import annotations
import argparse
import json
import tempfile
import zipfile
from pathlib import Path

def probe_v5(path: Path) -> dict:
    from scipy.io import whosmat
    return {"format": "MATLAB-v5", "variables": [
        {"name": name, "shape": list(shape), "class": kind}
        for name, shape, kind in whosmat(str(path))
    ]}

def probe_hdf5(path: Path) -> dict:
    import h5py
    variables = []
    with h5py.File(path, "r") as f:
        def visitor(name, obj):
            if len(variables) >= 3000:
                return
            variables.append({"name": name, "kind": "dataset" if isinstance(obj, h5py.Dataset) else "group",
                              "shape": list(obj.shape) if isinstance(obj, h5py.Dataset) else None})
        f.visititems(visitor)
    return {"format": "HDF5-v7.3", "variables": variables, "truncated": len(variables) >= 3000}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--manifest",type=Path,default=Path("data/t4/gruntman_manifest.json"))
    parser.add_argument("--output",type=Path,default=Path("data/t4/gruntman_mat_variables.json"))
    parser.add_argument("--max-files",type=int,default=8)
    parser.add_argument("--max-member-mb",type=int,default=150)
    args=parser.parse_args()
    manifest=json.loads(args.manifest.read_text(encoding="utf-8"))
    results=[]
    for entry in manifest.get("files",[]):
        with zipfile.ZipFile(entry["local_file"]) as archive:
            candidates=[i for i in archive.infolist() if not i.is_dir() and
                        i.filename.lower().endswith(".mat") and not i.filename.startswith("__MACOSX/")]
            for info in sorted(candidates,key=lambda x:x.file_size):
                if len(results)>=args.max_files: break
                if info.file_size>args.max_member_mb*1024*1024: continue
                record={"archive_member":info.filename,"bytes":info.file_size}
                try:
                    with tempfile.TemporaryDirectory() as tmp:
                        target=Path(tmp)/"sample.mat"
                        with archive.open(info) as src, target.open("wb") as dst:
                            import shutil
                            shutil.copyfileobj(src,dst)
                        with target.open("rb") as fh: header=fh.read(128)
                        if header.startswith(b"MATLAB 5.0 MAT-file"):
                            record.update(probe_v5(target))
                        elif header.startswith(b"\\x89HDF\\r\\n\\x1a\\n") or b"MATLAB 7.3 MAT-file" in header:
                            record.update(probe_hdf5(target))
                        else:
                            record["error"]="unsupported MATLAB header"
                except Exception as exc:
                    record["error"]=f"{type(exc).__name__}: {exc}"
                results.append(record)
    report={"article_id":manifest.get("article_id"),"sampled_files":len(results),
            "records":results,"biologically_validated":False,
            "warning":"Variable names/shapes are metadata, not evidence of T4 subtype or calibrated direction."}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2,ensure_ascii=False))
if __name__=="__main__":
    main()
