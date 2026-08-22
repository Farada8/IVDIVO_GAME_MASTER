from __future__ import annotations
from typing import Iterable

VALID_STATES = {"KEEP","MERGE","HOLD","PRUNE","PROMOTION_REVIEW","READY_FOR_PILOT"}

def decision_yield(decision: str|None, uncertainty: str|None, test: str|None, production_return: str|None):
    missing=[k for k,v in {"decision":decision,"uncertainty":uncertainty,"test":test,"production_return":production_return}.items() if not v]
    return {"status":"HOLD_MISSING_DECISION_YIELD_FIELDS","missing":missing} if missing else {"status":"PASS_BOUNDED_META_ACTION"}

def existing_mechanism_gate(proposed: str, existing: Iterable[str]):
    norm=lambda x:" ".join(x.lower().replace("_"," ").split())
    p=norm(proposed)
    for x in existing:
        if p==norm(x): return "MERGE_WITH_EXISTING"
    return "ALLOW_BOUNDED_CANDIDATE"

def reservation_view(committed_ids, reserved_ids, proposed_id):
    committed=set(committed_ids); reserved=set(reserved_ids)
    if proposed_id in committed or proposed_id in reserved:
        return {"status":"HOLD_ID_COLLISION","collision":proposed_id}
    return {"status":"AVAILABLE_ONLY_IF_RESERVATION_VIEW_COMPLETE","candidate":proposed_id}

def merge_time_collision(committed_ids,reserved_ids,candidate_id):
    return candidate_id not in set(committed_ids)|set(reserved_ids)

def independent_families(records):
    return len({(r.get("project"),r.get("root_evidence_family"),r.get("mechanism_identity")) for r in records})

def replication_diversity(records, required_projects=2):
    projects={r.get("project") for r in records if r.get("outcome")=="PASS" and r.get("healthy_control") is True}
    return {"status":"PASS_DIVERSE_REPLICATION","projects":sorted(projects)} if len(projects)>=required_projects else {"status":"HOLD_REPLICATION_DIVERSITY","projects":sorted(projects)}

def promotion_tribunal(bundle):
    required=["application_target","rollback","readback","regression","source_provenance","evidence_boundary"]
    missing=[x for x in required if not bundle.get(x)]
    if missing: return {"status":"HOLD_INCOMPLETE_PROMOTION_BUNDLE","missing":missing}
    if bundle.get("external_gate_required") and not bundle.get("external_gate_satisfied"):
        return {"status":"HOLD_EXTERNAL_EVIDENCE"}
    if bundle.get("independent_projects",0)<bundle.get("required_independent_projects",1):
        return {"status":"HOLD_REPLICATION_DIVERSITY"}
    return {"status":"PROMOTION_REVIEW_NOT_AUTO_PROMOTION"}

def false_positive_control(candidate_hits_healthy: bool):
    return "FAIL_FALSE_POSITIVE" if candidate_hits_healthy else "PASS_FALSE_POSITIVE_CONTROL"

def candidate_utility(decision_delta: bool, duplicate: bool, trigger_live: bool, overhead: float|None=None, avoided_rework: float|None=None):
    if duplicate: return "MERGE"
    if not trigger_live: return "PRUNE_OR_HOLD_EXPIRED"
    if not decision_delta: return "PRUNE_LOW_INFORMATION"
    if overhead is not None and avoided_rework is not None and overhead>avoided_rework: return "PRUNE_OVERHEAD_DOMINATES"
    return "KEEP_BOUNDED"

def production_return(meta_authorized: bool, production_target: str|None):
    if not meta_authorized: return "RETURN_TO_PRODUCTION"
    if not production_target: return "HOLD_NO_RETURN_TARGET"
    return "META_BOUNDED_THEN_RETURN"

def rollback_witness(before_hash, after_hash, rollback_hash):
    return bool(before_hash and after_hash and rollback_hash and rollback_hash==before_hash and after_hash!=before_hash)

def private_raw_policy(classification):
    return "DRIVE_ONLY_POINTER_IN_GITHUB" if classification in {"PRIVATE","UNPUBLISHED","USER_UPLOAD_PRIVATE_REFERENCE"} else "PUBLICATION_POLICY_REVIEW"

def evidence_gap_vector(known, unknown, external_required):
    return {"known":sorted(set(known)),"unknown":sorted(set(unknown)),"external_required":sorted(set(external_required))}

def evidence_family_counter(records):
    return len({r["root"] for r in records})

def meta_overhead_ratio(meta_minutes, avoided_rework_minutes):
    if meta_minutes is None or avoided_rework_minutes is None: return None
    if avoided_rework_minutes==0: return float("inf") if meta_minutes>0 else 0.0
    return meta_minutes/avoided_rework_minutes
