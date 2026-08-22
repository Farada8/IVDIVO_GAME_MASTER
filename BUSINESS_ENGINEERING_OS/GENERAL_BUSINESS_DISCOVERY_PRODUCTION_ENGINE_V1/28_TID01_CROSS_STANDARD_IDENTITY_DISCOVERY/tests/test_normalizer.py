import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("tid01_normalizer", ROOT / "normalizer.py")
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MOD)
MANIFEST = json.loads((ROOT / "01_PUBLIC_FIXTURE_MANIFEST.json").read_text(encoding="utf-8"))
RESULT = MOD.run(MANIFEST)


class TID01Canaries(unittest.TestCase):
    def test_public_fixture_count(self):
        self.assertEqual(set(MANIFEST["fixtures"]), {"a2a_0_3", "ans", "dns_aid", "mcp_registry"})

    def test_a2a_well_known_path_drift_is_real(self):
        self.assertEqual(MANIFEST["a2a_paths"]["0.2.6"], "/.well-known/agent.json")
        self.assertEqual(MANIFEST["a2a_paths"]["0.3.0"], "/.well-known/agent-card.json")
        self.assertNotEqual(MANIFEST["a2a_paths"]["0.2.6"], MANIFEST["a2a_paths"]["0.3.0"])

    def test_a2a_agent_and_protocol_versions_are_separate(self):
        a2a = RESULT["normalized"]["a2a_0_3"]["identity"]
        self.assertEqual(a2a["protocol_version"], "0.3.0")
        self.assertEqual(a2a["agent_version"], "1.2.0")

    def test_ans_version_is_bound_to_versioned_identity(self):
        ans = RESULT["normalized"]["ans"]["identity"]
        self.assertEqual(ans["agent_version"], "1.2.0")
        self.assertEqual(ans["canonical_id"], "ans://v1.2.0.route.example.com")
        self.assertEqual(ans["identity_anchor_kind"], "FQDN_PROOF_OF_CONTROL_PLUS_VERSIONED_ANS_NAME")

    def test_trust_dimensions_do_not_collapse(self):
        a2a = RESULT["normalized"]["a2a_0_3"]["trust_evidence"]
        ans = RESULT["normalized"]["ans"]["trust_evidence"]
        dns = RESULT["normalized"]["dns_aid"]["trust_evidence"]
        self.assertEqual(a2a["card_signature"], "PRESENT")
        self.assertEqual(ans["domain_control"], "PROVEN_BY_ANS_PROFILE")
        self.assertEqual(ans["transparency_receipt"], "PRESENT")
        self.assertEqual(dns["integrity_digest"], "PRESENT")
        self.assertNotEqual(a2a, ans)

    def test_mcp_static_registry_does_not_claim_live_tools(self):
        mcp = RESULT["normalized"]["mcp_registry"]["capability_evidence"]
        self.assertEqual(mcp["source_type"], "STATIC_SERVER_JSON_METADATA")
        self.assertTrue(mcp["live_introspection_required"])
        self.assertEqual(mcp["static_items"], [])

    def test_mcp_installable_package_is_not_remote_endpoint(self):
        roles = {x["role"] for x in RESULT["normalized"]["mcp_registry"]["endpoints"]}
        self.assertEqual(roles, {"REMOTE_MCP", "INSTALLABLE_PACKAGE"})

    def test_normalizer_does_not_invent_a2a_global_id(self):
        self.assertIsNone(RESULT["normalized"]["a2a_0_3"]["identity"]["canonical_id"])
        self.assertIsNotNone(RESULT["normalized"]["ans"]["identity"]["canonical_id"])

    def test_all_predeclared_finding_classes_fire(self):
        ids = {x["id"] for x in RESULT["findings"]}
        self.assertEqual(ids, {"F001", "F002", "F003", "F004", "F005", "F006"})
        self.assertEqual(RESULT["finding_count"], 6)
        self.assertTrue(RESULT["semantic_gap_found"])

    def test_proof_boundary_stays_closed(self):
        p = RESULT["proof_boundary"]
        self.assertEqual(p["buyer_demand"], "UNPROVEN")
        self.assertEqual(p["wtp"], "UNKNOWN")
        self.assertIsNone(p["market_winner"])
        self.assertFalse(p["external_action_authorized"])


if __name__ == "__main__":
    unittest.main()
