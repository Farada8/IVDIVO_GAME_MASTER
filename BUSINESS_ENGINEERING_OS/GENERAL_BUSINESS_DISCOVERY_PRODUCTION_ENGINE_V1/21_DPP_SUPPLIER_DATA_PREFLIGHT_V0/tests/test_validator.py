import json
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from validator import compare_correction, validate_record

FIXTURE_PATH = ROOT / "02_SYNTHETIC_FIXTURE_AND_CORRECTION.json"

def fixture():
    return json.loads(FIXTURE_PATH.read_text())

class DppPreflightTests(unittest.TestCase):
    def test_correction_loop_passes_engineering_gate(self):
        r = compare_correction(fixture())
        self.assertTrue(r["engineering_pass"])
        self.assertGreaterEqual(r["closed_count"], 2)
    def test_expected_supplier_gaps_close(self):
        closed = set(compare_correction(fixture())["closed_missing_data_gaps"])
        self.assertEqual(closed, {"dimensions_mm", "compliance_document_refs", "material_composition"})
    def test_legal_scope_unknown_blocks_registry_ready_promotion(self):
        r = compare_correction(fixture())
        self.assertEqual(r["corrected"]["disposition"], "TECHNICAL_PREFLIGHT_COMPLETE_LEGAL_SCOPE_UNKNOWN")
        self.assertFalse(r["corrected"]["proof_boundary"]["legal_dpp_applicability_proven"])
    def test_missing_candidate_legal_identifiers_are_not_called_noncompliance(self):
        f = {x["field"]: x for x in compare_correction(fixture())["corrected"]["findings"]}
        self.assertEqual(f["gtin_or_equivalent"]["outcome"], "HOLD")
        self.assertEqual(f["gtin_or_equivalent"]["requiredness_state"], "LEGAL_REQUIREDNESS_UNKNOWN")
    def test_in_scope_still_fails_closed_when_requiredness_unresolved(self):
        r = validate_record(fixture()["corrected"], "IN_SCOPE_VERIFIED")
        self.assertEqual(r["disposition"], "IN_SCOPE_PRODUCT_RULE_REQUIREDNESS_UNRESOLVED")
        self.assertGreater(r["counts"]["HOLD"], 0)
    def test_registry_does_not_embed_full_dpp_payload(self):
        f = {x["field"]: x for x in compare_correction(fixture())["corrected"]["findings"]}
        self.assertEqual(f["registry_metadata.full_dpp_payload"]["outcome"], "PASS")
    def test_overpacked_registry_is_error(self):
        x = fixture(); x["corrected"]["registry_metadata"]["full_dpp_payload"] = {"all": "product data"}
        self.assertEqual(validate_record(x["corrected"], "UNKNOWN")["disposition"], "INVALID_PREFLIGHT")
    def test_populated_field_without_source_is_error(self):
        x = fixture(); x["corrected"]["candidate_fields"]["dimensions_mm"]["source_ref"] = None
        self.assertEqual(validate_record(x["corrected"], "UNKNOWN")["disposition"], "INVALID_PREFLIGHT")
    def test_unknown_source_reference_is_error(self):
        x = fixture(); x["corrected"]["candidate_fields"]["dimensions_mm"]["source_ref"] = "DOES-NOT-EXIST"
        self.assertEqual(validate_record(x["corrected"], "UNKNOWN")["disposition"], "INVALID_PREFLIGHT")
    def test_registry_identifier_mismatch_is_error(self):
        x = fixture(); x["corrected"]["registry_metadata"]["unique_product_identifier"] = "OTHER"
        self.assertEqual(validate_record(x["corrected"], "UNKNOWN")["disposition"], "INVALID_PREFLIGHT")
    def test_out_of_scope_verified_stays_data_map_only(self):
        self.assertEqual(validate_record(fixture()["corrected"], "OUT_OF_SCOPE_VERIFIED")["disposition"], "TECHNICAL_DATA_MAP_ONLY_OUT_OF_SCOPE_VERIFIED")
    def test_missing_core_identifier_is_gap(self):
        x = fixture(); x["corrected"]["candidate_fields"]["unique_product_identifier"]["value"] = None; x["corrected"]["registry_metadata"]["unique_product_identifier"] = None
        self.assertIn("unique_product_identifier", validate_record(x["corrected"], "UNKNOWN")["missing_supplier_data"])
    def test_correction_does_not_prove_market_or_registry_acceptance(self):
        r = compare_correction(fixture())
        self.assertFalse(r["proof_boundary"]["correction_loop_is_legal_compliance_proof"])
        self.assertFalse(r["proof_boundary"]["correction_loop_is_registry_acceptance_proof"])
        self.assertFalse(r["corrected"]["proof_boundary"]["buyer_demand_proven"])
        self.assertFalse(r["corrected"]["proof_boundary"]["wtp_proven"])

if __name__ == "__main__":
    unittest.main()
