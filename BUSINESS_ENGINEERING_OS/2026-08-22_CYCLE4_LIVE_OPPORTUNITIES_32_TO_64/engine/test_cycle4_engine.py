import unittest
from business_opportunity_engine import *

class Cycle4EngineTests(unittest.TestCase):
    def fixture(self,**kw):
        x={"id":"O","signal_id":"S","buyer_segment":"SME","deliverable":"brief","fatal_assumption":"need",
           "cheapest_no_outreach_test":"sample","kill_rule":"kill","founder_cash_pre_E4_eur":0,
           "credential_barrier":"LOW","business_type":"SERVICE","route":"CREATE","signal_fact":"public workload",
           "unit_economics":None,"willingness_to_pay":None,"derived_offer_market_grade":"E1",
           "manual_deliverable_possible":True}
        x.update(kw);return x
    def signal(self,**kw):
        x={"id":"S","observed":"2026-08-22","freshness_days":30};x.update(kw);return x
    def test_wtp_stays_null(self): self.assertIsNone(buyer_workload(self.fixture())["willingness_to_pay"])
    def test_zero_cash(self): self.assertTrue(founder_cash_timeline(self.fixture())["pass"])
    def test_high_barrier_routes_broker(self): self.assertEqual(create_broker_acquire(self.fixture(credential_barrier="HIGH"))["recommended"],"BROKER")
    def test_reimbursable_grant_not_zero_cash(self):
        r=[x for x in funding_topology(self.fixture()) if x["route"]=="GRANT_REIMBURSABLE"][0]
        self.assertFalse(r["founder_cash_zero_compatible"])
    def test_economics_unknown_is_hold_not_fake_number(self): self.assertFalse(seven_domains_gate(self.fixture())["domains"]["economics_known"])
    def test_retainer_blocked(self): self.assertFalse(recurring_value_gate(self.fixture())["retainer_authorized"])
    def test_acquisition_dscr_null(self): self.assertIsNone(acquisition_stress(self.fixture())["dscr"])
    def test_exploit_blocked_at_E1(self): self.assertFalse(graduation_gate(self.fixture())["exploit_authorized"])
    def test_stale_signal(self): self.assertFalse(freshness(self.signal(observed="2025-01-01"))["fresh"])
    def test_red_team_false_E4(self):
        o=self.fixture(derived_offer_market_grade="E4")
        self.assertFalse(red_team([o],[self.signal()])["pass"])
    def test_red_team_cash_breach(self):
        o=self.fixture(founder_cash_pre_E4_eur=1)
        self.assertFalse(red_team([o],[self.signal()])["pass"])
    def test_wip_cap(self):
        p=portfolio_dashboard([self.fixture(id=f"O{i}") for i in range(5)])
        self.assertEqual(p["active_count"],3)

if __name__=="__main__": unittest.main()
