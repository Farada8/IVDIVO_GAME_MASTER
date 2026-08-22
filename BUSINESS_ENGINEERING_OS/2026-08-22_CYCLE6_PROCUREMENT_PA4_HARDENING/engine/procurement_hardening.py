from dataclasses import dataclass
from enum import Enum
from typing import Optional


class GapState(str, Enum):
    MET = "MET"
    UNKNOWN = "UNKNOWN"
    CURABLE_BEFORE_DEADLINE = "CURABLE_BEFORE_DEADLINE"
    NONCURABLE = "NONCURABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class Decision(str, Enum):
    BID = "BID"
    HOLD_INSUFFICIENT_EVIDENCE = "HOLD_INSUFFICIENT_EVIDENCE"
    NO_BID = "NO_BID"


@dataclass(frozen=True)
class ProcurementEvidenceState:
    official_pack_complete: bool = False
    supplier_profile_verified: bool = False
    requirement_join_complete: bool = False
    noncurable_mandatory_gap_count: int = 0
    unknown_mandatory_gap_count: int = 0
    curable_gap_count: int = 0
    bid_effort_hours: Optional[float] = None
    bid_effort_cost_eur: Optional[float] = None


def decide_bid(state: ProcurementEvidenceState) -> Decision:
    """Fail closed. BID/NO_BID require the authoritative pack and verified supplier facts."""
    if not state.official_pack_complete:
        return Decision.HOLD_INSUFFICIENT_EVIDENCE
    if not state.supplier_profile_verified:
        return Decision.HOLD_INSUFFICIENT_EVIDENCE
    if not state.requirement_join_complete:
        return Decision.HOLD_INSUFFICIENT_EVIDENCE
    if state.unknown_mandatory_gap_count > 0:
        return Decision.HOLD_INSUFFICIENT_EVIDENCE
    if state.noncurable_mandatory_gap_count > 0:
        return Decision.NO_BID
    return Decision.BID


def pa4_ready(state: ProcurementEvidenceState) -> bool:
    """PA4 can only start after both reviewers can receive the same complete inputs."""
    return (
        state.official_pack_complete
        and state.supplier_profile_verified
        and state.requirement_join_complete
        and state.unknown_mandatory_gap_count == 0
    )


def estimated_cash_requirement_from_contract_value(estimated_value_eur: float) -> None:
    """Contract value is not evidence of working-capital need; preserve unknown as None."""
    _ = estimated_value_eur
    return None


def classify_gap(*, requirement_met: Optional[bool], curable_before_deadline: Optional[bool], applicable: bool = True) -> GapState:
    if not applicable:
        return GapState.NOT_APPLICABLE
    if requirement_met is True:
        return GapState.MET
    if requirement_met is None:
        return GapState.UNKNOWN
    if curable_before_deadline is True:
        return GapState.CURABLE_BEFORE_DEADLINE
    if curable_before_deadline is False:
        return GapState.NONCURABLE
    return GapState.UNKNOWN
