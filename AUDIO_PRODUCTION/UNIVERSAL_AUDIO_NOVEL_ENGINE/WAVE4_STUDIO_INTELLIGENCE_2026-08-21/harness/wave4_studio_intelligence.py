from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
from typing import Any, Iterable
import json
import math

AUDIO_MODES = ("NARRATED", "MULTI_VOICE", "DRAMATIZED")
FOUNDER_MARKERS = (
    "BELIEVE", "DON'T BELIEVE", "BORING", "CONFUSING", "WRITER TALK",
    "PERFORMANCE WRONG", "STRONG", "WANT MORE"
)
DIAGNOSIS_CLASSES = (
    "PERFORMANCE_DEFECT", "WRITING_DEFECT", "ADAPTATION_DEFECT",
    "TRANSLATION_DEFECT", "CONTEXT_REQUIRED", "NO_DEFECT"
)
DIRECTOR_DOMAINS = ("PERFORMANCE", "PAUSE", "MIC", "FOLEY", "AMBIENCE", "MUSIC", "SILENCE")
LOCK_EVIDENCE = ("multi_state", "pronunciation", "fatigue", "human_review")


def canonical_hash(obj: Any) -> str:
    return sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def build_benchmark_manifest(*, source_id: str, source_hash: str, exact_text: str, variants: list[dict[str, Any]]) -> dict[str, Any]:
    if not source_id or not source_hash or not exact_text:
        raise ValueError("BENCHMARK_SOURCE_REQUIRED")
    modes = [v.get("mode") for v in variants]
    if sorted(modes) != sorted(AUDIO_MODES):
        raise ValueError("BENCHMARK_REQUIRES_EXACT_THREE_MODES")
    if len(set(modes)) != 3:
        raise ValueError("BENCHMARK_DUPLICATE_MODE")
    exact_hash = sha256(exact_text.encode("utf-8")).hexdigest()
    normalized = []
    for v in variants:
        if v.get("exact_text_hash") != exact_hash:
            raise ValueError(f"BENCHMARK_TEXT_DRIFT:{v.get('mode')}")
        normalized.append({
            "mode": v["mode"],
            "exact_text_hash": exact_hash,
            "provider_settings_family": v.get("provider_settings_family"),
            "voice_binding_version": v.get("voice_binding_version"),
            "mix_profile": v.get("mix_profile"),
            "render_asset_hash": v.get("render_asset_hash"),
            "duration_seconds": v.get("duration_seconds"),
        })
    return {
        "source_id": source_id,
        "source_hash": source_hash,
        "exact_text_hash": exact_hash,
        "variants": sorted(normalized, key=lambda x: AUDIO_MODES.index(x["mode"])),
        "fairness": {
            "same_locked_text": True,
            "same_story_facts": True,
            "human_review_required": True,
            "cost_evidence_required": True,
        },
        "status": "READY_FOR_RENDER_EVIDENCE" if all(v.get("render_asset_hash") for v in normalized) else "HOLD_FOR_RENDER_EVIDENCE"
    }


def score_benchmark_variant(*, mode: str, human_scores: dict[str, float], cost: dict[str, float | None], duration_seconds: float | None) -> dict[str, Any]:
    if mode not in AUDIO_MODES:
        raise ValueError("UNKNOWN_AUDIO_MODE")
    required_scores = ("believability", "clarity", "want_more", "fatigue_resistance")
    if any(k not in human_scores for k in required_scores):
        return {"mode": mode, "status": "HOLD_HUMAN_SCORES", "composite": None}
    vals = [float(human_scores[k]) for k in required_scores]
    if any(v < 0 or v > 5 for v in vals):
        raise ValueError("HUMAN_SCORE_OUT_OF_RANGE")
    if not duration_seconds or duration_seconds <= 0:
        return {"mode": mode, "status": "HOLD_DURATION", "composite": None}
    provider_cost = cost.get("provider_cost")
    manual_cost = cost.get("manual_cost")
    if provider_cost is None or manual_cost is None:
        return {"mode": mode, "status": "HOLD_COST_EVIDENCE", "composite": None}
    accepted_minutes = duration_seconds / 60.0
    total_cost = float(provider_cost) + float(manual_cost)
    quality = sum(vals) / len(vals)
    return {
        "mode": mode,
        "status": "PASS_EVIDENCE_COMPLETE",
        "quality_mean_0_5": round(quality, 4),
        "total_cost": round(total_cost, 4),
        "cost_per_accepted_minute": round(total_cost / accepted_minutes, 4),
        "composite": round(quality / (1.0 + total_cost / max(accepted_minutes, 1e-9)), 6),
    }


