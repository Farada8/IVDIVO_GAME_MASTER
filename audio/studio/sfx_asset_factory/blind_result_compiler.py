#!/usr/bin/env python3
import argparse, csv, json
from pathlib import Path

REQUIRED={
 "A01_STORM","A01_CLOCK","A01_TRANSFORMER_50HZ","A02_RELAY_TREMBLE",
 "SELECTOR_916","LAMP_916_MARKED","S13_DOUBLE_RING","S14_UNMARKED_LAMP",
 "S17_COPPER_HISS","S19_TWO_PART_CUT"
}

def load_json(p): return json.loads(Path(p).read_text(encoding="utf-8"))

def compile_results(mapping,rows):
    by={(m["asset"],m["blind_label"]):m for m in mapping}
    errors=[];selections=[];seen=set();rejects=[]
    for r in rows:
        asset=r.get("asset","").strip()
        if not asset: continue
        if asset in seen: errors.append(f"DUPLICATE_ASSET:{asset}")
        seen.add(asset)
        choice=r.get("selection","").strip().upper()
        att=r.get("human_listen_confirmed","").strip().lower()
        if att not in {"true","yes","1"}:
            errors.append(f"HUMAN_ATTESTATION_MISSING:{asset}"); continue
        if choice=="REJECT_BOTH": rejects.append(asset); continue
        if choice not in {"X","Y"}:
            errors.append(f"BAD_SELECTION:{asset}:{choice or 'EMPTY'}"); continue
        m=by.get((asset,choice))
        if not m:
            errors.append(f"MAPPING_NOT_FOUND:{asset}:{choice}"); continue
        selections.append({"asset_id":asset,"candidate":m["candidate"],"sha256":m["sha256"],"human_blind_result":"ACCEPT","blind_label":choice})
    for asset in sorted(REQUIRED-seen): errors.append(f"MISSING_ASSET_RESULT:{asset}")
    if errors: return "FAIL",None,errors
    if rejects: return "HOLD",None,[f"REJECT_BOTH:{a}" for a in sorted(rejects)]
    lock={"schema_version":"room917.sfx_human_lock/2.0","status":"HUMAN_BLIND_ACCEPTED","source_blind_pack":"ROOM917_SFX_FULL_BLIND_v6.zip","selections":selections}
    return "PASS",lock,[]

def main():
    ap=argparse.ArgumentParser();ap.add_argument("mapping");ap.add_argument("results_csv");ap.add_argument("--out",default="ROOM917_SFX_HUMAN_LOCK_v2.json")
    a=ap.parse_args();mapping=load_json(a.mapping)
    with open(a.results_csv,newline="",encoding="utf-8-sig") as f: rows=list(csv.DictReader(f))
    status,lock,errors=compile_results(mapping,rows)
    if lock: Path(a.out).write_text(json.dumps(lock,indent=2),encoding="utf-8")
    print(json.dumps({"status":status,"errors":errors,"lock_written":bool(lock)},indent=2))
    return {"PASS":0,"HOLD":2,"FAIL":1}[status]

if __name__=="__main__": raise SystemExit(main())
