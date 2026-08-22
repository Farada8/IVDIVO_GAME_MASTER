import unittest
from cycle5_public_artifact_engine import *

class Cycle5Tests(unittest.TestCase):
    def test_01_canonical_url_tracking(self): self.assertEqual(canonical_official_url('https://example.ie/a?utm_source=x&gclid=y'),'https://example.ie/a')
    def test_02_canonical_url_etenders_identity(self): self.assertIn('resourceId=8899923',canonical_official_url('https://www.etenders.gov.ie/epps/cft/prepareViewCfTWS.do?resourceId=8899923&utm_source=x'))
    def test_03_freshness(self): self.assertEqual(signal_freshness('2026-08-21T00:00:00+00:00','2026-08-22T00:00:00+00:00',7)['status'],'FRESH')
    def test_04_stale(self): self.assertEqual(signal_freshness('2026-01-01T00:00:00+00:00','2026-08-22T00:00:00+00:00',30)['status'],'STALE')
    def test_05_syndication_dedupe(self):
        xs=[{'issuer':'A','title':'X','event_date':'2026-08-01','source_authority':'DISCOVERY_ONLY'},{'issuer':'A','title':'X','event_date':'2026-08-01','source_authority':'OFFICIAL_PRIMARY'}]
        self.assertEqual(len(dedupe_syndicated(xs)),1); self.assertEqual(dedupe_syndicated(xs)[0]['source_authority'],'OFFICIAL_PRIMARY')
    def test_06_procurement_open(self): self.assertEqual(procurement_state('2026-09-01T12:00:00+00:00','2026-08-22T00:00:00+00:00','Tender Submission')['state'],'OPEN')
    def test_07_procurement_past_deadline_contradiction(self): self.assertTrue(procurement_state('2026-01-01T12:00:00+00:00','2026-08-22T00:00:00+00:00','Open')['contradiction'])
    def test_08_awarded_precedence(self): self.assertEqual(procurement_state(None,'2026-08-22T00:00:00+00:00','Open','2026-08-20')['state'],'AWARDED')
    def test_09_supersession(self): self.assertEqual(sum(x['weight'] for x in resolve_supersession([{'policy_id':'P','effective_at':'2025-01-01'},{'policy_id':'P','effective_at':'2026-01-01'}])),1)
    def test_10_budget_not_buyer(self): self.assertFalse(budget_owner_gate(1e6,False,False)['buyer_proven'])
    def test_11_buyer_access(self): self.assertEqual(buyer_access_path({'official_procurement_portal':True}),'PUBLIC_PATH_VERIFIED')
    def test_12_nonconsumption(self): self.assertEqual(market_state_classifier(current_consumption=False,underserved=False,overserved=False),'NONCONSUMPTION')
    def test_13_undershot(self): self.assertEqual(market_state_classifier(current_consumption=True,underserved=True,overserved=False),'UNDERSHOT')
    def test_14_motivation_ability(self): self.assertEqual(motivation_ability({'funding':True,'support':True}),{'motivation':'UP','ability':'UP'})
    def test_15_asymmetry(self): self.assertEqual(incumbent_asymmetry(incumbent_margin_attractive=True,new_model_requires_different_process=True,entrant_low_cost=True),'ASYMMETRY_PLAUSIBLE_TEST')
    def test_16_falsifier(self): self.assertEqual(why_now_falsifier('x','y',False)['status'],'KILLED_OR_HOLD')
    def test_17_half_life_policy(self): self.assertEqual(opportunity_half_life('PROCUREMENT_OPEN'),7)
    def test_18_fatal_rank(self): self.assertEqual(rank_fatal_assumptions([{'id':'a','kill_power':1,'uncertainty':1,'testability':1},{'id':'b','kill_power':.5,'uncertainty':1,'testability':1}])[0]['id'],'a')
    def test_19_shared_graph(self): self.assertEqual(shared_assumption_graph([{'opportunity_id':'1','assumptions':['A']},{'opportunity_id':'2','assumptions':['A','B']}])['A'],['1','2'])
    def test_20_no_outreach(self): self.assertEqual(select_no_outreach_experiment([{'id':'a','founder_cash_eur':0,'requires_buyer_contact':False,'decision_value':1,'flip_probability':1,'time_hours':1}])['id'],'a')
    def test_21_artifact_evidence_ceiling(self):
        g=artifact_evidence_gate({'content':'x'}); self.assertEqual(g['evidence_ceiling'],'E2+'); self.assertFalse(g['buyer_proof'])
    def test_22_delivery_human_null(self): self.assertIsNone(delivery_time_record(1.2)['human_review_minutes_observed'])
    def test_23_e3_requires_external_behavior(self): self.assertEqual(e3_capture({'external_buyer':True,'behavioral_signal':True}),'E3'); self.assertEqual(e3_capture({'external_buyer':False,'behavioral_signal':True}),'HOLD_BELOW_E3')
    def test_24_e4_requires_cash_and_binding(self): self.assertEqual(e4_payment_proof({'cash_received':100,'deposit':True}),'E4'); self.assertEqual(e4_payment_proof({'cash_received':0,'purchase_order':True}),'HOLD_BELOW_E4')
    def test_25_price_null(self): self.assertIsNone(pricing_schema(None)['price'])
    def test_26_cash_committed_only(self): self.assertEqual(founder_cash_timeline([{'amount':-100,'committed':True},{'amount':1000,'committed':False}])['committed_net_cash'],-100)
    def test_27_reimbursement_gap(self): self.assertEqual(reimbursement_bridge({'reimbursement_after_spend':True}),'WORKING_CAPITAL_REQUIRED')
    def test_28_topology_hold(self): self.assertEqual(funding_topology(payer=None,funding_source='grant',upfront_cash_required=True)['status'],'HOLD_UNKNOWN_TOPOLOGY')
    def test_29_wc_null(self): self.assertEqual(working_capital_stress(materials=None,labour=1,grant_reimbursement=1,customer_deposit=0)['status'],'HOLD_NULL_INPUT')
    def test_30_margin_null(self): self.assertIsNone(contribution_margin(price=None,variable_cost=1,delivery_hours=1,hourly_time_cost=1)['contribution'])
    def test_31_queue_null(self): self.assertIsNone(service_queue(arrival_per_week=None,service_hours_per_case=1,available_hours_per_week=40)['utilization'])
    def test_32_wip_limit(self): self.assertEqual(wip_gate('OP01',['OP03','OP19'])['status'],'PASS'); self.assertEqual(wip_gate('OP01',['OP03','OP19','OP20'])['status'],'FREEZE_EXCESS')

if __name__=='__main__': unittest.main()
