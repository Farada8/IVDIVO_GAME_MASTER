import unittest
from tools.ivdivo_proof_chain import validate

def base():
    return {
        "authority_snapshot":{"project_id":"X","authority_id":"A","revision":"r1"},
        "artifacts":[{"artifact_id":"a1","sha256":"abc","readback_sha256":"abc"}],
        "evidence":[{"evidence_id":"e1","source_type":"MACHINE_TEST","status":"PASS","authority_weight":70}],
        "claims":[{"claim_id":"c1","evidence_ids":["e1"],"min_authority_weight":50,"required_artifact_ids":["a1"]}],
        "gates":[{"gate_id":"g1","required_claim_ids":["c1"],"declared_verdict":"PASS"}],
    }

class ProofChainTests(unittest.TestCase):
    def test_happy_path(self):
        self.assertEqual(validate(base())["status"], "PASS")

    def test_hash_mismatch_fails_closed(self):
        p=base(); p["artifacts"][0]["readback_sha256"]="def"
        self.assertEqual(validate(p)["status"], "FAIL_CLOSED")

    def test_human_cannot_be_inferred(self):
        p=base(); p["claims"][0]["requires_human_evidence"]=True; p["gates"][0]["declared_verdict"]="HOLD"
        out=validate(p)
        self.assertEqual(out["status"],"HOLD")
        self.assertEqual(out["claim_results"]["c1"]["reason"],"HUMAN_EVIDENCE_REQUIRED")

    def test_live_provider_cannot_be_machine_test(self):
        p=base(); p["claims"][0]["requires_live_external_evidence"]=True; p["gates"][0]["declared_verdict"]="HOLD"
        self.assertEqual(validate(p)["status"],"HOLD")

    def test_declared_pass_mismatch_fails_closed(self):
        p=base(); p["claims"][0]["requires_human_evidence"]=True
        self.assertEqual(validate(p)["status"],"FAIL_CLOSED")

    def test_duplicate_evidence_fails_closed(self):
        p=base(); p["evidence"].append(dict(p["evidence"][0]))
        self.assertEqual(validate(p)["status"],"FAIL_CLOSED")

    def test_fail_evidence_blocks_claim(self):
        p=base(); p["evidence"].append({"evidence_id":"e2","source_type":"MACHINE_TEST","status":"FAIL","authority_weight":90})
        p["claims"][0]["evidence_ids"].append("e2"); p["gates"][0]["declared_verdict"]="FAIL"
        self.assertEqual(validate(p)["status"],"FAIL")

    def test_deterministic_proof_id(self):
        a=validate(base())["proof_id"]; b=validate(base())["proof_id"]
        self.assertEqual(a,b)

    def test_fake_approval_id_does_not_unlock_gate(self):
        p=base(); p["gates"][0]["human_approval_required"]=True; p["gates"][0]["human_approval_evidence_id"]="missing"; p["gates"][0]["declared_verdict"]="HOLD"
        self.assertEqual(validate(p)["status"],"HOLD")

if __name__ == "__main__":
    unittest.main()
