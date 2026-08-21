import json
import tempfile
import unittest
from pathlib import Path
import sys

RUNTIME = Path(__file__).resolve().parents[1] / "runtime"
sys.path.insert(0, str(RUNTIME))

import production_control as pc
import production_control_cli as cli


CANARY_MANIFEST = {
    "project": "LESSON_ZERO_RU_AUDIO",
    "spoken_units": 36,
    "characters": 2163,
    "blocks": {
        "RB001": {"units": list(range(1, 25)), "chars": 1271, "hash": "h1"},
        "RB002": {"units": list(range(25, 30)), "chars": 203, "hash": "h2"},
        "RB003": {"units": list(range(30, 37)), "chars": 689, "hash": "h3"},
    },
}
CANARY_FIXTURE = {
    "scalar_fields": {"spoken_units": 36, "characters": 2163},
    "blocks": {
        "RB001": {"units": list(range(1, 25)), "chars": 1271, "hash": "h1"},
        "RB002": {"units": list(range(25, 30)), "chars": 203, "hash": "h2"},
        "RB003": {"units": list(range(30, 37)), "chars": 689, "hash": "h3"},
    },
}


class ProductionControlTests(unittest.TestCase):
    def test_canonical_hash_reproducible(self):
        self.assertEqual(pc.canonical_hash(CANARY_MANIFEST), pc.canonical_hash(dict(CANARY_MANIFEST)))

    def test_identity_fixture_passes(self):
        result = pc.validate_identity_fixture(CANARY_MANIFEST, CANARY_FIXTURE)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["block_count"], 3)

    def test_identity_scalar_drift_fails(self):
        bad = dict(CANARY_MANIFEST); bad["spoken_units"] = 35
        with self.assertRaisesRegex(ValueError, "IDENTITY_DRIFT"):
            pc.validate_identity_fixture(bad, CANARY_FIXTURE)

    def test_identity_block_hash_drift_fails(self):
        bad = json.loads(json.dumps(CANARY_MANIFEST)); bad["blocks"]["RB002"]["hash"] = "wrong"
        with self.assertRaisesRegex(ValueError, "IDENTITY_DRIFT"):
            pc.validate_identity_fixture(bad, CANARY_FIXTURE)

    def test_spend_ledger_reuses_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = pc.SpendLedger(Path(d) / "ledger.json")
            self.assertEqual(ledger.plan("req", "RB001"), "PLANNED")
            ledger.transition("req", "SENT", provider_request_id="p1")
            ledger.transition("req", "ACCEPTED", response_hash="r1")
            self.assertEqual(ledger.plan("req", "RB001"), "REUSED_ACCEPTED")

    def test_spend_ledger_persists(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "ledger.json"
            ledger = pc.SpendLedger(path); ledger.plan("req", "RB001"); ledger.transition("req", "SENT")
            loaded = pc.SpendLedger(path)
            self.assertEqual(loaded.snapshot()["req"]["state"], "SENT")

    def test_accepted_attempt_immutable(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = pc.SpendLedger(Path(d) / "ledger.json")
            ledger.plan("req", "RB001"); ledger.transition("req", "ACCEPTED")
            with self.assertRaisesRegex(ValueError, "IMMUTABLE"):
                ledger.transition("req", "REJECTED")

    def test_ambiguous_requires_reconciliation(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = pc.SpendLedger(Path(d) / "ledger.json")
            ledger.plan("req", "RB001"); ledger.transition("req", "AMBIGUOUS")
            self.assertEqual(ledger.plan("req", "RB001"), "RECONCILE_REQUIRED")
            with self.assertRaisesRegex(ValueError, "RECONCILIATION"):
                ledger.transition("req", "SENT")

    def test_error_auth_fail_closed(self):
        error = pc.normalize_provider_error(401)
        self.assertEqual(error["category"], "AUTH")
        self.assertEqual(pc.retry_decision(error), "FAIL_CLOSED")

    def test_error_rate_limit_retries(self):
        error = pc.normalize_provider_error(429)
        self.assertEqual(error["category"], "RATE_LIMIT")
        self.assertEqual(pc.retry_decision(error), "BACKOFF_RETRY")

    def test_response_started_quarantines_even_server_error(self):
        error = pc.normalize_provider_error(503)
        self.assertEqual(pc.retry_decision(error, response_started=True), "QUARANTINE_AMBIGUOUS")

    def test_capability_drift_pass(self):
        result = pc.capability_drift(
            {"voice_ids": ["v1"], "model_ids": ["m1"]},
            {"voices": {"v1": {}}, "models": {"m1": {}}},
        )
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["auto_substitution"])

    def test_capability_drift_fails_without_substitution(self):
        result = pc.capability_drift(
            {"voice_ids": ["v1"], "model_ids": ["m1"]},
            {"voices": {}, "models": []},
        )
        self.assertEqual(result["status"], "FAIL_DRIFT")
        self.assertFalse(result["auto_substitution"])

    def test_scoped_invalidation(self):
        deps = {"binding": ["RB001", "RB002", "RB003"], "pronunciation": ["RB001", "RB003"]}
        self.assertEqual(pc.scoped_invalidation(deps, ["pronunciation"]), ["RB001", "RB003"])

    def test_selective_rerender_one_block(self):
        self.assertEqual(pc.selective_rerender(["RB002"], ["RB001", "RB002", "RB003"]), ["RB002"])

    def test_selective_rerender_unknown_fails(self):
        with self.assertRaisesRegex(ValueError, "UNKNOWN_BLOCKS"):
            pc.selective_rerender(["RB999"], ["RB001"])

    def test_silent_reaction_zero_spoken_units(self):
        out = pc.promote_silent_reaction({
            "anchor_id": "S1", "character_id": "A", "trigger": "U1",
            "silent_action": "waits", "silence_policy": "PROTECTED",
        })
        self.assertEqual(out["spoken_unit_delta"], 0)

    def test_pause_rejects_generic_dramatic(self):
        with self.assertRaisesRegex(ValueError, "UNSUPPORTED_PAUSE_FUNCTION"):
            pc.compile_functional_pause(["DRAMATIC"])

    def test_pause_is_semantic_until_alignment(self):
        out = pc.compile_functional_pause(["AFTERMATH", "LISTENING"], duration_hypotheses_ms=[450, 750])
        self.assertIsNone(out["absolute_time"])
        self.assertEqual(out["timing_status"], "SEMANTIC_UNTIL_ALIGNMENT")

    def test_latency_has_no_absolute_pre_render_time(self):
        out = pc.compile_reply_latency("U024", "U026", "PROTECTED_WAIT")
        self.assertIsNone(out["absolute_time"])

    def test_microphone_perspectives(self):
        for state in ("CLOSE", "NORMAL", "ACROSS_ROOM", "MEDIA"):
            out = pc.compile_microphone_choreography("A", state)
            self.assertEqual(out["perspective"], state)
            self.assertFalse(out["extreme_pan_required"])

    def test_bad_microphone_perspective_fails(self):
        with self.assertRaisesRegex(ValueError, "UNSUPPORTED_MIC_PERSPECTIVE"):
            pc.compile_microphone_choreography("A", "MAGIC_WIDE")

    def test_ai_tell_repeated_endings_is_advisory(self):
        out = pc.ai_tell_flags(["yes.", "yes!", "no.", "yes?"], [0.2, 0.3], [0.2, 0.3])
        self.assertIn("REPEATED_ENDINGS", out["flags"])
        self.assertFalse(out["authoritative"])
        self.assertFalse(out["auto_reject"])

    def test_ai_tell_regular_pause_flag(self):
        out = pc.ai_tell_flags([], [0.5, 0.5, 0.5, 0.5], [0.1, 0.2])
        self.assertIn("PAUSE_REGULARITY", out["flags"])

    def test_performance_lock_requires_human_and_fatigue(self):
        out = pc.performance_lock_gate({"multi_state": True, "pronunciation": True, "pair": True})
        self.assertEqual(out["status"], "HOLD")
        self.assertIn("human_review", out["missing"])
        self.assertIn("fatigue", out["missing"])
        self.assertFalse(out["machine_may_auto_lock"])

    def test_performance_lock_can_lock_with_full_evidence(self):
        out = pc.performance_lock_gate({
            "multi_state": True, "pronunciation": True, "pair": True,
            "fatigue": True, "human_review": True,
        })
        self.assertEqual(out["status"], "LOCKED")

    def test_orchestration_candidate_requires_all_contracts(self):
        full = {k: True for k in ["clean_build", "resume", "scoped_invalidation", "selective_rerender", "fail_closed"]}
        self.assertEqual(pc.orchestration_acceptance(full)["status"], "PASS_CANDIDATE")
        full["resume"] = False
        self.assertEqual(pc.orchestration_acceptance(full)["status"], "HOLD")

    def test_cli_freeze_resume_no_dispatch(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            manifest = root / "manifest.json"; fixture = root / "fixture.json"; checkpoint = root / "checkpoint.json"
            manifest.write_text(json.dumps(CANARY_MANIFEST), encoding="utf-8")
            fixture.write_text(json.dumps(CANARY_FIXTURE), encoding="utf-8")
            frozen = cli.freeze_manifest(str(manifest), str(fixture), str(checkpoint))
            self.assertFalse(frozen["dispatch_allowed"])
            resumed = cli.resume_checkpoint(str(checkpoint), str(fixture))
            self.assertEqual(resumed["resent_requests"], 0)
            self.assertFalse(resumed["dispatch_allowed"])

    def test_cli_invalidation(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "deps.json"
            path.write_text(json.dumps({"pronunciation": ["RB001", "RB003"]}), encoding="utf-8")
            out = cli.invalidate(str(path), ["pronunciation"])
            self.assertEqual(out["invalidated"], ["RB001", "RB003"])
            self.assertFalse(out["dispatch_allowed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
