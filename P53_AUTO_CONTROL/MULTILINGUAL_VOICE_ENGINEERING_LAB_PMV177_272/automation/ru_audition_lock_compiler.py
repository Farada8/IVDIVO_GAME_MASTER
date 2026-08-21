#!/usr/bin/env python3
import argparse, json, hashlib
from pathlib import Path

REQUIRED_ROLES={"NATIVE_RU","STAGE","LIVE_AUDIO","CLOSE_PROTECTION"}

def sha(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--anchors",type=Path,required=True)
    ap.add_argument("--decisions",type=Path,nargs="+",required=True)
    ap.add_argument("--timing-pass",action="store_true")
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    a=json.loads(args.anchors.read_text(encoding="utf-8"))
    decisions=[]; roles=set()
    for p in args.decisions:
        d=json.loads(p.read_text(encoding="utf-8"))
        roles.add(d["reviewer"]["role"])
        decisions.extend(d.get("items",[]))
    missing=REQUIRED_ROLES-roles
    if missing:
        raise SystemExit("FAIL-CLOSED missing reviewer roles: "+",".join(sorted(missing)))
    if not args.timing_pass:
        raise SystemExit("FAIL-CLOSED performed timing evidence missing")
    patch_by_id={x["item_id"]:x for x in decisions if x.get("decision")=="PATCH" and x.get("replacement_text")}
    hold=[x for x in decisions if x.get("decision")=="HOLD"]
    if hold:
        raise SystemExit(f"FAIL-CLOSED unresolved HOLD decisions: {len(hold)}")
    locked=[]
    for x in a["anchors"]:
        bid=x["block_id"]
        text=patch_by_id.get(bid,{}).get("replacement_text",x["text_ru"])
        locked.append({**x,"text_ru":text,"text_ru_sha256":sha(text),"human_native_qa":"PASS","practitioner_qa":"PASS"})
    out={"artifact":"BODYGUARD_E01_RU_AUDITION_ANCHORS_v1_0_LOCKED","status":"LOCKED","source":a["artifact"],"anchors":locked,"review_roles":sorted(roles),"performed_timing":"PASS","ordered_anchor_hash":sha("\n".join(x["text_ru"] for x in locked))}
    args.out.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
    print("LOCKED",len(locked),out["ordered_anchor_hash"])

if __name__=="__main__": main()
