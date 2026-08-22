import unittest
from zero_capital_opportunity_engine import (
    EvidenceGrade, OpportunityCandidate, zero_cash_gate, next_action, score
)

class ZeroCapitalEngineTests(unittest.TestCase):
    def test_manual_tender_intelligence_passes_strict_zero_cash(self):
        c = OpportunityCandidate(
            name="Tender intelligence",
            cashless_start=5, buyer_before_build=5, speed_to_first_revenue=5,
            demand_signal=5, repeatability=5, financing_ladder=4,
            gross_margin_potential=5, evidence_grade=EvidenceGrade.E1_AUTHORITATIVE_SIGNAL,
        )
        self.assertTrue(zero_cash_gate(c))
        self.assertGreaterEqual(score(c), 90)
        self.assertEqual(next_action(c), "RUN_ZERO_COST_BUYER_DISCOVERY")

    def test_prefab_flip_fails_when_founder_cash_required(self):
        c = OpportunityCandidate(
            name="Prefab flip",
            cashless_start=1, buyer_before_build=1, speed_to_first_revenue=1,
            demand_signal=3, repeatability=2, financing_ladder=3,
            gross_margin_potential=3, founder_cash_pre_proof_eur=15000,
            irreversible_commitment_pre_payment=True,
        )
        self.assertFalse(zero_cash_gate(c))
        self.assertEqual(next_action(c), "RESTRUCTURE_OR_KILL_PRE_PROOF_CASH_REQUIREMENT")

    def test_reimbursement_grant_without_bridge_is_not_zero_cash(self):
        c = OpportunityCandidate(
            name="Reimbursement-only grant project",
            cashless_start=2, buyer_before_build=2, speed_to_first_revenue=2,
            demand_signal=4, repeatability=2, financing_ladder=4,
            gross_margin_potential=3, founder_cash_pre_proof_eur=5000,
            irreversible_commitment_pre_payment=True,
        )
        self.assertFalse(zero_cash_gate(c))

    def test_paid_pilot_routes_to_delivery(self):
        c = OpportunityCandidate(
            name="AI quote pilot",
            cashless_start=5, buyer_before_build=5, speed_to_first_revenue=5,
            demand_signal=5, repeatability=5, financing_ladder=5,
            gross_margin_potential=5, evidence_grade=EvidenceGrade.E4_PAID_PILOT_DEPOSIT_OR_PO,
        )
        self.assertEqual(next_action(c), "DELIVER_MANUALLY_AND_CAPTURE_UNIT_ECONOMICS")

if __name__ == '__main__':
    unittest.main()
