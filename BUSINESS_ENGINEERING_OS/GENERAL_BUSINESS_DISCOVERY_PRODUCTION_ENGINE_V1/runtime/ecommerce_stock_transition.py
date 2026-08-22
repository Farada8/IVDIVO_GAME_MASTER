from __future__ import annotations

from dataclasses import dataclass, asdict
from math import floor
from typing import Optional


@dataclass(frozen=True)
class StockEvidence:
    paid_orders: int = 0
    independent_buyers: int = 0
    weeks_observed: int = 0
    largest_week_share: Optional[float] = None
    post_cac_contribution_per_order: Optional[float] = None
    return_rate: Optional[float] = None
    delivery_sla_rate: Optional[float] = None
    landed_unit_cost: Optional[float] = None
    ireland_shipping_verified: bool = False
    moq_verified: bool = False
    replenishment_lead_time_verified: bool = False
    fatal_quality_or_safety_issue: bool = False
    repeat_or_stable_demand_signal: bool = False
    qc_process_verified: bool = False
    differentiation_test_defined: bool = False
    capital_stop_loss_ok: bool = False


def inventory_scenario(budget: float, landed_unit_cost: Optional[float]) -> dict:
    if budget not in (500, 2000, 5000):
        raise ValueError("budget must be one of 500, 2000, 5000")
    inventory = budget * 0.70
    freight_pack = budget * 0.15
    contingency = budget * 0.15
    units = None
    if landed_unit_cost is not None:
        if landed_unit_cost <= 0:
            raise ValueError("landed_unit_cost must be positive")
        units = floor(inventory / landed_unit_cost)
    return {
        "budget": budget,
        "inventory_allocation": inventory,
        "freight_pack_reserve": freight_pack,
        "contingency_reserve": contingency,
        "theoretical_units": units,
        "scenario_is_purchase_authorization": False,
    }


def small_batch_gate(e: StockEvidence) -> tuple[bool, list[str]]:
    missing: list[str] = []
    if e.landed_unit_cost is None:
        missing.append("LANDED_UNIT_COST")
    if not e.ireland_shipping_verified:
        missing.append("IRELAND_SHIPPING")
    if e.paid_orders < 20:
        missing.append("PAID_ORDERS_20")
    if e.independent_buyers < 10:
        missing.append("INDEPENDENT_BUYERS_10")
    if e.post_cac_contribution_per_order is None or e.post_cac_contribution_per_order <= 0:
        missing.append("POSITIVE_POST_CAC_CONTRIBUTION")
    if e.return_rate is None or e.return_rate > 0.10:
        missing.append("RETURN_RATE_LE_10_PERCENT")
    if e.delivery_sla_rate is None or e.delivery_sla_rate < 0.90:
        missing.append("DELIVERY_SLA_GE_90_PERCENT")
    if not e.moq_verified:
        missing.append("MOQ_VERIFIED")
    if not e.replenishment_lead_time_verified:
        missing.append("REPLENISHMENT_LEAD_TIME_VERIFIED")
    if not e.capital_stop_loss_ok:
        missing.append("CAPITAL_STOP_LOSS_OK")
    if e.fatal_quality_or_safety_issue:
        missing.append("FATAL_QUALITY_OR_SAFETY_ISSUE")
    return not missing, missing


def private_label_gate(e: StockEvidence) -> tuple[bool, list[str]]:
    sb_ok, sb_missing = small_batch_gate(e)
    missing = list(sb_missing)
    if not sb_ok:
        missing.append("SMALL_BATCH_GATE")
    if e.paid_orders < 50:
        missing.append("PAID_ORDERS_50")
    if e.weeks_observed < 6:
        missing.append("WEEKS_OBSERVED_6")
    if e.largest_week_share is None or e.largest_week_share > 0.40:
        missing.append("LARGEST_WEEK_SHARE_LE_40_PERCENT")
    if not e.repeat_or_stable_demand_signal:
        missing.append("REPEAT_OR_STABLE_DEMAND_SIGNAL")
    if not e.qc_process_verified:
        missing.append("QC_PROCESS_VERIFIED")
    if not e.differentiation_test_defined:
        missing.append("DIFFERENTIATION_TEST_DEFINED")
    return not missing, missing


def route(e: StockEvidence) -> dict:
    if e.fatal_quality_or_safety_issue:
        disposition = "DROP"
        blockers = ["FATAL_QUALITY_OR_SAFETY_ISSUE"]
    elif e.post_cac_contribution_per_order is not None and e.paid_orders >= 20 and e.post_cac_contribution_per_order <= 0:
        disposition = "DROP"
        blockers = ["NEGATIVE_POST_CAC_CONTRIBUTION"]
    else:
        pl_ok, pl_missing = private_label_gate(e)
        sb_ok, sb_missing = small_batch_gate(e)
        if pl_ok:
            disposition = "PRIVATE_LABEL_ELIGIBLE_FOR_SEPARATE_CAPITAL_APPROVAL"
            blockers = []
        elif sb_ok:
            disposition = "SMALL_BATCH_ELIGIBLE_FOR_SEPARATE_CAPITAL_APPROVAL"
            blockers = pl_missing
        else:
            disposition = "DROPSHIP_ECONOMICS_OR_DEMAND_EVIDENCE_INCOMPLETE"
            blockers = sb_missing
    return {
        "schema": "ivdivo.business.ecommerce_stock_transition/1.0",
        "disposition": disposition,
        "evidence": asdict(e),
        "blockers": blockers,
        "proof_boundary": {
            "route_is_purchase_authorization": False,
            "sales_are_profit_proof": False,
            "private_label_eligibility_is_private_label_profitability": False,
        },
    }
