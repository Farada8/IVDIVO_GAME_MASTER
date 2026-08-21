import unittest

from tools.ivdivo_durable_write_reconciler import (
    derive_idempotency_key, normalize_transaction, reconcile_transaction, transaction_hash
)
from tools.ivdivo_checkpoint_lineage import append_checkpoint, classify_retention, validate_ledger
from tools.ivdivo_interruption_learning import summarize_events


def base_tx():
    return {
        "transaction_id": "TX-001",
        "project_id": "IVDIVO",
        "work_unit": "RUN33",
        "authority_snapshot": {"repo_main_sha": "main-a", "state_revision": "2.0"},
        "blockers": [],
        "actions": [{
            "action_id": "GH-1",
            "artifact_id": "report",
            "store": "GITHUB",
            "operation": "write-report",
            "effect_class": "REVERSIBLE_WRITE",
            "side_effect_state": "RECONCILED",
            "readback_verified": True,
            "intended_identity": {"sha256": "aaa"},
            "observed_identity": {"sha256": "aaa"}
        }]
    }


def action(action_id, state="NOT_STARTED", effect="REVERSIBLE_WRITE"):
    return {
        "action_id": action_id,
        "artifact_id": action_id.lower(),
        "store": "DRIVE",
        "operation": "write",
        "effect_class": effect,
        "side_effect_state": state,
        "readback_verified": False,
        "intended_identity": {},
        "observed_identity": {},
    }


class DurableTransactionTests(unittest.TestCase):
    def test_key_deterministic(self):
        a = derive_idempotency_key(transaction_id="t", action_id="a", store="github", operation="put", artifact_id="x")
        b = derive_idempotency_key(transaction_id="t", action_id="a", store="GITHUB", operation="put", artifact_id="x")
        self.assertEqual(a, b)

    def test_hash_stable_across_key_order(self):
        tx = base_tx(); h1 = transaction_hash(tx)
        tx2 = {"actions": tx["actions"], "work_unit": tx["work_unit"], "project_id": tx["project_id"],
               "authority_snapshot": tx["authority_snapshot"], "transaction_id": tx["transaction_id"], "blockers": []}
        self.assertEqual(h1, transaction_hash(tx2))

    def test_secret_rejected(self):
        tx = base_tx(); tx["actions"][0]["api_key"] = "x"
        with self.assertRaises(ValueError): normalize_transaction(tx)

    def test_duplicate_action_rejected(self):
        tx = base_tx(); tx["actions"].append(dict(tx["actions"][0]))
        with self.assertRaises(ValueError): normalize_transaction(tx)

    def test_blocker_outranks_everything(self):
        tx = base_tx(); tx["blockers"] = ["FOUNDER_DECISION"]
        tx["actions"][0]["side_effect_state"] = "STARTED_UNKNOWN"; tx["actions"][0]["effect_class"] = "PAID_WRITE"
        result = reconcile_transaction(tx, current_repo_main_sha="different", current_state_revision="3")
        self.assertEqual(result["decision"], "STOP")

    def test_drift_outranks_unknown_external(self):
        tx = base_tx(); tx["actions"][0]["side_effect_state"] = "STARTED_UNKNOWN"; tx["actions"][0]["effect_class"] = "PAID_WRITE"
        result = reconcile_transaction(tx, current_repo_main_sha="different", current_state_revision="2.0")
        self.assertEqual(result["decision"], "REBASE_FIRST")

    def test_failed_action_outranks_unstarted_actions(self):
        tx = base_tx(); tx["actions"] = [action("FAILED-1", "FAILED"), action("NEW-1", "NOT_STARTED")]
        result = reconcile_transaction(tx, current_repo_main_sha="main-a", current_state_revision="2.0")
        self.assertEqual(result["decision"], "STOP"); self.assertEqual(result["reason"], "FAILED_ACTIONS_PRESENT")

    def test_identity_mismatch_stops(self):
        tx = base_tx(); tx["actions"][0]["observed_identity"] = {"sha256": "bbb"}
        result = reconcile_transaction(tx, current_repo_main_sha="main-a", current_state_revision="2.0")
        self.assertEqual(result["reason"], "IDENTITY_MISMATCH")

    def test_paid_unknown_quarantined(self):
        tx = base_tx(); tx["actions"][0]["effect_class"] = "PAID_WRITE"; tx["actions"][0]["side_effect_state"] = "STARTED_UNKNOWN"; tx["actions"][0]["readback_verified"] = False
        result = reconcile_transaction(tx, current_repo_main_sha="main-a", current_state_revision="2.0")
        self.assertEqual(result["decision"], "QUARANTINE_EXTERNAL_SIDE_EFFECT")

    def test_reversible_unknown_verify_before_retry(self):
        tx = base_tx(); tx["actions"][0]["side_effect_state"] = "STARTED_UNKNOWN"; tx["actions"][0]["readback_verified"] = False
        result = reconcile_transaction(tx, current_repo_main_sha="main-a", current_state_revision="2.0")
        self.assertEqual(result["decision"], "VERIFY_STORE_BEFORE_RETRY")

    def test_confirmed_without_readback(self):
        tx = base_tx(); tx["actions"][0]["side_effect_state"] = "CONFIRMED"; tx["actions"][0]["readback_verified"] = False
        result = reconcile_transaction(tx, current_repo_main_sha="main-a", current_state_revision="2.0")
        self.assertEqual(result["decision"], "VERIFY_READBACK")

    def test_only_safe_missing_actions_execute(self):
        tx = base_tx(); tx["actions"][0]["side_effect_state"] = "NOT_STARTED"; tx["actions"][0]["readback_verified"] = False
        result = reconcile_transaction(tx, current_repo_main_sha="main-a", current_state_revision="2.0")
        self.assertEqual(result["decision"], "EXECUTE_MISSING_SAFE_ACTIONS")

    def test_unstarted_paid_requires_gate(self):
        tx = base_tx(); tx["actions"][0]["side_effect_state"] = "NOT_STARTED"; tx["actions"][0]["effect_class"] = "PAID_WRITE"
        result = reconcile_transaction(tx, current_repo_main_sha="main-a", current_state_revision="2.0")
        self.assertEqual(result["decision"], "REQUIRE_EXPLICIT_DISPATCH_GATE")

    def test_complete(self):
        result = reconcile_transaction(base_tx(), current_repo_main_sha="main-a", current_state_revision="2.0")
        self.assertEqual(result["decision"], "TRANSACTION_COMPLETE")


