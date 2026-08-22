import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runtime"))
from ecommerce_stock_transition import StockEvidence, inventory_scenario, private_label_gate, route, small_batch_gate


class StockTransitionTests(unittest.TestCase):
    def test_null_cost_keeps_units_null(self):
        self.assertIsNone(inventory_scenario(500, None)["theoretical_units"])

    def test_budget_allocation_conserves_total(self):
        x = inventory_scenario(2000, 50)
        self.assertEqual(x["inventory_allocation"] + x["freight_pack_reserve"] + x["contingency_reserve"], 2000)

    def test_scenario_is_not_purchase_authorization(self):
        self.assertFalse(inventory_scenario(5000, 100)["scenario_is_purchase_authorization"])

    def test_current_missing_economics_stays_dropship(self):
        r = route(StockEvidence())
        self.assertEqual(r["disposition"], "DROPSHIP_ECONOMICS_OR_DEMAND_EVIDENCE_INCOMPLETE")
        self.assertIn("LANDED_UNIT_COST", r["blockers"])
        self.assertIn("IRELAND_SHIPPING", r["blockers"])

    def test_orders_without_profit_do_not_open_batch(self):
        e = StockEvidence(paid_orders=100, independent_buyers=80)
        ok, _ = small_batch_gate(e)
        self.assertFalse(ok)

    def test_negative_post_cac_after_20_orders_drops(self):
        e = StockEvidence(paid_orders=20, post_cac_contribution_per_order=-1)
        self.assertEqual(route(e)["disposition"], "DROP")

    def test_fatal_quality_issue_drops_even_with_strong_sales(self):
        e = StockEvidence(paid_orders=100, post_cac_contribution_per_order=30, fatal_quality_or_safety_issue=True)
        self.assertEqual(route(e)["disposition"], "DROP")

    def test_small_batch_requires_delivery_and_returns_observation(self):
        e = StockEvidence(
            paid_orders=20, independent_buyers=10, post_cac_contribution_per_order=20,
            landed_unit_cost=40, ireland_shipping_verified=True, moq_verified=True,
            replenishment_lead_time_verified=True, capital_stop_loss_ok=True,
        )
        ok, missing = small_batch_gate(e)
        self.assertFalse(ok)
        self.assertIn("RETURN_RATE_LE_10_PERCENT", missing)
        self.assertIn("DELIVERY_SLA_GE_90_PERCENT", missing)

    def test_complete_small_batch_evidence_routes_small_batch(self):
        e = StockEvidence(
            paid_orders=25, independent_buyers=20, post_cac_contribution_per_order=20,
            return_rate=.05, delivery_sla_rate=.95, landed_unit_cost=40,
            ireland_shipping_verified=True, moq_verified=True,
            replenishment_lead_time_verified=True, capital_stop_loss_ok=True,
        )
        self.assertEqual(route(e)["disposition"], "SMALL_BATCH_ELIGIBLE_FOR_SEPARATE_CAPITAL_APPROVAL")

    def test_small_batch_route_is_not_purchase_authorization(self):
        e = StockEvidence(
            paid_orders=25, independent_buyers=20, post_cac_contribution_per_order=20,
            return_rate=.05, delivery_sla_rate=.95, landed_unit_cost=40,
            ireland_shipping_verified=True, moq_verified=True,
            replenishment_lead_time_verified=True, capital_stop_loss_ok=True,
        )
        self.assertFalse(route(e)["proof_boundary"]["route_is_purchase_authorization"])

    def test_private_label_requires_six_week_distribution_and_qc(self):
        e = StockEvidence(
            paid_orders=60, independent_buyers=40, post_cac_contribution_per_order=20,
            return_rate=.05, delivery_sla_rate=.95, landed_unit_cost=40,
            ireland_shipping_verified=True, moq_verified=True,
            replenishment_lead_time_verified=True, capital_stop_loss_ok=True,
        )
        ok, missing = private_label_gate(e)
        self.assertFalse(ok)
        self.assertIn("WEEKS_OBSERVED_6", missing)
        self.assertIn("QC_PROCESS_VERIFIED", missing)

    def test_full_private_label_gate_is_only_eligibility(self):
        e = StockEvidence(
            paid_orders=60, independent_buyers=40, weeks_observed=8,
            largest_week_share=.20, post_cac_contribution_per_order=20,
            return_rate=.05, delivery_sla_rate=.95, landed_unit_cost=40,
            ireland_shipping_verified=True, moq_verified=True,
            replenishment_lead_time_verified=True, repeat_or_stable_demand_signal=True,
            qc_process_verified=True, differentiation_test_defined=True,
            capital_stop_loss_ok=True,
        )
        r = route(e)
        self.assertEqual(r["disposition"], "PRIVATE_LABEL_ELIGIBLE_FOR_SEPARATE_CAPITAL_APPROVAL")
        self.assertFalse(r["proof_boundary"]["private_label_eligibility_is_private_label_profitability"])


if __name__ == "__main__":
    unittest.main()
