#!/usr/bin/env python3
import argparse, csv, json, sys
from pathlib import Path

REQUIRED={"S07_TRANSFORMER_WAKE","S08_RELAY_RIPPLE","S10_SELECTOR_916","S11_GLASS_LAMP_916_PING",
"S13_INTERNAL_DOUBLE_RING_OLD","S14_UNMARKED_GLASS_LAMP_PING","S17_COPPER_HISS","S19_TWO_PART_LINE_CUT"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mapping",required=True)
    ap.add_argument("--results",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    mapping=json.loads(Path(a.mapping).read_text())
    by={(x["asset_id"],x["blind_label"]):x for x in mapping}
    with open(a.results,newline="",encoding="utf-8-sig") as f:
        rows=list(csv.DictReader(f))
    errors=[]; hold=[]; selections=[]; seen=set()
    for r in rows:
        aid=r["asset_id"].strip()
        if not aid: continue
        seen.add(aid)
        if r["human_listen_confirmed"].strip().lower() not in {"true","yes","1"}:
            errors.append(f"HUMAN_ATTESTATION_MISSING:{aid}"); continue
        choice=r["selection_A_B_C_or_REJECT_ALL"].strip().upper()
        if choice=="REJECT_ALL":
            hold.append(aid); continue
        if choice not in {"A","B","C"}:
            errors.append(f"BAD_SELECTION:{aid}:{choice or 'EMPTY'}"); continue
        m=by.get((aid,choice))
        if not m:
            errors.append(f"NO_MAPPING:{aid}:{choice}"); continue
        selections.append({"asset_id":aid,"candidate_id":m["candidate_id"],
                           "sha256":m["sha256"],"human_blind_result":"ACCEPT"})
    for aid in sorted(REQUIRED-seen): errors.append(f"MISSING_RESULT:{aid}")
    if errors:
        print(json.dumps({"status":"FAIL","errors":errors},indent=2)); return 1
    if hold:
        print(json.dumps({"status":"HOLD","reject_all":sorted(hold)},indent=2)); return 2
    lock={"schema_version":"room917.critical_sfx_human_lock/2.0",
          "status":"HUMAN_BLIND_ACCEPTED_PENDING_IDENTITY_BINDING_GATE",
          "selections":selections,
          "hard_law":"THIS_LOCK_SELECTS_BYTES; IT DOES_NOT AUTHORIZE RELEASE WITHOUT IDENTITY_BINDING_GATE_PASS"}
    Path(a.out).write_text(json.dumps(lock,indent=2)+"\n")
    print(json.dumps({"status":"PASS","lock":a.out,"selection_count":len(selections)},indent=2))
    return 0
if __name__=="__main__": raise SystemExit(main())
