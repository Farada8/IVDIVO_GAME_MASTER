from __future__ import annotations
REQUIRED=("generated_minutes","accepted_minutes","provider_spend","human_minutes","human_hourly_cost")
def compute(row:dict)->dict:
    missing=[k for k in REQUIRED if row.get(k) is None]
    if missing:return {"status":"HOLD_MISSING_EVIDENCE","missing":missing,"cost_per_accepted_minute":None}
    if row["accepted_minutes"]<=0:return {"status":"HOLD_NO_ACCEPTED_MINUTES","cost_per_accepted_minute":None}
    manual=row["human_minutes"]/60*row["human_hourly_cost"];total=row["provider_spend"]+manual
    return {"status":"PASS_EVIDENCE_COMPLETE","total_cost":round(total,4),"cost_per_accepted_minute":round(total/row["accepted_minutes"],4),"acceptance_yield":round(row["accepted_minutes"]/row["generated_minutes"],4) if row["generated_minutes"] else None}
def reject_estimate_as_actual(row:dict)->dict:
    if row.get("provider_spend_source") in {"ESTIMATE","PREDICTED","UNKNOWN"} or row.get("human_minutes_source") in {"ESTIMATE","PREDICTED","UNKNOWN"}:return {"decision":"REJECT_ACTUAL_CLAIM"}
    return {"decision":"ALLOW_IF_COMPLETE"}
