from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import date
from typing import Any, Iterable, Optional
from urllib.parse import urlparse
import hashlib
import json

VERSION = "business.opportunity.engine/4.0"
PUBLIC_EVIDENCE_CEILING = 2

PRIMARY_HOST_SUFFIXES = (
    "europa.eu", "ec.europa.eu", "gov.ie", "ncsc.gov.ie", "nis2.gov.ie",
    "seai.ie", "localenterprise.ie", "neh.gov.ie", "growdigital.gov.ie",
)

@dataclass(frozen=True)
class PublicSignal:
    signal_id: str
    title: str
    source_url: str
    jurisdiction: str
    publication_date: Optional[str] = None
    event_date: Optional[str] = None
    application_date: Optional[str] = None
    current: bool = True
    cluster_id: Optional[str] = None
    forced_action: bool = False
    source_kind: str = "OFFICIAL_PRIMARY"

@dataclass(frozen=True)
class Experiment:
    experiment_id: str
    description: str
    founder_cash_eur: int
    outreach_required: bool
    decisive_dimension: str

@dataclass(frozen=True)
class Opportunity:
    opportunity_id: str
    signal_id: str
    buyer_segment: str
    workload: str
    candidate_offer: str
    fatal_assumption: str
    create_vector: str
    broker_vector: str
    acquire_vector: str
    experiment: Experiment
    evidence_level: int = PUBLIC_EVIDENCE_CEILING
    wtp_proven: bool = False
    buyer_commitment: bool = False
    financing_awarded: bool = False
    not_legal_advice: bool = True
    automation_adjudicates_compliance: bool = False
    economics: Optional[dict[str, Any]] = None
    data_path: Optional[str] = None
    audit_source_url: Optional[str] = None


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


def digest(obj: Any) -> str:
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def _parse_iso(value: Optional[str]) -> Optional[date]:
    if value is None:
        return None
    return date.fromisoformat(value)


