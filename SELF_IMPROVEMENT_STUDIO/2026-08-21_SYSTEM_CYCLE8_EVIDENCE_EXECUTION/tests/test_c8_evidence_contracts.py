import unittest

from modules.c8_evidence_contracts import (
    book_scope_widen,
    economics_value,
    evidence_claim,
    evidence_family_count,
    governor,
    lock_ladder,
    package_identity,
    prompt_ir_parity,
    recovery_event,
    recovery_promotion_gate,
    registry_reservation_view,
    safe_missing_actions,
    secret_guard,
    stale_episode_check,
)


class Cycle8EvidenceContractsTests(unittest.TestCase):
    def setUp(self):
        self.committed = [f"SI-{n:04d}" for n in range(8, 16)]

    def test_01_next_unreserved_is_si0016(self):
        self.assertEqual(registry_reservation_view(self.committed, [])["next_id"], "SI-0016")

    def test_02_partial_registry_visibility_fails_closed(self):
        self.assertEqual(registry_reservation_view(self.committed, [], complete_visibility=False)["status"], "HOLD_PARTIAL_VISIBILITY")

    def test_03_committed_reserved_collision_holds(self):
        self.assertEqual(registry_reservation_view(self.committed, ["SI-0015"])["status"], "HOLD_COLLISION")

    def test_04_partial_write_runs_only_missing_safe_store(self):
        result = safe_missing_actions({"github": "COMMITTED_READBACK", "drive": "MISSING"})
        self.assertEqual(result["actions"], ["drive"])

    def test_05_paid_unknown_is_never_replayed(self):
        result = safe_missing_actions({"provider": "STARTED_UNKNOWN"}, paid_or_irreversible=True)
        self.assertEqual(result["decision"], "QUARANTINE_NO_REPLAY")

    def test_06_recovery_event_requires_complete_proof(self):
        event = {"fresh_authority": True, "checkpoint": True, "post_restart_authority_readback": True, "recovery_readback": True, "project_id_match": True, "source_hash_match": True, "checkpoint_main_sha": "abc", "current_main_sha": "abc"}
        self.assertEqual(recovery_event(event), "RECOVERY_EVENT_ACCEPTED")

    def test_07_stale_checkpoint_requires_rebase(self):
        event = {"fresh_authority": True, "checkpoint": True, "post_restart_authority_readback": True, "recovery_readback": True, "project_id_match": True, "source_hash_match": True, "checkpoint_main_sha": "old", "current_main_sha": "new"}
        self.assertEqual(recovery_event(event), "REBASE_FIRST")

    def test_08_machine_output_cannot_be_human_signal(self):
        self.assertEqual(evidence_claim("MACHINE", "root-1", claim_as="HUMAN_SIGNAL"), "REJECT_EVIDENCE_LAUNDERING")

    def test_09_derived_reports_share_one_root_family(self):
        records = [{"root_source": "A"}, {"root_source": "A"}, {"root_source": "B"}]
        self.assertEqual(evidence_family_count(records), 2)

    def test_10_unmeasured_zero_is_rejected(self):
        self.assertEqual(economics_value(0, measured=False), "REJECT_FALSE_ZERO")

    def test_11_null_is_valid_unknown(self):
        self.assertEqual(economics_value(None, measured=False), "UNKNOWN_VALID_NULL")

    def test_12_d01_e96_is_stale_after_e120(self):
        self.assertEqual(stale_episode_check(96, 120), "REJECT_STALE_EPISODE")

    def test_13_d01_e113_is_stale_after_e120(self):
        self.assertEqual(stale_episode_check(113, 120), "REJECT_STALE_EPISODE")

    def test_14_secret_bearing_payload_is_rejected(self):
        self.assertEqual(secret_guard({"api_key": "secret-value"}), "REJECT_SECRET_FIELD")

    def test_15_historical_package_cannot_be_relabelled(self):
        self.assertEqual(package_identity("sha-A", "sha-B", ["post-package-commit"]), "REJECT_RELABEL")

    def test_16_prompt_ir_omission_fails_parity(self):
        result = prompt_ir_parity({"protected_fact": "A", "prohibition": "B"}, {"protected_fact": "A"}, ["protected_fact", "prohibition"])
        self.assertEqual(result["status"], "PARITY_FAIL")

    def test_17_book_sensor_false_positive_blocks_scope_widening(self):
        self.assertEqual(book_scope_widen(1, True, 1), "HOLD_FALSE_POSITIVE")

    def test_18_mfc03_still_holds_without_human_adjudication(self):
        self.assertEqual(book_scope_widen(0, True, 0), "HOLD_HUMAN_ADJUDICATION")

    def test_19_machine_perceptual_proxy_cannot_be_human_pass(self):
        self.assertEqual(evidence_claim("MACHINE_PROXY", "nmm-root", claim_as="HUMAN_SIGNAL"), "REJECT_EVIDENCE_LAUNDERING")

    def test_20_provider_acceptance_does_not_imply_take_voice_release_lock(self):
        self.assertEqual(lock_ladder(provider_accepted=True), "PROVIDER_ACCEPTED_ONLY")

    def test_21_governor_selects_best_admissible_internal_gate_when_human_blocked(self):
        tasks = [
            {"id": "META_MORE", "priority": 3, "information_gain": 5, "admissible": True},
            {"id": "CYCLE8_PERSISTENCE_CLOSURE", "priority": 2, "information_gain": 8, "admissible": True},
            {"id": "D04_HUMAN_SIGNAL", "priority": 1, "information_gain": 10, "admissible": False},
        ]
        self.assertEqual(governor(tasks), "CYCLE8_PERSISTENCE_CLOSURE")

    def test_22_governor_prevents_meta_starvation_when_p1_evidence_is_admissible(self):
        tasks = [
            {"id": "META_MORE", "priority": 3, "information_gain": 5, "admissible": True},
            {"id": "D04_HUMAN_SIGNAL", "priority": 1, "information_gain": 10, "admissible": True},
        ]
        self.assertEqual(governor(tasks), "D04_HUMAN_SIGNAL")

    def test_23_false_resume_blocks_recovery_promotion(self):
        self.assertEqual(recovery_promotion_gate(3, 2, 1), "BLOCK_FALSE_RESUME")

    def test_24_wrong_project_or_source_identity_stops_recovery(self):
        event = {"fresh_authority": True, "checkpoint": True, "post_restart_authority_readback": True, "recovery_readback": True, "project_id_match": False, "source_hash_match": True, "checkpoint_main_sha": "abc", "current_main_sha": "abc"}
        self.assertEqual(recovery_event(event), "HOLD_RECOVERY_EVIDENCE")


if __name__ == "__main__":
    unittest.main()
