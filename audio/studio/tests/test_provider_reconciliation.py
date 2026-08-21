import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))
from provider_reconciliation import reconcile_ambiguous


class ProviderReconciliationTests(unittest.TestCase):
    def attempt(self):
        return {"state": "AMBIGUOUS", "request_hash": "req", "block_id": "RB001"}

    def test_found_accepted_reuses_existing_response(self):
        out = reconcile_ambiguous(self.attempt(), {
            "state": "FOUND_ACCEPTED",
            "provider_request_id": "p1",
            "response_hash": "r1",
        })
        self.assertEqual(out["status"], "RECONCILED_ACCEPTED")
        self.assertEqual(out["next_action"], "INGEST_EXISTING_RESPONSE")
        self.assertFalse(out["retry_allowed"])

    def test_found_accepted_requires_evidence(self):
        with self.assertRaisesRegex(ValueError, "EVIDENCE_INCOMPLETE"):
            reconcile_ambiguous(self.attempt(), {"state": "FOUND_ACCEPTED"})

    def test_not_found_releases_to_retry_policy(self):
        out = reconcile_ambiguous(self.attempt(), {"state": "NOT_FOUND"})
        self.assertTrue(out["retry_allowed"])
        self.assertEqual(out["status"], "RECONCILED_NOT_FOUND")

    def test_lookup_unsupported_stays_hold(self):
        out = reconcile_ambiguous(self.attempt(), {"state": "LOOKUP_UNSUPPORTED"})
        self.assertEqual(out["status"], "HOLD_AMBIGUOUS")
        self.assertFalse(out["retry_allowed"])

    def test_lookup_unavailable_stays_hold(self):
        out = reconcile_ambiguous(self.attempt(), {"state": "LOOKUP_UNAVAILABLE"})
        self.assertEqual(out["status"], "HOLD_AMBIGUOUS")
        self.assertFalse(out["retry_allowed"])

    def test_non_ambiguous_attempt_rejected(self):
        with self.assertRaisesRegex(ValueError, "NOT_AMBIGUOUS"):
            reconcile_ambiguous({"state": "SENT", "request_hash": "req", "block_id": "RB001"}, {"state": "NOT_FOUND"})

    def test_invalid_lookup_state_rejected(self):
        with self.assertRaisesRegex(ValueError, "LOOKUP_STATE_INVALID"):
            reconcile_ambiguous(self.attempt(), {"state": "MAYBE"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
