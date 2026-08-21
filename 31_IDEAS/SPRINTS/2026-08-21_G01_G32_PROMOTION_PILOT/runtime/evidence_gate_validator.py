#!/usr/bin/env python3
import json, sys

ALLOWED={"SOURCE_INTEGRITY","FULL_READ","SYNTHESIS","MACHINE_TEST","MODEL_REVIEW","HUMAN_SIGNAL","LIVE_PROVIDER","DRY_RUN","PERSISTED_READBACK","MARKET_BEHAVIOR","FOUNDER_DECISION"}
PROHIBITED={
    ("MACHINE_TEST","LITERARY_QUALITY"),
    ("MODEL_REVIEW","HUMAN_SIGNAL"),
    ("DRY_RUN","LIVE_PROVIDER"),
    ("PERSISTED_READBACK","FOUNDER_DECISION"),
    ("SOURCE_INTEGRITY","FULL_READ"),
}

def check(record):
    ec=record.get("evidence_class")
    claim=record.get("claim_class")
    errors=[]
    if ec not in ALLOWED:
        errors.append("UNKNOWN_EVIDENCE_CLASS")
    for k in ("evidence_source","verification_method","cannot_prove"):
        if not record.get(k):
            errors.append("MISSING_"+k.upper())
    if (ec,claim) in PROHIBITED:
        errors.append("EVIDENCE_COLLAPSE")
    if claim=="FOUNDER_LOCK" and ec!="FOUNDER_DECISION":
        errors.append("FOUNDER_LOCK_REQUIRES_FOUNDER_DECISION")
    if claim=="HUMAN_SIGNAL" and ec!="HUMAN_SIGNAL":
        errors.append("HUMAN_SIGNAL_REQUIRES_HUMAN_SIGNAL")
    if claim=="LIVE_RENDER" and ec!="LIVE_PROVIDER":
        errors.append("LIVE_RENDER_REQUIRES_LIVE_PROVIDER")
    return errors

if __name__=="__main__":
    fixtures=json.load(open(sys.argv[1],encoding="utf-8"))
    failed=0
    for f in fixtures:
        got=check(f)
        expected=f.get("expected_fail",False)
        ok=(bool(got)==expected)
        print(f["id"],"PASS" if ok else "FAIL",got)
        failed += int(not ok)
    raise SystemExit(1 if failed else 0)
