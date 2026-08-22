from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set

EXTERNAL_PLANES = {"HUMAN", "MARKET", "PROVIDER", "LEGAL", "LITERARY", "SCIENTIFIC_EXTERNAL"}
CURRENT_AUTHORITY = "V2_VERIFIED_CURRENT"

@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    root_family: str
    plane: str
    outcome: str
    independent: bool = True
    source: str = ""

@dataclass
class Candidate:
    candidate_id: str
    title: str
    target_scope: str
    required_planes: List[str] = field(default_factory=list)
    rollback_defined: bool = False
    protected_authorities: List[str] = field(default_factory=list)
    application_targets: List[str] = field(default_factory=list)
    evidence: List[Evidence] = field(default_factory=list)

def collapse_evidence_families(evidence: List[Evidence]) -> Dict[str, Evidence]:
    out = {}
    for e in evidence:
        if e.root_family not in out:
            out[e.root_family] = e
    return out

def independent_family_count(evidence: List[Evidence]) -> int:
    return len({e.root_family for e in evidence if e.independent})

def model_vote_count_as_evidence(model_reports: List[Evidence]) -> int:
    return independent_family_count(model_reports)

def typed_approval_gate(required: str, observed: Optional[str]) -> str:
    if observed is None:
        return "APPROVAL_EVENT_MISSING"
    if required != observed:
        return "WRONG_APPROVAL_EVENT_TYPE"
    return "PASS"

def project_slice_gate(slice_version: Optional[str], controlling_version: Optional[str], historical=False) -> str:
    if historical:
        return "EXEMPT_HISTORICAL_SLICE"
    if not slice_version or not controlling_version:
        return "UNRESOLVED_POINTER"
    return "CURRENT_MATCH" if slice_version == controlling_version else "STALE_CURRENT_SLICE"

def aggregate_score_allowed(fatal_unknowns: List[str]) -> bool:
    return len(fatal_unknowns) == 0

def proof_plane_transition_allowed(from_plane: str, to_plane: str, external_evidence_present: bool) -> bool:
    if to_plane in EXTERNAL_PLANES and not external_evidence_present:
        return False
    return True

def telemetry_value(value, measured: bool):
    return value if measured else None

def cross_store_status(github: str, drive: str) -> str:
    if github == "PASS" and drive == "PASS":
        return "CONVERGED"
    if github in {"PASS", "FAIL"} and drive in {"PASS", "FAIL"}:
        return "REPAIR_REQUIRED"
    return "HOLD_INCOMPLETE"

def double_loop_trigger(repeated_same_family_failures: int, causal_model_contradicted: bool=False,
                        gate_blocks_useful_work_without_protection: bool=False) -> bool:
    return repeated_same_family_failures >= 3 or causal_model_contradicted or gate_blocks_useful_work_without_protection

def metric_decision_link(metric_changes_decision: Optional[bool]) -> str:
    if metric_changes_decision is None:
        return "HOLD_UNPROVEN_DECISION_LINK"
    return "KEEP" if metric_changes_decision else "PRUNE_OR_DEMOTE"

def meta_wip_valid(primary: int, pilots: int) -> bool:
    return primary <= 1 and pilots <= 2 and (primary + pilots) <= 3

def semantic_dedupe(existing_mechanisms: Set[str], proposed_mechanism: str) -> str:
    return "MERGE_WITH_EXISTING" if proposed_mechanism in existing_mechanisms else "NEW_CANDIDATE_ALLOWED"

def local_vs_system(local_gain: bool, cross_domain_replications: int, regression_pass: bool) -> str:
    if not local_gain:
        return "NO_PROMOTION"
    if cross_domain_replications < 2:
        return "LOCAL_KEEP"
    if not regression_pass:
        return "HOLD_REGRESSION"
    return "SYSTEM_CANDIDATE"

def promotion_gate(candidate: Candidate, external_evidence_present: bool=False):
    reasons = []
    families = collapse_evidence_families(candidate.evidence)
    if not candidate.application_targets:
        reasons.append("APPLICATION_TARGETS_REQUIRED")
    if not candidate.rollback_defined:
        reasons.append("ROLLBACK_REQUIRED")
    if not candidate.protected_authorities:
        reasons.append("PROTECTED_AUTHORITIES_REQUIRED")
    for plane in candidate.required_planes:
        if plane in EXTERNAL_PLANES and not external_evidence_present:
            reasons.append(f"EXTERNAL_EVIDENCE_REQUIRED:{plane}")
    if not families:
        reasons.append("EVIDENCE_REQUIRED")
    return {"status": "HOLD" if reasons else "ELIGIBLE_FOR_BOUNDED_PROMOTION_REVIEW",
            "reasons": sorted(set(reasons)), "independent_families": len(families)}

def v3_readiness(real_downstream_net_gain_replications: int, cross_domain_replications: int,
                 regression_pass: bool, authority_regression: bool,
                 external_required_gates_satisfied: bool) -> str:
    if authority_regression:
        return "REJECT_AUTHORITY_REGRESSION"
    if not regression_pass:
        return "HOLD_REGRESSION"
    if real_downstream_net_gain_replications < 2:
        return "HOLD_REAL_NET_GAIN_REPLICATION"
    if cross_domain_replications < 2:
        return "HOLD_CROSS_DOMAIN_REPLICATION"
    if not external_required_gates_satisfied:
        return "HOLD_EXTERNAL_REQUIRED_GATES"
    return "ELIGIBLE_FOR_FOUNDER_PROMOTION_DECISION"

def missing_authority_result(has_complete_authority: bool) -> str:
    return "AUTHORITY_COMPLETE" if has_complete_authority else "HOLD_MISSING_AUTHORITY"

def package_identity(exact_hash_present: bool, source_head_bound: bool) -> str:
    return "PASS" if exact_hash_present and source_head_bound else "HOLD_PACKAGE_PROOF"

def false_zero_guard(value, measured: bool) -> str:
    if value == 0 and not measured:
        return "FAIL_FALSE_ZERO"
    return "PASS"

def free_substitute_disposition(substitute_coverage: str, residual_job: Optional[str]) -> str:
    if substitute_coverage == "FULL" and not residual_job:
        return "KILL_REDUNDANT_SCOPE"
    if substitute_coverage in {"HIGH", "FULL"} and residual_job:
        return "NARROW_TO_RESIDUAL_JOB"
    return "KEEP_HYPOTHESIS"

def backlog_is_progress(backlog_count: int, completed_decisive_tests: int) -> bool:
    return completed_decisive_tests > 0
