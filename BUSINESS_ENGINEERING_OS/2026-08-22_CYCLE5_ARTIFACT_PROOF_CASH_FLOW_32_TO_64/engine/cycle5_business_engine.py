from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
import json
import math
import re

TRACKING_PREFIXES = ("utm_", "fbclid", "gclid", "mc_")
OFFICIAL_HOST_SUFFIXES = (
    "gov.ie", "enterprise.gov.ie", "seai.ie", "etenders.gov.ie", "ncsc.gov.ie",
    "europa.eu", "ec.europa.eu", "digital-strategy.ec.europa.eu", "neh.gov.ie",
)


def parse_iso(value: str) -> datetime:
    v = value.strip().replace("Z", "+00:00")
    dt = datetime.fromisoformat(v)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def signal_age_days(published_at: str, now: str) -> int:
    delta = parse_iso(now) - parse_iso(published_at)
    return max(0, int(delta.total_seconds() // 86400))


def expiry_state(published_at: str, now: str, sla_days: int) -> dict[str, Any]:
    if sla_days <= 0:
        raise ValueError("sla_days must be > 0")
    age = signal_age_days(published_at, now)
    if age <= sla_days:
        state = "FRESH"
    elif age <= 2 * sla_days:
        state = "REVALIDATE"
    else:
        state = "STALE"
    return {"age_days": age, "sla_days": sla_days, "state": state}


def canonicalize_url(url: str) -> str:
    p = urlparse(url.strip())
    scheme = "https" if p.scheme in {"http", "https", ""} else p.scheme
    host = p.netloc.lower().split("@")[ -1 ]
    if host.startswith("www."):
        host = host[4:]
    q = []
    for k, v in parse_qsl(p.query, keep_blank_values=True):
        lk = k.lower()
        if lk in {"fbclid", "gclid"} or any(lk.startswith(prefix) for prefix in ("utm_", "mc_")):
            continue
        q.append((k, v))
    q.sort()
    path = re.sub(r"/{2,}", "/", p.path or "/")
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    return urlunparse((scheme, host, path, "", urlencode(q), ""))


def is_official_url(url: str) -> bool:
    host = urlparse(canonicalize_url(url)).netloc
    return any(host == suffix or host.endswith("." + suffix) for suffix in OFFICIAL_HOST_SUFFIXES)


def normalized_claim_signature(title: str, claim: str = "") -> str:
    text = re.sub(r"[^a-z0-9]+", " ", f"{title} {claim}".lower()).strip()
    tokens = [t for t in text.split() if t not in {"the", "a", "an", "of", "for", "and", "to", "in"}]
    return sha256(" ".join(tokens).encode("utf-8")).hexdigest()


def syndication_clusters(signals: list[dict[str, Any]]) -> dict[str, list[str]]:
    clusters: dict[str, list[str]] = defaultdict(list)
    for s in signals:
        sig = s.get("correlation_group") or normalized_claim_signature(s.get("title", ""), s.get("claim", ""))
        clusters[sig].append(s["signal_id"])
    return dict(clusters)


def procurement_status(*, published_at: str, deadline_at: str | None, declared_status: str | None, now: str,
                       notice_type: str | None = None, canonical_notice: bool = True,
                       conflicting_deadline: bool = False) -> dict[str, Any]:
    if not canonical_notice or conflicting_deadline:
        return {"status": "REVALIDATE_CANONICAL_NOTICE", "eligible_for_decision": False}
    if notice_type and notice_type.upper() in {"AWARD", "CAN", "CONTRACT_AWARD"}:
        return {"status": "AWARDED_OR_RESULT", "eligible_for_decision": False}
    if not deadline_at:
        return {"status": "UNKNOWN_DEADLINE", "eligible_for_decision": False}
    deadline = parse_iso(deadline_at)
    current = parse_iso(now)
    if current >= deadline:
        return {"status": "CLOSED_OR_PAST_DEADLINE", "eligible_for_decision": False}
    if (declared_status or "").lower() in {"closed", "evaluation", "awarded", "cancelled"}:
        return {"status": declared_status.upper(), "eligible_for_decision": False}
    return {"status": "OPEN", "eligible_for_decision": True, "days_remaining": math.ceil((deadline-current).total_seconds()/86400)}


def build_supersession_graph(records: list[dict[str, Any]]) -> dict[str, Any]:
    by_topic: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in records:
        by_topic[r["topic_key"]].append(r)
    edges = []
    current = {}
    for topic, rows in by_topic.items():
        rows = sorted(rows, key=lambda r: parse_iso(r["published_at"]))
        current[topic] = rows[-1]["record_id"]
        for a, b in zip(rows, rows[1:]):
            edges.append({"from": a["record_id"], "to": b["record_id"], "relation": "SUPERSEDED_BY"})
    return {"current": current, "edges": edges}


def budget_owner_confidence(*, budget_amount: float | None, contracting_authority: str | None,
                            named_budget_owner: str | None, buyer_role_evidence: str | None) -> dict[str, Any]:
    if named_budget_owner and buyer_role_evidence:
        confidence = "HIGH"
    elif contracting_authority:
        confidence = "MEDIUM_ORG_ONLY"
    else:
        confidence = "LOW"
    return {
        "budget_amount": budget_amount,
        "contracting_authority": contracting_authority,
        "named_budget_owner": named_budget_owner,
        "buyer_role_evidence": buyer_role_evidence,
        "budget_owner_confidence": confidence,
        "willingness_to_pay": None,
        "buyer_person_inferred": False,
    }


def verify_access_path(urls: list[str]) -> dict[str, Any]:
    canonical = [canonicalize_url(u) for u in urls]
    official = [u for u in canonical if is_official_url(u)]
    return {"status": "PASS" if official else "HOLD_NO_OFFICIAL_ACCESS_PATH", "official_urls": official, "all_urls": canonical}


def classify_disruption(*, nonconsumer_blocked: bool, incumbent_overperformance: bool,
                        simpler_lower_cost_sufficient: bool, new_context_job: bool = False) -> str:
    if nonconsumer_blocked and (simpler_lower_cost_sufficient or new_context_job):
        return "NEW_MARKET_NONCONSUMPTION"
    if incumbent_overperformance and simpler_lower_cost_sufficient:
        return "LOW_END_OVERSHOT"
    if not nonconsumer_blocked and not incumbent_overperformance:
        return "SUSTAINING_OR_UNCLEAR"
    return "UNDERSPECIFIED_HOLD"


def motivation_ability_change(*, forced_action: bool, funding_support: bool, tooling_support: bool,
                              skills_support: bool) -> dict[str, str]:
    motivation = "UP" if forced_action or funding_support else "UNCHANGED_OR_UNKNOWN"
    ability = "UP" if tooling_support or skills_support else "UNCHANGED_OR_UNKNOWN"
    return {"motivation": motivation, "ability": ability}


def incumbent_asymmetry(*, incumbent_revenue_cannibalization: bool, incumbent_sales_motion_mismatch: bool,
                        entrant_manual_first: bool) -> dict[str, Any]:
    asymmetry = sum([incumbent_revenue_cannibalization, incumbent_sales_motion_mismatch, entrant_manual_first])
    return {"score": asymmetry, "state": "MATERIAL_HYPOTHESIS" if asymmetry >= 2 else "WEAK_OR_UNPROVEN"}


def evaluate_falsifier(*, opportunity_id: str, falsifier: str, observed_kill_evidence: bool) -> dict[str, Any]:
    return {"opportunity_id": opportunity_id, "falsifier": falsifier,
            "verdict": "KILL_OR_RESHAPE" if observed_kill_evidence else "SURVIVES_PUBLIC_FALSIFIER",
            "market_proof": False}


def opportunity_half_life(signal_class: str) -> int:
    table = {
        "TENDER": 14, "GRANT": 30, "PROGRAMME": 60, "POLICY": 120,
        "LAW": 180, "STRATEGY": 180, "BUDGET": 90, "PROJECT": 30,
    }
    return table.get(signal_class.upper(), 30)


def cross_cutting_assumption_queue(opportunities: list[dict[str, Any]], limit: int = 10) -> list[dict[str, Any]]:
    agg: dict[str, dict[str, Any]] = {}
    for o in opportunities:
        for a in o.get("fatal_assumptions", []):
            claim = a["claim"].strip().lower()
            row = agg.setdefault(claim, {"claim": a["claim"], "opportunity_ids": [], "priority_sum": 0.0})
            row["opportunity_ids"].append(o["opportunity_id"])
            row["priority_sum"] += float(a.get("kill_power", 0))*float(a.get("uncertainty",0))*float(a.get("testability",0))
    out = list(agg.values())
    for r in out:
        r["cross_cutting_score"] = round(r["priority_sum"] * (1 + math.log2(max(1, len(set(r["opportunity_ids"]))))), 4)
        r["opportunity_ids"] = sorted(set(r["opportunity_ids"]))
    return sorted(out, key=lambda r: r["cross_cutting_score"], reverse=True)[:limit]


def shared_assumption_graph(opportunities: list[dict[str, Any]]) -> dict[str, list[str]]:
    graph: dict[str, set[str]] = defaultdict(set)
    for o in opportunities:
        for a in o.get("fatal_assumptions", []):
            key = normalized_claim_signature(a.get("claim", ""))
            graph[key].add(o["opportunity_id"])
    return {k: sorted(v) for k, v in graph.items() if len(v) > 1}


def decision_quality_delta(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    fields = sorted(set(before) | set(after))
    changed = [f for f in fields if before.get(f) != after.get(f)]
    resolved = [f for f in changed if before.get(f) in {None, "UNKNOWN", "UNRANKED"} and after.get(f) not in {None, "UNKNOWN", "UNRANKED"}]
    return {"changed_fields": changed, "resolved_unknowns": resolved, "decision_changed": before.get("decision") != after.get("decision")}


def artifact_test(*, sources: int, canonical_sources: int, decisions_before: int, decisions_after: int,
                  unresolved_fatal: int) -> dict[str, Any]:
    useful = canonical_sources >= 1 and decisions_after < decisions_before and unresolved_fatal == 0
    return {"verdict": "PUBLIC_ARTIFACT_PASS" if useful else "PUBLIC_ARTIFACT_HOLD",
            "market_evidence_grade": "E2+", "willingness_to_pay": None,
            "sources": sources, "canonical_sources": canonical_sources,
            "decisions_before": decisions_before, "decisions_after": decisions_after,
            "unresolved_fatal": unresolved_fatal}


def mom_test_filter(question: str) -> dict[str, Any]:
    q = question.strip().lower()
    bad = []
    if any(x in q for x in ["would you", "would your", "do you think", "is this a good idea", "would you pay"]):
        bad.append("HYPOTHETICAL_OR_OPINION")
    if any(x in q for x in ["our product", "my product", "we built", "my idea"]):
        bad.append("PITCH_CONTAMINATION")
    if "how much would" in q:
        bad.append("HYPOTHETICAL_PRICE")
    return {"verdict": "REWRITE" if bad else "PASS_BEHAVIORAL", "issues": bad}


def e3_conversation_evidence(*, participant_role: str, problem_recent_example: str | None,
                             existing_workaround: str | None, cost_or_consequence: str | None,
                             voluntary_followup: bool) -> dict[str, Any]:
    complete = all([participant_role, problem_recent_example, existing_workaround, cost_or_consequence])
    return {"evidence_grade": "E3" if complete else "HOLD_INCOMPLETE_CONVERSATION_EVIDENCE",
            "participant_role": participant_role, "recent_example": problem_recent_example,
            "existing_workaround": existing_workaround, "cost_or_consequence": cost_or_consequence,
            "voluntary_followup": voluntary_followup, "payment_proof": False}


def e4_payment_proof(*, instrument: str | None, amount_eur: float | None, payer_identity_bound: bool,
                     scope_bound: bool, payment_received_or_po: bool) -> dict[str, Any]:
    allowed = {"DEPOSIT", "PAID_PILOT", "PURCHASE_ORDER", "SIGNED_PAID_ORDER"}
    ok = instrument in allowed and amount_eur is not None and amount_eur > 0 and payer_identity_bound and scope_bound and payment_received_or_po
    return {"evidence_grade": "E4" if ok else "HOLD_NO_PAYMENT_PROOF", "instrument": instrument,
            "amount_eur": amount_eur, "payer_identity_bound": payer_identity_bound, "scope_bound": scope_bound}


def pricing_experiment(*, price_eur: float | None = None, external_signal: dict[str, Any] | None = None) -> dict[str, Any]:
    if external_signal is None:
        return {"price_eur": None, "status": "NULL_UNTIL_EXTERNAL_SIGNAL", "evidence": None}
    return {"price_eur": price_eur, "status": "HYPOTHESIS_FROM_EXTERNAL_SIGNAL" if price_eur is not None else "SIGNAL_WITHOUT_PRICE",
            "evidence": external_signal}


def cash_timeline(events: list[dict[str, Any]]) -> dict[str, Any]:
    ordered = sorted(events, key=lambda e: e["day"])
    cash = 0.0
    minimum = 0.0
    series = []
    for e in ordered:
        cash += float(e.get("inflow", 0)) - float(e.get("outflow", 0))
        minimum = min(minimum, cash)
        series.append({**e, "cumulative_cash": round(cash, 2)})
    return {"events": series, "minimum_cash_position": round(minimum, 2), "required_bridge": round(-minimum, 2)}


def reimbursement_bridge(*, eligible_cost_eur: float, reimbursement_eur: float, reimbursement_day: int,
                         supplier_payment_day: int, customer_deposit_eur: float = 0.0) -> dict[str, Any]:
    events = [
        {"day": 0, "inflow": customer_deposit_eur, "outflow": 0, "label": "customer_deposit"},
        {"day": supplier_payment_day, "inflow": 0, "outflow": eligible_cost_eur, "label": "supplier_payment"},
        {"day": reimbursement_day, "inflow": reimbursement_eur, "outflow": 0, "label": "grant_reimbursement"},
    ]
    out = cash_timeline(events)
    out["grant_is_upfront_cash"] = False
    return out


def funding_topology(*, customer_deposit: bool, supplier_terms: bool, reimbursable_grant: bool,
                     debt_committed: bool) -> list[str]:
    routes=[]
    if customer_deposit: routes.append("CUSTOMER_FUNDED")
    if supplier_terms: routes.append("SUPPLIER_FUNDED")
    if reimbursable_grant: routes.append("REIMBURSEMENT_BRIDGE_REQUIRED")
    if debt_committed: routes.append("DEBT_FUNDED")
    return routes or ["UNFUNDED_HOLD"]


def working_capital_stress(*, materials_eur: float | None, labour_eur: float | None,
                           customer_deposit_eur: float | None, receivable_days: int | None,
                           supplier_days: int | None) -> dict[str, Any]:
    if None in {materials_eur, labour_eur, customer_deposit_eur, receivable_days, supplier_days}:
        return {"status": "HOLD_NULL_INPUT", "peak_cash_gap_eur": None}
    direct = float(materials_eur)+float(labour_eur)
    initial_gap = max(0.0, direct-float(customer_deposit_eur))
    timing_risk = max(0, int(receivable_days)-int(supplier_days))
    return {"status": "PASS_MODEL", "peak_cash_gap_eur": round(initial_gap,2), "timing_risk_days": timing_risk}


def contribution_margin(*, revenue_eur: float | None, direct_cost_eur: float | None,
                        founder_hours: float | None, founder_hour_cost_eur: float | None,
                        pickup_rework_cost_eur: float | None = 0.0) -> dict[str, Any]:
    if None in {revenue_eur, direct_cost_eur, founder_hours, founder_hour_cost_eur, pickup_rework_cost_eur}:
        return {"status": "HOLD_NULL_INPUT", "contribution_margin_eur": None, "contribution_margin_pct": None}
    full_variable = float(direct_cost_eur) + float(founder_hours)*float(founder_hour_cost_eur) + float(pickup_rework_cost_eur)
    cm = float(revenue_eur)-full_variable
    pct = None if revenue_eur == 0 else cm/float(revenue_eur)
    return {"status": "PASS_MODEL", "full_variable_cost_eur": round(full_variable,2),
            "contribution_margin_eur": round(cm,2), "contribution_margin_pct": None if pct is None else round(pct,4)}


def queue_capacity(*, demand_units_per_week: float, service_hours_per_unit: float,
                   founder_hours_per_week: float, wip_limit: int = 3) -> dict[str, Any]:
    if service_hours_per_unit <= 0 or founder_hours_per_week <= 0:
        raise ValueError("hours must be > 0")
    capacity = founder_hours_per_week/service_hours_per_unit
    utilization = demand_units_per_week/capacity
    if utilization >= 1:
        state = "OVERLOADED"
    elif utilization >= 0.85:
        state = "HIGH_DELAY_RISK"
    else:
        state = "BOUNDED"
    return {"capacity_units_per_week": round(capacity,3), "utilization": round(utilization,3),
            "state": state, "wip_limit": wip_limit,
            "note": "Queueing delay rises non-linearly as utilization approaches 1; WIP must stay bounded."}


def canonical_hash(value: Any) -> str:
    raw=json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
    return sha256(raw).hexdigest()
