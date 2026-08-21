from copy import deepcopy
import unittest

from tools.ivdivo_session_checkpoint import build_checkpoint, classify_resume, verify_checkpoint


def base_state():
    return {
        "checkpoint_id": "SYS-TEST-001",
        "project_id": "IVDIVO_ENGINE",
        "active_line": "SESSION_RESILIENCE",
        "work_unit": "RUN32",
        "current_phase": "ENGINEERING",
        "checkpoint_status": "ACTIVE",
        "authority_snapshot": {
            "repo": "Farada8/IVDIVO_GAME_MASTER",
            "repo_main_sha": "abc123",
            "state_pointer": "CURRENT_IVDIVO_ENGINE_MACHINE_EXECUTION.json",
            "state_revision": "1.1",
            "source_hash": None,
        },
        "last_verified_frontier": "PROMPT_12",
        "last_completed_artifact": "report.md",
        "selected_next_action": {
            "action_id": "PROMPT_13",
            "description": "continue",
            "executable_here": True,
        },
        "blockers": [],
        "writes": [
            {
                "write_id": "GH-1",
                "target": "github",
                "status": "DURABLE",
                "readback_verified": True,
            }
        ],
        "artifacts": [
            {
                "artifact_id": "A-1",
                "status": "DURABLE_WORKING",
                "durable_pointer": "github:path",
            }
        ],
        "evidence_boundary": ["NO_FAKE_HUMAN_PASS"],
    }


class SessionCheckpointTests(unittest.TestCase):
    def test_exact_resume(self):
        cp = build_checkpoint(base_state(), created_at="2026-08-21T18:00:00+00:00")
        result = classify_resume(cp, current_repo_main_sha="abc123", current_state_revision="1.1")
        self.assertEqual(result["decision"], "RESUME_EXACT")

    def test_repo_drift_requires_rebase(self):
        cp = build_checkpoint(base_state(), created_at="2026-08-21T18:00:00+00:00")
        result = classify_resume(cp, current_repo_main_sha="def456", current_state_revision="1.1")
        self.assertEqual(result["decision"], "REBASE_FIRST")
        self.assertIn("repo_main_sha", result["drift"])

    def test_state_revision_drift_requires_rebase(self):
        cp = build_checkpoint(base_state(), created_at="2026-08-21T18:00:00+00:00")
        result = classify_resume(cp, current_repo_main_sha="abc123", current_state_revision="1.2")
        self.assertEqual(result["decision"], "REBASE_FIRST")
        self.assertIn("state_revision", result["drift"])

    def test_pending_write_requires_recovery_first(self):
        state = base_state()
        state["writes"].append({
            "write_id": "DRIVE-2",
            "target": "drive",
            "status": "PENDING",
            "readback_verified": False,
        })
        cp = build_checkpoint(state, created_at="2026-08-21T18:00:00+00:00")
        result = classify_resume(cp, current_repo_main_sha="abc123", current_state_revision="1.1")
        self.assertEqual(result["decision"], "RECOVER_VOLATILE_FIRST")
        self.assertIn("DRIVE-2", result["pending_write_ids"])

    def test_chat_local_artifact_requires_recovery_first(self):
        state = base_state()
        state["artifacts"].append({
            "artifact_id": "LOCAL-WAV",
            "status": "CHAT_LOCAL_ONLY",
            "durable_pointer": None,
        })
        cp = build_checkpoint(state, created_at="2026-08-21T18:00:00+00:00")
        result = classify_resume(cp, current_repo_main_sha="abc123", current_state_revision="1.1")
        self.assertEqual(result["decision"], "RECOVER_VOLATILE_FIRST")
        self.assertIn("LOCAL-WAV", result["volatile_artifact_ids"])

    def test_tamper_fails_closed(self):
        cp = build_checkpoint(base_state(), created_at="2026-08-21T18:00:00+00:00")
        cp["payload"]["current_phase"] = "TAMPERED"
        ok, reason = verify_checkpoint(cp)
        self.assertFalse(ok)
        self.assertEqual(reason, "CHECKPOINT_HASH_MISMATCH")
        result = classify_resume(cp, current_repo_main_sha="abc123", current_state_revision="1.1")
        self.assertEqual(result["decision"], "STOP")

    def test_credential_like_field_rejected(self):
        state = base_state()
        state["api_key"] = "should-not-persist"
        with self.assertRaises(ValueError):
            build_checkpoint(state, created_at="2026-08-21T18:00:00+00:00")

    def test_blocker_stops_resume(self):
        state = base_state()
        state["blockers"] = ["HUMAN_EVIDENCE_REQUIRED"]
        cp = build_checkpoint(state, created_at="2026-08-21T18:00:00+00:00")
        result = classify_resume(cp, current_repo_main_sha="abc123", current_state_revision="1.1")
        self.assertEqual(result["decision"], "STOP")
        self.assertEqual(result["reason"], "BLOCKERS_PRESENT")

    def test_blocker_outranks_pending_recovery(self):
        state = base_state()
        state["blockers"] = ["FOUNDER_DECISION_REQUIRED"]
        state["writes"].append({
            "write_id": "DRIVE-PENDING",
            "target": "drive",
            "status": "PENDING",
            "readback_verified": False,
        })
        cp = build_checkpoint(state, created_at="2026-08-21T18:00:00+00:00")
        result = classify_resume(cp, current_repo_main_sha="abc123", current_state_revision="1.1")
        self.assertEqual(result["decision"], "STOP")
        self.assertEqual(result["reason"], "BLOCKERS_PRESENT")

    def test_authority_drift_outranks_pending_recovery(self):
        state = base_state()
        state["writes"].append({
            "write_id": "DRIVE-PENDING",
            "target": "drive",
            "status": "PENDING",
            "readback_verified": False,
        })
        cp = build_checkpoint(state, created_at="2026-08-21T18:00:00+00:00")
        result = classify_resume(cp, current_repo_main_sha="new-main", current_state_revision="1.1")
        self.assertEqual(result["decision"], "REBASE_FIRST")
        self.assertIn("repo_main_sha", result["drift"])


if __name__ == "__main__":
    unittest.main()
