from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Optional

APPLIES = "APPLIES"
NOT_APPLICABLE = "NOT_APPLICABLE"
UNKNOWN = "UNKNOWN"
PENDING_EXCEPTION_REVIEW = "PENDING_EXCEPTION_REVIEW"
APPLIES_SPECIAL_PRESENTATION = "APPLIES_SPECIAL_PRESENTATION_REGIME"
NOT_APPLICABLE_EXCEPTION = "NOT_APPLICABLE_CONFIRMED_EXCEPTION"

VALID_ROLES = {"PROVIDER", "DEPLOYER", "BOTH"}
VALID_CODE_STATES = {"SIGNED", "NOT_SIGNED", "UNKNOWN"}


@dataclass(frozen=True)
class ObligationDecision:
    obligation_id: str
    status: str
    reason: str
    required_evidence: List[str]

    def to_dict(self) -> dict:
        return asdict(self)


def _role_has(role: str, target: str) -> bool:
    return role == target or role == "BOTH"


def _a50_1(case: dict) -> ObligationDecision:
    if not _role_has(case["role"], "PROVIDER"):
        return ObligationDecision("A50_1", NOT_APPLICABLE, "Actor is not the provider for this system.", [])
    if not case.get("direct_interaction_with_natural_persons", False):
        return ObligationDecision("A50_1", NOT_APPLICABLE, "No direct natural-person interaction declared.", [])
    obvious = case.get("ai_interaction_obvious")
    if obvious is True:
        return ObligationDecision(
            "A50_1",
            PENDING_EXCEPTION_REVIEW,
            "The obviousness exception is fact-sensitive and interpreted restrictively; do not silently skip disclosure.",
            ["ObviousnessExceptionDecision"],
        )
    if obvious is None:
        return ObligationDecision(
            "A50_1", UNKNOWN, "Obviousness of the AI interaction is unresolved.", ["InteractionScopeEvidence"]
        )
    return ObligationDecision(
        "A50_1",
        APPLIES,
        "Provider system directly interacts with natural persons and no obviousness exception is established.",
        ["InteractionDisclosureEvidence", "PresentationAccessibilityEvidence"],
    )


def _a50_2(case: dict) -> ObligationDecision:
    if not _role_has(case["role"], "PROVIDER"):
        return ObligationDecision("A50_2", NOT_APPLICABLE, "Actor is not the provider for this system.", [])
    if not case.get("generates_synthetic_content", False):
        return ObligationDecision("A50_2", NOT_APPLICABLE, "Synthetic audio/image/video/text generation not declared.", [])

    potential_scope_exception = any(
        case.get(k) is True
        for k in [
            "source_code_only",
            "machine_to_machine_only",
            "closed_loop_pre_final_output_only",
            "standard_editing_only",
            "b2b_industrial_exception_claimed",
        ]
    )
    if potential_scope_exception:
        return ObligationDecision(
            "A50_2",
            PENDING_EXCEPTION_REVIEW,
            "A potential marking scope exclusion/exception was claimed; cumulative factual conditions require evidence review.",
            ["MarkingScopeExceptionDecision"],
        )
    return ObligationDecision(
        "A50_2",
        APPLIES,
        "Provider generates in-scope synthetic content and no exclusion is established.",
        ["MachineReadableMarkingEvidence", "PresentationAccessibilityEvidence"],
    )


def _a50_3(case: dict) -> ObligationDecision:
    if not _role_has(case["role"], "DEPLOYER"):
        return ObligationDecision("A50_3", NOT_APPLICABLE, "Actor is not the deployer for this use.", [])
    if not (case.get("emotion_recognition", False) or case.get("biometric_categorisation", False)):
        return ObligationDecision("A50_3", NOT_APPLICABLE, "No emotion-recognition/biometric-categorisation exposure declared.", [])
    return ObligationDecision(
        "A50_3",
        APPLIES,
        "Deployer exposes natural persons to emotion-recognition and/or biometric-categorisation operation.",
        ["ExposureNoticeEvidence", "PresentationAccessibilityEvidence", "SeparatePersonalDataLegalReview"],
    )


