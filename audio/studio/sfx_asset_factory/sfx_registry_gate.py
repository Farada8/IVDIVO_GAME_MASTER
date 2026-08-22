#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path

REQUIRED = {
    "S13_INTERNAL_DOUBLE_RING_OLD",
    "S14_UNMARKED_GLASS_LAMP_PING",
    "S17_COPPER_HISS",
    "S19_TWO_PART_LINE_CUT",
}

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def validate_manifest(m):
    errors=[]
    recs=m.get("records",[])
    keys=set(); by={}
    for r in recs:
        k=(r.get("asset_id"), r.get("candidate"))
        if k in keys: errors.append(f"DUPLICATE_RECORD:{k}")
        keys.add(k); by[k]=r
        if r.get("machine_qc")!="PASS": errors.append(f"MACHINE_QC_NOT_PASS:{k}")
        if len(r.get("sha256",""))!=64: errors.append(f"BAD_SHA256:{k}")
    ids={r.get("asset_id") for r in recs}
    for req in sorted(REQUIRED-ids): errors.append(f"MISSING_REQUIRED:{req}")
    for a in m.get("alias_registry",[]):
        k=(a.get("canonical_cue_id"),a.get("candidate"))
        if a.get("byte_identity")!="PASS": errors.append(f"ALIAS_NOT_BYTE_IDENTICAL:{k}")
        if k in by and by[k].get("sha256") != a.get("sha256"): errors.append(f"ALIAS_HASH_MISMATCH:{k}")
    return errors,by

def validate_lock(m, lock):
    errors,by=validate_manifest(m)
    if errors: return "FAIL",errors
    sels=lock.get("selections",[])
    if not sels: return "HOLD",["HUMAN_BLIND_SELECTIONS_PENDING"]
    seen=set()
    for s in sels:
        aid=s.get("asset_id"); cand=s.get("candidate"); sha=s.get("sha256")
        seen.add(aid); r=by.get((aid,cand))
        if not r: errors.append(f"LOCK_SELECTION_NOT_IN_MANIFEST:{aid}:{cand}")
        elif r.get("sha256")!=sha: errors.append(f"LOCK_HASH_MISMATCH:{aid}:{cand}")
        if s.get("human_blind_result")!="ACCEPT": errors.append(f"NO_HUMAN_ACCEPT:{aid}")
    for aid in sorted(REQUIRED-seen): errors.append(f"LOCK_MISSING_REQUIRED:{aid}")
    return ("FAIL",errors) if errors else ("PASS",[])

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("manifest"); ap.add_argument("--lock")
    args=ap.parse_args(); m=load(args.manifest)
    if args.lock: status,errors=validate_lock(m,load(args.lock))
    else:
        errors,_=validate_manifest(m); status="FAIL" if errors else "PASS"
    print(json.dumps({"status":status,"errors":errors},indent=2))
    return {"PASS":0,"HOLD":2,"FAIL":1}[status]

if __name__=="__main__": raise SystemExit(main())
