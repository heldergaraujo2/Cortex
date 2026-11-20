"""Inspect top-level fields of Gruntman MATLAB protocolStruct without guessing meaning."""
from __future__ import annotations
import argparse,json,tempfile,zipfile,shutil
from pathlib import Path
from scipy.io import loadmat

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--manifest",type=Path,default=Path("data/t4/gruntman_manifest.json"))
 p.add_argument("--output",type=Path,default=Path("data/t4/gruntman_struct_fields.json"))
 p.add_argument("--max-files",type=int,default=3)
 a=p.parse_args()
 manifest=json.loads(a.manifest.read_text(encoding="utf-8"))
 records=[]
 for item in manifest["files"]:
  with zipfile.ZipFile(item["local_file"]) as archive:
   members=sorted((x for x in archive.infolist() if x.filename.endswith(".mat") and not x.filename.startswith("__MACOSX/") and x.file_size<60*1024*1024),key=lambda x:x.file_size)
   for member in members[:max(0,a.max_files-len(records))]:
    record={"archive_member":member.filename,"bytes":member.file_size}
    try:
     with tempfile.TemporaryDirectory() as directory:
      dest=Path(directory)/"sample.mat"
      with archive.open(member) as source,dest.open("wb") as target:shutil.copyfileobj(source,target)
      data=loadmat(dest,variable_names=["protocolStruct"],struct_as_record=True,squeeze_me=False)
      obj=data.get("protocolStruct")
      record["field_names"]=list(obj.dtype.names or []) if obj is not None else []
      record["struct_shape"]=list(obj.shape) if obj is not None else None
    except Exception as e:record["error"]=f"{type(e).__name__}: {e}"
    records.append(record)
 result={"article_id":manifest.get("article_id"),"records":records,"biologically_validated":False,"note":"Field names alone do not prove physiological subtype labels or directions."}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
