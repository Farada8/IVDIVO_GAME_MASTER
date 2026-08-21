"""Bounded Cycle8 writing-production canary model.
Research/pilot only. It does not decide story canon or replace current runtime authority.
"""

STORY_FIELDS = [
    "hero","want","why_now","opposition","wrong_strategy",
    "price","midpoint","climax_choice","resolution","series_hook_status"
]

def approval_event_gate(required, observed):
    if observed is None:
        return "APPROVAL_EVENT_MISSING"
    if observed.get("type") != required.get("type") or observed.get("target") != required.get("target"):
        return "APPROVAL_EVENT_MISSING"
    if not observed.get("authority_source"):
        return "APPROVAL_EVENT_MISSING"
    return "PASS"

def story_core_gate(state):
    missing=[f for f in STORY_FIELDS if state.get(f) in (None,"","UNKNOWN")]
    return {"status":"STORY_CORE_READY" if not missing else "PROSE_NO_GO","missing":missing}

def evidence_class_gate(required, observed):
    return "SUPPORTED" if required == observed else "EVIDENCE_CLASS_MISMATCH"

def metric_gate(value, measured, source_ref=None):
    if not measured:
        return "UNKNOWN_NULL" if value is None else "FAIL_FALSE_ZERO"
    if source_ref is None:
        return "FAIL_NO_SOURCE"
    return "MEASURED_ZERO" if value == 0 else "MEASURED_VALUE"

def hook_gate(main_conflict_closed, hook_present, hook_reopens_conflict=False):
    if hook_present and (not main_conflict_closed or hook_reopens_conflict):
        return "HOOK_QUARANTINED"
    return "CLOSED_THEN_HOOK" if hook_present else ("CLOSED_NO_HOOK" if main_conflict_closed else "OPEN_STORY")

def jurisdiction_gate(knowledge_scope, jurisdiction_scope, requested_action, authority_evidence=False):
    command_actions={"COMMAND","POLICE","JUDICIAL","ADMIN"}
    if requested_action in command_actions and not authority_evidence:
        return "OVERREACH"
    if knowledge_scope and jurisdiction_scope in (None,"","NONE") and requested_action == "ADVICE":
        return "ADVISORY_ONLY"
    if authority_evidence:
        return "AUTHORIZED"
    if requested_action == "ADVICE":
        return "AUTHORIZED_ADVICE"
    return "UNRESOLVED"
