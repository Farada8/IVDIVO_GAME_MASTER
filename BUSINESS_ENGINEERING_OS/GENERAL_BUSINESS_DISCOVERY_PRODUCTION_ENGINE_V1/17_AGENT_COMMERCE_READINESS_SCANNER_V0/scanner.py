from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

RULESET_VERSION = "2026-08-22.2"
KNOWN_UCP_VERSIONS = {"2026-04-08", "2026-01-23"}
UCP_TRANSPORTS = {"rest", "mcp", "a2a", "embedded"}
EVIDENCE_STATES = {"OBSERVED_PUBLIC", "PROBED_PUBLIC", "MERCHANT_DECLARED", "UNKNOWN", "NOT_APPLICABLE"}
OUTCOMES = {"PASS", "FAIL", "UNKNOWN", "NOT_APPLICABLE"}

OAI_REQUIRED = (
    "is_eligible_search", "is_eligible_checkout",
    "item_id", "title", "description", "url", "brand", "image_url",
    "price", "availability", "seller_name", "seller_url",
    "return_policy", "target_countries", "store_country",
)
AVAILABILITY = {"in_stock", "out_of_stock", "pre_order", "backorder", "unknown"}
PRICE_RE = re.compile(r"^(?:0|[1-9]\d*)(?:\.\d+)?\s+[A-Z]{3}$")


@dataclass(frozen=True)
class Finding:
    rule_id: str
    outcome: str
    lane: str
    message: str
    evidence_state: str


def finding(rule_id: str, outcome: str, lane: str, message: str, evidence_state: str) -> Finding:
    if outcome not in OUTCOMES:
        raise ValueError(outcome)
    if evidence_state not in EVIDENCE_STATES:
        raise ValueError(evidence_state)
    return Finding(rule_id, outcome, lane, message, evidence_state)


def estate(block: dict[str, Any] | None) -> str:
    state = (block or {}).get("evidence_state", "UNKNOWN")
    return state if state in EVIDENCE_STATES else "UNKNOWN"


def check_feed(snapshot: dict[str, Any]) -> list[Finding]:
    block = snapshot.get("openai_feed") or {}
    state = estate(block)
    if state == "NOT_APPLICABLE":
        return [finding("OAI-FEED-00", "NOT_APPLICABLE", "OPENAI_FEED", "Feed lane marked not applicable.", state)]
    if state == "UNKNOWN":
        return [finding("OAI-FEED-00", "UNKNOWN", "OPENAI_FEED", "No admissible feed observation/declaration.", state)]

    products = block.get("products")
    if not isinstance(products, list) or not products:
        return [finding("OAI-FEED-01", "FAIL", "OPENAI_FEED", "Observed/declared feed has no product rows.", state)]

    out: list[Finding] = []
    for i, product in enumerate(products):
        tag = f"product[{i}]"
        if not isinstance(product, dict):
            out.append(finding("OAI-FEED-02", "FAIL", "OPENAI_FEED", f"{tag} is not an object.", state))
            continue
        missing = [key for key in OAI_REQUIRED if product.get(key) in (None, "", [])]
        out.append(finding(
            "OAI-FEED-02", "FAIL" if missing else "PASS", "OPENAI_FEED",
            f"{tag} missing required fields: {', '.join(missing)}." if missing else f"{tag} contains scanner-required OpenAI feed fields.", state,
        ))
        if product.get("is_eligible_checkout") is True and product.get("is_eligible_search") is not True:
            out.append(finding("OAI-FEED-03", "FAIL", "OPENAI_FEED", f"{tag} checkout=true requires search=true.", state))
        else:
            out.append(finding("OAI-FEED-03", "PASS", "OPENAI_FEED", f"{tag} eligibility dependency is consistent.", state))

        price = product.get("price")
        if price is None:
            out.append(finding("OAI-FEED-04", "UNKNOWN", "OPENAI_FEED", f"{tag} price unavailable.", state))
        elif not isinstance(price, str) or not PRICE_RE.match(price):
            out.append(finding("OAI-FEED-04", "FAIL", "OPENAI_FEED", f"{tag} price must be 'positive-number ISO4217'.", state))
        else:
            amount = float(price.split()[0])
            out.append(finding("OAI-FEED-04", "PASS" if amount > 0 else "FAIL", "OPENAI_FEED", f"{tag} price syntax/positivity checked.", state))

        availability = product.get("availability")
        if availability not in AVAILABILITY:
            out.append(finding("OAI-FEED-05", "FAIL", "OPENAI_FEED", f"{tag} invalid availability={availability!r}.", state))
        elif availability == "pre_order" and not product.get("availability_date"):
            out.append(finding("OAI-FEED-05", "FAIL", "OPENAI_FEED", f"{tag} pre_order requires availability_date.", state))
        else:
            out.append(finding("OAI-FEED-05", "PASS", "OPENAI_FEED", f"{tag} availability dependency checked.", state))

        if product.get("is_eligible_checkout") is True:
            missing_policy = [key for key in ("seller_privacy_policy", "seller_tos") if not product.get(key)]
            out.append(finding(
                "OAI-FEED-06", "FAIL" if missing_policy else "PASS", "OPENAI_FEED",
                f"{tag} checkout=true missing {', '.join(missing_policy)}." if missing_policy else f"{tag} checkout seller policy links present.", state,
            ))
        else:
            out.append(finding("OAI-FEED-06", "NOT_APPLICABLE", "OPENAI_FEED", f"{tag} not marked checkout eligible.", state))
    return out


