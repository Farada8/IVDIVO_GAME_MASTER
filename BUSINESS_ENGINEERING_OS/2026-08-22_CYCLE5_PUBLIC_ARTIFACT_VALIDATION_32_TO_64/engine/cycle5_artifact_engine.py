from dataclasses import dataclass
from typing import Any, Dict, List, Optional

PUBLIC_MAX_EVIDENCE = "E2+"

@dataclass(frozen=True)
class ArtifactResult:
    status: str
    reasons: List[str]
    evidence_ceiling: str = PUBLIC_MAX_EVIDENCE


def require_public_source(record: Dict[str, Any]) -> List[str]:
    failures = []
    if not record.get("source_url") and not record.get("source_ref"):
        failures.append("SOURCE_REQUIRED")
    if not record.get("source_date"):
        failures.append("SOURCE_DATE_REQUIRED")
    return failures


def validate_public_artifact(record: Dict[str, Any]) -> ArtifactResult:
    failures = require_public_source(record)
    if not record.get("decision"):
        failures.append("DECISION_REQUIRED")
    if record.get("wtp_proven") is True:
        failures.append("PUBLIC_ARTIFACT_CANNOT_PROVE_WTP")
    if record.get("payment_proven") is True:
        failures.append("PUBLIC_ARTIFACT_CANNOT_PROVE_PAYMENT")
    return ArtifactResult("FAIL" if failures else "PASS", failures)


def procurement_fit_vector(opportunity: Dict[str, Any], capability: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "deadline_known": bool(opportunity.get("deadline")),
        "estimated_value": opportunity.get("estimated_value"),
        "sector_match": None if capability.get("sectors") is None else opportunity.get("sector") in capability["sectors"],
        "geography_match": None if capability.get("geographies") is None else opportunity.get("geography") in capability["geographies"],
        "qualification_known": opportunity.get("qualification_known"),
        "fatal_unknowns": [
            k for k in ("qualification_known", "insurance_required", "turnover_threshold", "framework_access")
            if opportunity.get(k) is None
        ],
    }


def retrofit_route(property_info: Dict[str, Any]) -> Dict[str, Any]:
    year = property_info.get("construction_year")
    whole_house = property_info.get("whole_house")
    welfare_eligible = property_info.get("warmer_homes_eligible")
    if welfare_eligible is True:
        return {"route": "FULLY_FUNDED_WARMER_HOMES", "cash_timing": "SCHEME_FUNDED", "needs_specialist": False}
    if year is not None and year < 1940:
        return {
            "route": "TRADITIONAL_HOME_PILOT",
            "cash_timing": "OSS_GRANT_DEDUCTED_UPFRONT",
            "needs_specialist": True,
            "required_specialist": "Traditional Building Professional",
        }
    if whole_house is True:
        return {"route": "ONE_STOP_SHOP", "cash_timing": "OSS_GRANT_DEDUCTED_UPFRONT", "needs_specialist": False}
    if whole_house is False:
        return {"route": "INDIVIDUAL_GRANTS", "cash_timing": "GRANT_AFTER_COMPLETED_WORKS", "needs_specialist": False}
    return {"route": "ROUTE_UNRESOLVED", "cash_timing": None, "needs_specialist": None}


def ai_support_substitution(business: Dict[str, Any]) -> Dict[str, Any]:
    generic = business.get("offer_type") == "GENERIC_DIGITAL_DIAGNOSTIC"
    leo_eligible = business.get("leo_eligible")
    completed = business.get("digital_for_business_completed")
    return {
        "public_substitute_risk": "HIGH" if generic and leo_eligible is not False else "LOWER",
        "grow_digital_precondition_known": completed is not None,
        "grow_digital_precondition_met": completed is True,
        "recommended_positioning": "SECTOR_WORKFLOW_EVIDENCE_AND_IMPLEMENTATION_BACKLOG" if generic else "KEEP_SPECIFIC_IMPLEMENTATION_SCOPE",
    }


def artifact_decision_utility(before: Optional[str], after: Optional[str]) -> Dict[str, Any]:
    if not before or not after:
        return {"decision_delta": None, "useful": None}
    changed = before.strip() != after.strip()
    return {"decision_delta": changed, "useful": changed}


def validate_wip(items: List[Dict[str, Any]]) -> ArtifactResult:
    primary = sum(1 for x in items if x.get("role") == "PRIMARY")
    pilots = sum(1 for x in items if x.get("role") == "PILOT")
    failures = []
    if primary > 1:
        failures.append("PRIMARY_WIP_GT_1")
    if pilots > 2:
        failures.append("PILOT_WIP_GT_2")
    if primary + pilots > 3:
        failures.append("ACTIVE_WIP_GT_3")
    return ArtifactResult("FAIL" if failures else "PASS", failures)


def self_improvement_disposition(observation: Dict[str, Any]) -> Dict[str, Any]:
    if observation.get("auto_promote") is True:
        return {"status": "REJECT", "reason": "AUTO_PROMOTION_FORBIDDEN"}
    if not observation.get("evidence"):
        return {"status": "HOLD", "reason": "EVIDENCE_REQUIRED"}
    return {"status": "CANDIDATE", "reason": "ROUTE_TO_SELF_IMPROVEMENT_V2"}
