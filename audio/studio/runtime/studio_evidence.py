#!/usr/bin/env python3
"""IVDIVO Audio Studio evidence layer v1.1.

Evidence-only logic for cross-mode benchmark fairness, human performance review,
measured economics and studio release readiness. It does not compile story/director
artifacts, dispatch providers, repair audio, or auto-lock artistic decisions.

Production-authoritative external evidence is receipt-backed and class-validated.
Caller-supplied booleans remain insufficient for provider/human/live/alignment/
economics/durability/cross-project release claims.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from typing import Any, Iterable

from external_evidence_trust import validate_external_evidence

AUDIO_MODES = ("NARRATED", "MULTI_VOICE", "DRAMATIZED")
QUALITY_DIMENSIONS = ("believability", "clarity", "want_more", "fatigue_resistance")
PERFORMANCE_REQUIRED = ("multi_state", "pronunciation", "fatigue", "human_review")
PERFORMANCE_SCOPE_BY_FAMILY = {
    "multi_state": "MULTI_STATE",
    "pronunciation": "PRONUNCIATION",
    "fatigue": "FATIGUE",
    "human_review": "PERFORMANCE",
    "pair": "PAIR",
}


def text_hash(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def build_benchmark_manifest(*, source_id: str, source_hash: str, exact_text: str,
                             variants: list[dict[str, Any]]) -> dict[str, Any]:
    if not source_id or not source_hash or not exact_text:
        raise ValueError("BENCHMARK_SOURCE_REQUIRED")
    modes = [v.get("mode") for v in variants]
    if len(variants) != 3 or set(modes) != set(AUDIO_MODES):
        raise ValueError("BENCHMARK_REQUIRES_EXACT_THREE_MODES")
    exact_hash = text_hash(exact_text)
    normalized = []
    for variant in variants:
        if variant.get("exact_text_hash") != exact_hash:
            raise ValueError(f"BENCHMARK_TEXT_DRIFT:{variant.get('mode')}")
        if variant.get("source_hash") not in (None, source_hash):
            raise ValueError(f"BENCHMARK_SOURCE_DRIFT:{variant.get('mode')}")
        normalized.append({
            "mode": variant["mode"],
            "source_hash": source_hash,
            "exact_text_hash": exact_hash,
            "render_asset_hash": variant.get("render_asset_hash"),
            "duration_seconds": variant.get("duration_seconds"),
            "provider_settings_family": variant.get("provider_settings_family"),
            "voice_binding_version": variant.get("voice_binding_version"),
            "mix_profile": variant.get("mix_profile"),
        })
    return {
        "schema": "IVDIVO_AUDIO_MODE_BENCHMARK_v1",
        "source_id": source_id,
        "source_hash": source_hash,
        "exact_text_hash": exact_hash,
        "variants": sorted(normalized, key=lambda row: AUDIO_MODES.index(row["mode"])),
        "fairness": {
            "same_locked_text": True,
            "same_story_facts": True,
            "same_source_hash": True,
            "human_review_required": True,
            "measured_cost_required": True,
        },
        "status": "READY_FOR_EVALUATION" if all(v["render_asset_hash"] and v["duration_seconds"] for v in normalized)
        else "HOLD_FOR_RENDER_EVIDENCE",
    }


def score_benchmark_variant(*, mode: str, human_scores: dict[str, float],
                            duration_seconds: float | None, provider_cost: float | None,
                            manual_minutes: float | None, manual_hourly_cost: float | None) -> dict[str, Any]:
    if mode not in AUDIO_MODES:
        raise ValueError("UNKNOWN_AUDIO_MODE")
    missing = [key for key in QUALITY_DIMENSIONS if key not in human_scores]
    if missing:
        return {"mode": mode, "status": "HOLD_HUMAN_SCORES", "missing": missing, "composite": None}
    values = [float(human_scores[key]) for key in QUALITY_DIMENSIONS]
    if any(value < 0 or value > 5 for value in values):
        raise ValueError("HUMAN_SCORE_OUT_OF_RANGE")
    if duration_seconds is None or duration_seconds <= 0:
        return {"mode": mode, "status": "HOLD_DURATION", "composite": None}
    if provider_cost is None or manual_minutes is None or manual_hourly_cost is None:
        return {"mode": mode, "status": "HOLD_COST_EVIDENCE", "composite": None}
    if provider_cost < 0 or manual_minutes < 0 or manual_hourly_cost < 0:
        raise ValueError("NEGATIVE_ECONOMIC_INPUT")
    accepted_minutes = duration_seconds / 60.0
    manual_cost = manual_minutes / 60.0 * manual_hourly_cost
    total_cost = provider_cost + manual_cost
    quality = sum(values) / len(values)
    return {
        "mode": mode,
        "status": "PASS_EVIDENCE_COMPLETE",
        "quality_mean_0_5": round(quality, 4),
        "provider_cost": round(provider_cost, 4),
        "manual_cost": round(manual_cost, 4),
        "total_cost": round(total_cost, 4),
        "cost_per_accepted_minute": round(total_cost / accepted_minutes, 4),
        "composite": round(quality, 6),
        "authority_scope": "ANALYTIC_ONLY_UNTIL_RECEIPT_BOUND",
    }


def compare_benchmark(scores: list[dict[str, Any]]) -> dict[str, Any]:
    if len(scores) != 3 or {score.get("mode") for score in scores} != set(AUDIO_MODES):
        raise ValueError("BENCHMARK_SCORE_SET_INCOMPLETE")
    blocked = sorted(score["mode"] for score in scores if score.get("status") != "PASS_EVIDENCE_COMPLETE")
    if blocked:
        return {"status": "HOLD", "blocked_modes": blocked, "winner": None, "auto_select": False}
    best = max(float(score["quality_mean_0_5"]) for score in scores)
    leaders = [score["mode"] for score in scores if float(score["quality_mean_0_5"]) == best]
    return {
        "status": "REVIEW_REQUIRED",
        "quality_leaders": sorted(leaders),
        "winner": None,
        "auto_select": False,
        "scores": scores,
        "law": "Machine may summarize evidence but may not choose final artistic mode.",
    }


@dataclass
class PerformanceEvidence:
    candidate_id: str
    role_id: str
    multi_state: bool = False
    pronunciation: bool = False
    fatigue: bool = False
    human_review: bool = False
    pair: bool | None = None
    human_scores: dict[str, float] | None = None
    hard_fails: list[str] | None = None
    trusted_human_evidence: dict[str, Any] | None = None


def performance_evidence_gate(evidence: PerformanceEvidence, *, pair_required: bool = False) -> dict[str, Any]:
    """Gate voice-lock eligibility through family-specific trusted human receipts.

    The legacy booleans remain useful planning signals, but they can no longer
    make a candidate eligible by themselves.
    """
    missing = [key for key in PERFORMANCE_REQUIRED if not getattr(evidence, key)]
    if pair_required and evidence.pair is not True:
        missing.append("pair")
    if evidence.hard_fails:
        return {
            "status": "FAIL_HARD",
            "missing": sorted(set(missing)),
            "hard_fails": sorted(set(evidence.hard_fails)),
            "machine_may_auto_lock": False,
            "voice_lock": False,
            "production_authoritative": False,
        }

    scores = evidence.human_scores or {}
    if evidence.human_review and not scores:
        missing.append("human_scores")

    receipt_map = evidence.trusted_human_evidence or {}
    required_families = list(PERFORMANCE_REQUIRED)
    if pair_required:
        required_families.append("pair")
    validations: dict[str, Any] = {}
    expected_candidate_hash = text_hash(f"{evidence.role_id}:{evidence.candidate_id}")
    for family in required_families:
        if not getattr(evidence, family if family != "pair" else "pair"):
            continue
        validation = validate_external_evidence(
            "HUMAN_REVIEW",
            receipt_map.get(family),
            expected_scope=PERFORMANCE_SCOPE_BY_FAMILY[family],
        )
        validations[family] = validation
        if not validation.get("verified"):
            missing.append(f"trusted_{family}_evidence")
            continue
        if validation.get("candidate_hash") != expected_candidate_hash:
            validations[family] = {
                **validation,
                "status": "FAIL_CANDIDATE_BINDING",
                "verified": False,
                "expected_candidate_hash": expected_candidate_hash,
            }
            missing.append(f"trusted_{family}_candidate_binding")

    return {
        "status": "ELIGIBLE_FOR_HUMAN_LOCK_DECISION" if not missing else "HOLD",
        "missing": sorted(set(missing)),
        "human_scores": scores,
        "trusted_human_validations": validations,
        "machine_may_auto_lock": False,
        "voice_lock": False,
        "production_authoritative": not missing,
    }


def compress_human_review(flags: list[dict[str, Any]], *, total_duration_seconds: float,
                          max_fraction: float = 0.10, min_seconds: float = 30.0) -> dict[str, Any]:
    if total_duration_seconds <= 0:
        raise ValueError("TOTAL_DURATION_REQUIRED")
    if not (0 < max_fraction <= 1):
        raise ValueError("MAX_FRACTION_INVALID")
    severity_weight = {"FATAL": 1000, "MAJOR": 100, "MINOR": 10, "ADVISORY": 1}
    items = []
    for flag in flags:
        start = float(flag.get("start", 0))
        end = float(flag.get("end", start))
        if start < 0 or end < start:
            raise ValueError("FLAG_INTERVAL_INVALID")
        severity = str(flag.get("severity", "ADVISORY")).upper()
        priority = severity_weight.get(severity, 1) + float(flag.get("confidence", 0)) * 10
        items.append({**flag, "start": start, "end": end, "priority": priority})
    items.sort(key=lambda item: (-item["priority"], item["start"]))
    budget = max(min_seconds, total_duration_seconds * max_fraction)
    selected, used = [], 0.0
    for item in items:
        duration = max(1.0, item["end"] - item["start"])
        if str(item.get("severity", "")).upper() == "FATAL" or not selected or used + duration <= budget:
            selected.append(item)
            used += duration
    return {
        "status": "PASS_REVIEW_PLAN",
        "selected": selected,
        "review_seconds": round(used, 3),
        "review_fraction": round(used / total_duration_seconds, 4),
        "machine_may_clear_release": False,
        "full_blind_listen_required_for_final_acceptance": True,
    }


@dataclass
class EconomicsRecord:
    render_id: str
    mode: str
    generated_seconds: float
    accepted_seconds: float
    provider_cost: float | None
    manual_minutes: float | None
    manual_hourly_cost: float | None
    cache_reused_seconds: float = 0.0
    regeneration_seconds: float = 0.0


def economics_report(records: Iterable[EconomicsRecord]) -> dict[str, Any]:
    rows = list(records)
    if not rows:
        raise ValueError("ECONOMICS_RECORDS_REQUIRED")
    if any(row.mode not in AUDIO_MODES for row in rows):
        raise ValueError("ECONOMICS_UNKNOWN_MODE")
    missing = []
    for row in rows:
        if row.provider_cost is None:
            missing.append(f"{row.render_id}:provider_cost")
        if row.manual_minutes is None:
            missing.append(f"{row.render_id}:manual_minutes")
        if row.manual_hourly_cost is None:
            missing.append(f"{row.render_id}:manual_hourly_cost")
    if missing:
        return {"status": "HOLD_MISSING_EVIDENCE", "missing": sorted(missing)}
    if any(min(row.generated_seconds, row.accepted_seconds, float(row.provider_cost), float(row.manual_minutes),
                   float(row.manual_hourly_cost), row.cache_reused_seconds, row.regeneration_seconds) < 0 for row in rows):
        raise ValueError("NEGATIVE_ECONOMIC_INPUT")
    generated = sum(row.generated_seconds for row in rows)
    accepted = sum(row.accepted_seconds for row in rows)
    if accepted <= 0:
        raise ValueError("NO_ACCEPTED_AUDIO")
    provider_cost = sum(float(row.provider_cost) for row in rows)
    manual_cost = sum(float(row.manual_minutes) / 60.0 * float(row.manual_hourly_cost) for row in rows)
    accepted_minutes = accepted / 60.0
    cache = sum(row.cache_reused_seconds for row in rows)
    regeneration = sum(row.regeneration_seconds for row in rows)
    return {
        "status": "PASS_EVIDENCE_COMPLETE",
        "generated_minutes": round(generated / 60.0, 4),
        "accepted_minutes": round(accepted_minutes, 4),
        "provider_cost": round(provider_cost, 4),
        "manual_cost": round(manual_cost, 4),
        "total_cost": round(provider_cost + manual_cost, 4),
        "cost_per_accepted_minute": round((provider_cost + manual_cost) / accepted_minutes, 4),
        "acceptance_yield": round(accepted / generated, 4) if generated else None,
        "cache_reuse_fraction": round(cache / max(generated + cache, 1e-9), 4),
        "regeneration_fraction": round(regeneration / max(generated, 1e-9), 4),
        "authority_scope": "ANALYTIC_ONLY_UNTIL_DURABLE_ECONOMICS_RECEIPT_BOUND",
    }


def studio_release_evidence_matrix(
    evidence: dict[str, Any],
    *,
    expected_provider: str | None = None,
    provider_max_age_seconds: float = 21600,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Production release-evidence gate.

    Internal deterministic facts remain booleans. Every external class must be
    supplied as its original class-specific receipt payload and is revalidated
    here. A dictionary of all ``True`` values therefore fails closed.
    """
    internal_required = ("locked_source_identity", "production_control_on_main")
    external_required = {
        "provider_preflight_pass": ("AUTH_PROVIDER", None),
        "live_render_provenance": ("LIVE_AUDIO", None),
        "real_alignment_timeline": ("REAL_ALIGNMENT", None),
        "performance_human_pass": ("HUMAN_REVIEW", "PERFORMANCE"),
        "blind_listener_pass": ("HUMAN_REVIEW", "BLIND_LISTENER"),
        "measured_economics": ("MEASURED_ECONOMICS", None),
        "durable_raw_assets": ("DURABLE_RAW_ASSET", None),
        "durable_recovery": ("DURABLE_RECOVERY", None),
        "cross_project_live_portability": ("CROSS_PROJECT_LIVE", None),
    }
    missing = [key for key in internal_required if evidence.get(key) is not True]
    validations: dict[str, Any] = {}
    for key, (evidence_class, scope) in external_required.items():
        validation = validate_external_evidence(
            evidence_class,
            evidence.get(key),
            expected_scope=scope,
            expected_provider=expected_provider if evidence_class == "AUTH_PROVIDER" else None,
            max_age_seconds=provider_max_age_seconds,
            now=now,
        )
        validations[key] = validation
        if not validation.get("verified"):
            missing.append(key)
    return {
        "status": "GO_FOR_FOUNDER_RELEASE_DECISION" if not missing else "HOLD",
        "missing": sorted(set(missing)),
        "external_validations": validations,
        "machine_may_declare_production_ready": False,
        "production_ready": False,
        "production_authoritative_gate": True,
        "law": "External evidence must pass class-specific receipt validation. Even a complete matrix routes to Founder/human release decision; machine evidence never self-promotes artistic product readiness.",
    }
