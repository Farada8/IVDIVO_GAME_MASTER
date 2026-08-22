import unittest
from cycle5_business_engine import *

NOW="2026-08-22T00:06:00+00:00"

class Cycle5EngineTests(unittest.TestCase):
    def test_expiry(self):
        self.assertEqual(expiry_state("2026-08-10T00:00:00+00:00", NOW, 14)["state"], "FRESH")
        self.assertEqual(expiry_state("2026-07-20T00:00:00+00:00", NOW, 14)["state"], "STALE")

    def test_url_canonicalization(self):
        u=canonicalize_url("http://www.seai.ie/x/?utm_source=a&b=2&a=1#frag")
        self.assertEqual(u,"https://seai.ie/x?a=1&b=2")
        self.assertTrue(is_official_url(u))

    def test_syndication(self):
        signals=[{"signal_id":"a","title":"Grant announced","claim":"funding opens"},{"signal_id":"b","title":"Grant announced","claim":"funding opens"}]
        clusters=syndication_clusters(signals)
        self.assertEqual(len(clusters),1)

    def test_procurement_conflict_holds(self):
        out=procurement_status(published_at="2026-08-01T00:00:00+00:00",deadline_at="2026-09-01T00:00:00+00:00",declared_status="Open",now=NOW,conflicting_deadline=True)
        self.assertEqual(out["status"],"REVALIDATE_CANONICAL_NOTICE")

    def test_procurement_open(self):
        out=procurement_status(published_at="2026-08-01T00:00:00+00:00",deadline_at="2026-09-01T00:00:00+00:00",declared_status="Open",now=NOW)
        self.assertEqual(out["status"],"OPEN")

    def test_supersession(self):
        g=build_supersession_graph([{"topic_key":"x","record_id":"a","published_at":"2026-01-01T00:00:00+00:00"},{"topic_key":"x","record_id":"b","published_at":"2026-02-01T00:00:00+00:00"}])
        self.assertEqual(g["current"]["x"],"b")

    def test_budget_not_wtp(self):
        out=budget_owner_confidence(budget_amount=1_000_000,contracting_authority="HSE",named_budget_owner=None,buyer_role_evidence=None)
        self.assertIsNone(out["willingness_to_pay"])
        self.assertFalse(out["buyer_person_inferred"])

    def test_access_official(self):
        out=verify_access_path(["https://www.etenders.gov.ie/epps/cft/prepareViewCfTWS.do?resourceId=1"])
        self.assertEqual(out["status"],"PASS")

    def test_disruption_classification(self):
        self.assertEqual(classify_disruption(nonconsumer_blocked=True,incumbent_overperformance=False,simpler_lower_cost_sufficient=True),"NEW_MARKET_NONCONSUMPTION")

    def test_motivation_ability_separate(self):
        self.assertEqual(motivation_ability_change(forced_action=True,funding_support=False,tooling_support=False,skills_support=False),{"motivation":"UP","ability":"UNCHANGED_OR_UNKNOWN"})

    def test_falsifier(self):
        self.assertEqual(evaluate_falsifier(opportunity_id="OP1",falsifier="x",observed_kill_evidence=True)["verdict"],"KILL_OR_RESHAPE")

    def test_assumption_queue(self):
        ops=[{"opportunity_id":"A","fatal_assumptions":[{"claim":"buyer workload recurs","kill_power":1,"uncertainty":1,"testability":1}]},{"opportunity_id":"B","fatal_assumptions":[{"claim":"buyer workload recurs","kill_power":1,"uncertainty":1,"testability":1}]}]
        self.assertEqual(cross_cutting_assumption_queue(ops)[0]["opportunity_ids"],["A","B"])

    def test_artifact_does_not_raise_market_grade(self):
        out=artifact_test(sources=5,canonical_sources=5,decisions_before=5,decisions_after=2,unresolved_fatal=0)
        self.assertEqual(out["verdict"],"PUBLIC_ARTIFACT_PASS")
        self.assertEqual(out["market_evidence_grade"],"E2+")
        self.assertIsNone(out["willingness_to_pay"])

    def test_mom_filter(self):
        self.assertEqual(mom_test_filter("Would you pay for this?")["verdict"],"REWRITE")
        self.assertEqual(mom_test_filter("Tell me about the last time you missed a tender deadline.")["verdict"],"PASS_BEHAVIORAL")

    def test_e3_not_payment(self):
        out=e3_conversation_evidence(participant_role="Owner",problem_recent_example="missed tender",existing_workaround="weekly browse",cost_or_consequence="lost time",voluntary_followup=True)
        self.assertEqual(out["evidence_grade"],"E3")
        self.assertFalse(out["payment_proof"])

    def test_e4_requires_money_or_po(self):
        self.assertEqual(e4_payment_proof(instrument="PAID_PILOT",amount_eur=100,payer_identity_bound=True,scope_bound=True,payment_received_or_po=True)["evidence_grade"],"E4")
        self.assertNotEqual(e4_payment_proof(instrument=None,amount_eur=None,payer_identity_bound=False,scope_bound=False,payment_received_or_po=False)["evidence_grade"],"E4")

    def test_price_stays_null(self):
        self.assertIsNone(pricing_experiment()["price_eur"])

    def test_cash_bridge(self):
        out=reimbursement_bridge(eligible_cost_eur=1000,reimbursement_eur=500,reimbursement_day=60,supplier_payment_day=10)
        self.assertEqual(out["required_bridge"],1000)
        self.assertFalse(out["grant_is_upfront_cash"])

    def test_working_capital_null_safe(self):
        self.assertEqual(working_capital_stress(materials_eur=None,labour_eur=1,customer_deposit_eur=0,receivable_days=30,supplier_days=0)["status"],"HOLD_NULL_INPUT")

    def test_contribution_full_cost(self):
        out=contribution_margin(revenue_eur=1000,direct_cost_eur=300,founder_hours=5,founder_hour_cost_eur=40,pickup_rework_cost_eur=50)
        self.assertEqual(out["full_variable_cost_eur"],550)
        self.assertEqual(out["contribution_margin_eur"],450)

    def test_queue(self):
        self.assertEqual(queue_capacity(demand_units_per_week=10,service_hours_per_unit=4,founder_hours_per_week=20)["state"],"OVERLOADED")

if __name__=="__main__": unittest.main(verbosity=2)
