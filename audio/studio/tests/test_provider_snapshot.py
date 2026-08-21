import copy
import sys
import unittest
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1] / "runtime"
sys.path.insert(0, str(RUNTIME))

from provider_snapshot import (
    assert_secret_free,
    compare_stable_snapshots,
    compile_snapshot,
    dispatch_capability_gate,
    verify_snapshot,
)


def preflight(**overrides):
    row = {
        "schema_version": "1.0",
        "provider": "elevenlabs",
        "checked_at": "2026-08-21T18:00:00+00:00",
        "secret_env_present": True,
        "connectivity": "PASS",
        "credential": "PASS",
        "status": "PASS",
        "failures": [],
        "models_request_meta": {"http_status": 200, "provider_request_id": "req-list"},
        "models": {
            "eleven_v3": {
                "status": "PASS", "name": "Eleven v3", "can_do_text_to_speech": True,
                "maximum_text_length_per_request": 5000, "concurrency_group": "standard",
            }
        },
        "voices": {
            "voice_a": {"status": "PASS", "name": "A", "category": "premade", "is_legacy": False}
        },
    }
    row.update(overrides)
    return row


class ProviderSnapshotTests(unittest.TestCase):
    def test_safe_secret_presence_flag_is_allowed(self):
        snap = compile_snapshot(preflight())
        self.assertEqual(snap["status"], "PASS")
        self.assertFalse(snap["secret_persisted"])

    def test_actual_api_key_field_is_rejected(self):
        row = preflight()
        row["api_key"] = "do-not-store"
        with self.assertRaisesRegex(ValueError, "SECRET_LIKE_FIELD_FORBIDDEN"):
            compile_snapshot(row)

    def test_targeted_snapshot_is_not_account_inventory(self):
        snap = compile_snapshot(preflight(), inventory_scope="TARGETED")
        self.assertFalse(snap["stable"]["account_inventory_complete"])
        self.assertFalse(snap["machine_may_infer_unlisted_voices"])

    def test_account_wide_scope_must_be_explicit(self):
        snap = compile_snapshot(preflight(), inventory_scope="ACCOUNT_WIDE")
        self.assertTrue(snap["stable"]["account_inventory_complete"])

    def test_volatile_change_does_not_create_stable_drift(self):
        a = compile_snapshot(preflight())
        b_row = preflight(checked_at="2026-08-21T18:05:00+00:00")
        b_row["models_request_meta"] = {"http_status": 200, "provider_request_id": "req-new"}
        b = compile_snapshot(b_row)
        out = compare_stable_snapshots(a, b)
        self.assertEqual(out["status"], "PASS_NO_STABLE_DRIFT")
        self.assertTrue(out["volatile_changed"])

    def test_voice_capability_drift_holds_without_swap(self):
        a = compile_snapshot(preflight())
        b_row = preflight()
        b_row["voices"]["voice_a"]["status"] = "FAIL"
        b = compile_snapshot(b_row)
        out = compare_stable_snapshots(a, b)
        self.assertEqual(out["status"], "HOLD_STABLE_CAPABILITY_DRIFT")
        gate = dispatch_capability_gate(b, required_model_ids=["eleven_v3"], required_voice_ids=["voice_a"])
        self.assertEqual(gate["status"], "HOLD")
        self.assertFalse(gate["auto_substitution"])

    def test_missing_unlisted_voice_fails_closed(self):
        snap = compile_snapshot(preflight())
        out = dispatch_capability_gate(snap, required_model_ids=["eleven_v3"], required_voice_ids=["voice_missing"])
        self.assertEqual(out["status"], "HOLD")
        self.assertEqual(out["missing_voice_ids"], ["voice_missing"])

    def test_tampered_stable_payload_fails_hash(self):
        snap = compile_snapshot(preflight())
        snap["stable"]["voices"]["voice_a"]["name"] = "tampered"
        with self.assertRaisesRegex(ValueError, "PROVIDER_STABLE_SNAPSHOT_HASH_MISMATCH"):
            verify_snapshot(snap)

    def test_unauthenticated_preflight_remains_hold(self):
        snap = compile_snapshot(preflight(credential="FAIL", status="FAIL", secret_env_present=False, failures=["FAIL_PROVIDER_CREDENTIAL"]))
        self.assertEqual(snap["status"], "HOLD")
        gate = dispatch_capability_gate(snap, required_model_ids=["eleven_v3"], required_voice_ids=["voice_a"])
        self.assertEqual(gate["status"], "HOLD")


if __name__ == "__main__":
    unittest.main(verbosity=2)
