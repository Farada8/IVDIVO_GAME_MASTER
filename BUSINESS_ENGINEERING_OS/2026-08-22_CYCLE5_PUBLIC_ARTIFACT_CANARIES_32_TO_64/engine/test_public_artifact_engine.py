import unittest

from public_artifact_engine import (
    compile_public_artifact,
    evidence_ceiling_guard,
    price_hypothesis,
    register_library_discovery,
    route_market_experiment,
    self_improvement_candidate,
    validate_buyer_interaction_receipt,
    validate_money_receipt,
    wip_guard,
)


def opportunity(**overrides):
    row = {
        "opportunity_id": "OP01",
        "name": "Tender intelligence + bid/no-bid briefs",
        "buyer_segment": "construction SMEs",
        "buyer_workload": "monitor tenders and decide bid/no-bid",
        "offer": "weekly curated opportunity brief + bid/no-bid memo",
        "evidence_grade": "E2+",
        "willingness_to_pay": None,
        "paid_amount_eur": None,
        "buyer_commitment": None,
        "repeat_purchase": None,
        "unit_economics": None,
        "gross_margin": None,
        "conversion_rate": None,
        "procurement_eligibility": None,
        "legal_clearance": None,
    }
    row.update(overrides)
    return row


def artifact():
    return compile_public_artifact(
        opportunity(),
        artifact_template_id="TENDER_DECISION_BRIEF_v1",
        public_sources=[
            {"source_ref": "https://example.test/tender/1", "observed_at": "2026-08-22", "authority": "OFFICIAL_PRIMARY"}
        ],
        decision_checks=["lot fit", "qualification", "deadline"],
        missing_data=["contractor capacity"],
        target_candidate="Example Contractor Ltd",
    )


class LibraryBoundaryTests(unittest.TestCase):
    def test_file_library_reference_is_not_raw_durable(self):
        row = register_library_discovery(title="IHRM", file_library_ref="file_123")
        self.assertEqual(row["status"], "FILE_LIBRARY_REFERENCE_ONLY")
        self.assertFalse(row["raw_copyright_binary_public_git_allowed"])

    def test_drive_id_without_hash_is_not_raw_durable(self):
        row = register_library_discovery(title="IHRM", file_library_ref="file_123", raw_drive_id="drive_1")
        self.assertEqual(row["status"], "FILE_LIBRARY_REFERENCE_ONLY")

    def test_drive_and_byte_hash_is_raw_durable(self):
        row = register_library_discovery(title="IHRM", file_library_ref="file_123", raw_drive_id="drive_1", byte_hash="a" * 64)
        self.assertEqual(row["status"], "RAW_DURABLE")
        self.assertFalse(row["raw_copyright_binary_public_git_allowed"])


class EvidenceCeilingTests(unittest.TestCase):
    def test_valid_public_record_passes(self):
        self.assertEqual(evidence_ceiling_guard(opportunity())["status"], "PASS")

    def test_public_wtp_claim_fails(self):
        out = evidence_ceiling_guard(opportunity(willingness_to_pay=250))
        self.assertEqual(out["status"], "FAIL")
        self.assertIn("PUBLIC_SOURCE_CANNOT_PROVE:willingness_to_pay", out["violations"])

    def test_e3_record_fails_public_compiler(self):
        out = compile_public_artifact(
            opportunity(evidence_grade="E3"),
            artifact_template_id="X",
            public_sources=[{"source_ref": "s", "observed_at": "2026-08-22"}],
            decision_checks=[],
            missing_data=[],
        )
        self.assertEqual(out["status"], "FAIL_EVIDENCE_CEILING")


