#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

def getv(d, canonical, legacy=None):
    if canonical in d: return d[canonical]
    if legacy and legacy in d: return d[legacy]
    raise KeyError(canonical)

def overlap(a0,a1,b0,b1): return max(a0,b0)<min(a1,b1)

def block_time(b):
    if "start_seconds" in b and "end_seconds" in b:
        return float(b["start_seconds"]),float(b["end_seconds"])
    if "start_s" in b and "end_s" in b:
        return float(b["start_s"]),float(b["end_s"])
    return None

def classify(interval,lineage):
    s=float(getv(interval,"start_seconds","start_s"))
    e=float(getv(interval,"end_seconds","end_s"))
    for p in lineage.get("protected_global",[]):
        if ("start_seconds" in p and "end_seconds" in p) or ("start_s" in p and "end_s" in p):
            ps=float(p.get("start_seconds",p.get("start_s"))); pe=float(p.get("end_seconds",p.get("end_s")))
            if overlap(s,e,ps,pe): return "PROTECTED_AUTHORED_PAUSE","EXACT_PROTECTED_RANGE"
    resolved=[]
    for b in lineage.get("blocks",[]):
        bt=block_time(b)
        if bt and overlap(s,e,*bt): resolved.append(b)
    if not resolved:
        return "UNKNOWN_REQUIRES_LISTEN_OR_LIVE_TIMELINE","NO_RESOLVED_BLOCK_TIMING"
    room_required=any(lineage.get("rooms",{}).get(b["room_id"],{}).get("bed_expectation","").startswith("CONTINUOUS") for b in resolved)
    threshold=float(interval.get("threshold_dbfs",-999)); dur=e-s
    if room_required and threshold<=-85.0 and dur>=0.5:
        return "MISSING_ROOM_OR_AMBIENCE_SUPPORT","RESOLVED_BLOCK_PLUS_CONTINUOUS_ROOM_CONTRACT_PLUS_NEAR_DIGITAL_SILENCE"
    return "UNKNOWN_REQUIRES_LISTEN_OR_LIVE_TIMELINE","LEVEL_NOT_SUFFICIENT_FOR_SAFE_CLASSIFICATION"

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--intervals",required=True); ap.add_argument("--lineage",required=True); ap.add_argument("--out",required=True)
    args=ap.parse_args()
    data=json.loads(Path(args.intervals).read_text()); lin=json.loads(Path(args.lineage).read_text())
    src=data.get("intervals",data.get("rows",[])); rows=[]
    for x in src:
        s=float(getv(x,"start_seconds","start_s")); e=float(getv(x,"end_seconds","end_s"))
        c,r=classify(x,lin)
        y=dict(x); y.pop("start_s",None); y.pop("end_s",None)
        y["start_seconds"]=s; y["end_seconds"]=e; y["duration_seconds"]=float(x.get("duration_seconds",e-s))
        y["classification"]=c; y["classification_reason"]=r; y["patch_authorized"]=c=="MISSING_ROOM_OR_AMBIENCE_SUPPORT"
        rows.append(y)
    out={"schema_version":"room917.interval_classification/1.1","canonical_interval_schema":"ivdivo.audio.canonical_interval/1.0","count":len(rows),"rows":rows}
    Path(args.out).write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n")
    print(f"PASS intervals={len(rows)} patchable={sum(r['patch_authorized'] for r in rows)}")
if __name__=="__main__": main()
