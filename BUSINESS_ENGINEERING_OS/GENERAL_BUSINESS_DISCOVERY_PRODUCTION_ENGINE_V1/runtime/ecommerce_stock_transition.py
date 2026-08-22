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
    if budget not in (500, 2000, 5000): raise ValueError('budget must be one of 500, 2000, 5000')
    if landed_unit_cost is not None and landed_unit_cost <= 0: raise ValueError('landed_unit_cost must be positive')
    inventory, freight_pack, contingency = budget*.70, budget*.15, budget*.15
    units = None if landed_unit_cost is None else floor(inventory/landed_unit_cost)
    return {'budget':budget,'inventory_allocation':inventory,'freight_pack_reserve':freight_pack,'contingency_reserve':contingency,'theoretical_units':units,'scenario_is_purchase_authorization':False}

def small_batch_gate(e: StockEvidence):
    m=[]
    if e.landed_unit_cost is None: m.append('LANDED_UNIT_COST')
    if not e.ireland_shipping_verified: m.append('IRELAND_SHIPPING')
    if e.paid_orders < 20: m.append('PAID_ORDERS_20')
    if e.independent_buyers < 10: m.append('INDEPENDENT_BUYERS_10')
    if e.post_cac_contribution_per_order is None or e.post_cac_contribution_per_order <= 0: m.append('POSITIVE_POST_CAC_CONTRIBUTION')
    if e.return_rate is None or e.return_rate > .10: m.append('RETURN_RATE_LE_10_PERCENT')
    if e.delivery_sla_rate is None or e.delivery_sla_rate < .90: m.append('DELIVERY_SLA_GE_90_PERCENT')
    if not e.moq_verified: m.append('MOQ_VERIFIED')
    if not e.replenishment_lead_time_verified: m.append('REPLENISHMENT_LEAD_TIME_VERIFIED')
    if not e.capital_stop_loss_ok: m.append('CAPITAL_STOP_LOSS_OK')
    if e.fatal_quality_or_safety_issue: m.append('FATAL_QUALITY_OR_SAFETY_ISSUE')
    return not m, m

def private_label_gate(e: StockEvidence):
    sb_ok, m = small_batch_gate(e); m=list(m)
    if not sb_ok: m.append('SMALL_BATCH_GATE')
    if e.paid_orders < 50: m.append('PAID_ORDERS_50')
    if e.weeks_observed < 6: m.append('WEEKS_OBSERVED_6')
    if e.largest_week_share is None or e.largest_week_share > .40: m.append('LARGEST_WEEK_SHARE_LE_40_PERCENT')
    if not e.repeat_or_stable_demand_signal: m.append('REPEAT_OR_STABLE_DEMAND_SIGNAL')
    if not e.qc_process_verified: m.append('QC_PROCESS_VERIFIED')
    if not e.differentiation_test_defined: m.append('DIFFERENTIATION_TEST_DEFINED')
    return not m, m

def route(e: StockEvidence) -> dict:
    if e.fatal_quality_or_safety_issue:
        d,b='DROP',['FATAL_QUALITY_OR_SAFETY_ISSUE']
    elif e.post_cac_contribution_per_order is not None and e.paid_orders >= 20 and e.post_cac_contribution_per_order <= 0:
        d,b='DROP',['NEGATIVE_POST_CAC_CONTRIBUTION']
    else:
        pl,plm=private_label_gate(e); sb,sbm=small_batch_gate(e)
        if pl: d,b='PRIVATE_LABEL_ELIGIBLE_FOR_SEPARATE_CAPITAL_APPROVAL',[]
        elif sb: d,b='SMALL_BATCH_ELIGIBLE_FOR_SEPARATE_CAPITAL_APPROVAL',plm
        else: d,b='DROPSHIP_ECONOMICS_OR_DEMAND_EVIDENCE_INCOMPLETE',sbm
    return {'schema':'ivdivo.business.ecommerce_stock_transition/1.0','disposition':d,'evidence':asdict(e),'blockers':b,'proof_boundary':{'route_is_purchase_authorization':False,'sales_are_profit_proof':False,'private_label_eligibility_is_private_label_profitability':False}}
