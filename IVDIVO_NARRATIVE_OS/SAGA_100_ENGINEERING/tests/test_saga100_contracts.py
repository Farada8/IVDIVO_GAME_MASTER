import unittest

from IVDIVO_NARRATIVE_OS.SAGA_100_ENGINEERING.engine.saga100_contracts import (
    book_independence_gate,
    capability_transition_gate,
    continuity_substitution_gate,
    crossing_eligibility_gate,
    no_repeat_gate,
    resolve_authority,
    reveal_budget_gate,
    strategic_freshness_gate,
)


class Saga100ContractTests(unittest.TestCase):
    def test_r25_authority_same_rank_conflict_holds(self):
        result = resolve_authority([
            {"authority_class":"CURRENT_NARRATIVE_OS","ref":"B04-overlay","value":"B04_FIRST_CROSSING"},
            {"authority_class":"CURRENT_NARRATIVE_OS","ref":"other-current","value":"B04_OTHER_ROLE"},
        ])
        self.assertEqual(result.status, "HOLD")
        self.assertIn("SAME_RANK_AUTHORITY_CONFLICT", result.reasons)

    def test_r25_higher_authority_wins(self):
        result = resolve_authority([
            {"authority_class":"HISTORICAL_SEED","ref":"old","value":"SECOND_CROSSING"},
            {"authority_class":"FOUNDER_NEWEST_DIRECT_INSTRUCTION","ref":"override","value":"FIRST_CROSSING"},
        ])
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.data["winner"]["value"], "FIRST_CROSSING")

    def test_r26_outcome_critical_unknown_holds(self):
        result = continuity_substitution_gate(
            ["hero_identity","relationship_R1","habitat"],
            {"hero_identity":"UNKNOWN","relationship_R1":"KNOWN","habitat":"KNOWN"},
            outcome_critical=["hero_identity"],
        )
        self.assertEqual(result.status, "HOLD")

    def test_r27_capability_skip_fails(self):
        result = capability_transition_gate(
            "KNOWN", "LEGALIZED_USE", ["BOOK-X"], ["CONSEQ-X"]
        )
        self.assertEqual(result.status, "FAIL")
        self.assertIn("UNPROVEN_CAPABILITY_STAGE_SKIP", result.reasons)

    def test_r27_single_step_with_evidence_passes(self):
        result = capability_transition_gate(
            "KNOWN", "CONTACT_ACCESS", ["BOOK-X:scene-proof"], ["C-001"]
        )
        self.assertEqual(result.status, "PASS")

    def test_r28_fan_service_crossing_fails(self):
        result = crossing_eligibility_gate({
            "prerequisite_line_closure": True,
            "upstream_consequences_loaded": True,
            "irreducible_line_dependencies": 1,
            "rights_or_jurisdiction_conflict": False,
            "advanced_actor_auto_commands": True,
            "shared_civilization_delta": False,
        })
        self.assertEqual(result.status, "FAIL")
        self.assertGreaterEqual(len(result.reasons), 3)

    def test_r28_b08_style_bounded_crossing_can_pass(self):
        result = crossing_eligibility_gate({
            "prerequisite_line_closure": True,
            "upstream_consequences_loaded": True,
            "irreducible_line_dependencies": 3,
            "rights_or_jurisdiction_conflict": True,
            "advanced_actor_auto_commands": False,
            "shared_civilization_delta": True,
        })
        self.assertEqual(result.status, "PASS")

    def test_r29_unfinished_book_fails(self):
        book = {field: "x" for field in (
            "hero","want","why_now","opposition","wrong_strategy","price",
            "midpoint","climax_choice","resolution","change"
        )}
        book["main_conflict_closed"] = False
        book["series_hook_before_resolution"] = True
        result = book_independence_gate(book)
        self.assertEqual(result.status, "FAIL")

    def test_r29_complete_book_passes(self):
        book = {field: "x" for field in (
            "hero","want","why_now","opposition","wrong_strategy","price",
            "midpoint","climax_choice","resolution","change"
        )}
        book["main_conflict_closed"] = True
        book["series_hook_before_resolution"] = False
        self.assertEqual(book_independence_gate(book).status, "PASS")

    def test_r30_repetition_under_four_axes_fails(self):
        prior = {
            "primary_human_problem":"consent", "protagonist_social_position":"cadet",
            "arena":["training"], "genre_emphasis":["mystery"],
            "ivdivo_amplifier":["embodiment"], "closure_type":"hearing",
            "relationship_configuration":["mentor"]
        }
        candidate = dict(prior)
        candidate["arena"] = ["evacuation"]
        candidate["closure_type"] = "physical_climax"
        result = no_repeat_gate(candidate, prior)
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(result.data["count"], 2)

    def test_r30_four_or_more_axes_passes(self):
        prior = {
            "primary_human_problem":"consent", "protagonist_social_position":"cadet",
            "arena":["training"], "genre_emphasis":["mystery"],
            "ivdivo_amplifier":["embodiment"], "closure_type":"hearing",
            "relationship_configuration":["mentor"]
        }
        candidate = {
            "primary_human_problem":"standing", "protagonist_social_position":"operator",
            "arena":["evacuation"], "genre_emphasis":["procedural","action"],
            "ivdivo_amplifier":["distributed_civic_life"], "closure_type":"physical_climax",
            "relationship_configuration":["rival_romance","team"]
        }
        self.assertEqual(no_repeat_gate(candidate, prior).status, "PASS")

    def test_r31_future_reveal_spent_early_fails(self):
        result = reveal_budget_gate([
            {"id":"R-A","level":2,"requires_future_founder_lock":False,"spent_now":True},
            {"id":"R-B","level":5,"requires_future_founder_lock":True,"spent_now":True},
        ], allowed_ceiling=3)
        self.assertEqual(result.status, "FAIL")

    def test_r32_reproduces_narr009_omission(self):
        result = strategic_freshness_gate(
            ["LONG_HORIZON_SAGA","SAGA_SEQUENCE"],
            ["CURRENT_EXECUTION_AUTHORITY"],
        )
        self.assertEqual(result.status, "FAIL")
        self.assertIn("LONG_HORIZON_STRATEGIC_AUTHORITY", result.data["missing_layers"])

    def test_r32_current_plus_strategic_passes(self):
        result = strategic_freshness_gate(
            ["LONG_HORIZON_SAGA","SAGA_SEQUENCE"],
            ["CURRENT_EXECUTION_AUTHORITY","LONG_HORIZON_STRATEGIC_AUTHORITY"],
        )
        self.assertEqual(result.status, "PASS")


if __name__ == "__main__":
    unittest.main()
