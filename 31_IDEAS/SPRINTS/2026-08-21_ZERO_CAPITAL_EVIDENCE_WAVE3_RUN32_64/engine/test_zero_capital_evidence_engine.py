import unittest

try:
    from engine.zero_capital_evidence_engine import *
except ModuleNotFoundError:
    from zero_capital_evidence_engine import *


class TestWave3(unittest.TestCase):
    def setUp(self):
        self.c = Constraints()
        self.good = Opportunity(5, 5, 5, 5, 4, 5, 4, 2, 2, 3)

    def test_zero_cash_pass(self):
        self.assertTrue(zero_cash_gate(self.good, self.c))

    def test_cash_fail(self):
        with self.assertRaises(GateError):
            zero_cash_gate(Opportunity(5, 5, 5, 5, 4, 5, 4, 2, 2, 3, founder_cash_eur=1), self.c)

    def test_no_outreach(self):
        with self.assertRaises(GateError):
            action_gate("SEND_EMAIL", self.c)

    def test_analysis_allowed(self):
        self.assertTrue(action_gate("ANALYSE", self.c))

    def test_official_source(self):
        with self.assertRaises(GateError):
            official_source_gate(Opportunity(5, 5, 5, 5, 4, 5, 4, 2, 2, 3, official_source=False))

    def test_liability(self):
        with self.assertRaises(GateError):
            liability_gate(Opportunity(5,5,5,5,4,5,4,2,2,3,legal_or_assurance_claim=True))

    def test_public_ceiling(self):
        self.assertEqual(cap_proof("E4", self.c), "E2_PLUS")

    def test_real_buyer_can_be_e3_only_if_observed(self):
        self.assertEqual(cap_proof("E3", self.c, external_buyer_event=True), "E3")

    def test_payment_can_be_e4_only_if_observed(self):
        self.assertEqual(cap_proof("E4", self.c, payment_event=True), "E4")

    def test_score_bounded(self):
        self.assertTrue(0 <= score(self.good) <= 100)


if __name__ == "__main__":
    unittest.main()