def compare_benchmark(scores: list[dict[str, Any]]) -> dict[str, Any]:
    if {s.get("mode") for s in scores} != set(AUDIO_MODES):
        raise ValueError("BENCHMARK_SCORE_SET_INCOMPLETE")
    blocked = [s["mode"] for s in scores if s.get("status") != "PASS_EVIDENCE_COMPLETE"]
    if blocked:
        return {"status": "HOLD", "blocked_modes": sorted(blocked), "winner": None}
    winner = max(scores, key=lambda s: s["composite"])
    return {"status": "PASS", "winner": winner["mode"], "scores": scores}


@dataclass(frozen=True)
class DirectorCue:
    cue_id: str
    domain: str
    anchor_unit_id: str
    function: str
    instruction: str
    absolute_time_seconds: float | None = None
    source_fact_id: str | None = None
    authoritative: bool = False


def compile_automatic_director(scene: dict[str, Any]) -> dict[str, Any]:
    units = scene.get("spoken_units") or []
    if not units:
        raise ValueError("SCENE_SPOKEN_UNITS_REQUIRED")
    ids = [u.get("unit_id") for u in units]
    if any(not x for x in ids) or len(ids) != len(set(ids)):
        raise ValueError("SCENE_UNIT_IDS_INVALID")
    cues: list[DirectorCue] = []
    for i, u in enumerate(units, 1):
        uid = u["unit_id"]
        objective = u.get("objective")
        if objective:
            cues.append(DirectorCue(f"AUTO_PERF_{i:03d}", "PERFORMANCE", uid, "OBJECTIVE", f"Play objective: {objective}"))
        listener_state = u.get("listener_state")
        if listener_state in {"LISTENING", "HESITATION", "RECOGNITION", "REFUSAL", "SHOCK"}:
            cues.append(DirectorCue(f"AUTO_PAUSE_{i:03d}", "PAUSE", uid, listener_state, f"Preserve semantic {listener_state.lower()} space; duration waits for alignment"))
        perspective = u.get("mic_perspective")
        if perspective:
            if perspective not in {"CLOSE", "NORMAL", "ACROSS_ROOM", "MEDIA"}:
                raise ValueError("UNSUPPORTED_MIC_PERSPECTIVE")
            cues.append(DirectorCue(f"AUTO_MIC_{i:03d}", "MIC", uid, "PERSPECTIVE", perspective))
    for j, ev in enumerate(scene.get("declared_events") or [], 1):
        anchor = ev.get("anchor_unit_id")
        if anchor not in set(ids):
            raise ValueError("EVENT_ANCHOR_UNKNOWN")
        kind = ev.get("kind")
        if kind not in {"FOLEY", "AMBIENCE", "MUSIC", "SILENCE"}:
            raise ValueError("UNSUPPORTED_DECLARED_EVENT_KIND")
        if kind in {"FOLEY", "MUSIC"} and not ev.get("source_fact_id"):
            raise ValueError("CAUSAL_EVENT_SOURCE_FACT_REQUIRED")
        cues.append(DirectorCue(
            f"AUTO_EVT_{j:03d}", kind, anchor, ev.get("function", "DECLARED_EVENT"),
            ev.get("instruction", ""), source_fact_id=ev.get("source_fact_id")
        ))
    return {
        "scene_id": scene.get("scene_id"),
        "source_text_hash": scene.get("source_text_hash"),
        "story_mutation": False,
        "absolute_timing_status": "SEMANTIC_UNTIL_REAL_ALIGNMENT",
        "cues": [asdict(c) for c in cues],
        "machine_authority": "ADVISORY",
    }


