#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--semantic-lineage",required=True)
    ap.add_argument("--timing-map",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    lin=json.loads(Path(args.semantic_lineage).read_text(encoding="utf-8"))
    tm=json.loads(Path(args.timing_map).read_text(encoding="utf-8"))
    times={x["block_id"]:x for x in tm.get("blocks",[])}
    errors=[]; blocks=[]
    for b in lin.get("blocks",[]):
        n=dict(b); t=times.get(b["block_id"])
        if t:
            grade=t.get("evidence_grade")
            if grade not in {"ACCEPTED_ALIGNMENT","LIVE_TIMELINE"}:
                errors.append(f"{b['block_id']}: timing evidence grade must be ACCEPTED_ALIGNMENT/LIVE_TIMELINE")
            else:
                s=float(t["start_seconds"]); e=float(t["end_seconds"])
                if e<=s: errors.append(f"{b['block_id']}: invalid timing")
                else:
                    n["start_seconds"]=s; n["end_seconds"]=e; n["timing_evidence_grade"]=grade
                    n["timing_source"]=t.get("source")
        blocks.append(n)
    resolved=sum(1 for b in blocks if "start_seconds" in b)
    out=dict(lin); out["schema_version"]="room917.resolved_cue_lineage/1.0"; out["blocks"]=blocks
    out["timing_state"]="RESOLVED_COMPLETE" if resolved==len(blocks) else ("RESOLVED_PARTIAL" if resolved else "SEMANTIC_ONLY")
    out["resolved_block_count"]=resolved
    out["status"]="FAIL" if errors else "PASS"
    Path(args.out).write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    if errors:
        print("\n".join(errors),file=sys.stderr); return 2
    print(f"PASS timing={out['timing_state']} resolved={resolved}/{len(blocks)}")
    return 0
if __name__=="__main__": raise SystemExit(main())