def _a50_4_deepfake(case: dict) -> ObligationDecision:
    if not _role_has(case["role"], "DEPLOYER"):
        return ObligationDecision("A50_4_DEEPFAKE", NOT_APPLICABLE, "Actor is not the deployer for this content.", [])
    if not case.get("deepfake", False):
        return ObligationDecision("A50_4_DEEPFAKE", NOT_APPLICABLE, "Deepfake content not declared.", [])
    if case.get("law_enforcement_authorised_exception", False):
        return ObligationDecision(
            "A50_4_DEEPFAKE",
            PENDING_EXCEPTION_REVIEW,
            "Law-enforcement authorisation is claimed and must be verified against the statutory conditions.",
            ["LawEnforcementExceptionDecision"],
        )
    if case.get("evidently_creative_artistic_satirical_fictional", False):
        return ObligationDecision(
            "A50_4_DEEPFAKE",
            APPLIES_SPECIAL_PRESENTATION,
            "Creative/artistic/satirical/fictional context changes the manner of disclosure, not the need for an appropriate disclosure.",
            ["ContentDisclosureEvidence", "CreativePresentationDecision", "PresentationAccessibilityEvidence"],
        )
    return ObligationDecision(
        "A50_4_DEEPFAKE",
        APPLIES,
        "Deployer uses deepfake content without a confirmed exception/special creative regime.",
        ["ContentDisclosureEvidence", "PresentationAccessibilityEvidence"],
    )


def _a50_4_text(case: dict) -> ObligationDecision:
    if not _role_has(case["role"], "DEPLOYER"):
        return ObligationDecision("A50_4_PUBLIC_INTEREST_TEXT", NOT_APPLICABLE, "Actor is not the deployer for this text.", [])
    if not case.get("public_interest_text", False):
        return ObligationDecision("A50_4_PUBLIC_INTEREST_TEXT", NOT_APPLICABLE, "No in-scope public-interest text publication declared.", [])
    reviewed = case.get("human_review_or_editorial_control")
    responsible = case.get("editorial_responsibility_assumed")
    if reviewed is True and responsible is True:
        return ObligationDecision(
            "A50_4_PUBLIC_INTEREST_TEXT",
            NOT_APPLICABLE_EXCEPTION,
            "Human review/editorial control and editorial responsibility are both evidenced in the input.",
            ["EditorialExceptionEvidence"],
        )
    if reviewed is None or responsible is None:
        return ObligationDecision(
            "A50_4_PUBLIC_INTEREST_TEXT",
            UNKNOWN,
            "Editorial exception cannot be resolved because review/control and/or editorial responsibility is unknown.",
            ["EditorialExceptionEvidence"],
        )
    return ObligationDecision(
        "A50_4_PUBLIC_INTEREST_TEXT",
        APPLIES,
        "Public-interest AI text is published without both elements required for the editorial exception.",
        ["PublicInterestTextDisclosureEvidence", "PresentationAccessibilityEvidence"],
    )


def route_case(case: dict) -> dict:
    role = case.get("role")
    if role not in VALID_ROLES:
        return {
            "case_id": case.get("case_id"),
            "status": "HOLD_SCOPE_ROLE_UNKNOWN",
            "decisions": [],
            "code_route": "HOLD",
            "legal_compliance_proven": False,
            "external_action_authorized": False,
        }

    code_state = case.get("code_adherence", "UNKNOWN")
    if code_state not in VALID_CODE_STATES:
        raise ValueError(f"invalid code_adherence: {code_state}")

    decisions = [_a50_1(case), _a50_2(case), _a50_3(case), _a50_4_deepfake(case), _a50_4_text(case)]
    active = [d for d in decisions if d.status in {APPLIES, APPLIES_SPECIAL_PRESENTATION}]
    pending = [d for d in decisions if d.status in {UNKNOWN, PENDING_EXCEPTION_REVIEW}]

    if code_state == "SIGNED":
        code_route = "MAP_SIGNED_CODE_COMMITMENTS_TO_EVIDENCE_NO_AUTOMATIC_COMPLIANCE"
    elif code_state == "NOT_SIGNED":
        code_route = "DOCUMENT_ALTERNATIVE_EQUIVALENTLY_ADEQUATE_MEASURES"
    else:
        code_route = "HOLD_CODE_ROUTE_UNKNOWN"

    if pending:
        status = "HOLD_UNRESOLVED_SCOPE_OR_EXCEPTION"
    elif active:
        status = "IMPLEMENTATION_EVIDENCE_REQUIRED"
    else:
        status = "NO_ACTIVE_ARTICLE50_ROUTE_IN_DECLARED_FACTS"

    return {
        "case_id": case.get("case_id"),
        "status": status,
        "decisions": [d.to_dict() for d in decisions],
        "article_50_5_cross_cutting": bool(active),
        "code_route": code_route,
        "legal_compliance_proven": False,
        "external_action_authorized": False,
    }


def route_many(cases: List[dict]) -> List[dict]:
    return [route_case(c) for c in cases]
