import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scanner import scan


def ready_snapshot():
    product = {
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
    profile = {
        "ucp": {
            "version": "2026-04-08",
            "services": {"dev.ucp.shopping": [{
                "version": "2026-04-08",
                "spec": "https://ucp.dev/specification/overview",
                "transport": "rest",
                "endpoint": "https://merchant.example/ucp/v1",
                "schema": "https://ucp.dev/2026-04-08/services/shopping/rest.openapi.json",
            }]},
            "capabilities": {
                "dev.ucp.shopping.checkout": [{"version": "2026-04-08"}],
                "dev.ucp.shopping.order": [{"version": "2026-04-08"}],
            },
        },
        "keys": [{"kid": "key1", "kty": "EC"}],
    }
    return {
        "merchant_id": "READY",
        "openai_feed": {"evidence_state": "MERCHANT_DECLARED", "products": [product]},
        "ucp": {
            "evidence_state": "PROBED_PUBLIC",
            "well_known_http_status": 200,
            "authentication_required": False,
            "profile": profile,
            "checkout_endpoints": {"create": True, "update": True, "complete": True},
            "identity_path": "guest",
            "order_events": ["created", "shipped", "delivered"],
            "order_request_signing": True,
        },
    }


class ScannerTests(unittest.TestCase):
    def test_ready_snapshot_reaches_conformance_not_approval(self):
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

    def test_missing_order_delivered_is_fail(self):
        snapshot = ready_snapshot()
        snapshot["ucp"]["order_events"] = ["created", "shipped"]
        result = scan(snapshot)
        self.assertTrue(any(f["rule_id"] == "UCP-09" and f["outcome"] == "FAIL" for f in result["findings"]))


if __name__ == "__main__":
    unittest.main()
