#!/usr/bin/env python3
"""IVDIVO self-improvement value/pruning guard.

Consumes measured telemetry; does not create telemetry and never promotes a mechanism
to CURRENT authority. It returns a review disposition only.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

def evaluate(payload: dict) -> dict:
    required=["candidate_id","telemetry"]
    if any(k not in payload for k in required) or not isinstance(payload.get("telemetry"),dict):
        return {"status":"FAIL_CLOSED","disposition":"STOP","reasons":["MISSING_REQUIRED_INPUT"]}
    t=payload["telemetry"]
    measurement_state=str(t.get("measurement_state", "UNMEASURED")).upper()
    def num(k):
        v=t.get(k,0)
        return float(v) if isinstance(v,(int,float)) and not isinstance(v,bool) else 0.0

    tp=num("true_positive_findings")
    fp=num("false_positive_findings")
    accepted=num("accepted_repairs")
    avoided=num("avoided_rework_cycles")
    saved=num("measured_minutes_saved")
    overhead=num("measured_overhead_minutes")
    artifacts=num("new_artifacts")
    prompts=num("new_prompts")
    pilots=num("real_project_pilots")
    human=num("independent_human_evidence_count")
    regressions=num("regressions_introduced")
    blocked=num("unsafe_or_unauthorized_actions_blocked")

    alerts=tp+fp
    precision=(tp/alerts) if alerts else None
    benefit = accepted*2.0 + avoided*1.5 + saved/30.0 + pilots*2.0 + blocked*1.0
    cost = overhead/30.0 + artifacts*0.15 + prompts*0.05 + fp*0.75 + regressions*3.0
    net=benefit-cost

    reasons=[]
    if regressions>0:
        disposition="REVISE_OR_ROLLBACK"
        reasons.append("REGRESSION_INTRODUCED")
    elif pilots < 1:
        disposition="HOLD_FOR_REAL_PILOT"
        reasons.append("NO_REAL_PROJECT_PILOT")
    elif measurement_state != "COMPLETE":
        disposition="HOLD_FOR_MEASUREMENT"
        reasons.append("VALUE_TELEMETRY_NOT_COMPLETE")
    elif alerts >= 4 and precision is not None and precision < 0.5:
        disposition="PRUNE_OR_REVISE"
        reasons.append("LOW_PRECISION")
    elif net < 0:
        disposition="PRUNE_OR_REVISE"
        reasons.append("NEGATIVE_MEASURED_NET_VALUE")
    elif pilots >= 2 and human >= 1 and net > 0:
        disposition="PROMOTION_REVIEW_ELIGIBLE"
        reasons.append("REAL_MULTI_PROJECT_AND_HUMAN_EVIDENCE")
    else:
        disposition="KEEP_CANDIDATE"
        reasons.append("POSITIVE_BUT_INCOMPLETE_EVIDENCE")
    return {
        "status":"PASS",
        "candidate_id":payload["candidate_id"],
        "disposition":disposition,
        "metrics":{
            "precision":precision,
            "benefit_points":round(benefit,3),
            "cost_points":round(cost,3),
            "net_points":round(net,3),
            "real_project_pilots":pilots,
            "independent_human_evidence_count":human,
            "measurement_state":measurement_state,
        },
        "reasons":reasons,
        "authority_boundary":"REVIEW_DISPOSITION_ONLY; NEVER_AUTO_PROMOTE_OR_REWRITE_CANON",
    }

def main():
    p=argparse.ArgumentParser(); p.add_argument("input",type=Path); a=p.parse_args()
    try: payload=json.loads(a.input.read_text(encoding="utf-8"))
    except Exception as exc:
        print(json.dumps({"status":"FAIL_CLOSED","disposition":"STOP","reasons":[f"INPUT_ERROR:{exc}"]})); return 2
    out=evaluate(payload); print(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True))
    return 0 if out["status"]=="PASS" else 1
if __name__=="__main__": raise SystemExit(main())
