"""Cycle32C bounded self-improvement convergence utilities.
Engineering behavior only; no human/provider/market/literary proof is inferred.
"""
SUCCESS_NO_CHANGE={"REUSE_CURRENT","NO_OP","PROTECT_NO_CHANGE","HOLD_REAL_EVIDENCE"}
EXTERNAL={"HUMAN","PROVIDER","MARKET","LEGAL","LITERARY"}

def authority_snapshot(current_surfaces):
    return {k:v for k,v in sorted((current_surfaces or {}).items()) if v is not None}

def embedded_slice_freshness(embedded, controlling, historical=False):
    if historical:return "HISTORICAL_EXEMPT"
    if embedded is None or controlling is None:return "UNKNOWN"
    return "CURRENT_MATCH" if embedded==controlling else "STALE_EMBEDDED_SLICE"

def empty_scaffold_guard(children_count, substantive_count=0):
    return "NOT_PROGRESS_EMPTY_SCAFFOLD" if children_count==0 or substantive_count==0 else "SUBSTANTIVE"

def file_library_transfer(can_transfer_bytes):
    return "PHYSICAL_TRANSFER_ALLOWED" if can_transfer_bytes else "FILE_LIBRARY_REFERENCE_ONLY"

def parallel_dedupe(same_semantics, stronger_current=False, unique_delta=False):
    if same_semantics and stronger_current:return "REUSE_STRONGER_CURRENT"
    if unique_delta:return "SALVAGE_UNIQUE_DELTA"
    return "KEEP_SEPARATE" if not same_semantics else "MERGE_REVIEW"

def v3_promotion_guard(v2_verified, independent_evidence, application_readback):
    return "PROMOTION_ELIGIBLE_REVIEW" if v2_verified and independent_evidence and application_readback else "KEEP_V2_CURRENT_V3_CANDIDATE"

def candidate_id_reservation(fresh_registry, open_reservations, requested):
    if requested in set(fresh_registry or ())|set(open_reservations or ()):return "COLLISION"
    return "RESERVABLE_AFTER_FRESH_READ"

def stale_pointer_repair(pointer_state, controlling_state):
    return "NO_OP" if pointer_state==controlling_state else "TARGETED_POINTER_REPAIR"

def effect_entry(before, after, evidence_class, counterfactual=None):
    return {"decision_before":before,"decision_after":after,"changed":None if before is None or after is None else before!=after,"evidence_class":evidence_class,"counterfactual":counterfactual}

def noop_success(disposition): return disposition in SUCCESS_NO_CHANGE

def meta_starvation(founder_switched=False,p0_blocker=False,direct_prerequisite=False):
    return "META_AUTHORIZED" if any([founder_switched,p0_blocker,direct_prerequisite]) else "RETURN_TO_PRODUCTION"

def production_effect_trace(decision_delta, external_claim=False):
    if external_claim:return "HOLD_EXTERNAL_EVIDENCE"
    return "EFFECT_OBSERVED" if decision_delta else "NO_DECISION_EFFECT"

def cross_store_plan(github_write, drive_write):
    return {"github":bool(github_write),"drive":bool(drive_write),"completion_requires_readback":True}

def stale_branch_salvage(is_stale, unique_delta):
    if not is_stale:return "USE_BRANCH_IF_CI_GREEN"
    return "REBASE_SALVAGE_UNIQUE" if unique_delta else "PROVENANCE_ONLY"

def branch_freshness(ahead,behind):
    if behind and ahead:return "DIVERGED"
    if behind:return "BEHIND"
    if ahead:return "AHEAD"
    return "CLEAN"

def transaction_bundle(github_ok,drive_ok,github_readback=False,drive_readback=False):
    if github_ok and drive_ok and github_readback and drive_readback:return "CLOSED"
    if github_ok or drive_ok:return "PARTIAL_RECOVERY_REQUIRED"
    return "PLANNED_OR_FAILED"

def partial_recovery(successful_actions, intended_actions):
    return sorted(set(intended_actions)-set(successful_actions))

def evidence_firewall(source_class,target_class):
    if source_class==target_class:return "SAME_CLASS"
    if target_class in EXTERNAL and source_class not in EXTERNAL:return "BLOCK_SUBSTITUTION"
    return "REVIEW"

def external_evidence(observed): return "OBSERVED" if observed else "HOLD_REAL_EVIDENCE"

def experiment_budget(expected_information_gain,cost,reversible=True):
    if expected_information_gain is None or cost is None:return "HOLD_UNKNOWN"
    if not reversible and cost>0:return "ESCALATE_IRREVERSIBLE"
    return "ADMISSIBLE" if expected_information_gain>0 else "NO_OP"

def double_loop(recurrence,model_contradiction=False,guardrail_failure=False):
    return "DOUBLE_LOOP_REVIEW" if recurrence>=2 or model_contradiction or guardrail_failure else "LOCAL_LOOP"

def slo_error_budget(integrity_failures,budget):
    return "STOP_FEATURE_ACCUMULATION" if integrity_failures>=budget else "WITHIN_BUDGET"

def deprecation(duplicate=False,dead=False,audit_required=True):
    if duplicate or dead:return "ARCHIVE_PRESERVE_PROVENANCE" if audit_required else "DELETE_ALLOWED"
    return "KEEP"

def backlog_governor(items):
    ready=[x for x in items if x.get('ready')]
    if not ready:return None
    return max(ready,key=lambda x:(x.get('information_gain',0),-x.get('cost',0)))

def decision_latency(start,end):
    if start is None or end is None:return None
    return end-start

def operator_burden(minutes=None,actions=None,rework=None):
    if minutes is None:return {"minutes":None,"status":"HOLD_NO_HUMAN_MEASUREMENT"}
    return {"minutes":minutes,"actions":actions,"rework":rework,"status":"OBSERVED"}

def causal_attribution(baseline,treatment,confounders_bounded):
    if baseline is None or treatment is None or not confounders_bounded:return "HOLD_ATTRIBUTION"
    return "NARROW_ATTRIBUTION_SUPPORTED" if baseline!=treatment else "NO_EFFECT"

def transfer_replication(project_results,same_contract):
    if not same_contract:return "NOT_REPLICATION_CONTRACT_DRIFT"
    return "REPLICATED" if len(project_results)>=2 and all(project_results) else "INSUFFICIENT_REPLICATION"

def false_positive_guard(flagged,healthy_control_changed):
    if flagged and not healthy_control_changed:return "FALSE_POSITIVE"
    return "CONTROL_OK"

def promotion_packet(evidence_pass,approved=False,applied=False,readback=False):
    if not evidence_pass:return "DEVELOPMENT"
    if not approved:return "READY_FOR_APPROVAL"
    if not applied:return "APPROVED_NOT_APPLIED"
    return "VERIFIED_CURRENT" if readback else "APPLIED_AWAITING_READBACK"

def self_application(authority_checked,canary,regression,readback,rollback):
    return "PASS" if all([authority_checked,canary,regression,readback,rollback]) else "HOLD"

def next_cycle_router(real_external_gate_available,engineering_blocker=False):
    if real_external_gate_available:return "ROUTE_REAL_EVIDENCE"
    if engineering_blocker:return "ROUTE_ENGINEERING_BLOCKER"
    return "ROUTE_HIGHEST_VOI_PRODUCTION"
