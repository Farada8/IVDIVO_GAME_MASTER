#!/usr/bin/env python3
import json, sys
from pathlib import Path

REQUIRED=["candidate_id","decision","authority_preserved","causal_model","uncertainty","experiment","fitness","rollback"]

def validate(d):
    errors=[]
    for k in REQUIRED:
        if k not in d: errors.append(f"MISSING:{k}")
    if not d.get("decision") or not d["decision"].get("can_change"): errors.append("NO_DECISION_RELEVANCE")
    if d.get("authority_preserved") is not True: errors.append("AUTHORITY_NOT_PRESERVED")
    cm=d.get("causal_model",{})
    if not cm.get("intended_effect"): errors.append("NO_INTENDED_EFFECT")
    if not cm.get("guardrail_effects"): errors.append("NO_GUARDRAILS")
    if "delays" not in cm: errors.append("NO_DELAY_REVIEW")
    if "compensating_responses" not in cm: errors.append("NO_POLICY_RESISTANCE_REVIEW")
    if not d.get("uncertainty",{}).get("unknowns"): errors.append("NO_EXPLICIT_UNCERTAINTY")
    e=d.get("experiment",{})
    if not e.get("bounded_scope"): errors.append("NO_BOUNDED_CANARY")
    if not e.get("reversible"): errors.append("NOT_REVERSIBLE_OR_NOT_DECLARED")
    f=d.get("fitness",{})
    if not f.get("primary"): errors.append("NO_PRIMARY_FITNESS")
    if not f.get("guardrails"): errors.append("NO_FITNESS_GUARDRAILS")
    r=d.get("rollback",{})
    if not r.get("trigger") or not r.get("target"): errors.append("NO_ROLLBACK_PLAN")
    return {"artifact":"IVDIVO_SELF_IMPROVEMENT_V3_CANDIDATE_GATE_RESULT_v0_1","candidate_id":d.get("candidate_id"),"verdict":"CANDIDATE_READY" if not errors else "FAIL_CLOSED","errors":errors,"authority_effect":"NONE_CANDIDATE_ONLY"}

if __name__=="__main__":
    src=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    Path(sys.argv[2]).write_text(json.dumps(validate(src),indent=2),encoding="utf-8")
