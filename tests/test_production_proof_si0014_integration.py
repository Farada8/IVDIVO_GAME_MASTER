import copy
import unittest

from tools.ivdivo_durable_write_reconciler import reconcile_transaction
from tools.ivdivo_mirror_integrity import compare


def mirror_record(store: str):
    return {
        "logical_id": "PP-R15-ARTIFACT",
        "authority_epoch": "epoch-1",
        "frontier_token": "RUN32-R15",
        "status_token": "PERSISTED",
        "mirror_mode": "SEMANTIC",
        "content_fingerprint": "proof-r15-v1",
        "source_revision": f"{store}-rev-1",
    }


def partial_plan():
    return {
        "transaction_id": "PP-R15-TX-001",
        "project_id": "SELF_IMPROVEMENT",
        "work_unit": "PRODUCTION_PROOF_R15_MULTI_STORE_RECOVERY",
        "authority_snapshot": {
            "repo_main_sha": "MAIN-SHA-1",
            "state_revision": "STATE-REV-1",
        },
        "actions": [
            {
                "action_id": "github_write",
                "artifact_id": "PP-R15-ARTIFACT",
                "store": "GITHUB",
                "operation": "CREATE_OR_UPDATE",
                "effect_class": "REVERSIBLE_WRITE",
                "side_effect_state": "CONFIRMED",
                "readback_verified": True,
                "intended_identity": {"fingerprint": "proof-r15-v1"},
                "observed_identity": {"fingerprint": "proof-r15-v1"},
            },
            {
                "action_id": "drive_write",
                "artifact_id": "PP-R15-ARTIFACT",
                "store": "DRIVE",
                "operation": "CREATE_OR_UPDATE",
                "effect_class": "REVERSIBLE_WRITE",
                "side_effect_state": "NOT_STARTED",
                "readback_verified": False,
                "intended_identity": {"fingerprint": "proof-r15-v1"},
            },
        ],
        "evidence_boundary": ["CONTROLLED_TEST_ONLY", "NO_REAL_STORE_WRITE_PERFORMED_BY_RECONCILER"],
    }


class ProductionProofSI0014IntegrationTests(unittest.TestCase):
    def test_partial_write_recovers_only_missing_safe_peer_then_mirror_converges(self):
        before = compare({
            "github_records": [mirror_record("github")],
            "drive_records": [],
        })
        self.assertEqual(before["status"], "ISSUES_FOUND")
        self.assertIn("MISSING_DRIVE_MIRROR", before["items"][0]["issues"])

        plan = partial_plan()
        decision = reconcile_transaction(
            plan,
            current_repo_main_sha="MAIN-SHA-1",
            current_state_revision="STATE-REV-1",
        )
        self.assertEqual(decision["decision"], "EXECUTE_MISSING_SAFE_ACTIONS")
        self.assertEqual(decision["action_ids"], ["drive_write"])

        completed = copy.deepcopy(plan)
        completed["actions"][1]["side_effect_state"] = "CONFIRMED"
        completed["actions"][1]["readback_verified"] = True
        completed["actions"][1]["observed_identity"] = {"fingerprint": "proof-r15-v1"}
        decision2 = reconcile_transaction(
            completed,
            current_repo_main_sha="MAIN-SHA-1",
            current_state_revision="STATE-REV-1",
        )
        self.assertEqual(decision2["decision"], "TRANSACTION_COMPLETE")

        after = compare({
            "github_records": [mirror_record("github")],
            "drive_records": [mirror_record("drive")],
        })
        self.assertEqual(after["status"], "PASS")

    def test_authority_drift_rebases_before_missing_peer_write(self):
        decision = reconcile_transaction(
            partial_plan(),
            current_repo_main_sha="NEWER-MAIN-SHA",
            current_state_revision="STATE-REV-1",
        )
        self.assertEqual(decision["decision"], "REBASE_FIRST")
        self.assertEqual(decision["reason"], "AUTHORITY_OR_STATE_DRIFT")


if __name__ == "__main__":
    unittest.main()
