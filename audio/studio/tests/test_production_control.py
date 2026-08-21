import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from production_control import (
    SpendLedger, capability_drift, dependency_descendants, dispatch_gate,
    normalize_provider_error, reconcile_ambiguous, release_control_gate,
    request_identity, retry_decision, selective_rerender,
)


class ProductionControlTests(unittest.TestCase):
    def ledger(self):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        return SpendLedger(Path(td.name) / "ledger.json")

    def test_request_identity_uses_existing_hash(self):
        self.assertEqual(request_identity({"request_hash":"abc"}), "abc")

    def test_request_identity_deterministic(self):
        a = {"path":"/x","body":{"b":2,"a":1},"block_id":"B1"}
        b = {"block_id":"B1","body":{"a":1,"b":2},"path":"/x"}
        self.assertEqual(request_identity(a), request_identity(b))

    def test_plan_then_reload(self):
        td=tempfile.TemporaryDirectory(); self.addCleanup(td.cleanup)
        p=Path(td.name)/"l.json"; l=SpendLedger(p)
        self.assertEqual(l.plan("h","B"),"PLANNED")
        self.assertEqual(SpendLedger(p).get("h").block_id,"B")

    def test_hash_block_collision_fails(self):
        l=self.ledger(); l.plan("h","B1")
        with self.assertRaises(ValueError): l.plan("h","B2")

    def test_dispatch_first_send_ready(self):
        l=self.ledger(); out=dispatch_gate({"request_hash":"h","block_id":"B"},l)
        self.assertTrue(out["dispatch_allowed"])

    def test_dispatch_existing_planned_holds(self):
        l=self.ledger(); req={"request_hash":"h","block_id":"B"}; dispatch_gate(req,l)
        self.assertEqual(dispatch_gate(req,l)["status"],"HOLD_EXISTING_ATTEMPT")

    def test_accepted_requires_response_hash(self):
        l=self.ledger(); l.plan("h","B")
        with self.assertRaises(ValueError): l.transition("h","ACCEPTED")

    def test_accepted_is_immutable(self):
        l=self.ledger(); l.plan("h","B"); l.transition("h","ACCEPTED",response_hash="r")
        with self.assertRaises(ValueError): l.transition("h","REJECTED")

    def test_accepted_dispatch_reuses(self):
        l=self.ledger(); l.plan("h","B"); l.transition("h","ACCEPTED",response_hash="r")
        self.assertEqual(dispatch_gate({"request_hash":"h","block_id":"B"},l)["status"],"REUSE")

    def test_ambiguous_cannot_resend(self):
        l=self.ledger(); l.plan("h","B"); l.transition("h","AMBIGUOUS")
        with self.assertRaises(ValueError): l.transition("h","SENT")

    def test_ambiguous_gate_holds(self):
        l=self.ledger(); l.plan("h","B"); l.transition("h","AMBIGUOUS")
        self.assertEqual(dispatch_gate({"request_hash":"h","block_id":"B"},l)["status"],"HOLD_AMBIGUOUS")

    def test_ambiguous_unknown_charge_holds(self):
        l=self.ledger(); l.plan("h","B"); l.transition("h","AMBIGUOUS")
        self.assertEqual(reconcile_ambiguous(l,"h",provider_confirmed_charge=None)["status"],"HOLD")

    def test_ambiguous_charge_without_response_holds(self):
        l=self.ledger(); l.plan("h","B"); l.transition("h","AMBIGUOUS")
        self.assertEqual(reconcile_ambiguous(l,"h",provider_confirmed_charge=True)["status"],"HOLD")

    def test_ambiguous_charge_with_response_accepts(self):
        l=self.ledger(); l.plan("h","B"); l.transition("h","AMBIGUOUS")
        out=reconcile_ambiguous(l,"h",provider_confirmed_charge=True,response_hash="r",cost=0.12)
        self.assertEqual(out["status"],"ACCEPTED_RECONCILED"); self.assertEqual(l.accepted_cost(),0.12)

    def test_ambiguous_no_charge_rejects(self):
        l=self.ledger(); l.plan("h","B"); l.transition("h","AMBIGUOUS")
        self.assertEqual(reconcile_ambiguous(l,"h",provider_confirmed_charge=False)["status"],"REJECTED_RECONCILED")

    def test_error_auth(self): self.assertEqual(normalize_provider_error(401)["category"],"AUTH")
    def test_error_voice_precedes_404(self): self.assertEqual(normalize_provider_error(404,"voice_missing")["category"],"VOICE")
    def test_error_rate_retry(self): self.assertTrue(normalize_provider_error(429)["retryable"])
    def test_error_500_retry(self): self.assertEqual(retry_decision(normalize_provider_error(500)),"BACKOFF_RETRY")
    def test_response_started_quarantines(self): self.assertEqual(retry_decision(normalize_provider_error(500),response_started=True),"QUARANTINE_AMBIGUOUS")

    def test_capability_pass(self):
        snap={"voices":{"v":{"status":"PASS"}},"models":{"m":{"status":"PASS"}}}
        self.assertEqual(capability_drift({"voice_ids":["v"],"model_ids":["m"]},snap)["status"],"PASS")

    def test_capability_missing_fails_no_substitution(self):
        out=capability_drift({"voice_ids":["v"],"model_ids":["m"]},{"voices":{},"models":{}})
        self.assertEqual(out["status"],"FAIL_DRIFT"); self.assertFalse(out["auto_substitution"])

    def test_capability_failed_status_fails(self):
        snap={"voices":{"v":{"status":"FAIL"}},"models":{"m":{"status":"PASS"}}}
        self.assertEqual(capability_drift({"voice_ids":["v"],"model_ids":["m"]},snap)["failed_voices"],["v"])

    def test_dependency_descendants(self):
        g={"A":["B","C"],"B":["D"],"C":[]}
        self.assertEqual(dependency_descendants(g,["A"]),["B","C","D"])

    def test_dependency_cycle_safe(self):
        g={"A":["B"],"B":["A"]}
        self.assertEqual(dependency_descendants(g,["A"]),["A","B"])

    def test_selective_rerender(self):
        self.assertEqual(selective_rerender(["B2","B2"],["B1","B2"]),["B2"])

    def test_selective_unknown_fails(self):
        with self.assertRaises(ValueError): selective_rerender(["X"],["B"])

    def test_release_gate_holds_without_human_economics(self):
        ev={"provider_preflight":1,"idempotency":1,"ambiguous_recovery":1,"alignment":1,"durable_provenance":1}
        out=release_control_gate(ev); self.assertEqual(out["status"],"HOLD"); self.assertIn("human_review",out["missing"])

    def test_release_control_pass_not_production_ready(self):
        keys=["provider_preflight","idempotency","ambiguous_recovery","alignment","human_review","measured_economics","durable_provenance"]
        out=release_control_gate({k:True for k in keys}); self.assertEqual(out["status"],"PASS_CONTROL_LAYER"); self.assertFalse(out["production_ready"])


if __name__ == '__main__':
    unittest.main()
