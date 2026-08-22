from dataclasses import dataclass


@dataclass(frozen=True)
class Opportunity:
    opportunity_id: str
    live_public_signal: bool
    case_fixture_only: bool = False
    sibling_lane: bool = False
    significant_capex: bool = False
    real_demand_evidence: bool = False
    public_procurement: bool = False
    full_pack_acquired: bool = False
    explicit_bidder_designation: bool = False
    direct_service: bool = False
    generic_diagnostic_substituted: bool = False
    real_post_diagnostic_packet: bool = False


def route(o: Opportunity) -> str:
    """Fail-closed portfolio routing without a synthetic total score."""
    if o.sibling_lane:
        return "SIBLING_LANE_COMPARE_ONLY"
    if o.significant_capex and not o.real_demand_evidence:
        return "HOLD_CAPEX_PENDING_DEMAND"
    if o.direct_service:
        return "CHEAP_DIRECT_REVENUE_TEST"
    if o.generic_diagnostic_substituted and not o.real_post_diagnostic_packet:
        return "PILOT_RESIDUAL_IMPLEMENTATION_JOB"
    if o.public_procurement:
        if not o.full_pack_acquired:
            return "EXPLORE_PACK_FIRST"
        if not o.explicit_bidder_designation:
            return "HOLD_NO_BIDDER_DESIGNATION"
        return "QUALIFICATION_ANALYSIS_ALLOWED"
    if o.case_fixture_only:
        return "FIXTURE_ONLY_NOT_PORTFOLIO_AUTHORITY"
    if o.live_public_signal:
        return "WATCH_AND_DEFINE_CHEAP_TEST"
    return "HOLD_NO_CURRENT_SIGNAL"
