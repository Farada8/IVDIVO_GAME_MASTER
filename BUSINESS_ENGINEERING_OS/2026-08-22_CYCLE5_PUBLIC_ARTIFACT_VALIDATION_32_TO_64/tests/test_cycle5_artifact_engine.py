import unittest

from engine.cycle5_artifact_engine import (
    validate_public_artifact,
    procurement_fit_vector,
    retrofit_route,
    ai_support_substitution,
    artifact_decision_utility,
    validate_wip,
    self_improvement_disposition,
)


class Cycle5ArtifactEngineTests(unittest.TestCase):
    def test_public_artifact_cannot_prove_wtp(self):
        r = validate_public_artifact({"source_ref": "official", "source_date": "2026-08-22", "decision": "bid/no-bid", "wtp_proven": True})
        self.assertEqual(r.status, "FAIL")
        self.assertIn("PUBLIC_ARTIFACT_CANNOT_PROVE_WTP", r.reasons)

    def test_missing_source_or_date_fails(self):
        r = validate_public_artifact({"decision": "route"})
        self.assertIn("SOURCE_REQUIRED", r.reasons)
        self.assertIn("SOURCE_DATE_REQUIRED", r.reasons)

    def test_valid_public_artifact_passes_at_e2_ceiling(self):
        r = validate_public_artifact({"source_ref": "official", "source_date": "2026-08-22", "decision": "screen"})
        self.assertEqual(r.status, "PASS")
        self.assertEqual(r.evidence_ceiling, "E2+")

    def test_procurement_vector_preserves_nulls(self):
        v = procurement_fit_vector({"sector": "energy", "deadline": "2026-09-14"}, {"sectors": None, "geographies": None})
        self.assertIsNone(v["sector_match"])
        self.assertIn("qualification_known", v["fatal_unknowns"])

    def test_traditional_home_routes_to_specialist(self):
        r = retrofit_route({"construction_year": 1930, "whole_house": True})
        self.assertEqual(r["route"], "TRADITIONAL_HOME_PILOT")
        self.assertEqual(r["required_specialist"], "Traditional Building Professional")

    def test_oss_cash_timing(self):
        self.assertEqual(retrofit_route({"construction_year": 1980, "whole_house": True})["cash_timing"], "OSS_GRANT_DEDUCTED_UPFRONT")

    def test_individual_grant_cash_timing(self):
        self.assertEqual(retrofit_route({"construction_year": 1980, "whole_house": False})["cash_timing"], "GRANT_AFTER_COMPLETED_WORKS")

    def test_generic_ai_diagnostic_flags_public_substitution(self):
        r = ai_support_substitution({"offer_type": "GENERIC_DIGITAL_DIAGNOSTIC", "leo_eligible": True, "digital_for_business_completed": False})
        self.assertEqual(r["public_substitute_risk"], "HIGH")
        self.assertEqual(r["recommended_positioning"], "SECTOR_WORKFLOW_EVIDENCE_AND_IMPLEMENTATION_BACKLOG")

    def test_decision_utility_requires_before_after(self):
        self.assertIsNone(artifact_decision_utility(None, "x")["useful"])

    def test_decision_utility_detects_change(self):
        self.assertTrue(artifact_decision_utility("maybe", "no-bid")["useful"])

    def test_wip_limit(self):
        self.assertEqual(validate_wip([{"role": "PRIMARY"}, {"role": "PILOT"}, {"role": "PILOT"}]).status, "PASS")

    def test_wip_over_limit_fails(self):
        self.assertEqual(validate_wip([{"role": "PRIMARY"}, {"role": "PILOT"}, {"role": "PILOT"}, {"role": "PILOT"}]).status, "FAIL")

    def test_self_improvement_no_auto_promotion(self):
        self.assertEqual(self_improvement_disposition({"auto_promote": True, "evidence": ["x"]})["status"], "REJECT")

    def test_self_improvement_candidate_with_evidence(self):
        self.assertEqual(self_improvement_disposition({"auto_promote": False, "evidence": ["artifact failure"]})["status"], "CANDIDATE")


if __name__ == "__main__":
    unittest.main()
