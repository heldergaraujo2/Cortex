"""Probe actual T4 stimulus structure metadata without exporting biological traces."""
from __future__ import annotations
import argparse, json, shutil, tempfile, zipfile
from pathlib import Path
import numpy as np
from scipy.io import loadmat

def describe(value, depth=0):
    if depth > 2:
        return {"type": type(value).__name__}
    if isinstance(value, np.ndarray):
        out = {"type": "ndarray", "shape": list(value.shape), "dtype": str(value.dtype)}
        if value.dtype.names:
            out["fields"] = {k: describe(value[k].flat[0], depth+1) if value[k].size else {"empty": True} for k in value.dtype.names[:60]}
        elif value.dtype == object and value.size:
            out["first_element"] = describe(value.flat[0], depth+1)
        elif value.size <= 24 and value.dtype.kind in "iufb":
            out["small_numeric_preview"] = value.tolist()
        return out
    if isinstance(value, np.void) and value.dtype.names:
        return {"type": "struct", "fields": {k: describe(value[k],depth+1) for k in value.dtype.names[:60]}}
    if isinstance(value, (str, int, float, bool)):
        return {"type": type(value).__name__, "value": value if isinstance(value,str) and len(value)<120 else None}
    return {"type": type(value).__name__}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",type=Path,default=Path("data/t4/gruntman_manifest.json"))
    p.add_argument("--output",type=Path,default=Path("data/t4/gruntman_stimulus_schema.json"))
    p.add_argument("--max-files",type=int,default=3)
    args=p.parse_args()
    manifest=json.loads(args.manifest.read_text(encoding="utf-8"))
    results=[]
    for item in manifest["files"]:
        with zipfile.ZipFile(item["local_file"]) as archive:
            members=sorted((x for x in archive.infolist() if x.filename.endswith(".mat") and not x.filename.startswith("__MACOSX/") and x.file_size<60*1024*1024),key=lambda x:x.file_size)
            for member in members:
                if len(results)>=args.max_files:break
                rec={"archive_member":member.filename}
                try:
                    with tempfile.TemporaryDirectory() as tmp:
                        path=Path(tmp)/"sample.mat"
                        with archive.open(member) as src,path.open("wb") as dst:shutil.copyfileobj(src,dst)
                        data=loadmat(path,variable_names=["protocolStruct"],struct_as_record=True,squeeze_me=False)
                        obj=data["protocolStruct"]
                        rec["fields"]={name:describe(obj[name].flat[0]) for name in ("orientations","stimSeqCell","stim","inputParams","repeats","randomize") if name in (obj.dtype.names or ())}
                except Exception as exc:
                    rec["error"]=f"{type(exc).__name__}: {exc}"
                results.append(rec)
    report={"article_id":manifest.get("article_id"),"records":results,"biologically_validated":False,"warning":"Metadata and tiny previews only. No neural responses or subtype identities inferred."}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2,ensure_ascii=False))
if __name__=="__main__":main()
