import unittest

from tools.ivdivo_book_intelligence import (
    audit_library,
    build_adapter_packet,
    build_mechanism_card,
    can_redistribute_source,
    dedupe_mechanism_cards,
    mechanism_semantic_key,
    promotion_decision,
    route_book_use,
    validate_source_passport,
)


def passport(source_id, group, stage="MECHANISMS_EXTRACTED", rights="USER_PROVIDED", targets=None):
    return {
        "source_id": source_id,
        "title": source_id,
        "provenance": "fixture",
        "rights_status": rights,
        "lifecycle_stage": stage,
        "content_locator": f"fixture:{source_id}",
        "independent_source_group": group,
        "domain_targets": targets or ["GENERAL"],
    }


class BookIntelligenceTests(unittest.TestCase):
    def test_passport_requires_independent_group(self):
        p = passport("S1", "G1")
        p.pop("independent_source_group")
        self.assertIn("missing:independent_source_group", validate_source_passport(p))

    def test_open_source_may_be_redistributable(self):
        self.assertTrue(can_redistribute_source(passport("O", "OG", rights="OPEN_LICENSE")))

    def test_user_provided_not_redistributable_by_default(self):
        self.assertFalse(can_redistribute_source(passport("U", "UG", rights="USER_PROVIDED")))

    def test_semantic_key_stable_for_spacing_and_case(self):
        self.assertEqual(
            mechanism_semantic_key("Repair  the earliest layer."),
            mechanism_semantic_key("repair the earliest layer"),
        )

    def test_originality_gate_holds_unstripped_mechanism(self):
        p = passport("S1", "G1")
        c = build_mechanism_card(
            mechanism_id="M1",
            statement="Repair the earliest failed layer before descendants.",
            source_ids=["S1"],
            failure_modes=["local optimization"],
            domain_targets=["SELF_IMPROVEMENT"],
            evidence_locators=["S1:1"],
        )
        self.assertEqual(promotion_decision(c, {"S1": p})["disposition"], "HOLD")

    def test_two_independent_sources_without_project_evidence_is_local_test(self):
        p1, p2 = passport("S1", "G1"), passport("S2", "G2")
        c = build_mechanism_card(
            mechanism_id="M1",
            statement="Repair the earliest failed layer before descendants.",
            source_ids=["S1", "S2"],
            failure_modes=["local optimization"],
            domain_targets=["SELF_IMPROVEMENT"],
            evidence_locators=["S1:1", "S2:1"],
        )
        c["project_specific_expression_removed"] = True
        self.assertEqual(promotion_decision(c, {"S1": p1, "S2": p2})["disposition"], "LOCAL_TEST")

    def test_one_project_pass_is_pilot_ready(self):
        p1 = passport("S1", "G1")
        c = build_mechanism_card(
            mechanism_id="M1",
            statement="Keep verification separate from validation.",
            source_ids=["S1"],
            failure_modes=["unit tests mistaken for real outcome"],
            domain_targets=["GENERAL"],
            evidence_locators=["S1:2"],
        )
        c["project_specific_expression_removed"] = True
        c["pilot_evidence"] = [{"project_id": "P1", "status": "PASS", "measurable_gain": True}]
        self.assertEqual(promotion_decision(c, {"S1": p1})["disposition"], "PILOT_READY")

    def test_two_project_passes_can_be_promotable(self):
        p1 = passport("S1", "G1")
        c = build_mechanism_card(
            mechanism_id="M1",
            statement="Keep verification separate from validation.",
            source_ids=["S1"],
            failure_modes=["unit tests mistaken for real outcome"],
            domain_targets=["GENERAL"],
            evidence_locators=["S1:2"],
        )
        c["project_specific_expression_removed"] = True
        c["pilot_evidence"] = [
            {"project_id": "P1", "status": "PASS", "measurable_gain": True},
            {"project_id": "P2", "status": "PASS", "measurable_gain": True},
        ]
        self.assertEqual(promotion_decision(c, {"S1": p1})["disposition"], "PROMOTABLE")

    def test_major_regression_rejects(self):
        p1 = passport("S1", "G1")
        c = build_mechanism_card(
            mechanism_id="M1",
            statement="Use bounded mechanism selection.",
            source_ids=["S1"],
            failure_modes=["undercoverage"],
            domain_targets=["GENERAL"],
            evidence_locators=["S1:3"],
        )
        c["project_specific_expression_removed"] = True
        c["pilot_evidence"] = [{"project_id": "P1", "status": "REGRESSION", "severity": "MAJOR"}]
        self.assertEqual(promotion_decision(c, {"S1": p1})["disposition"], "REJECT")

    def test_duplicate_does_not_add_evidence_weight(self):
        c = {
            "mechanism_id": "M1",
            "statement": "Same mechanism",
            "semantic_key": mechanism_semantic_key("Same mechanism"),
        }
        d = dedupe_mechanism_cards([c, dict(c, mechanism_id="M2")])
        self.assertEqual(len(d["unique"]), 1)
        self.assertEqual(d["duplicate_clusters"][0]["evidence_weight_added_by_duplication"], 0)

    def test_route_prefers_domain_target(self):
        p_story = passport("S1", "G1", stage="STRUCTURE_MAPPED", targets=["STORY"])
        p_general = passport("S2", "G2", stage="STRUCTURE_MAPPED", targets=["GENERAL"])
        r = route_book_use(domain="STORY", task="repair scene", source_passports=[p_general, p_story])
        self.assertEqual(r["selected_source_ids"][0], "S1")

    def test_adapter_omits_held_mechanism(self):
        p1 = passport("S1", "G1")
        c = build_mechanism_card(
            mechanism_id="M1",
            statement="A mechanism still contains source-specific expression.",
            source_ids=["S1"],
            failure_modes=[],
            domain_targets=["STORY"],
            evidence_locators=["S1:4"],
        )
        pkt = build_adapter_packet(
            domain="STORY",
            task="scene",
            mechanism_cards=[c],
            source_passports={"S1": p1},
        )
        self.assertEqual(pkt["mechanisms"], [])

    def test_library_audit_counts_invalid(self):
        p1 = passport("S1", "G1")
        p2 = passport("S2", "G2")
        p2["rights_status"] = "NOPE"
        out = audit_library([p1, p2])
        self.assertEqual(out["valid"], 1)
        self.assertEqual(len(out["invalid"]), 1)


if __name__ == "__main__":
    unittest.main()
