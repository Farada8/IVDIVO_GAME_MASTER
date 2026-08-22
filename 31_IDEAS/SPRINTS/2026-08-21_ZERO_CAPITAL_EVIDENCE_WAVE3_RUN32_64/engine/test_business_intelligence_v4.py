import unittest

try:
    from engine.business_intelligence_v4 import *
except ModuleNotFoundError:
    from business_intelligence_v4 import *


class TestBusinessIntelligenceV4(unittest.TestCase):
    def make_thesis(self):
        return OpportunityThesis(
            what_changed="A dated regulatory or capital-flow event changed the operating environment.",
            why_now="The affected actor has a current implementation deadline or economic trigger.",
            affected_actor="EU SME manufacturer",
            trigger="effective requirement",
            payer="operations/compliance budget owner",
            falsifier="official postponement or evidence that the work is fully automated/free",
            zero_cash_deliverable=True,
            liability_boundary_ok=True,
            components={
                "signal_strength": 0.9,
                "source_quality": 1.0,
                "urgency": 0.9,
                "buyer_specificity": 0.7,
                "zero_cash_deliverability": 1.0,
                "competition_pressure": 0.4,
                "liability": 0.3,
                "channel_leverage": 0.7,
                "repeatability": 0.8,
            },
        )

    def test_signal_provenance(self):
        s = Signal("official-source", "2026-08-21", "2026-09-01", "REGULATION", "SME", 0.95)
        self.assertTrue(signal_provenance_gate(s))

    def test_bad_confidence_fails(self):
        with self.assertRaises(BusinessIntelligenceGateError):
            signal_provenance_gate(Signal("source", "2026-08-21", None, "X", "Y", 1.2))

    def test_why_now_complete(self):
        self.assertTrue(why_now_gate(self.make_thesis()))

    def test_zero_cash_required(self):
        t = self.make_thesis()
        bad = OpportunityThesis(t.what_changed,t.why_now,t.affected_actor,t.trigger,t.payer,t.falsifier,False,True,t.components)
        with self.assertRaises(BusinessIntelligenceGateError):
            why_now_gate(bad)

    def test_decomposed_score(self):
        out = decomposed_score(self.make_thesis())
        self.assertEqual(out["authority"], "ROUTING_ONLY_E2_PLUS_CEILING")
        self.assertTrue(0 <= out["score"] <= 100)
        self.assertEqual(set(out["components"]), set(REQUIRED_COMPONENTS))

    def test_missing_component_fails(self):
        t = self.make_thesis()
        c = dict(t.components)
        c.pop("urgency")
        bad = OpportunityThesis(t.what_changed,t.why_now,t.affected_actor,t.trigger,t.payer,t.falsifier,True,True,c)
        with self.assertRaises(BusinessIntelligenceGateError):
            decomposed_score(bad)

    def test_public_proof_ceiling(self):
        self.assertEqual(public_evidence_ceiling("E4"), "E2_PLUS")
        self.assertEqual(public_evidence_ceiling("E2"), "E2")

    def test_decision_lineage(self):
        d = decision_lineage(["source:a"], "signal is current", "market may be commoditized", "KEEP_RESEARCH", "next public evidence changes score")
        self.assertIsNone(d["actual_consequence"])
        self.assertEqual(d["decision"], "KEEP_RESEARCH")


if __name__ == "__main__":
    unittest.main()