def _shopping_services(profile: dict[str, Any]) -> list[dict[str, Any]]:
    raw = ((profile.get("ucp") or {}).get("services") or {}).get("dev.ucp.shopping")
    if isinstance(raw, dict):
        return [raw]
    if isinstance(raw, list):
        return [item for item in raw if isinstance(item, dict)]
    return []


def _validate_service_binding(service: dict[str, Any]) -> list[str]:
    transport = service.get("transport")
    missing: list[str] = []
    for key in ("version", "spec", "transport"):
        if not service.get(key):
            missing.append(key)
    if transport not in UCP_TRANSPORTS:
        missing.append(f"supported_transport({transport!r})")
        return missing
    # UCP 2026-04-08 transport-specific profile requirements:
    # REST/MCP need schema+endpoint; A2A needs endpoint; Embedded needs schema.
    if transport in {"rest", "mcp"}:
        for key in ("schema", "endpoint"):
            if not service.get(key):
                missing.append(key)
    elif transport == "a2a":
        if not service.get("endpoint"):
            missing.append("endpoint")
    elif transport == "embedded":
        if not service.get("schema"):
            missing.append("schema")
    return missing


def check_ucp(snapshot: dict[str, Any]) -> list[Finding]:
    block = snapshot.get("ucp") or {}
    state = estate(block)
    if state == "NOT_APPLICABLE":
        return [finding("UCP-00", "NOT_APPLICABLE", "UCP", "UCP lane marked not applicable.", state)]
    if state == "UNKNOWN":
        return [finding("UCP-00", "UNKNOWN", "UCP", "No public UCP probe or merchant declaration.", state)]

    status = block.get("well_known_http_status")
    profile = block.get("profile")
    out: list[Finding] = []
    if status != 200:
        out.append(finding("UCP-01", "FAIL" if status is not None else "UNKNOWN", "UCP", f"/.well-known/ucp HTTP status={status!r}; public 200 required for discovery.", state))
        return out

    if block.get("authentication_required") is True:
        out.append(finding("UCP-02", "FAIL", "UCP", "/.well-known/ucp must be publicly accessible without authentication.", state))
    else:
        out.append(finding("UCP-02", "PASS", "UCP", "Public profile access is not marked auth-gated.", state))

    if not isinstance(profile, dict):
        out.append(finding("UCP-03", "FAIL", "UCP", "HTTP 200 observed but no parsed UCP profile object supplied.", state))
        return out

    ucp = profile.get("ucp") or {}
    version = ucp.get("version")
    if not version:
        out.append(finding("UCP-04", "FAIL", "UCP", "UCP profile has no version.", state))
    elif version in KNOWN_UCP_VERSIONS:
        out.append(finding("UCP-04", "PASS", "UCP", f"UCP version {version} recognized by ruleset.", state))
    else:
        out.append(finding("UCP-04", "UNKNOWN", "UCP", f"UCP version {version} not in ruleset allowlist; refresh spec before judging.", state))

    services = _shopping_services(profile)
    if not services:
        out.append(finding("UCP-05", "FAIL", "UCP", "No dev.ucp.shopping service binding declared.", state))
        transports: set[str] = set()
    else:
        invalid: list[str] = []
        transports = set()
        for idx, service in enumerate(services):
            transport = service.get("transport")
            if isinstance(transport, str):
                transports.add(transport)
            missing = _validate_service_binding(service)
            if missing:
                invalid.append(f"binding[{idx}] {','.join(missing)}")
        out.append(finding(
            "UCP-05", "FAIL" if invalid else "PASS", "UCP",
            "Invalid shopping bindings: " + "; ".join(invalid) if invalid else f"Valid shopping transport bindings: {', '.join(sorted(transports))}.", state,
        ))

    if "payment_handlers" not in ucp:
        out.append(finding("UCP-05P", "FAIL", "UCP", "ucp.payment_handlers registry is required even when empty.", state))
    elif not isinstance(ucp.get("payment_handlers"), dict):
        out.append(finding("UCP-05P", "FAIL", "UCP", "ucp.payment_handlers must be an object registry.", state))
    else:
        out.append(finding("UCP-05P", "PASS", "UCP", "ucp.payment_handlers registry is present.", state))

    capabilities = ucp.get("capabilities") or {}
    checkout = "dev.ucp.shopping.checkout" in capabilities
    out.append(finding("UCP-06", "PASS" if checkout else "FAIL", "UCP", "Checkout capability " + ("declared." if checkout else "not declared for checkout-readiness target."), state))

    if checkout and "rest" in transports:
        endpoints = block.get("checkout_endpoints") or {}
        required = ("create", "update", "complete")
        values = [endpoints.get(key) for key in required]
        if any(value is False for value in values):
            failed = [key for key in required if endpoints.get(key) is False]
            out.append(finding("UCP-07", "FAIL", "UCP", f"REST checkout endpoint probe failed: {', '.join(failed)}.", state))
        elif any(value is None for value in values):
            unknown = [key for key in required if endpoints.get(key) is None]
            out.append(finding("UCP-07", "UNKNOWN", "UCP", f"REST checkout endpoints unprobed: {', '.join(unknown)}.", state))
        else:
            out.append(finding("UCP-07", "PASS", "UCP", "REST create/update/complete checkout endpoints observed available.", state))
    elif checkout:
        out.append(finding("UCP-07", "NOT_APPLICABLE", "UCP", "REST endpoint probes are not applicable to non-REST-only service bindings.", state))
    else:
        out.append(finding("UCP-07", "NOT_APPLICABLE", "UCP", "Checkout endpoint checks require checkout capability.", state))

    identity = block.get("identity_path")
    if identity == "guest":
        out.append(finding("UCP-08", "PASS", "UCP", "Guest checkout path declared/observed by admissible input.", state))
    elif identity == "identity_linking":
        oauth = block.get("oauth_metadata_public")
        outcome = "PASS" if oauth is True else ("FAIL" if oauth is False else "UNKNOWN")
        out.append(finding("UCP-08", outcome, "UCP", "Identity linking requires public OAuth authorization-server metadata.", state))
    elif identity is None:
        out.append(finding("UCP-08", "UNKNOWN", "UCP", "User identification path not supplied; public profile alone may not resolve it.", state))
    else:
        out.append(finding("UCP-08", "FAIL", "UCP", f"Unrecognized identity_path={identity!r}.", state))

    order = "dev.ucp.shopping.order" in capabilities
    if order:
        if "order_events" not in block:
            out.append(finding("UCP-09", "UNKNOWN", "UCP", "Order lifecycle events are not proven by the supplied evidence.", state))
        else:
            events = set(block.get("order_events") or [])
            required_events = {"created", "shipped", "delivered"}
            missing_events = sorted(required_events - events)
            out.append(finding(
                "UCP-09", "FAIL" if missing_events else "PASS", "UCP",
                f"Order lifecycle missing events: {', '.join(missing_events)}." if missing_events else "Order lifecycle covers created/shipped/delivered.", state,
            ))

        webhook = block.get("order_webhook_enabled")
        if webhook is True:
            keys = profile.get("keys") or profile.get("signing_keys")
            out.append(finding("UCP-10", "PASS" if keys else "FAIL", "UCP", "Signing key material " + ("declared." if keys else "missing for declared webhook flow."), state))
            signed = block.get("order_request_signing")
            outcome = "PASS" if signed is True else ("FAIL" if signed is False else "UNKNOWN")
            out.append(finding("UCP-11", outcome, "UCP", "Order webhook request-signing probe/declaration.", state))
        elif webhook is False:
            out.extend([
                finding("UCP-10", "NOT_APPLICABLE", "UCP", "Signing-key webhook check not applicable: webhook flow marked disabled.", state),
                finding("UCP-11", "NOT_APPLICABLE", "UCP", "Webhook signing check not applicable: webhook flow marked disabled.", state),
            ])
        else:
            out.extend([
                finding("UCP-10", "UNKNOWN", "UCP", "Order capability observed but webhook delivery mode is unproven.", state),
                finding("UCP-11", "UNKNOWN", "UCP", "Order capability observed but webhook signing state is unproven.", state),
            ])
    else:
        out.extend([
            finding("UCP-09", "NOT_APPLICABLE", "UCP", "Order capability not declared.", state),
            finding("UCP-10", "NOT_APPLICABLE", "UCP", "Order signing-key check requires a relevant order webhook flow.", state),
            finding("UCP-11", "NOT_APPLICABLE", "UCP", "Order signing probe requires a relevant order webhook flow.", state),
        ])
    return out