class LineageTests(unittest.TestCase):
    def test_append_root_and_child(self):
        a = append_checkpoint({"entries": []}, entry_id="e1", work_unit="W", checkpoint_id="c1", checkpoint_sha256="a"*64, repo_main_sha="m1", state_revision="1")
        b = append_checkpoint(a, entry_id="e2", work_unit="W", checkpoint_id="c2", checkpoint_sha256="b"*64, repo_main_sha="m2", state_revision="2", parent_entry_id="e1")
        rows = {e["entry_id"]: e for e in b["entries"]}
        self.assertEqual(rows["e1"]["status"], "SUPERSEDED"); self.assertEqual(rows["e2"]["generation"], 1)

    def test_second_root_rejected(self):
        a = append_checkpoint({"entries": []}, entry_id="e1", work_unit="W", checkpoint_id="c1", checkpoint_sha256="a"*64, repo_main_sha="m", state_revision="1")
        with self.assertRaises(ValueError): append_checkpoint(a, entry_id="e2", work_unit="W", checkpoint_id="c2", checkpoint_sha256="b"*64, repo_main_sha="m", state_revision="1")

    def test_existing_multiple_roots_rejected(self):
        ledger = {"entries":[
            {"entry_id":"e1","work_unit":"W","checkpoint_id":"c1","checkpoint_sha256":"a"*64,"parent_entry_id":None,"generation":0,"status":"SUPERSEDED"},
            {"entry_id":"e2","work_unit":"W","checkpoint_id":"c2","checkpoint_sha256":"b"*64,"parent_entry_id":None,"generation":0,"status":"ACTIVE"}]}
        with self.assertRaises(ValueError): validate_ledger(ledger)

    def test_existing_multiple_active_heads_rejected(self):
        ledger = {"entries":[
            {"entry_id":"e1","work_unit":"W","checkpoint_id":"c1","checkpoint_sha256":"a"*64,"parent_entry_id":None,"generation":0,"status":"SUPERSEDED"},
            {"entry_id":"e2","work_unit":"W","checkpoint_id":"c2","checkpoint_sha256":"b"*64,"parent_entry_id":"e1","generation":1,"status":"ACTIVE"},
            {"entry_id":"e3","work_unit":"W","checkpoint_id":"c3","checkpoint_sha256":"c"*64,"parent_entry_id":"e2","generation":2,"status":"ACTIVE"}]}
        with self.assertRaises(ValueError): validate_ledger(ledger)

    def test_duplicate_checkpoint_sha_rejected(self):
        ledger = {"entries":[
            {"entry_id":"e1","work_unit":"W1","checkpoint_id":"c1","checkpoint_sha256":"a"*64,"parent_entry_id":None,"generation":0,"status":"ACTIVE"},
            {"entry_id":"e2","work_unit":"W2","checkpoint_id":"c2","checkpoint_sha256":"a"*64,"parent_entry_id":None,"generation":0,"status":"ACTIVE"}]}
        with self.assertRaises(ValueError): validate_ledger(ledger)

    def test_cross_work_parent_rejected(self):
        a = append_checkpoint({"entries": []}, entry_id="e1", work_unit="W1", checkpoint_id="c1", checkpoint_sha256="a"*64, repo_main_sha="m", state_revision="1")
        with self.assertRaises(ValueError): append_checkpoint(a, entry_id="e2", work_unit="W2", checkpoint_id="c2", checkpoint_sha256="b"*64, repo_main_sha="m", state_revision="1", parent_entry_id="e1")

    def test_generation_mismatch_rejected(self):
        ledger = {"entries": [
            {"entry_id":"e1","work_unit":"W","checkpoint_id":"c1","checkpoint_sha256":"a"*64,"parent_entry_id":None,"generation":0,"status":"SUPERSEDED"},
            {"entry_id":"e2","work_unit":"W","checkpoint_id":"c2","checkpoint_sha256":"b"*64,"parent_entry_id":"e1","generation":3,"status":"ACTIVE"}]}
        with self.assertRaises(ValueError): validate_ledger(ledger)

    def test_incident_retention(self):
        ledger = {"entries": [
            {"entry_id":"e1","work_unit":"W","checkpoint_id":"c1","checkpoint_sha256":"a"*64,"parent_entry_id":None,"generation":0,"status":"INCIDENT_EVIDENCE","incident_id":"I-1"},
            {"entry_id":"e2","work_unit":"W","checkpoint_id":"c2","checkpoint_sha256":"b"*64,"parent_entry_id":"e1","generation":1,"status":"ACTIVE"}]}
        result = classify_retention(ledger); mapping = {x["entry_id"]:x["retention"] for x in result["entries"]}
        self.assertEqual(mapping["e1"], "AUDIT_KEEP"); self.assertEqual(mapping["e2"], "EPHEMERAL_RECOVERY_CURRENT")


