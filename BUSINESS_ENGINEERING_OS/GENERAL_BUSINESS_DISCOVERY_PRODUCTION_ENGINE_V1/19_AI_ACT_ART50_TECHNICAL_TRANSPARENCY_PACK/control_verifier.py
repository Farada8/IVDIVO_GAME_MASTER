from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import router

PASS_CONTROL = "PASS_CONTROL"
FAIL_CONTROL = "FAIL_CONTROL"
UNKNOWN_CONTROL = "UNKNOWN_CONTROL"
REVIEW_REQUIRED = "REVIEW_REQUIRED"
NOT_ACTIVE = "NOT_ACTIVE"

TECHNICAL_EVIDENCE = {
    "InteractionDisclosureEvidence",
    "PresentationAccessibilityEvidence",
    "MachineReadableMarkingEvidence",
    "ExposureNoticeEvidence",
    "ContentDisclosureEvidence",
    "PublicInterestTextDisclosureEvidence",
}

REVIEW_EVIDENCE = {
    "ObviousnessExceptionDecision",
    "InteractionScopeEvidence",
    "MarkingScopeExceptionDecision",
    "SeparatePersonalDataLegalReview",
    "LawEnforcementExceptionDecision",
    "CreativePresentationDecision",
    "EditorialExceptionEvidence",
}

ACTIVE_ROUTER_STATES = {router.APPLIES, router.APPLIES_SPECIAL_PRESENTATION}
PENDING_ROUTER_STATES = {router.UNKNOWN, router.PENDING_EXCEPTION_REVIEW}


def _control_finding(obligation_id: str, evidence_name: str, state: str, reason: str) -> Dict[str, str]:
    return {
        "obligation_id": obligation_id,
        "evidence_object": evidence_name,
        "state": state,
        "reason": reason,
    }


def verify_case(item: Dict[str, Any]) -> Dict[str, Any]:
    case = item.get("case", {})
    evidence = item.get("evidence", {})
    routed = router.route_case(case)
    findings: List[Dict[str, str]] = []
    review_items: List[Dict[str, str]] = []

    legacy = item.get("legacy_transition_claim")
    if legacy and legacy.get("placed_on_market_before_2026_08_02") is True:
        review_items.append({
            "type": "LEGISLATIVE_REVIEW_REQUIRED",
            "reason": (
                "A pre-2026-08-02 Article 50(2) grandfathering transition is claimed. "
                "Current Commission signing FAQ describes the 2026-12-02 transition as an AI Omnibus proposal that would apply if adopted; do not automate it as operative law."
            ),
        })

    for decision in routed.get("decisions", []):
        status = decision["status"]
        obligation_id = decision["obligation_id"]

        if status in PENDING_ROUTER_STATES:
            review_items.append({
                "type": "SCOPE_OR_EXCEPTION_REVIEW_REQUIRED",
                "obligation_id": obligation_id,
                "reason": decision["reason"],
            })
            continue

        if status not in ACTIVE_ROUTER_STATES:
            continue

        for evidence_name in decision.get("required_evidence", []):
            if evidence_name in REVIEW_EVIDENCE:
                review_items.append({
                    "type": "SEPARATE_REVIEW_PLANE",
                    "obligation_id": obligation_id,
                    "evidence_object": evidence_name,
                    "reason": "This review object is not converted into a technical control PASS by a boolean fixture.",
                })
                continue
            if evidence_name not in TECHNICAL_EVIDENCE:
                review_items.append({
                    "type": "UNCLASSIFIED_EVIDENCE_OBJECT",
                    "obligation_id": obligation_id,
                    "evidence_object": evidence_name,
                    "reason": "Evidence object is outside the verifier allowlist and requires explicit classification.",
                })
                continue

            value = evidence.get(evidence_name)
            if value is True:
                state = PASS_CONTROL
                reason = "Required technical evidence object is explicitly declared present."
            elif value is False:
                state = FAIL_CONTROL
                reason = "Active route requires this technical evidence object and the fixture explicitly declares it absent."
            else:
                state = UNKNOWN_CONTROL
                reason = "Active route requires this technical evidence object but presence/absence is not established."
            findings.append(_control_finding(obligation_id, evidence_name, state, reason))

    if any(f["state"] == FAIL_CONTROL for f in findings):
        overall = "CONTROL_GAPS_FOUND"
    elif review_items or any(f["state"] == UNKNOWN_CONTROL for f in findings):
        overall = "REVIEW_REQUIRED"
    elif findings and all(f["state"] == PASS_CONTROL for f in findings):
        overall = "PASS_TECHNICAL_CONTROLS_DECLARED"
    else:
        overall = NOT_ACTIVE

    result = {
        "case_id": item.get("case_id") or case.get("case_id"),
        "router_status": routed.get("status"),
        "overall": overall,
        "findings": findings,
        "review_items": review_items,
        "legal_compliance_proven": False,
        "independent_verification_proven": False,
        "customer_demand_proven": False,
        "wtp_proven": False,
        "transaction_proven": False,
        "external_action_authorized": False,
    }
    return result


def verify_many(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [verify_case(item) for item in items]


def main() -> int:
    root = Path(__file__).resolve().parent
    payload = json.loads((root / "05_CONTROL_VERIFICATION_FIXTURES.json").read_text(encoding="utf-8"))
    output = {
        "schema": "ivdivo.pew03.control_verification_results/0.1",
        "results": verify_many(payload["cases"]),
        "legal_compliance_proven": False,
        "customer_demand_proven": False,
        "wtp_proven": False,
        "transaction_proven": False,
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
