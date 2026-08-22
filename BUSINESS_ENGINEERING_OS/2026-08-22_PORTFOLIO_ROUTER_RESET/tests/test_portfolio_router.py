import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.portfolio_router import Opportunity, route


class PortfolioRouterTests(unittest.TestCase):
    def test_public_procurement_without_pack_routes_pack_first(self):
        o = Opportunity("PROC", True, public_procurement=True)
        self.assertEqual(route(o), "EXPLORE_PACK_FIRST")

    def test_pack_without_bidder_stays_hold(self):
        o = Opportunity("PROC", True, public_procurement=True, full_pack_acquired=True)
        self.assertEqual(route(o), "HOLD_NO_BIDDER_DESIGNATION")

    def test_pack_and_bidder_allow_qualification_not_bid(self):
        o = Opportunity("PROC", True, public_procurement=True, full_pack_acquired=True, explicit_bidder_designation=True)
        self.assertEqual(route(o), "QUALIFICATION_ANALYSIS_ALLOWED")

    def test_sibling_lane_cannot_hijack_frontier(self):
        o = Opportunity("ART", True, sibling_lane=True)
        self.assertEqual(route(o), "SIBLING_LANE_COMPARE_ONLY")

    def test_capex_without_demand_is_held(self):
        o = Opportunity("CAPEX", True, significant_capex=True)
        self.assertEqual(route(o), "HOLD_CAPEX_PENDING_DEMAND")

    def test_direct_service_routes_to_cheap_revenue_test(self):
        o = Opportunity("DIRECT", False, direct_service=True)
        self.assertEqual(route(o), "CHEAP_DIRECT_REVENUE_TEST")

    def test_generic_diagnostic_substitution_routes_residual_job(self):
        o = Opportunity("AI", True, generic_diagnostic_substituted=True)
        self.assertEqual(route(o), "PILOT_RESIDUAL_IMPLEMENTATION_JOB")

    def test_unproven_signal_does_not_become_primary(self):
        o = Opportunity("UNKNOWN", False)
        self.assertEqual(route(o), "HOLD_NO_CURRENT_SIGNAL")


if __name__ == "__main__":
    unittest.main(verbosity=2)