class LearningTests(unittest.TestCase):
    def test_no_real_evidence_hold(self):
        result = summarize_events([{"event_id":"1","project_id":"P","work_unit":"W","recovery_decision":"REBASE_FIRST"}])
        self.assertEqual(result["promotion_recommendation"], "HOLD")

    def test_false_resume_always_hold(self):
        result = summarize_events([{"event_id":"1","project_id":"P","work_unit":"W","recovery_decision":"RESUME_EXACT","real_interruption":True,"false_resume":True}])
        self.assertEqual(result["reason"], "FALSE_RESUME_PRESENT")

    def test_cross_project_minimum_promotable_review(self):
        events = [
            {"event_id":"1","project_id":"P1","work_unit":"W1","recovery_decision":"REBASE_FIRST","real_interruption":True,"duplicate_work_units_avoided":1,"writes_reconciled":1},
            {"event_id":"2","project_id":"P2","work_unit":"W2","recovery_decision":"RECOVER_VOLATILE_FIRST","real_interruption":True,"duplicate_work_units_avoided":1,"writes_reconciled":2},
            {"event_id":"3","project_id":"P1","work_unit":"W3","recovery_decision":"RESUME_EXACT","real_interruption":True,"duplicate_work_units_avoided":1,"writes_reconciled":0}]
        result = summarize_events(events)
        self.assertEqual(result["promotion_recommendation"], "ELIGIBLE_FOR_PROMOTION_REVIEW")

    def test_high_real_false_stop_narrows(self):
        events = [{"event_id":str(i),"project_id":"P1" if i%2 else "P2","work_unit":f"W{i}","recovery_decision":"STOP","real_interruption":True,"false_stop": i<2} for i in range(10)]
        result = summarize_events(events)
        self.assertEqual(result["promotion_recommendation"], "NARROW")

    def test_synthetic_false_stops_do_not_inflate_real_false_stop_rate(self):
        events = [
            {"event_id":"r1","project_id":"P1","work_unit":"W1","recovery_decision":"REBASE_FIRST","real_interruption":True},
            {"event_id":"r2","project_id":"P2","work_unit":"W2","recovery_decision":"RECOVER_VOLATILE_FIRST","real_interruption":True},
            {"event_id":"r3","project_id":"P1","work_unit":"W3","recovery_decision":"RESUME_EXACT","real_interruption":True},
        ] + [{"event_id":f"s{i}","project_id":"S","work_unit":f"S{i}","recovery_decision":"STOP","real_interruption":False,"false_stop":True} for i in range(20)]
        result = summarize_events(events)
        self.assertEqual(result["promotion_recommendation"], "ELIGIBLE_FOR_PROMOTION_REVIEW")
        self.assertEqual(result["metrics"]["real_false_stop_rate"], 0.0)


if __name__ == "__main__": unittest.main()
