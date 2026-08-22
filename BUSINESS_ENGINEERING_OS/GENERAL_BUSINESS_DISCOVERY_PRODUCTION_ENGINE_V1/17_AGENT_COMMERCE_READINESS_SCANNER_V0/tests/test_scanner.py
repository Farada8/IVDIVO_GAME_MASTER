import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scanner import scan


def ready_product():
    return {
        "is_eligible_search": True,
        "is_eligible_checkout": True,
        "item_id": "SKU1",
        "title": "Widget",
        "description": "Useful widget",
        "url": "https://merchant.example/p/SKU1",
        "brand": "Example",
        "image_url": "https://merchant.example/i/SKU1.png",
        "price": "19.99 EUR",
        "availability": "in_stock",
        "seller_name": "Example Store",
        "seller_url": "https://merchant.example",
        "seller_privacy_policy": "https://merchant.example/privacy",
        "seller_tos": "https://merchant.example/terms",
        "return_policy": "https://merchant.example/returns",
        "target_countries": ["IE"],
        "store_country": "IE",
    }


def service(transport="rest"):
    base = {
        "version": "2026-04-08",
        "spec": "https://ucp.dev/2026-04-08/specification/overview",
        "transport": transport,
    }
    if transport == "rest":
        base.update(schema="https://ucp.dev/2026-04-08/services/shopping/rest.openapi.json", endpoint="https://merchant.example/ucp/v1")
    elif transport == "mcp":
        base.update(schema="https://ucp.dev/2026-04-08/services/shopping/mcp.openrpc.json", endpoint="https://merchant.example/ucp/mcp")
    elif transport == "a2a":
        base.update(endpoint="https://merchant.example/.well-known/agent-card.json")
    elif transport == "embedded":
        base.update(schema="https://ucp.dev/2026-04-08/services/shopping/embedded.openrpc.json")
    return base


def ready_snapshot(transport="rest", include_order=True):
    capabilities = {"dev.ucp.shopping.checkout": [{"version": "2026-04-08"}]}
    if include_order:
        capabilities["dev.ucp.shopping.order"] = [{"version": "2026-04-08"}]
    profile = {
        "ucp": {
            "version": "2026-04-08",
            "services": {"dev.ucp.shopping": [service(transport)]},
            "capabilities": capabilities,
            "payment_handlers": {},
        },
        "keys": [{"kid": "key1", "kty": "EC"}],
    }
    ucp = {
        "evidence_state": "MERCHANT_DECLARED",
        "well_known_http_status": 200,
        "authentication_required": False,
        "profile": profile,
        "identity_path": "guest",
    }
    if transport == "rest":
        ucp["checkout_endpoints"] = {"create": True, "update": True, "complete": True}
    if include_order:
        ucp.update(
            order_events=["created", "shipped", "delivered"],
            order_webhook_enabled=True,
            order_request_signing=True,
        )
    return {
        "merchant_id": "READY",
        "openai_feed": {"evidence_state": "MERCHANT_DECLARED", "products": [ready_product()]},
        "ucp": ucp,
    }


