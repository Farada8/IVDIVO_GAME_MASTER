from dataclasses import dataclass
from typing import Optional, Iterable

PUBLIC_MAX = "E2_PUBLIC_SIGNAL"

@dataclass(frozen=True)
class Evidence:
    kind: str
    source: str
    measured: bool = True

def evidence_ceiling(evidence: Iterable[Evidence]) -> str:
    kinds = {e.kind for e in evidence}
    if "PAYMENT" in kinds: return "E4_PAYMENT"
    if "HUMAN" in kinds: return "E3_HUMAN_INTEREST"
    if "PUBLIC_SIGNAL" in kinds: return PUBLIC_MAX
    if "KNOWLEDGE" in kinds: return "K_ONLY"
    return "E0_NONE"

def null_safe_number(value, measured: bool): return value if measured else None

def budget_proxy(public_budget: Optional[float], buyer_payment_observed: bool=False) -> str:
    if buyer_payment_observed: return "PAYMENT_EVIDENCE"
    return "BUDGET_PROXY_ONLY" if public_budget is not None else "UNKNOWN"

def incumbent_bundling(discovery: bool, qualification: bool, evidence_assembly: bool) -> str:
    if discovery and qualification and evidence_assembly: return "KILL_UNDIFFERENTIATED"
    if discovery and not qualification: return "MUTATE_TO_QUALIFICATION_EVIDENCE"
    return "SURVIVES_BUNDLING_GATE"

def data_readiness(public_fields: int, required_fields: int, private_or_site_fields: int=0) -> str:
    if required_fields <= 0: return "INVALID_SPEC"
    if private_or_site_fields > 0: return "HUMAN_OR_CLIENT_DATA_REQUIRED"
    ratio = public_fields / required_fields
    if ratio >= 0.8: return "AUTOMATION_CANDIDATE"
    if ratio >= 0.5: return "HYBRID_MANUAL_REVIEW"
    return "HOLD_DATA_GAP"

def recurrence_gate(events_per_year: Optional[int], same_job: bool) -> str:
    if events_per_year is None: return "HOLD_UNKNOWN_RECURRENCE"
    if same_job and events_per_year >= 4: return "RECURRING_JOB"
    if same_job and events_per_year >= 2: return "PROJECT_REPEAT_NOT_SUBSCRIPTION_PROVEN"
    return "ONE_OFF_OR_WEAK"

def zero_cash_route(service_type: str, requires_capex: bool, partner_delivery: bool, prepay_possible: bool) -> str:
    if requires_capex and not (partner_delivery or prepay_possible): return "HOLD_CAPITAL_REQUIRED"
    if partner_delivery: return "BROKER_ORCHESTRATE"
    if prepay_possible: return "CUSTOMER_FUNDED_CREATE"
    if service_type == "analysis": return "MANUAL_SERVICE_FIRST"
    return "HOLD_ROUTE_UNKNOWN"

def privacy_gate(contains_personal_data: bool, open_data: bool, purpose_justified: bool) -> str:
    if contains_personal_data and not open_data: return "REJECT_NONOPEN_PERSONAL_DATA"
    if contains_personal_data and not purpose_justified: return "REJECT_UNJUSTIFIED_PERSONAL_DATA"
    return "PASS_PUBLIC_DATA"

def supersession_gate(compiled_source_version: str, current_source_version: str) -> str:
    return "REVALIDATE" if compiled_source_version != current_source_version else "CURRENT"

def freshness_gate(compiled_main_sha: str, current_main_sha: str) -> str:
    return "REBASE_REVALIDATE" if compiled_main_sha != current_main_sha else "FRESH"

def library_evidence_weight(is_exact_byte_duplicate: bool, is_broken: bool) -> int:
    return 0 if is_broken or is_exact_byte_duplicate else 1

def namespace_collision(existing_semantic_fingerprint: Optional[str], incoming_semantic_fingerprint: str) -> str:
    if existing_semantic_fingerprint is None: return "FREE"
    if existing_semantic_fingerprint == incoming_semantic_fingerprint: return "ALIAS_SAME_SEMANTICS"
    return "REJECT_COLLISION"

def wip_gate(primary_count: int, pilot_count: int) -> str:
    return "PASS_WIP" if primary_count == 1 and pilot_count <= 2 else "HOLD_WIP_LIMIT"

def human_exit_gate(no_outreach: bool, founder_authorized: bool, decision_changing_gap: bool, consent_packet_ready: bool) -> str:
    if no_outreach and not founder_authorized: return "HOLD_NO_OUTREACH"
    if not decision_changing_gap: return "HOLD_LOW_INFORMATION_VALUE"
    if not consent_packet_ready: return "HOLD_CONSENT_PACKET"
    return "READY_FOR_HUMAN_VALIDATION"
