from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, List

@dataclass(frozen=True)
class Opportunity:
    id: str
    name: str
    budget_eur: Optional[float]
    deadline_local: Optional[str]
    commission_type: str
    source: str
    status: str
    eligibility_verified: Optional[bool] = None
    site_class: Optional[str] = None
    official_brief_verified: bool = False


def deadline_state(op: Opportunity, now_iso: str) -> str:
    if not op.deadline_local:
        return 'VERIFY_DEADLINE'
    now = datetime.fromisoformat(now_iso)
    dl = datetime.fromisoformat(op.deadline_local)
    if dl <= now:
        return 'EXPIRED'
    days = (dl - now).total_seconds() / 86400
    if days <= 3: return 'CRITICAL'
    if days <= 10: return 'URGENT'
    return 'OPEN'


def eligibility_gate(op: Opportunity) -> str:
    if op.eligibility_verified is True: return 'PASS'
    if op.eligibility_verified is False: return 'FAIL'
    return 'HOLD'


def application_readiness(op: Opportunity, site_known: bool, portfolio_mapped: bool,
                          budget_complete: bool, submission_complete: bool=False) -> str:
    if not op.source: return 'A0'
    if not op.official_brief_verified: return 'A0'
    if op.eligibility_verified is not True: return 'A1'
    if not site_known: return 'A2'
    if not portfolio_mapped: return 'A3'
    if not budget_complete: return 'A4'
    if not submission_complete: return 'A5'
    return 'A6'


def budget_advisory(budget_eur: Optional[float], artist_fee_ratio: float=0.22,
                    contingency_ratio: float=0.05) -> Dict[str, Optional[float]]:
    if budget_eur is None:
        return {'artist_fee_target': None, 'contingency_target': None}
    if artist_fee_ratio < 0 or contingency_ratio < 0:
        raise ValueError('ratios must be non-negative')
    return {
        'artist_fee_target': round(budget_eur * artist_fee_ratio, 2),
        'contingency_target': round(budget_eur * contingency_ratio, 2),
    }


def bid_decision(op: Opportunity, now_iso: str, site_known: bool,
                 portfolio_mapped: bool, cash_exposure_known: bool) -> Dict[str, object]:
    ds = deadline_state(op, now_iso)
    eg = eligibility_gate(op)
    reasons: List[str] = []
    if ds == 'EXPIRED': return {'decision':'KILL','reasons':['expired'], 'vector':{'deadline':ds,'eligibility':eg}}
    if eg == 'FAIL': return {'decision':'KILL','reasons':['ineligible'], 'vector':{'deadline':ds,'eligibility':eg}}
    if ds == 'VERIFY_DEADLINE': reasons.append('verify_deadline')
    if eg == 'HOLD': reasons.append('verify_eligibility')
    if not op.official_brief_verified: reasons.append('official_brief_missing')
    if not site_known: reasons.append('site_unknown')
    if not portfolio_mapped: reasons.append('portfolio_mapping_incomplete')
    if not cash_exposure_known: reasons.append('cash_exposure_unknown')
    decision = 'KEEP' if not reasons else 'HOLD'
    return {'decision':decision,'reasons':reasons,'vector':{
        'deadline':ds,'eligibility':eg,'brief':op.official_brief_verified,
        'site_known':site_known,'portfolio_mapped':portfolio_mapped,
        'cash_exposure_known':cash_exposure_known}}


def historical_claim_gate(source_count: int, is_allegory: bool=False) -> str:
    if is_allegory: return 'ALLEGORY_ALLOWED_LABEL_REQUIRED'
    return 'PASS' if source_count >= 1 else 'HOLD'


def material_lock(substrate_known: bool, moisture_checked: bool) -> str:
    return 'PASS' if substrate_known and moisture_checked else 'HOLD'


def trompe_loeil_gate(primary_viewpoint_known: bool, geometry_known: bool) -> str:
    return 'PASS' if primary_viewpoint_known and geometry_known else 'HOLD'


def proof_ceiling(interaction: bool=False, payment: bool=False) -> str:
    if payment: return 'E4+'
    if interaction: return 'E3'
    return 'E2+'
