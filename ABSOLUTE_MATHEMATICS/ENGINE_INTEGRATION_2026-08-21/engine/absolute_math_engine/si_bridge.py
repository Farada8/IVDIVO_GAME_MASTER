from __future__ import annotations

REQUIRED_SI_KEYS={"normalized_state","dag","task_ir","decision","telemetry_event"}

def validate_si0012_plan(plan):
    missing=REQUIRED_SI_KEYS-set(plan)
    if missing:
        return {"ok":False,"reason":"SI_PLAN_MISSING_KEYS","missing":sorted(missing)}
    if plan["decision"].get("decision")=="STOP":
        return {"ok":False,"reason":plan["decision"].get("reason","SI_STOP")}
    return {"ok":True,"reason":"SI_PLAN_ACCEPTED"}

def compile_math_feedback(plan,research_result):
    check=validate_si0012_plan(plan)
    return {"bridge_version":"1.0","si_check":check,
            "project_id":plan.get("normalized_state",{}).get("project_id"),
            "authority_ref":plan.get("normalized_state",{}).get("authority_source",{}).get("locator"),
            "math_result":research_result,"allowed_mutation":"CANDIDATE_ARTIFACT_ONLY",
            "requires_external_promotion":True}