def validate_director_score(score: dict[str, Any]) -> dict[str, Any]:
    if score.get("story_mutation") is not False:
        raise ValueError("DIRECTOR_MAY_NOT_MUTATE_STORY")
    bad = []
    for cue in score.get("cues", []):
        if cue.get("domain") not in DIRECTOR_DOMAINS:
            bad.append(cue.get("cue_id"))
        if cue.get("absolute_time_seconds") is not None:
            bad.append(cue.get("cue_id"))
    return {"status": "PASS" if not bad else "FAIL", "bad_cues": bad}


@dataclass
class PerformanceEvidence:
    candidate_id: str
    role_id: str
    multi_state: bool = False
    pronunciation: bool = False
    fatigue: bool = False
    human_review: bool = False
    pair: bool | None = None
    ai_tell_flags: list[str] | None = None
    human_scores: dict[str, float] | None = None


def performance_intelligence(e: PerformanceEvidence, *, pair_required: bool = False) -> dict[str, Any]:
    missing = [k for k in LOCK_EVIDENCE if not getattr(e, k)]
    if pair_required and e.pair is not True:
        missing.append("pair")
    scores = e.human_scores or {}
    score_status = "PRESENT" if scores else "MISSING"
    return {
        "candidate_id": e.candidate_id,
        "role_id": e.role_id,
        "machine_flags": sorted(e.ai_tell_flags or []),
        "machine_flags_authoritative": False,
        "human_scores_status": score_status,
        "human_scores": scores,
        "lock_status": "PROVISIONAL_PILOT_LOCK_ELIGIBLE" if not missing else "HOLD",
        "missing_evidence": missing,
        "season_lock": False,
        "machine_may_auto_lock": False,
    }


def compare_cast_candidates(rows: list[dict[str, Any]]) -> dict[str, Any]:
    eligible = [r for r in rows if r.get("lock_status") == "PROVISIONAL_PILOT_LOCK_ELIGIBLE"]
    if not eligible:
        return {"status": "HOLD", "winner": None}
    scored = []
    for r in eligible:
        hs = r.get("human_scores")
        if not hs:
            continue
        vals = [float(v) for v in hs.values()]
        scored.append((sum(vals)/len(vals), r))
    if not scored:
        return {"status": "HOLD_HUMAN_SCORES", "winner": None}
    scored.sort(key=lambda x: x[0], reverse=True)
    return {"status": "REVIEW_RECOMMENDATION_ONLY", "winner": scored[0][1].get("candidate_id"), "auto_lock": False}


