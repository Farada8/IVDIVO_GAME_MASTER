#!/usr/bin/env python3
"""IVDIVO routing write-through consistency checker.

Advisory only. It validates propagation of terminal routing events across persisted
routing layers. It never creates Founder locks and never rewrites story text.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

EVENT_RULES = {
    "FOUNDER_LOCK": {
        "expected_status":"FOUNDER_LOCKED",
        "required_roles":{"PROJECT_STATE","PORTFOLIO_ROUTER","WORKSTATE"},
    },
    "FINAL_STORY_GATE_PASS": {
        "expected_status":"FINAL_STORY_GATE_PASS",
        "required_roles":{"PROJECT_STATE","PORTFOLIO_ROUTER"},
    },
    "EXTERNAL_PROVIDER_REQUIRED": {
        "expected_status":"EXTERNAL_PROVIDER_REQUIRED",
        "required_roles":{"PROJECT_STATE"},
    },
    "HUMAN_EVIDENCE_REQUIRED": {
        "expected_status":"HUMAN_EVIDENCE_REQUIRED",
        "required_roles":{"PROJECT_STATE"},
    },
}

def check(payload: dict) -> dict:
    event=payload.get("event")
    if event not in EVENT_RULES:
        return {"status":"FAIL_CLOSED","issues":["UNKNOWN_EVENT"],"repairs":[]}
    project_id=str(payload.get("project_id",""))
    event_artifact_id=payload.get("event_artifact_id")
    if not project_id or not event_artifact_id:
        return {"status":"FAIL_CLOSED","issues":["PROJECT_OR_EVENT_ARTIFACT_MISSING"],"repairs":[]}
    layers=payload.get("layers")
    if not isinstance(layers,list):
        return {"status":"FAIL_CLOSED","issues":["LAYERS_INVALID"],"repairs":[]}
    issues=[]; repairs=[]; by_role={}
    for layer in layers:
        role=layer.get("role")
        if role:
            by_role.setdefault(role,[]).append(layer)
    rule=EVENT_RULES[event]
    for role in sorted(rule["required_roles"]):
        if role not in by_role:
            issues.append(f"REQUIRED_LAYER_MISSING:{role}")
            repairs.append({"role":role,"action":"CREATE_OR_UPDATE_ROUTING_MIRROR_ONLY"})
    for role, records in by_role.items():
        if len(records)>1:
            issues.append(f"DUPLICATE_LAYER_ROLE:{role}")
    for role, records in by_role.items():
        for r in records:
            observed=r.get("observed_status")
            if role in rule["required_roles"] and observed != rule["expected_status"]:
                issues.append(f"STATUS_STALE:{role}:{observed}")
                repairs.append({"role":role,"action":"PATCH_ROUTING_ONLY","expected_status":rule["expected_status"]})
            bound=r.get("event_artifact_id")
            if role in rule["required_roles"] and bound != event_artifact_id:
                issues.append(f"EVENT_PROVENANCE_MISMATCH:{role}")
                repairs.append({"role":role,"action":"BIND_EVENT_ARTIFACT","event_artifact_id":event_artifact_id})
            if r.get("track_event"):
                normalized=r.get("normalized_event")
                if normalized != event:
                    issues.append(f"EVENT_STATE_STALE:{role}:{normalized}")
                    repairs.append({"role":role,"action":"PATCH_ROUTING_ONLY","expected_event":event})
            if r.get("story_text_mutation_requested"):
                issues.append(f"ILLEGAL_STORY_MUTATION_REQUEST:{role}")
    # A terminal Founder lock must not route to more story prose.
    if event=="FOUNDER_LOCK":
        for role, records in by_role.items():
            for r in records:
                nxt=str(r.get("next_action",""))
                if any(tok in nxt for tok in ("DRAFT_NEXT_EPISODE","GENERATE_E25","CONTINUE_STORY_PROSE")):
                    issues.append(f"LOCKED_PROJECT_PROSE_ROUTE:{role}")
                    repairs.append({"role":role,"action":"ROUTE_DOWNSTREAM_OR_NEXT_PROJECT_NOT_PROSE"})
    if any(i.startswith("ILLEGAL_STORY_MUTATION") or i.startswith("LOCKED_PROJECT_PROSE_ROUTE") for i in issues):
        status="FAIL"
    elif issues:
        status="ISSUES_FOUND"
    else:
        status="PASS"
    return {"status":status,"project_id":project_id,"event":event,"issues":issues,"repairs":repairs,
            "law":"ROUTING_REPAIR_ONLY; NEVER_INFER_OR_CREATE_FOUNDER_AUTHORITY"}

def main():
    p=argparse.ArgumentParser(); p.add_argument("input",type=Path); a=p.parse_args()
    try: payload=json.loads(a.input.read_text(encoding="utf-8"))
    except Exception as exc:
        print(json.dumps({"status":"FAIL_CLOSED","issues":[f"INPUT_ERROR:{exc}"]})); return 2
    out=check(payload); print(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True))
    return 0 if out["status"] in {"PASS","ISSUES_FOUND"} else 1
if __name__=="__main__": raise SystemExit(main())
