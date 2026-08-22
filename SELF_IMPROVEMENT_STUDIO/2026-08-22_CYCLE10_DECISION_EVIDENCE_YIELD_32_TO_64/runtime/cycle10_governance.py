from __future__ import annotations
from typing import Iterable
import hashlib

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

def meta_wip_limiter(primary_meta:int, pilots:int, founder_switched:bool=False, prerequisite:bool=False, production_blocked:bool=False):
    """Bound meta/self-improvement WIP so production is not displaced by unlimited meta-work."""
    allowed = founder_switched or prerequisite or production_blocked
    if primary_meta <= 1 and pilots <= 2:
        return {"status":"PASS_WIP_BOUNDED","exception_used":False}
    if allowed:
        reason = "FOUNDER_SWITCH" if founder_switched else "PREREQUISITE" if prerequisite else "PRODUCTION_BLOCKED"
        return {"status":"PASS_WIP_EXCEPTION","exception_used":True,"reason":reason}
    return {"status":"STOP_WIP_LIMIT","exception_used":False}

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

# Unique mechanisms salvaged from Cycle32D executable candidate after semantic dedupe.
# These extend Cycle10; they do not create another engine or authority layer.
def prompt_functional_fingerprint(card):
    fields=("consumer","evidence_class","gate","action_semantics","state_mutation")
    normalized=[str(card.get(k,"")).strip().lower() for k in fields]
    return hashlib.sha256("|".join(normalized).encode("utf-8")).hexdigest()[:20]

def dedupe_prompt_bank(cards):
    seen={}; duplicates=[]
    for card in cards:
        fp=prompt_functional_fingerprint(card)
        if fp in seen:
            duplicates.append((seen[fp],card.get("id")))
        else:
            seen[fp]=card.get("id")
    return {"status":"PASS_UNIQUE" if not duplicates else "MERGE_FUNCTIONAL_DUPLICATES","unique":len(seen),"total":len(cards),"duplicates":duplicates}

def ordinal_voi_route(tests):
    eligible=[t for t in tests if t.get("decision_consumer")]
    if not eligible:
        return {"status":"HOLD_NO_DECISION_CONSUMER","selected":None}
    def key(t):
        return (int(t.get("decision_flip",0))+int(t.get("evidence_independence",0)), -int(t.get("burden",3)), -int(t.get("risk",3)))
    selected=max(eligible,key=key)
    return {"status":"SELECT_SMALLEST_HIGH_INFORMATION_TEST","selected":selected.get("id"),"basis":"ordinal decision-change/evidence-independence before burden/risk"}

def cost_of_delay_band(consequence):
    c=(consequence or "").lower()
    if any(x in c for x in ("data loss","authority corruption","irreversible","payment replay","safety")):
        return "HIGH"
    if any(x in c for x in ("blocks production","deadline","stale merge","rework")):
        return "MEDIUM"
    return "LOW"

def selective_rollback_plan(changed, dependency_graph, locked=None):
    locked=set(locked or ()); affected=[]; stack=list(dependency_graph.get(changed,())); seen=set()
    while stack:
        node=stack.pop()
        if node in seen or node in locked:
            continue
        seen.add(node); affected.append(node); stack.extend(dependency_graph.get(node,()))
    return {"status":"PASS_SELECTIVE_REVALIDATION","changed":changed,"revalidate":affected,"locked_preserved":sorted(locked)}

def validate_asset_registry(items):
    bad=[]
    for item in items:
        sha=item.get("sha256","")
        if not item.get("filename") or len(sha)!=64 or any(ch not in "0123456789abcdef" for ch in sha.lower()) or item.get("size_bytes",0)<0 or not item.get("role"):
            bad.append(item.get("filename"))
    return {"status":"PASS" if not bad else "FAIL_ASSET_REGISTRY","count":len(items),"bad":bad}