class PublicArtifactTests(unittest.TestCase):
    def test_valid_e2plus_compiles(self):
        out = artifact()
        self.assertEqual(out["status"], "PUBLIC_SAMPLE_READY")
        self.assertFalse(out["market_proof_claimed"])
        self.assertFalse(out["dispatch_allowed"])
        self.assertIsNone(out["willingness_to_pay"])

    def test_missing_source_ref_raises(self):
        with self.assertRaises(ValueError):
            compile_public_artifact(
                opportunity(), artifact_template_id="X",
                public_sources=[{"observed_at": "2026-08-22"}],
                decision_checks=[], missing_data=[]
            )

    def test_missing_source_date_raises(self):
        with self.assertRaises(ValueError):
            compile_public_artifact(
                opportunity(), artifact_template_id="X",
                public_sources=[{"source_ref": "s"}],
                decision_checks=[], missing_data=[]
            )

    def test_artifact_hash_is_deterministic(self):
        self.assertEqual(artifact()["artifact_hash"], artifact()["artifact_hash"])


class BuyerReceiptTests(unittest.TestCase):
    def test_absent_buyer_receipt_holds(self):
        self.assertEqual(validate_buyer_interaction_receipt(None, artifact_hash=artifact()["artifact_hash"])["status"], "HOLD_NO_REAL_BUYER_INTERACTION")

    def test_synthetic_buyer_receipt_fails(self):
        a = artifact()
        receipt = {"kind":"BUYER_INTERACTION","source_type":"SYNTHETIC","artifact_hash":a["artifact_hash"],"observed_at":"2026-08-22","buyer_role":"MD","interaction_outcome":"positive"}
        self.assertEqual(validate_buyer_interaction_receipt(receipt, artifact_hash=a["artifact_hash"])["status"], "FAIL_SYNTHETIC_OR_WRONG_CLASS")

    def test_wrong_buyer_artifact_lineage_fails(self):
        a = artifact()
        receipt = {"kind":"BUYER_INTERACTION","source_type":"REAL_HUMAN","artifact_hash":"wrong","observed_at":"2026-08-22","buyer_role":"MD","interaction_outcome":"positive"}
        self.assertEqual(validate_buyer_interaction_receipt(receipt, artifact_hash=a["artifact_hash"])["status"], "FAIL_ARTIFACT_LINEAGE")

    def test_real_buyer_receipt_promotes_only_to_e3(self):
        a = artifact()
        receipt = {"kind":"BUYER_INTERACTION","source_type":"REAL_HUMAN","artifact_hash":a["artifact_hash"],"observed_at":"2026-08-22","buyer_role":"MD","interaction_outcome":"would_review_paid_pilot"}
        out = validate_buyer_interaction_receipt(receipt, artifact_hash=a["artifact_hash"])
        self.assertEqual(out["status"], "PASS_E3_OBSERVED")
        self.assertEqual(out["evidence_grade"], "E3")


class MoneyReceiptTests(unittest.TestCase):
    def test_absent_money_holds(self):
        self.assertEqual(validate_money_receipt(None, artifact_hash=artifact()["artifact_hash"])["status"], "HOLD_NO_REAL_MONEY_OR_PO")

    def test_synthetic_money_fails(self):
        a = artifact()
        receipt = {"kind":"PAYMENT","source_type":"SYNTHETIC","artifact_hash":a["artifact_hash"],"observed_at":"2026-08-22","transaction_or_po_id":"x","amount_eur":100}
        self.assertEqual(validate_money_receipt(receipt, artifact_hash=a["artifact_hash"])["status"], "FAIL_SYNTHETIC_OR_WRONG_CLASS")

    def test_wrong_money_artifact_lineage_fails(self):
        a = artifact()
        receipt = {"kind":"PAYMENT","source_type":"REAL_TRANSACTION","artifact_hash":"wrong","observed_at":"2026-08-22","transaction_or_po_id":"x","amount_eur":100}
        self.assertEqual(validate_money_receipt(receipt, artifact_hash=a["artifact_hash"])["status"], "FAIL_ARTIFACT_LINEAGE")

    def test_nonpositive_money_fails(self):
        a = artifact()
        receipt = {"kind":"PAYMENT","source_type":"REAL_TRANSACTION","artifact_hash":a["artifact_hash"],"observed_at":"2026-08-22","transaction_or_po_id":"x","amount_eur":0}
        self.assertEqual(validate_money_receipt(receipt, artifact_hash=a["artifact_hash"])["status"], "FAIL_NONPOSITIVE_AMOUNT")

    def test_real_payment_promotes_to_e4(self):
        a = artifact()
        receipt = {"kind":"PAYMENT","source_type":"REAL_TRANSACTION","artifact_hash":a["artifact_hash"],"observed_at":"2026-08-22","transaction_or_po_id":"txn-1","amount_eur":100}
        out = validate_money_receipt(receipt, artifact_hash=a["artifact_hash"])
        self.assertEqual(out["status"], "PASS_E4_MONEY_OBSERVED")
        self.assertEqual(out["evidence_grade"], "E4")