class ScannerTests(unittest.TestCase):
    def test_ready_rest_snapshot_reaches_conformance_not_approval(self):
        result = scan(ready_snapshot())
        self.assertEqual(result["disposition"], "READY_FOR_PLATFORM_CONFORMANCE_TEST_NOT_APPROVAL")
        self.assertTrue(result["proof_boundary"]["readiness_not_platform_approval"])

    def test_unknown_is_hold_not_fail(self):
        result = scan({"merchant_id": "U", "openai_feed": {"evidence_state": "UNKNOWN"}, "ucp": {"evidence_state": "UNKNOWN"}})
        self.assertEqual(result["disposition"], "HOLD_UNRESOLVED_EVIDENCE")
        self.assertEqual(result["counts"]["FAIL"], 0)

    def test_missing_required_feed_field_is_defect(self):
        snapshot = ready_snapshot()
        del snapshot["openai_feed"]["products"][0]["return_policy"]
        result = scan(snapshot)
        self.assertEqual(result["disposition"], "BLOCKED_BY_DETERMINISTIC_DEFECT")
        self.assertTrue(any(f["rule_id"] == "OAI-FEED-02" and f["outcome"] == "FAIL" for f in result["findings"]))

    def test_checkout_requires_search(self):
        snapshot = ready_snapshot()
        snapshot["openai_feed"]["products"][0]["is_eligible_search"] = False
        result = scan(snapshot)
        self.assertTrue(any(f["rule_id"] == "OAI-FEED-03" and f["outcome"] == "FAIL" for f in result["findings"]))

    def test_ucp_404_is_fail(self):
        snapshot = ready_snapshot()
        snapshot["ucp"] = {"evidence_state": "PROBED_PUBLIC", "well_known_http_status": 404}
        result = scan(snapshot)
        self.assertTrue(any(f["rule_id"] == "UCP-01" and f["outcome"] == "FAIL" for f in result["findings"]))

    def test_identity_linking_without_oauth_metadata_fails(self):
        snapshot = ready_snapshot()
        snapshot["ucp"]["identity_path"] = "identity_linking"
        snapshot["ucp"]["oauth_metadata_public"] = False
        result = scan(snapshot)
        self.assertTrue(any(f["rule_id"] == "UCP-08" and f["outcome"] == "FAIL" for f in result["findings"]))

    def test_unrecognized_ucp_version_is_unknown_not_fail(self):
        snapshot = ready_snapshot()
        snapshot["ucp"]["profile"]["ucp"]["version"] = "2099-01-01"
        result = scan(snapshot)
        self.assertTrue(any(f["rule_id"] == "UCP-04" and f["outcome"] == "UNKNOWN" for f in result["findings"]))
        self.assertNotEqual(result["disposition"], "READY_FOR_PLATFORM_CONFORMANCE_TEST_NOT_APPROVAL")

    def test_missing_order_delivered_is_fail_when_explicitly_declared(self):
        snapshot = ready_snapshot()
        snapshot["ucp"]["order_events"] = ["created", "shipped"]
        result = scan(snapshot)
        self.assertTrue(any(f["rule_id"] == "UCP-09" and f["outcome"] == "FAIL" for f in result["findings"]))

    def test_missing_payment_handlers_registry_is_fail(self):
        snapshot = ready_snapshot()
        del snapshot["ucp"]["profile"]["ucp"]["payment_handlers"]
        result = scan(snapshot)
        self.assertTrue(any(f["rule_id"] == "UCP-05P" and f["outcome"] == "FAIL" for f in result["findings"]))

    def test_mcp_transport_is_valid_and_rest_probe_not_applicable(self):
        snapshot = ready_snapshot("mcp", include_order=False)
        result = scan(snapshot)
        self.assertFalse(any(f["rule_id"] == "UCP-05" and f["outcome"] == "FAIL" for f in result["findings"]))
        self.assertTrue(any(f["rule_id"] == "UCP-07" and f["outcome"] == "NOT_APPLICABLE" for f in result["findings"]))

    def test_a2a_transport_does_not_require_schema(self):
        result = scan(ready_snapshot("a2a", include_order=False))
        self.assertFalse(any(f["rule_id"] == "UCP-05" and f["outcome"] == "FAIL" for f in result["findings"]))

    def test_embedded_transport_does_not_require_endpoint(self):
        result = scan(ready_snapshot("embedded", include_order=False))
        self.assertFalse(any(f["rule_id"] == "UCP-05" and f["outcome"] == "FAIL" for f in result["findings"]))

    def test_public_profile_does_not_fail_hidden_order_events(self):
        snapshot = ready_snapshot("rest", include_order=True)
        snapshot["ucp"]["evidence_state"] = "PROBED_PUBLIC"
        snapshot["ucp"].pop("order_events")
        snapshot["ucp"].pop("order_webhook_enabled")
        snapshot["ucp"].pop("order_request_signing")
        result = scan(snapshot)
        self.assertFalse(any(f["rule_id"] in {"UCP-09", "UCP-10", "UCP-11"} and f["outcome"] == "FAIL" for f in result["findings"]))
        self.assertTrue(any(f["rule_id"] == "UCP-09" and f["outcome"] == "UNKNOWN" for f in result["findings"]))

    def test_google_signing_keys_alias_is_accepted_for_webhook(self):
        snapshot = ready_snapshot()
        snapshot["ucp"]["profile"]["signing_keys"] = snapshot["ucp"]["profile"].pop("keys")
        result = scan(snapshot)
        self.assertTrue(any(f["rule_id"] == "UCP-10" and f["outcome"] == "PASS" for f in result["findings"]))


if __name__ == "__main__":
    unittest.main()
