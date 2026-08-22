import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.evidence_acquisition import (  # noqa: E402
    BidderDesignation,
    DocumentRouteEvidence,
    RequirementRow,
    SupplierEvidencePacket,
    acquisition_next_action,
    benchmark_may_satisfy_target,
    bidder_authority_ready,
    bidder_bound_identity,
    bidder_next_action,
    bind_supplier_field,
    bounded_decision,
    content_hash,
    dependency_cut_set,
    fatal_gap_ids,
    indexed_absence_claim,
    join_precondition_state,
    proof_frontier,
    protect_no_change,
    target_authority_ready,
    unknown_ids,
    validate_join_state,
)


class EvidenceAcquisitionCanaries(unittest.TestCase):
    def test_01_route_known_does_not_mean_pack_acquired(self):
        route = DocumentRouteEvidence("8872468", True, False)
        self.assertFalse(route.pack_acquired)
        self.assertEqual(route.state, "DOCUMENT_ROUTE_KNOWN_ATTACHMENT_INVENTORY_NOT_ACQUIRED")

    def test_02_inventory_acquired_is_pack_acquired(self):
        route = DocumentRouteEvidence("8872468", True, True, True)
        self.assertTrue(route.pack_acquired)
        self.assertEqual(route.state, "PACK_ACQUIRED")

    def test_03_unknown_route_is_distinct_state(self):
        self.assertEqual(DocumentRouteEvidence("x", False).state, "DOCUMENT_ROUTE_UNKNOWN")

    def test_04_missing_file_has_no_synthetic_hash(self):
        self.assertIsNone(content_hash(None))

    def test_05_real_bytes_hash_deterministically(self):
        self.assertEqual(content_hash(b"abc"), content_hash(b"abc"))
        self.assertNotEqual(content_hash(b"abc"), content_hash(b"abd"))

    def test_06_index_absence_does_not_prove_nonexistence(self):
        self.assertEqual(indexed_absence_claim(False), "DOCUMENT_EXISTENCE_UNKNOWN")

    def test_07_index_presence_is_only_presence(self):
        self.assertEqual(indexed_absence_claim(True), "INDEX_RESULT_PRESENT")

    def test_08_historical_pack_cannot_satisfy_target(self):
        self.assertFalse(benchmark_may_satisfy_target("8176962", "8872468"))

    def test_09_same_resource_identity_is_not_cross_resource_carryover(self):
        self.assertTrue(benchmark_may_satisfy_target("8872468", "8872468"))

    def test_10_bidder_name_without_provenance_is_not_designated(self):
        self.assertFalse(BidderDesignation("8872468", "SYNTHESIS-IVDIVO LIMITED", None).designated)

    def test_11_explicit_designation_requires_name_and_provenance(self):
        d = BidderDesignation("8872468", "SYNTHESIS-IVDIVO LIMITED", "decision-001")
        self.assertTrue(d.designated)

    def test_12_company_identity_binds_only_on_exact_designated_name(self):
        d = BidderDesignation("8872468", "SYNTHESIS-IVDIVO LIMITED", "decision-001")
        self.assertTrue(bidder_bound_identity(d, "SYNTHESIS-IVDIVO LIMITED"))

    def test_13_different_company_cannot_bind_to_designation(self):
        d = BidderDesignation("8872468", "OTHER LTD", "decision-001")
        self.assertFalse(bidder_bound_identity(d, "SYNTHESIS-IVDIVO LIMITED"))

    def test_14_company_fact_without_designation_stays_unbound(self):
        d = BidderDesignation("8872468")
        self.assertIsNone(bind_supplier_field(d, "SYNTHESIS-IVDIVO LIMITED", "identity-doc"))

    def test_15_designated_company_may_bind_real_evidence(self):
        d = BidderDesignation("8872468", "SYNTHESIS-IVDIVO LIMITED", "decision-001")
        self.assertEqual(bind_supplier_field(d, "SYNTHESIS-IVDIVO LIMITED", "tax-doc"), "tax-doc")

    def test_16_identity_only_packet_is_not_capability_packet(self):
        p = SupplierEvidencePacket("SYNTHESIS-IVDIVO LIMITED", {"identity": "formation-doc"})
        self.assertFalse(p.has_capability_evidence)

    def test_17_capability_packet_needs_real_capability_evidence(self):
        p = SupplierEvidencePacket("SYNTHESIS-IVDIVO LIMITED", {"insurance": "cert-001"})
        self.assertTrue(p.has_capability_evidence)

    def test_18_target_authority_is_independent_gate(self):
        self.assertFalse(target_authority_ready(DocumentRouteEvidence("8872468", True, False)))

    def test_19_bidder_authority_fails_without_designation(self):
        d = BidderDesignation("8872468")
        p = SupplierEvidencePacket("SYNTHESIS-IVDIVO LIMITED", {"insurance": "cert"})
        self.assertFalse(bidder_authority_ready(d, p))

    def test_20_bidder_authority_requires_matching_designated_packet(self):
        d = BidderDesignation("8872468", "SYNTHESIS-IVDIVO LIMITED", "decision")
        p = SupplierEvidencePacket("SYNTHESIS-IVDIVO LIMITED", {"insurance": "cert"})
        self.assertTrue(bidder_authority_ready(d, p))

    def test_21_join_blocks_when_both_sides_missing(self):
        route = DocumentRouteEvidence("8872468", True, False)
        self.assertEqual(join_precondition_state(route, BidderDesignation("8872468"), SupplierEvidencePacket()), "BLOCKED_TARGET_AND_BIDDER_AUTHORITY")

    def test_22_join_blocks_target_even_if_bidder_ready(self):
        route = DocumentRouteEvidence("8872468", True, False)
        d = BidderDesignation("8872468", "BIDDER", "proof")
        p = SupplierEvidencePacket("BIDDER", {"insurance": "cert"})
        self.assertEqual(join_precondition_state(route, d, p), "BLOCKED_TARGET_AUTHORITY")

    def test_23_join_blocks_bidder_even_if_target_ready(self):
        route = DocumentRouteEvidence("8872468", True, True)
        self.assertEqual(join_precondition_state(route, BidderDesignation("8872468"), SupplierEvidencePacket()), "BLOCKED_BIDDER_AUTHORITY")

    def test_24_join_ready_requires_both_authorities(self):
        route = DocumentRouteEvidence("8872468", True, True)
        d = BidderDesignation("8872468", "BIDDER", "proof")
        p = SupplierEvidencePacket("BIDDER", {"insurance": "cert"})
        self.assertEqual(join_precondition_state(route, d, p), "READY_FOR_ATOMIC_JOIN")

    def test_25_join_state_taxonomy_accepts_only_known_states(self):
        self.assertEqual(validate_join_state("CURABLE_BEFORE_DEADLINE"), "CURABLE_BEFORE_DEADLINE")

    def test_26_join_state_taxonomy_rejects_magic_scores(self):
        with self.assertRaises(ValueError):
            validate_join_state("82_PERCENT_MATCH")

    def test_27_fatal_gap_requires_mandatory_noncurable_row(self):
        rows = [RequirementRow("R1", True, "NONCURABLE"), RequirementRow("R2", False, "NONCURABLE")]
        self.assertEqual(fatal_gap_ids(rows), ["R1"])

    def test_28_unknown_queue_preserves_unknown_rows(self):
        rows = [RequirementRow("R1", True, "UNKNOWN"), RequirementRow("R2", True, "MET")]
        self.assertEqual(unknown_ids(rows), ["R1"])

    def test_29_dependency_cut_set_exposes_two_root_blockers(self):
        route = DocumentRouteEvidence("8872468", True, False)
        blockers = dependency_cut_set(route, BidderDesignation("8872468"), SupplierEvidencePacket())
        self.assertEqual(blockers, ["ROOT_A_TARGET_PACK_NOT_ACQUIRED", "ROOT_B_NO_EXPLICIT_BIDDER_DESIGNATION"])

    def test_30_no_loop_router_escalates_known_failed_route(self):
        route = DocumentRouteEvidence("8872468", True, False)
        self.assertEqual(acquisition_next_action(route), "AUTHENTICATED_EXPORT_OR_USER_PROVIDED_OFFICIAL_PACK")
        self.assertEqual(bidder_next_action(BidderDesignation("8872468")), "OBTAIN_EXPLICIT_CASE_SPECIFIC_BIDDER_DESIGNATION")

    def test_31_proof_frontier_cannot_promote_from_engineering(self):
        frontier = proof_frontier()
        self.assertFalse(frontier["pa4"])
        self.assertFalse(frontier["pa5"])
        self.assertFalse(frontier["e3"])
        self.assertFalse(frontier["e4"])
        self.assertIsNone(frontier["price"])

    def test_32_bounded_decision_requires_join_rows_and_pa4_after_candidate(self):
        self.assertEqual(bounded_decision(False, []), "HOLD_PRECONDITIONS_NOT_MET")
        self.assertEqual(bounded_decision(True, [RequirementRow("R1", True, "UNKNOWN")]), "HOLD_UNKNOWN_REQUIREMENTS")
        self.assertEqual(bounded_decision(True, [RequirementRow("R1", True, "NONCURABLE")]), "NO_BID_CANDIDATE_REQUIRES_PA4")
        self.assertEqual(bounded_decision(True, [RequirementRow("R1", True, "MET")]), "BID_CANDIDATE_REQUIRES_PA4")
        self.assertTrue(protect_no_change(DocumentRouteEvidence("8872468", True, False), BidderDesignation("8872468")))


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(EvidenceAcquisitionCanaries)
    if suite.countTestCases() != 32:
        raise SystemExit(f"expected exactly 32 tests, got {suite.countTestCases()}")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
