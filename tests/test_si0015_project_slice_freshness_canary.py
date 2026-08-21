import unittest

from tools.si0015_project_slice_freshness_canary import ProjectSlice, classify_slice


class SI0015ProjectSliceFreshnessCanaries(unittest.TestCase):
    def test_stale_bloodbound_current_slice(self):
        fixture = ProjectSlice(
            slice_kind="CURRENT",
            embedded_frontier="D10_WORKING",
            controlling_frontiers=("D10_FOUNDER_LOCKED",),
        )
        self.assertEqual(classify_slice(fixture), "STALE_CURRENT_SLICE")

    def test_resume_does_not_satisfy_d01_founder_lock(self):
        fixture = ProjectSlice(
            slice_kind="CURRENT",
            embedded_frontier="D01_FINAL_GATE_PASS_READY_FOR_LOCK",
            controlling_frontiers=("D01_FINAL_GATE_PASS_READY_FOR_LOCK",),
            required_approval_event="FOUNDER_EXPLICIT_LOCK_D01",
            observed_events=("RESUME",),
        )
        self.assertEqual(classify_slice(fixture), "APPROVAL_EVENT_MISSING")

    def test_historical_slice_is_exempt(self):
        fixture = ProjectSlice(
            slice_kind="HISTORICAL",
            embedded_frontier="D10_WORKING",
            controlling_frontiers=("D10_FOUNDER_LOCKED",),
        )
        self.assertEqual(classify_slice(fixture), "EXEMPT_HISTORICAL_SLICE")

    def test_unresolved_pointer_fails_closed(self):
        fixture = ProjectSlice(
            slice_kind="CURRENT",
            embedded_frontier="UNKNOWN",
            controlling_frontiers=(),
            pointer_resolved=False,
        )
        self.assertEqual(classify_slice(fixture), "UNRESOLVED_POINTER")

    def test_competing_current_frontiers_fail_closed(self):
        fixture = ProjectSlice(
            slice_kind="CURRENT",
            embedded_frontier="A",
            controlling_frontiers=("A", "B"),
        )
        self.assertEqual(classify_slice(fixture), "UNRESOLVED_POINTER")

    def test_current_match_is_clean(self):
        fixture = ProjectSlice(
            slice_kind="CURRENT",
            embedded_frontier="B02_FINAL_STORY_GATE_GREEN",
            controlling_frontiers=("B02_FINAL_STORY_GATE_GREEN",),
        )
        self.assertEqual(classify_slice(fixture), "CURRENT_MATCH")

    def test_exact_approval_event_allows_matching_transition(self):
        fixture = ProjectSlice(
            slice_kind="CURRENT",
            embedded_frontier="D01_FOUNDER_LOCKED",
            controlling_frontiers=("D01_FOUNDER_LOCKED",),
            required_approval_event="FOUNDER_EXPLICIT_LOCK_D01",
            observed_events=("FOUNDER_EXPLICIT_LOCK_D01",),
        )
        self.assertEqual(classify_slice(fixture), "CURRENT_MATCH")


if __name__ == "__main__":
    unittest.main()
