#!/usr/bin/env python3
import argparse, csv, hashlib, json, random, shutil, sys, zipfile
from pathlib import Path

def sha256(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def receipt_assets(r):
    assets=r.get("assets",[])
    if isinstance(assets,dict):
        out=[]
        for aid, rows in assets.items():
            for cid,h,d in rows:
                out.append({"contract_asset_id":aid,"candidate_id":cid,"filename":cid+".wav","sha256":h})
        return out
    return assets

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--receipt",required=True)
    ap.add_argument("--wav-dir",required=True)
    ap.add_argument("--out-dir",required=True)
    ap.add_argument("--seed",type=int,default=91720260822)
    a=ap.parse_args()

    receipt=json.loads(Path(a.receipt).read_text())
    items=receipt_assets(receipt)
    by_asset={}
    errors=[]
    for x in items:
        p=Path(a.wav_dir)/x["filename"]
        if not p.exists():
            errors.append(f"MISSING:{p.name}"); continue
        actual=sha256(p)
        if actual!=x["sha256"]:
            errors.append(f"HASH_MISMATCH:{p.name}")
        by_asset.setdefault(x["contract_asset_id"],[]).append((x,p,actual))
    if errors:
        print(json.dumps({"status":"FAIL","errors":errors},indent=2))
        return 1
    for aid,rows in by_asset.items():
        if len(rows)<3:
            errors.append(f"NEEDS_3_VARIANTS:{aid}:{len(rows)}")
    if errors:
        print(json.dumps({"status":"FAIL","errors":errors},indent=2)); return 1

    out=Path(a.out_dir); blind=out/"blind"; sealed=out/"sealed"
    blind.mkdir(parents=True,exist_ok=True); sealed.mkdir(parents=True,exist_ok=True)
    rng=random.Random(a.seed)
    mapping=[]
    for aid in sorted(by_asset):
        rows=sorted(by_asset[aid],key=lambda z:z[0]["candidate_id"])
        labels=["A","B","C"]; rng.shuffle(labels)
        for label,(meta,p,actual) in zip(labels,rows):
            dst=blind/f"{aid}_BLIND_{label}.wav"; shutil.copyfile(p,dst)
            mapping.append({"asset_id":aid,"blind_label":label,
                            "candidate_id":meta["candidate_id"],"sha256":actual})
    (sealed/"ROOM917_E01_CRITICAL_SFX_BLIND_MAPPING_SEALED_v2.json").write_text(json.dumps(mapping,indent=2)+"\n")
    with open(blind/"ROOM917_E01_CRITICAL_SFX_BLIND_RESULTS_v2.csv","w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["asset_id","selection_A_B_C_or_REJECT_ALL","human_listen_confirmed","headphones","mono","phone","notes"])
        for aid in sorted(by_asset): w.writerow([aid,"","","","","",""])
    manifest={"schema_version":"room917.critical_sfx_blind_package/2.0",
              "status":"READY_FOR_HUMAN_BLIND_LISTEN",
              "source_receipt":Path(a.receipt).name,
              "asset_count":len(by_asset),"files_per_asset":3,
              "hard_law":"SEALED_MAPPING_MUST_NOT_BE_OPENED_BEFORE_RESULTS_ARE_FROZEN"}
    (blind/"ROOM917_E01_CRITICAL_SFX_BLIND_PACKAGE_MANIFEST_v2.json").write_text(json.dumps(manifest,indent=2)+"\n")
    zpath=out/"ROOM917_E01_CRITICAL_SFX_BLIND_PACKAGE_v2.zip"
    with zipfile.ZipFile(zpath,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(blind.iterdir()):
            z.write(p,p.name)
    print(json.dumps({"status":"PASS","blind_zip":str(zpath),"blind_zip_sha256":sha256(zpath),
                      "sealed_mapping":str(sealed/"ROOM917_E01_CRITICAL_SFX_BLIND_MAPPING_SEALED_v2.json")},indent=2))
    return 0
if __name__=="__main__": raise SystemExit(main())