def classify(findings: list[Finding]) -> str:
    critical = [item for item in findings if item.outcome != "NOT_APPLICABLE"]
    if any(item.outcome == "FAIL" for item in critical):
        return "BLOCKED_BY_DETERMINISTIC_DEFECT"
    if any(item.outcome == "UNKNOWN" for item in critical):
        return "HOLD_UNRESOLVED_EVIDENCE"
    if critical and all(item.outcome == "PASS" for item in critical):
        return "READY_FOR_PLATFORM_CONFORMANCE_TEST_NOT_APPROVAL"
    return "NO_APPLICABLE_EVIDENCE"


def scan(snapshot: dict[str, Any]) -> dict[str, Any]:
    findings = check_feed(snapshot) + check_ucp(snapshot)
    counts = {key: sum(item.outcome == key for item in findings) for key in sorted(OUTCOMES)}
    return {
        "schema": "ivdivo.agent_commerce.readiness_scan/0.2",
        "ruleset_version": RULESET_VERSION,
        "merchant_id": snapshot.get("merchant_id"),
        "disposition": classify(findings),
        "counts": counts,
        "findings": [asdict(item) for item in findings],
        "proof_boundary": {
            "readiness_not_platform_approval": True,
            "machine_readable_not_checkout_ready": True,
            "public_observation_not_merchant_declaration": True,
            "transport_binding_specific_requirements": True,
            "unknown_not_fail": True,
            "unknown_not_pass": True,
        },
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: scanner.py SNAPSHOT.json", file=sys.stderr)
        return 2
    snapshot = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(json.dumps(scan(snapshot), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