def is_primary_source(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return any(host == suffix or host.endswith("." + suffix) for suffix in PRIMARY_HOST_SUFFIXES)


def validate_signal(signal: PublicSignal) -> dict[str, Any]:
    if not signal.signal_id or not signal.title or not signal.jurisdiction:
        return {"valid": False, "reason": "MISSING_ID_TITLE_OR_JURISDICTION"}
    if not signal.source_url.startswith("https://"):
        return {"valid": False, "reason": "SOURCE_URL_REQUIRED"}
    if signal.source_kind == "OFFICIAL_PRIMARY" and not is_primary_source(signal.source_url):
        return {"valid": False, "reason": "PRIMARY_SOURCE_HOST_NOT_RECOGNISED"}
    for value in (signal.publication_date, signal.event_date, signal.application_date):
        if value is not None:
            _parse_iso(value)
    if not signal.current:
        return {"valid": False, "reason": "SUPERSEDED_OR_NONCURRENT"}
    return {
        "valid": True,
        "reason": "CURRENT_SIGNAL",
        "date_triad_preserved": True,
        "source_primary": is_primary_source(signal.source_url),
    }


def cluster_evidence_weight(signals: Iterable[PublicSignal]) -> int:
    keys = set()
    for s in signals:
        keys.add(s.cluster_id or s.signal_id)
    return len(keys)


def select_zero_cash_decisive_test(experiments: Iterable[Experiment]) -> Experiment:
    eligible = [e for e in experiments if e.founder_cash_eur == 0 and not e.outreach_required and e.decisive_dimension]
    if not eligible:
        raise ValueError("NO_ZERO_CASH_NO_OUTREACH_DECISIVE_TEST")
    return sorted(eligible, key=lambda e: (len(e.description), e.experiment_id))[0]


def validate_opportunity(signal: PublicSignal, opp: Opportunity, *, no_outreach: bool = True, founder_cash_eur: int = 0) -> dict[str, Any]:
    s = validate_signal(signal)
    if not s["valid"]:
        return {"valid": False, "reason": "INVALID_SIGNAL:" + s["reason"]}
    if opp.signal_id != signal.signal_id:
        return {"valid": False, "reason": "SIGNAL_ID_MISMATCH"}
    required = [opp.buyer_segment, opp.workload, opp.candidate_offer, opp.fatal_assumption,
                opp.create_vector, opp.broker_vector, opp.acquire_vector]
    if not all(isinstance(x, str) and x.strip() for x in required):
        return {"valid": False, "reason": "MISSING_TYPED_OPPORTUNITY_FIELD"}
    if opp.evidence_level > PUBLIC_EVIDENCE_CEILING:
        return {"valid": False, "reason": "PUBLIC_RESEARCH_EVIDENCE_CEILING_EXCEEDED"}
    if opp.wtp_proven or opp.buyer_commitment:
        return {"valid": False, "reason": "PUBLIC_SIGNAL_CANNOT_PROVE_WTP_OR_COMMITMENT"}
    if opp.financing_awarded:
        return {"valid": False, "reason": "PUBLIC_GRANT_SIGNAL_CANNOT_PROVE_AWARD"}
    if not opp.not_legal_advice or opp.automation_adjudicates_compliance:
        return {"valid": False, "reason": "LEGAL_ADJUDICATION_BOUNDARY_VIOLATION"}
    if no_outreach and opp.experiment.outreach_required:
        return {"valid": False, "reason": "OUTREACH_PROHIBITED"}
    if founder_cash_eur == 0 and opp.experiment.founder_cash_eur != 0:
        return {"valid": False, "reason": "NONZERO_FOUNDER_CASH_TEST"}
    if opp.economics is not None:
        for key in ("price", "cac", "gross_margin", "conversion_rate", "sales_cycle_days"):
            if key in opp.economics and opp.economics[key] is None:
                continue
            if key in opp.economics and not isinstance(opp.economics[key], (int, float)):
                return {"valid": False, "reason": "INVALID_ECONOMIC_VALUE"}
    if opp.audit_source_url != signal.source_url:
        return {"valid": False, "reason": "AUDIT_SOURCE_BINDING_REQUIRED"}
    return {
        "valid": True,
        "reason": "BOUNDED_PUBLIC_OPPORTUNITY",
        "evidence_ceiling": PUBLIC_EVIDENCE_CEILING,
        "economics_unknown": opp.economics is None,
        "vectors": {
            "CREATE": opp.create_vector,
            "BROKER": opp.broker_vector,
            "ACQUIRE": opp.acquire_vector,
        },
        "magic_total_score": None,
        "legal_advice": False,
        "decision_hash": digest({"signal": asdict(signal), "opportunity": asdict(opp)}),
    }


def automation_readiness(opp: Opportunity) -> dict[str, Any]:
    if not opp.data_path:
        return {"ready": False, "reason": "DATA_PATH_UNKNOWN"}
    if opp.automation_adjudicates_compliance:
        return {"ready": False, "reason": "ADJUDICATION_PROHIBITED"}
    return {"ready": True, "reason": "EVIDENCE_WORKFLOW_AUTOMATABLE_NOT_LEGAL_ADJUDICATION"}


def grant_bridge(*, eligible: bool, awarded: bool = False) -> dict[str, Any]:
    if awarded:
        return {"eligible": eligible, "awarded": False, "reason": "AWARD_REQUIRES_EXTERNAL_AWARD_EVIDENCE"}
    return {"eligible": eligible, "awarded": False, "reason": "ELIGIBILITY_ONLY"}


def external_capital(kind: str, amount_eur: Optional[float]) -> dict[str, Any]:
    return {"kind": kind, "amount_eur": amount_eur, "free": False, "founder_cash_eur": 0}


def transposition_state(*, eu_rule: str, national_status: str) -> dict[str, Any]:
    return {
        "eu_rule": eu_rule,
        "national_status": national_status,
        "final_national_detail_proven": national_status.upper() == "TRANSPOSED_AND_VERIFIED",
    }


def public_artifact_proxy(url: str) -> dict[str, Any]:
    return {"url": url, "private_internal_process_proven": False, "proxy_only": True}


def decision_delta(before: str, after: str, evidence_ref: str) -> dict[str, Any]:
    changed = before != after
    return {"changed": changed, "before": before, "after": after, "evidence_ref": evidence_ref,
            "progress": "DECISION_DELTA" if changed else "NO_DECISION_PROGRESS"}


def portfolio_wip(opportunity_ids: list[str], cap: int = 5) -> dict[str, Any]:
    if cap <= 0:
        raise ValueError("cap must be positive")
    active = opportunity_ids[:cap]
    queued = opportunity_ids[cap:]
    return {"cap": cap, "active": active, "queued": queued, "bounded": len(active) <= cap}


def self_improvement_candidate(name: str, repetitions: int, evidence_refs: list[str]) -> dict[str, Any]:
    return {
        "name": name,
        "repetitions": repetitions,
        "evidence_refs": list(dict.fromkeys(evidence_refs)),
        "status": "CANDIDATE_DISCOVERY_ONLY",
        "auto_promoted": False,
    }


def validate_library_authority(previous_count: int, delta_ids: list[str], expected_total: int) -> dict[str, Any]:
    unique_delta = list(dict.fromkeys(delta_ids))
    actual = previous_count + len(unique_delta)
    return {"valid": actual == expected_total, "previous": previous_count, "delta": len(unique_delta), "actual": actual}
