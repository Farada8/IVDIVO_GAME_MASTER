import unittest


ATTRACTION_STATES = {"ATTRACTION_AUTHORIZED", "ROMANCE_ACTIVE", "ROMANCE_LOCKED"}


def check_route(authority_state: str, p53_mode: str):
    findings = []
    if authority_state in ATTRACTION_STATES and p53_mode == "OFF":
        findings.append("AUTHORITY_EDGE_OMITTED")
    if authority_state not in ATTRACTION_STATES and p53_mode in {"FULL", "LITE"}:
        findings.append("ATTRACTION_INVENTED_WITHOUT_AUTHORITY")
    return findings


class MFC03OrbitalYouthAuthorityContractTests(unittest.TestCase):
    """Bounded replication fixture; this is a contract test, not a new engine."""

    def test_known_positive_c02_route_is_flagged_once(self):
        self.assertEqual(
            check_route("ATTRACTION_AUTHORIZED", "OFF"),
            ["AUTHORITY_EDGE_OMITTED"],
        )

    def test_corrected_c04_route_is_clean(self):
        self.assertEqual(check_route("ATTRACTION_AUTHORIZED", "LITE"), [])

    def test_legitimate_non_attraction_off_routes_are_clean(self):
        controls = [
            ("FRIENDSHIP", "OFF"),  # Ollie ↔ Ethan
            ("FRIENDSHIP", "OFF"),  # general ensemble
            ("NONE", "OFF"),        # Maya ↔ local transit peers
            ("FAMILY", "OFF"),      # Maya ↔ host
        ]
        self.assertEqual([check_route(*control) for control in controls], [[], [], [], []])

    def test_no_attraction_authority_cannot_be_upgraded_silently(self):
        self.assertEqual(
            check_route("FRIENDSHIP", "LITE"),
            ["ATTRACTION_INVENTED_WITHOUT_AUTHORITY"],
        )

    def test_terminal_green_surface_is_protected_no_change(self):
        final_gate = {
            "fatal": 0,
            "major": 0,
            "blocking_medium": 0,
            "next_evidence": "EXTERNAL_OR_FOUNDER_OR_FACTUAL_OR_READER",
            "broad_internal_rewrite_authorized": False,
        }
        action = (
            "PROTECT_NO_CHANGE"
            if final_gate["fatal"] == 0
            and final_gate["major"] == 0
            and final_gate["blocking_medium"] == 0
            and not final_gate["broad_internal_rewrite_authorized"]
            else "REVIEW_REQUIRED"
        )
        self.assertEqual(action, "PROTECT_NO_CHANGE")


if __name__ == "__main__":
    unittest.main()
