"""Business Engineering OS Cycle5 public-artifact validator.

Public-only artifacts can structure decisions but cannot manufacture buyer proof.
No third-party dependencies.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List

PA_ORDER = {"PA0": 0, "PA1": 1, "PA2": 2, "PA3": 3, "PA4": 4, "PA5": 5}
PUBLIC_MARKET_GRADES = {"E0", "E1", "E2", "E2+"}


@dataclass
class SourceRef:
    url: str
    authority: str
    observed_at: str
    freshness_status: str = "CURRENT"


@dataclass
class Artifact:
    artifact_id: str
    lane: str
    decision: str
    decision_owner_class: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    unknowns: List[str]
    falsifier: str
    next_action: str
    sources: List[SourceRef]
    sample_data: bool = True
    market_claim_grade: str = "E2+"
    pa_grade: str = "PA0"
    notes: List[str] = field(default_factory=list)


def validate_artifact(a: Artifact) -> List[str]:
    errors: List[str] = []
    if not a.artifact_id:
        errors.append("artifact_id_required")
    if not a.decision:
        errors.append("decision_required")
    if not a.decision_owner_class:
        errors.append("decision_owner_required")
    if not a.falsifier:
        errors.append("falsifier_required")
    if not a.next_action:
        errors.append("next_action_required")
    if not a.sources:
        errors.append("source_required")
    for source in a.sources:
        if not source.url:
            errors.append("source_url_required")
        if not source.authority:
            errors.append("source_authority_required")
        if not source.observed_at:
            errors.append("source_observed_at_required")
    if a.market_claim_grade not in PUBLIC_MARKET_GRADES:
        errors.append("public_artifact_market_claim_exceeds_E2+")
    if PA_ORDER.get(a.pa_grade, 99) > PA_ORDER["PA4"]:
        errors.append("public_only_cannot_reach_PA5")

    forbidden_true_claims = (
        "willingness_to_pay_proven",
        "profitability_proven",
        "finance_approved",
        "procurement_eligible_proven",
        "grant_approved",
    )
    for key in forbidden_true_claims:
        if a.outputs.get(key) is True:
            errors.append(f"unsupported_claim:{key}")
    return sorted(set(errors))


def procurement_sample() -> Artifact:
    return Artifact(
        artifact_id="PA-PROC-001",
        lane="procurement_intelligence",
        decision="Should a contractor spend time on full tender-document review for this opportunity?",
        decision_owner_class="SME contractor / bid manager",
        inputs={
            "resource_id": "8872468",
            "title": "Climate Summer Works: Roof replacements and energy efficiency upgrades at St. Joseph's Secondary School and adjacent former Convent Building, Ballybunion",
            "contracting_authority": "St Joseph's Secondary School (Ballybunion)",
            "published": "2026-08-19T10:33:23+01:00",
            "submission_deadline": "2026-09-02T17:00:00+01:00",
            "estimated_value_eur": 1600000,
            "procedure": "Open",
            "procurement_type": "Works",
            "cpv": ["45260000", "45261210", "45111100", "45321000"],
        },
        outputs={
            "public_scope_match": "POTENTIAL",
            "decision": "PROCEED_TO_FULL_DOCUMENT_REVIEW",
            "bid_decision": "UNKNOWN",
            "willingness_to_pay_proven": False,
            "procurement_eligible_proven": False,
        },
        unknowns=[
            "selection_criteria", "financial_standing", "insurance_limits",
            "experience_requirements", "bonding", "award_weighting",
            "site_visit_rules", "programme_constraints",
        ],
        falsifier="Full tender documents show mandatory qualifications or delivery constraints incompatible with the verified supplier profile.",
        next_action="Download and extract the full tender pack before any BID/NO-BID recommendation.",
        sources=[SourceRef(
            "https://www.etenders.gov.ie/epps/cft/prepareViewCfTWS.do?resourceId=8872468",
            "eTenders / Government of Ireland", "2026-08-22"
        )],
        pa_grade="PA3",
    )


def retrofit_sample() -> Artifact:
    return Artifact(
        artifact_id="PA-RETRO-001",
        lane="retrofit_orchestration",
        decision="Which SEAI route should a homeowner investigate first: individual grants or a One Stop Shop?",
        decision_owner_class="Homeowner / retrofit coordinator",
        inputs={
            "property_case": "SAMPLE_ONLY", "owner_status": "UNKNOWN",
            "mprn": "UNKNOWN", "build_year": "UNKNOWN", "existing_ber": "UNKNOWN",
            "target_measures": "UNKNOWN", "budget_eur": "UNKNOWN",
        },
        outputs={
            "route": "INPUTS_REQUIRED_BEFORE_ROUTE",
            "rules": [
                "Grant approval must be in place before works start.",
                "Individual grants require an SEAI registered contractor for the relevant measure.",
                "One Stop Shop manages assessment, grant application, contractor works and follow-up BER.",
                "Complete One Stop Shop upgrade targets at least B BER.",
            ],
            "registered_oss_public_count": 31,
            "willingness_to_pay_proven": False,
            "finance_approved": False,
        },
        unknowns=[
            "property_eligibility", "technical_assessment", "measure_sequence",
            "quotes", "contractor_capacity", "loan_eligibility",
        ],
        falsifier="Property facts or updated SEAI rules make the assumed route unavailable, technically inappropriate or financially unsuitable.",
        next_action="Collect MPRN, build/occupation year, dwelling type, BER, measures and budget, then route against current SEAI rules.",
        sources=[
            SourceRef("https://www.seai.ie/grants/home-energy-grants/one-stop-shop", "SEAI", "2026-08-22"),
            SourceRef("https://www.seai.ie/grants/home-energy-grants/individual-grants/support-for-individual-grants", "SEAI", "2026-08-22"),
            SourceRef("https://www.seai.ie/grants/find-a-registered-professional/one-stop-shop-providers", "SEAI", "2026-08-22"),
        ],
        pa_grade="PA3",
    )


def sme_ai_sample() -> Artifact:
    return Artifact(
        artifact_id="PA-AI-001",
        lane="sme_ai_workflow",
        decision="Which post-Digital-for-Business workflow/software opportunities should a small enterprise scope for Grow Digital?",
        decision_owner_class="Small enterprise owner / implementation adviser",
        inputs={
            "business_case": "SAMPLE_ONLY", "paid_employees": 8,
            "trading_months": 18, "digital_for_business_completed_months_ago": 12,
            "enterprise_ireland_or_ida_client": False, "solvent_assumption": True,
            "software_new_to_business": True,
        },
        outputs={
            "preliminary_scheme_path": "POTENTIALLY_ELIGIBLE_IF_ASSUMPTIONS_VERIFIED",
            "grant_rate": 0.50, "grant_min_eur": 500, "grant_max_eur": 5000,
            "candidate_categories": [
                "CRM", "job_tracking", "workflow_management", "e-invoicing",
                "cloud_accounting", "BIM", "analytics_AI",
            ],
            "training_configuration_share_max": 0.50,
            "willingness_to_pay_proven": False,
        },
        unknowns=[
            "LEO_confirmation", "financial_statement_review", "specific_software_eligibility",
            "project_cost", "implementation_scope", "existing_system_inventory",
        ],
        falsifier="LEO review or project facts show the enterprise/expenditure is ineligible, software is not new, or free/subsidised support already supplies the same implementation sufficiently.",
        next_action="Verify the Digital for Business report and map one high-friction workflow to eligible off-the-shelf software plus bounded configuration/training.",
        sources=[
            SourceRef("https://www.localenterprise.ie/portal/growdigital/grow-digital-grant.html", "Local Enterprise Office", "2026-08-22"),
            SourceRef("https://www.localenterprise.ie/portal/growdigital/who-is-eligible-/", "Local Enterprise Office", "2026-08-22"),
        ],
        pa_grade="PA3",
    )


def current_portfolio() -> List[Artifact]:
    return [procurement_sample(), retrofit_sample(), sme_ai_sample()]
