from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List

ALLOWED_STATES = {
    "PRESENT",
    "ABSENT_VERIFIED",
    "NOT_OBSERVABLE_PUBLICLY",
    "VENDOR_SPECIFIC_UNKNOWN",
    "NOT_APPLICABLE",
}

ALLOWED_ISSUE_CLASSES = {
    "ACTIONABLE_GAP",
    "NOT_OBSERVABLE_PUBLICLY",
    "VENDOR_SPECIFIC_UNKNOWN",
    "NOISE",
}

DIMENSIONS = {
    "official_agentic_discovery": {
        "positive": "DOCUMENTED_AGENTIC_DISCOVERY",
        "verify": "Obtain a current first-party platform/merchant integration statement or authorized integration evidence.",
    },
    "ucp_public_profile": {
        "positive": "UCP_PROFILE_PUBLICLY_OBSERVED",
        "verify": "Fetch the merchant's /.well-known/ucp directly and validate version, services, capabilities, payment handlers and keys; search-engine non-finding is insufficient.",
    },
    "product_data_plane": {
        "positive": "PRODUCT_DATA_PLANE_DOCUMENTED",
        "verify": "Verify the current product feed/catalog integration and freshness path using the relevant platform or authorized merchant data.",
    },
    "protocol_checkout_surface": {
        "positive": "PROTOCOL_CHECKOUT_CHANNEL_OR_CAPABILITY_DOCUMENTED",
        "verify": "Verify the current ACP/UCP checkout capability using merchant-authorized conformance evidence; a human checkout page does not prove an agent checkout interface.",
    },
    "fulfillment_order_state": {
        "positive": "MACHINE_FULFILLMENT_OR_ORDER_STATE_DOCUMENTED",
        "verify": "Verify machine-usable fulfillment options and order lifecycle/state synchronization in the declared protocol surface.",
    },
    "authorization_trust_controls": {
        "positive": "AUTHORIZATION_TRUST_CONTROLS_DOCUMENTED",
        "verify": "Verify signatures, idempotency, request tracing/versioning, permission/intent constraints and key handling through authorized conformance evidence.",
    },
    "payment_handler_boundary": {
        "positive": "PAYMENT_HANDLER_BOUNDARY_DOCUMENTED",
        "verify": "Verify declared/authorized payment-handler configuration and merchant-of-record boundary for the active integration.",
    },
    "agent_discovery_interop": {
        "positive": "AGENT_INTEROP_SURFACE_DOCUMENTED",
        "verify": "Verify only explicitly exposed A2A/MCP/DNS-AID or equivalent discovery/interop surfaces; do not require a protocol merely because it exists in the ecosystem.",
    },
    "evidence_freshness": {
        "positive": "CURRENT_DATED_EVIDENCE_PRESENT",
        "verify": "Refresh the evidence from a current first-party source before making a readiness claim.",
    },
}

GENERIC_ADVICE_BANNED = {
    "improve seo",
    "add more keywords",
    "write better product descriptions",
    "add llms.txt",
    "add schema.org",
    "make the site faster",
}


@dataclass(frozen=True)
class Finding:
    dimension: str
    classification: str
    message: str
    next_verification: str


@dataclass(frozen=True)
class ScanResult:
    fixture_id: str
    disposition: str
    positive_signals: List[str]
    findings: List[Finding]
    generic_seo_signal_ignored: bool
    proof_promotion: bool = False
    external_action_authorized: bool = False

    def to_dict(self) -> dict:
        out = asdict(self)
        return out


def _validate_fixture(fixture: dict) -> None:
    if not fixture.get("fixture_id"):
        raise ValueError("fixture_id is required")
    observations = fixture.get("observations")
    if not isinstance(observations, dict):
        raise ValueError("observations must be an object")
    missing = set(DIMENSIONS) - set(observations)
    extra = set(observations) - set(DIMENSIONS)
    if missing or extra:
        raise ValueError(f"dimension mismatch missing={sorted(missing)} extra={sorted(extra)}")
    for key, state in observations.items():
        if state not in ALLOWED_STATES:
            raise ValueError(f"invalid state for {key}: {state}")