class RouterAndPortfolioTests(unittest.TestCase):
    def test_router_stops_at_buyer_gate_without_receipt(self):
        out = route_market_experiment(artifact())
        self.assertEqual(out["status"], "BUYER_REVIEW_REQUIRED")
        self.assertFalse(out["send_allowed"])

    def test_router_reaches_e3_only_with_real_buyer_receipt(self):
        a = artifact()
        buyer = {"kind":"BUYER_INTERACTION","source_type":"REAL_HUMAN","artifact_hash":a["artifact_hash"],"observed_at":"2026-08-22","buyer_role":"MD","interaction_outcome":"positive"}
        out = route_market_experiment(a, buyer_receipt=buyer)
        self.assertEqual(out["status"], "E3_OBSERVED_MONEY_REQUIRED")
        self.assertEqual(out["current_evidence_grade"], "E3")
        self.assertFalse(out["send_allowed"])

    def test_router_reaches_e4_only_with_real_buyer_and_money(self):
        a = artifact()
        buyer = {"kind":"BUYER_INTERACTION","source_type":"REAL_HUMAN","artifact_hash":a["artifact_hash"],"observed_at":"2026-08-22","buyer_role":"MD","interaction_outcome":"positive"}
        money = {"kind":"PURCHASE_ORDER","source_type":"REAL_TRANSACTION","artifact_hash":a["artifact_hash"],"observed_at":"2026-08-22","transaction_or_po_id":"po-1","amount_eur":200}
        out = route_market_experiment(a, buyer_receipt=buyer, money_receipt=money)
        self.assertEqual(out["status"], "E4_OBSERVED")
        self.assertFalse(out["send_allowed"])

    def test_wip_max_three(self):
        self.assertEqual(wip_guard("OP01", ["OP03", "OP19"])["status"], "PASS")
        self.assertEqual(wip_guard("OP01", ["OP03", "OP19", "OP20"])["status"], "FAIL")

    def test_duplicate_wip_fails(self):
        self.assertEqual(wip_guard("OP01", ["OP01"])["status"], "FAIL")


class HypothesisAndLearningTests(unittest.TestCase):
    def test_price_range_is_never_validated_by_construction(self):
        row = price_hypothesis(75, 250)
        self.assertFalse(row["validated"])
        self.assertEqual(row["evidence_grade"], "HYPOTHESIS_ONLY")

    def test_invalid_price_range_raises(self):
        with self.assertRaises(ValueError):
            price_hypothesis(300, 100)

    def test_learning_candidate_requires_evidence_and_never_auto_promotes(self):
        row = self_improvement_candidate(defect="x", root_cause="y", repair="z", retest_result="PASS", evidence_hashes=["a"])
        self.assertEqual(row["authority"], "CANDIDATE_ONLY")
        self.assertFalse(row["auto_promote"])
        with self.assertRaises(ValueError):
            self_improvement_candidate(defect="x", root_cause="", repair="z", retest_result="PASS", evidence_hashes=[])


if __name__ == "__main__":
    unittest.main(verbosity=2)
