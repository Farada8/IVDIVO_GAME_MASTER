def cluain_gate(records):
    required=("context","timeframe","overall_budget","photo_refs","applicant_role","delivery_context")
    rows=[]
    for rec in records:
        missing=[k for k in required if rec.get(k) in (None,"","UNKNOWN",False) or rec.get(k)==[]]
        rows.append({"title":rec.get("title"),"ready":not missing,"missing":missing})
    ready=sum(1 for r in rows if r["ready"])
    return {"status":"PASS_THREE_PROJECT_EVIDENCE" if ready>=3 else "HOLD_THREE_PROJECT_RECORDS","ready":ready,"required":3,"rows":rows}

def inis_gate(images, cv_ready, concept, technical, maintenance_green, budget):
    blockers=[]
    if images<=0: blockers.append("PREVIOUS_WORK_IMAGES")
    if images>10: blockers.append("IMAGE_LIMIT")
    if not cv_ready: blockers.append("CV")
    if not concept: blockers.append("CONCEPT")
    if not technical: blockers.append("TECHNICAL")
    if not maintenance_green: blockers.append("MAINTENANCE_GREEN")
    if not budget: blockers.append("BUDGET")
    return {"status":"READY_FOR_FINAL_RED_TEAM" if not blockers else "HOLD_APPLICATION_PACKAGE","blockers":blockers,"past_project_budget_required_for_previous_images":False}

def route(cluain, inis):
    if cluain["status"].startswith("HOLD") and inis["status"].startswith("HOLD"):
        return "INIS_EVIDENCE_BURDEN_LOWER" if cluain.get("ready",0)<3 else "DEPENDENCY_REVIEW"
    return "FINAL_RED_TEAM_ROUTE"
