from dataclasses import dataclass
from typing import Optional, Dict, Any, Iterable


@dataclass(frozen=True)
class FrozenPacket:
    target_manifest_hash: Optional[str]
    bidder_manifest_hash: Optional[str]

    @property
    def complete(self) -> bool:
        return bool(self.target_manifest_hash and self.bidder_manifest_hash)


@dataclass(frozen=True)
class Reviewer:
    reviewer_id: Optional[str]
    reviewer_class: Optional[str]
    independent: bool
    blind_to_first_output: bool

    @property
    def valid_blind(self) -> bool:
        return bool(self.reviewer_id and self.reviewer_class and self.independent and self.blind_to_first_output)


def pa4_gate(packet: FrozenPacket, reviewer: Reviewer) -> Dict[str, Any]:
    if not packet.complete:
        return {"status": "HOLD_MISSING_FROZEN_MANIFESTS", "pa4": False}
    if not reviewer.valid_blind:
        return {"status": "HOLD_NO_INDEPENDENT_BLIND_REVIEWER", "pa4": False}
    return {"status": "READY_FOR_BLIND_PA4_RUN", "pa4": False}


def compare_rows(first: Optional[dict], blind: Optional[dict], same_packet_hash: bool) -> Dict[str, Any]:
    if not first or not blind or not same_packet_hash:
        return {"status": "HOLD_NO_COMPARABLE_OUTPUTS", "false_positive": None, "false_negative": None}
    keys = sorted(set(first) | set(blind))
    fp = sum(1 for k in keys if first.get(k) is True and blind.get(k) is False)
    fn = sum(1 for k in keys if first.get(k) is False and blind.get(k) is True)
    return {"status": "COMPARABLE", "false_positive": fp, "false_negative": fn}


def schema_revision_allowed(reproducible_divergence: bool) -> bool:
    return bool(reproducible_divergence)


def external_action_authorized(explicit_outreach_authorization: bool) -> bool:
    return bool(explicit_outreach_authorization)


def pa5_gate(real_target_user: bool, before_decision: Optional[str], after_decision: Optional[str],
             before_ts: Optional[str], after_ts: Optional[str], interaction_artifact: Optional[str]) -> Dict[str, Any]:
    required = [real_target_user, before_decision, after_decision, before_ts, after_ts, interaction_artifact]
    ok = all(bool(x) for x in required)
    return {"status": "PA5_EVIDENCE_PRESENT" if ok else "HOLD_NO_REAL_DECISION_USE", "pa5": ok}


def observed_time(before_minutes: Optional[float], after_minutes: Optional[float]) -> Optional[float]:
    if before_minutes is None or after_minutes is None:
        return None
    if before_minutes < 0 or after_minutes < 0:
        raise ValueError("negative observed time is invalid")
    return before_minutes - after_minutes


def rework_delta(use1_errors: Optional[int], use2_errors: Optional[int]) -> Optional[int]:
    if use1_errors is None or use2_errors is None:
        return None
    if use1_errors < 0 or use2_errors < 0:
        raise ValueError("negative error count is invalid")
    return use1_errors - use2_errors


def monetary_value(observed_quantity: Optional[float], external_unit_value: Optional[float]) -> Optional[float]:
    if observed_quantity is None or external_unit_value is None:
        return None
    if external_unit_value < 0:
        raise ValueError("negative value basis is invalid")
    return observed_quantity * external_unit_value


def e3_gate(pa5: bool, real_behavioral_cost_or_commitment: bool) -> bool:
    return bool(pa5 and real_behavioral_cost_or_commitment)


def e4_gate(cash_received: Optional[float], binding_transaction_ref: Optional[str]) -> bool:
    return bool(cash_received is not None and cash_received > 0 and binding_transaction_ref)


def residual_job_gate(job_components: Iterable[str], covered_components: Iterable[str]) -> Dict[str, Any]:
    jobs = set(job_components)
    covered = set(covered_components)
    residual = sorted(jobs - covered)
    if not residual:
        return {"status": "HOLD_RESHAPE_OR_REJECT", "residual_job": []}
    return {"status": "RESIDUAL_JOB_EXISTS", "residual_job": residual}


def proof_grade_guard(source_grade: str, polished: bool = False, ci_green: bool = False) -> str:
    # Presentation/CI cannot upgrade semantic evidence grade.
    return source_grade


def stale_conflict_guard(current_claim: Any, newer_or_authoritative_claim: Any, conflict: bool) -> str:
    if conflict:
        return "REVALIDATE"
    return "CURRENT_AS_ASSERTED"


def cross_store_commit(github_written: bool, github_readback: bool, drive_written: bool, drive_readback: bool) -> str:
    if all([github_written, github_readback, drive_written, drive_readback]):
        return "PERSISTED"
    if github_written or drive_written:
        return "RECONCILE_PARTIAL"
    return "NOT_WRITTEN"


def si_candidate(distinct_cases: int, regression_reproduced: bool) -> bool:
    return bool(distinct_cases >= 2 and regression_reproduced)


def next_frontier(target_pack_acquired: bool, bidder_packet_acquired: bool, pa4: bool, pa5: bool) -> str:
    if not target_pack_acquired:
        return "ACQUIRE_TARGET_PACK"
    if not bidder_packet_acquired:
        return "ACQUIRE_EXPLICIT_BIDDER_PACKET"
    if not pa4:
        return "RUN_BLIND_PA4"
    if not pa5:
        return "RUN_SMALLEST_REAL_DECISION_USE_TEST"
    return "DERIVE_FROM_NEW_EVIDENCE"


def planned_award_date_guard(
    workspace_status: Optional[str],
    contract_award_date: Optional[str],
    award_notice_or_binding_award_proven: bool = False,
) -> Dict[str, Any]:
    """A future/admin award-date field is not evidence that an award has happened.

    Current workspace metadata may expose a Contract Award Date while the CfT is still
    in Tender Submission. Only a separate award notice or binding award provenance can
    set awarded=True.
    """
    if award_notice_or_binding_award_proven:
        return {
            "awarded": True,
            "status": "AWARD_PROVEN_BY_SEPARATE_AUTHORITY",
            "workspace_status": workspace_status,
            "contract_award_date": contract_award_date,
        }
    if contract_award_date:
        return {
            "awarded": False,
            "status": "PLANNED_AWARD_DATE_NEQ_AWARDED_CONTRACT",
            "workspace_status": workspace_status,
            "contract_award_date": contract_award_date,
        }
    return {
        "awarded": False,
        "status": "NO_AWARD_EVIDENCE",
        "workspace_status": workspace_status,
        "contract_award_date": None,
    }
