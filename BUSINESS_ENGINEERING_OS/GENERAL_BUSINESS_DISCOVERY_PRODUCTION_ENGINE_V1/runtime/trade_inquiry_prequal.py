from dataclasses import dataclass
from typing import Optional, Tuple


REQUIRED = (
    "area",
    "property_type",
    "surface",
    "condition",
    "access",
    "photos_available",
    "timing",
    "authority_to_request",
    "contact_consent",
)


@dataclass(frozen=True)
class Inquiry:
    area: Optional[str] = None
    property_type: Optional[str] = None
    surface: Optional[str] = None
    condition: Optional[str] = None
    access: Optional[str] = None
    photos_available: Optional[bool] = None
    timing: Optional[str] = None
    authority_to_request: Optional[bool] = None
    contact_consent: Optional[bool] = None
    structural_issue: bool = False
    specialist_access: bool = False
    configured_area: bool = True


def missing_fields(i: Inquiry) -> Tuple[str, ...]:
    missing = []
    for field in REQUIRED:
        if getattr(i, field) is None:
            missing.append(field)
    return tuple(missing)


def route(i: Inquiry) -> str:
    if i.contact_consent is False or i.authority_to_request is False:
        return "HOLD_CONSENT_OR_AUTHORITY"
    if not i.configured_area:
        return "HOLD_OUTSIDE_AREA"
    if i.structural_issue or i.specialist_access:
        return "OUT_OF_SCOPE_SPECIALIST"
    if missing_fields(i):
        return "NEED_MORE_INFO"
    if i.access in {"unknown", "difficult"} or i.condition in {"unknown", "heavy_failure"}:
        return "SITE_SURVEY_REQUIRED"
    return "PREQUALIFIED_FOR_SURVEY_QUOTE_PREP"


def quote_prep_checklist(i: Inquiry) -> Tuple[str, ...]:
    r = route(i)
    if r not in {"PREQUALIFIED_FOR_SURVEY_QUOTE_PREP", "SITE_SURVEY_REQUIRED"}:
        return tuple()
    base = ["confirm_scope", "measure_area", "confirm_coats_and_prep", "confirm_access", "confirm_exclusions", "capture_photos", "record_acceptance_criteria"]
    if r == "SITE_SURVEY_REQUIRED":
        base.insert(0, "mandatory_site_survey")
    return tuple(base)


def synthetic_manual_minutes(i: Inquiry) -> float:
    # Model for internal comparison only; not an observed operator baseline.
    base = 12.0
    base += 2.0 * len(missing_fields(i))
    if i.access in {None, "unknown", "difficult"}:
        base += 2.0
    if i.condition in {None, "unknown", "heavy_failure"}:
        base += 2.0
    return base


def synthetic_assisted_minutes(i: Inquiry) -> float:
    # Human still reviews the route and quote-prep checklist.
    base = 3.0
    base += 0.5 * len(missing_fields(i))
    if route(i) == "SITE_SURVEY_REQUIRED":
        base += 1.0
    return base


def modeled_time_delta(i: Inquiry) -> float:
    return synthetic_manual_minutes(i) - synthetic_assisted_minutes(i)


def can_claim_real_time_saving(observed_manual_minutes: Optional[float], observed_assisted_minutes: Optional[float], sample_size: int) -> bool:
    return observed_manual_minutes is not None and observed_assisted_minutes is not None and sample_size >= 20