def compress_human_review(flags: list[dict[str, Any]], *, total_duration_seconds: float, max_fraction: float = 0.10, min_seconds: float = 30.0) -> dict[str, Any]:
    if total_duration_seconds <= 0:
        raise ValueError("TOTAL_DURATION_REQUIRED")
    if not (0 < max_fraction <= 1):
        raise ValueError("MAX_FRACTION_INVALID")
    sev_weight = {"FATAL": 100, "MAJOR": 30, "MINOR": 8, "ADVISORY": 1}
    items = []
    for f in flags:
        start = float(f.get("start", 0))
        end = float(f.get("end", start))
        if end < start or start < 0:
            raise ValueError("FLAG_INTERVAL_INVALID")
        severity = f.get("severity", "ADVISORY")
        score = sev_weight.get(severity, 1) + float(f.get("confidence", 0)) * 10
        items.append({**f, "start": start, "end": end, "priority": score})
    items.sort(key=lambda x: (-x["priority"], x["start"]))
    budget = max(min_seconds, total_duration_seconds * max_fraction)
    selected, used = [], 0.0
    for item in items:
        dur = max(1.0, item["end"] - item["start"])
        if selected and used + dur > budget:
            continue
        selected.append(item)
        used += dur
        if used >= budget:
            break
    fatal_unselected = [x for x in items if x.get("severity") == "FATAL" and x not in selected]
    if fatal_unselected:
        for x in fatal_unselected:
            selected.append(x)
            used += max(1.0, x["end"] - x["start"])
    return {
        "status": "PASS_PLAN",
        "selected": selected,
        "review_seconds": round(used, 3),
        "review_fraction": round(used / total_duration_seconds, 4),
        "machine_may_clear_release": False,
        "full_listen_still_required_for_final_blind_acceptance": True,
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
    if any(r.mode not in AUDIO_MODES for r in rows):
        raise ValueError("ECONOMICS_UNKNOWN_MODE")
    missing = []
    for r in rows:
        if r.provider_cost is None: missing.append(f"{r.render_id}:provider_cost")
        if r.manual_minutes is None: missing.append(f"{r.render_id}:manual_minutes")
        if r.manual_hourly_cost is None: missing.append(f"{r.render_id}:manual_hourly_cost")
    if missing:
        return {"status": "HOLD_MISSING_EVIDENCE", "missing": missing}
    generated = sum(r.generated_seconds for r in rows)
    accepted = sum(r.accepted_seconds for r in rows)
    provider_cost = sum(float(r.provider_cost) for r in rows)
    manual_cost = sum(float(r.manual_minutes) / 60.0 * float(r.manual_hourly_cost) for r in rows)
    cache = sum(r.cache_reused_seconds for r in rows)
    regen = sum(r.regeneration_seconds for r in rows)
    if accepted <= 0:
        raise ValueError("NO_ACCEPTED_AUDIO")
    accepted_min = accepted / 60.0
    return {
        "status": "PASS_EVIDENCE_COMPLETE",
        "generated_minutes": round(generated/60.0, 4),
        "accepted_minutes": round(accepted_min, 4),
        "provider_cost": round(provider_cost, 4),
        "manual_cost": round(manual_cost, 4),
        "total_cost": round(provider_cost + manual_cost, 4),
        "cost_per_accepted_minute": round((provider_cost + manual_cost)/accepted_min, 4),
        "acceptance_yield": round(accepted/generated, 4) if generated else None,
        "cache_reuse_fraction": round(cache/max(generated + cache, 1e-9), 4),
        "regeneration_fraction": round(regen/max(generated, 1e-9), 4),
    }


def selective_repair_plan(defects: list[dict[str, Any]], dependency_map: dict[str, list[str]]) -> dict[str, Any]:
    actions = []
    for d in defects:
        did = d.get("defect_id")
        layer = d.get("earliest_layer")
        asset = d.get("asset_id")
        if not did or not layer or not asset:
            raise ValueError("DEFECT_FIELDS_REQUIRED")
        deps = sorted(set(dependency_map.get(asset, [])))
        actions.append({
            "defect_id": did,
            "repair_layer": layer,
            "rerender_asset": asset,
            "invalidate_downstream": deps,
            "rewrite_story": False,
            "full_chapter_rerender": False,
        })
    return {"status": "PASS_PLAN", "actions": actions}


def studio_release_gate(*, benchmark: dict[str, Any], performance: list[dict[str, Any]], economics: dict[str, Any], blind_human_review: bool, live_provider_evidence: bool) -> dict[str, Any]:
    missing = []
    if benchmark.get("status") != "PASS": missing.append("benchmark")
    if any(p.get("lock_status") != "PROVISIONAL_PILOT_LOCK_ELIGIBLE" for p in performance): missing.append("performance")
    if economics.get("status") != "PASS_EVIDENCE_COMPLETE": missing.append("economics")
    if not blind_human_review: missing.append("blind_human_review")
    if not live_provider_evidence: missing.append("live_provider_evidence")
    return {
        "status": "GO_STUDIO_V1" if not missing else "HOLD",
        "missing": missing,
        "machine_may_override": False,
    }
