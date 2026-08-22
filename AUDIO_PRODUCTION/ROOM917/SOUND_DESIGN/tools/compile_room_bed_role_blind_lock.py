#!/usr/bin/env python3
import argparse,csv,json
from pathlib import Path

EXPECTED={"GREYHAVEN_LOBBY","SWITCHBOARD_ALCOVE"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mapping",required=True)
    ap.add_argument("--results",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    mapping=json.loads(Path(a.mapping).read_text())
    truth={x["blind_label"]:x for x in mapping}
    with open(a.results,newline="",encoding="utf-8-sig") as f:
        rows=list(csv.DictReader(f))
    errors=[]; hold=[]; seen=set(); accepted=[]
    for r in rows:
        lab=r["blind_label"].strip().upper()
        if not lab: continue
        seen.add(lab)
        role=r["assigned_role_LOBBY_or_ALCOVE"].strip().upper()
        norm_role={"LOBBY":"GREYHAVEN_LOBBY","ALCOVE":"SWITCHBOARD_ALCOVE",
                   "GREYHAVEN_LOBBY":"GREYHAVEN_LOBBY","SWITCHBOARD_ALCOVE":"SWITCHBOARD_ALCOVE"}.get(role)
        if lab not in truth:
            errors.append(f"UNKNOWN_LABEL:{lab}"); continue
        if not norm_role:
            errors.append(f"BAD_ROLE:{lab}:{role or 'EMPTY'}"); continue
        if norm_role!=truth[lab]["role"]:
            hold.append(f"ROLE_MISIDENTIFIED:{lab}:{norm_role}")
        for field in ["room_distinct","loop_seam_clean","false_clue_free","mono_ok","phone_ok"]:
            value=r[field].strip().upper()
            if value not in {"PASS","YES","TRUE","1"}:
                hold.append(f"{field.upper()}_NOT_PASS:{lab}:{value or 'EMPTY'}")
        accepted.append({"blind_label":lab,"assigned_role":norm_role,
                         "candidate_id":truth[lab]["candidate_id"],"sha256":truth[lab]["sha256"]})
    if set(truth)-seen:
        errors.append("MISSING_BLIND_LABELS:"+",".join(sorted(set(truth)-seen)))
    if errors:
        print(json.dumps({"status":"FAIL","errors":errors},indent=2)); return 1
    if hold:
        print(json.dumps({"status":"HOLD","reasons":hold},indent=2)); return 2
    lock={"schema_version":"room917.room_bed_human_lock/3.0",
          "status":"HUMAN_ROLE_BLIND_PASS_PENDING_IDENTITY_GATE",
          "selections":accepted,
          "hard_law":"ROLE_BLIND_PASS_SELECTS_ACCEPTED_BYTES_BUT_DOES_NOT_AUTHORIZE_D003_PATCH_UNTIL_IDENTITY_GATE_AND_EXACT_INTERVAL_OR_MASTER_RECOVERY_PASS"}
    Path(a.out).write_text(json.dumps(lock,indent=2)+"\n")
    print(json.dumps({"status":"PASS","lock":a.out},indent=2)); return 0

if __name__=="__main__": raise SystemExit(main())
