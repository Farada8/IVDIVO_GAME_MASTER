from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ServiceCase:
    retail_price: float
    delivery_cost_before_acquisition: float
    verified_scope_quote: bool = False
    competency_ok: bool = False
    insurance_ok: bool = False
    responsibility_defined: bool = False
    direct_cost_sheet_verified: bool = False
    paying_referral_partner: bool = False
    referral_contribution: Optional[float] = None


def pre_acquisition_contribution(case: ServiceCase) -> float:
    return case.retail_price - case.delivery_cost_before_acquisition


def acquisition_ceiling(case: ServiceCase, share: float = 0.20) -> Optional[float]:
    c = pre_acquisition_contribution(case)
    if c <= 0:
        return 0.0
    return c * share


def route(case: ServiceCase) -> str:
    c = pre_acquisition_contribution(case)
    if c <= 0:
        return "HOLD_OR_DROP"
    if case.verified_scope_quote and case.competency_ok and case.insurance_ok and case.responsibility_defined:
        return "SUBCONTRACT_ELIGIBLE"
    if case.direct_cost_sheet_verified:
        return "DIRECT_ELIGIBLE"
    if case.paying_referral_partner and (case.referral_contribution or 0) > 0:
        return "REFERRAL_ONLY_ELIGIBLE"
    return "REFERENCE_ONLY_HOLD"


def can_set_real_max_acquisition_cost(observed_close_rate: Optional[float], verified_job_contribution: Optional[float]) -> bool:
    return observed_close_rate is not None and verified_job_contribution is not None