def scan_fixture(fixture: dict) -> ScanResult:
    """Route only admissible protocol evidence. Never infer private backend state.

    `generic_seo_signal` is intentionally ignored and exists as a negative control.
    """
    _validate_fixture(fixture)
    observations: Dict[str, str] = fixture["observations"]

    positives: List[str] = []
    findings: List[Finding] = []

    for dimension, state in observations.items():
        spec = DIMENSIONS[dimension]
        if state == "PRESENT":
            positives.append(spec["positive"])
        elif state == "ABSENT_VERIFIED":
            findings.append(
                Finding(
                    dimension=dimension,
                    classification="ACTIONABLE_GAP",
                    message="Protocol-specific surface is authoritatively verified absent.",
                    next_verification=spec["verify"],
                )
            )
        elif state == "NOT_OBSERVABLE_PUBLICLY":
            findings.append(
                Finding(
                    dimension=dimension,
                    classification="NOT_OBSERVABLE_PUBLICLY",
                    message="Public evidence cannot resolve this merchant-internal or authenticated state.",
                    next_verification=spec["verify"],
                )
            )
        elif state == "VENDOR_SPECIFIC_UNKNOWN":
            findings.append(
                Finding(
                    dimension=dimension,
                    classification="VENDOR_SPECIFIC_UNKNOWN",
                    message="The state depends on platform/onboarding/protocol-specific implementation evidence not currently available.",
                    next_verification=spec["verify"],
                )
            )
        elif state == "NOT_APPLICABLE":
            continue

    has_actionable = any(f.classification == "ACTIONABLE_GAP" for f in findings)
    ucp_present = observations["ucp_public_profile"] == "PRESENT"
    discovery_present = observations["official_agentic_discovery"] == "PRESENT"
    data_present = observations["product_data_plane"] == "PRESENT"
    checkout_present = observations["protocol_checkout_surface"] == "PRESENT"

    if has_actionable:
        disposition = "PROTOCOL_SPECIFIC_GAP_FOUND"
    elif ucp_present:
        disposition = "PUBLIC_PROTOCOL_SURFACE_PRESENT_BACKEND_UNVERIFIED"
    elif discovery_present and data_present and checkout_present:
        disposition = "DISCOVERY_AND_CHANNEL_SIGNAL_BACKEND_UNVERIFIED"
    elif discovery_present and data_present:
        disposition = "DISCOVERY_READY_SIGNAL_CHECKOUT_UNVERIFIED"
    elif discovery_present:
        disposition = "DISCOVERY_SIGNAL_DATA_PLANE_UNVERIFIED"
    else:
        disposition = "EVIDENCE_INCOMPLETE_FAIL_CLOSED"

    return ScanResult(
        fixture_id=fixture["fixture_id"],
        disposition=disposition,
        positive_signals=sorted(positives),
        findings=findings,
        generic_seo_signal_ignored=True,
    )


def scan_many(fixtures: List[dict]) -> List[dict]:
    return [scan_fixture(f).to_dict() for f in fixtures]


def validate_no_generic_advice(results: List[dict]) -> None:
    for result in results:
        text_parts = [result.get("disposition", "")]
        for finding in result.get("findings", []):
            text_parts.extend(
                [finding.get("message", ""), finding.get("next_verification", "")]
            )
        lowered = " ".join(text_parts).lower()
        hits = [phrase for phrase in GENERIC_ADVICE_BANNED if phrase in lowered]
        if hits:
            raise AssertionError(f"generic advice leakage for {result.get('fixture_id')}: {hits}")


def validate_issue_classes(results: List[dict]) -> None:
    for result in results:
        for finding in result.get("findings", []):
            if finding["classification"] not in ALLOWED_ISSUE_CLASSES:
                raise AssertionError(f"unsupported issue class: {finding['classification']}")
