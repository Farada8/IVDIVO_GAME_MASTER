#!/usr/bin/env python3
"""IVDIVO Audio Novel Studio — provider-neutral production control contracts.

This module promotes deterministic Wave-2/Wave-3 harness contracts into the
real Audio Studio runtime without importing project-specific story facts.

It owns:
- immutable request/spend ledger semantics;
- ambiguous-response quarantine and normalized error policy;
- capability/model/voice drift checks without auto substitution;
- identity fixtures and scoped invalidation;
- silent reactions, functional pauses, reply latency and microphone states;
- advisory AI-tell flags;
- performance lock evidence gate.

It deliberately does NOT perform provider dispatch or human artistic judgment.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Iterable
import json
import re
import statistics

LEDGER_STATES = {"PLANNED", "SENT", "AMBIGUOUS", "ACCEPTED", "REJECTED"}
VALID_PAUSE_FUNCTIONS = {
    "THOUGHT", "HESITATION", "RECOGNITION", "STATUS", "REFUSAL", "ATTRACTION",
    "SHOCK", "LISTENING", "OBJECT_ACTION", "AFTERMATH", "COMIC_TIMING",
    "INTERRUPTION_WINDOW", "NO_REPLY",
}
MIC_PERSPECTIVES = {"CLOSE", "NORMAL", "ACROSS_ROOM", "MEDIA"}
LATENCY_STATES = {
    "PROTECTED_WAIT", "FAST_DEFENSIVE", "WAIT_THEN_PUNCTURE",
    "FASTER_DEFLECTION", "PLAIN_NO_RUSH", "IMMEDIATE", "SHORT_WAIT",
    "LONG_WAIT", "INTERRUPT", "OVERLAP",
}
PERFORMANCE_HARD_FAILS = {
    "TRAILER_VOICE", "MELODRAMATIC_EMPHASIS", "IDENTICAL_ENDINGS", "NO_LISTENING",
    "STATUS_FLATTENING", "ROBOTIC_BREATH", "ADULT_ON_YOUTH", "FALSE_INTIMACY",
}


def canonical_hash(obj: Any) -> str:
    raw = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(raw).hexdigest()


def validate_identity_fixture(manifest: dict[str, Any], expected: dict[str, Any]) -> dict[str, Any]:
    """Fail closed if named immutable fixture fields drift.

    `expected` is data, not story hardcoding. It may contain scalar fields and a
    `blocks` mapping whose per-block fields are compared exactly.
    """
    scalar_fields = expected.get("scalar_fields", {})
    for field, value in scalar_fields.items():
        if manifest.get(field) != value:
            raise ValueError(f"IDENTITY_DRIFT:{field}")

    expected_blocks = expected.get("blocks", {})
    actual_blocks = manifest.get("blocks", {})
    if set(actual_blocks) != set(expected_blocks):
        raise ValueError("IDENTITY_DRIFT:block_set")
    for block_id, fields in expected_blocks.items():
        actual = actual_blocks[block_id]
        for field, value in fields.items():
            if actual.get(field) != value:
                raise ValueError(f"IDENTITY_DRIFT:{block_id}:{field}")
    return {
        "status": "PASS",
        "fixture_hash": canonical_hash(expected),
        "manifest_hash": canonical_hash(manifest),
        "block_count": len(expected_blocks),
    }


@dataclass
class Attempt:
    request_hash: str
    block_id: str
    state: str
    provider_request_id: str | None = None
    response_hash: str | None = None


class SpendLedger:
    """Persistent request ledger that prevents blind duplicate paid dispatch."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.attempts: dict[str, Attempt] = {}
        if self.path.exists():
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            self.attempts = {key: Attempt(**value) for key, value in raw.items()}

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {key: asdict(value) for key, value in self.attempts.items()}
        self.path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def plan(self, request_hash: str, block_id: str) -> str:
        current = self.attempts.get(request_hash)
        if current:
            if current.state == "ACCEPTED":
                return "REUSED_ACCEPTED"
            if current.state == "AMBIGUOUS":
                return "RECONCILE_REQUIRED"
            return f"EXISTS_{current.state}"
        self.attempts[request_hash] = Attempt(request_hash, block_id, "PLANNED")
        self._save()
        return "PLANNED"

    def transition(
        self,
        request_hash: str,
        state: str,
        *,
        provider_request_id: str | None = None,
        response_hash: str | None = None,
    ) -> None:
        if state not in LEDGER_STATES:
            raise ValueError("INVALID_LEDGER_STATE")
        if request_hash not in self.attempts:
            raise KeyError(request_hash)
        current = self.attempts[request_hash]
        if current.state == "ACCEPTED" and state != "ACCEPTED":
            raise ValueError("ACCEPTED_ATTEMPT_IMMUTABLE")
        if current.state == "AMBIGUOUS" and state == "SENT":
            raise ValueError("AMBIGUOUS_REQUIRES_RECONCILIATION")
        current.state = state
        if provider_request_id is not None:
            current.provider_request_id = provider_request_id
        if response_hash is not None:
            current.response_hash = response_hash
        self._save()

    def snapshot(self) -> dict[str, Any]:
        return {key: asdict(value) for key, value in self.attempts.items()}


def normalize_provider_error(
    status: int | None = None,
    code: str | None = None,
    message: str = "",
) -> dict[str, Any]:
    c = (code or "").upper()
    m = message.upper()
    if status in (401, 403) or "AUTH" in c:
        category, retryable = "AUTH", False
    elif "VOICE" in c:
        category, retryable = "VOICE", False
    elif "MODEL" in c:
        category, retryable = "MODEL", False
    elif "ALIGN" in c:
        category, retryable = "ALIGNMENT", False
    elif "FORMAT" in c or "AUDIO_FORMAT" in c:
        category, retryable = "FORMAT", False
    elif "QUOTA" in c or "CREDIT" in m:
        category, retryable = "QUOTA", False
    elif status == 429 or "RATE" in c:
        category, retryable = "RATE_LIMIT", True
    elif status in (408, 504) or "TIMEOUT" in c:
        category, retryable = "TIMEOUT", True
    elif status in (400, 404, 422) or "INVALID" in c:
        category, retryable = "INVALID_REQUEST", False
    else:
        category = "PROVIDER"
        retryable = bool(status in (500, 502, 503))
    return {
        "category": category,
        "retryable": retryable,
        "status": status,
        "code": code,
    }


def retry_decision(error: dict[str, Any], *, response_started: bool = False) -> str:
    if response_started:
        return "QUARANTINE_AMBIGUOUS"
    return "BACKOFF_RETRY" if error.get("retryable") else "FAIL_CLOSED"


def capability_drift(expected: dict[str, Any], snapshot: dict[str, Any]) -> dict[str, Any]:
    voices = snapshot.get("voices", {})
    models = snapshot.get("models", {})
    model_ids = set(models) if isinstance(models, dict) else set(models or [])
    missing_voices = [voice_id for voice_id in expected.get("voice_ids", []) if voice_id not in voices]
    missing_models = [model_id for model_id in expected.get("model_ids", []) if model_id not in model_ids]
    return {
        "status": "PASS" if not missing_voices and not missing_models else "FAIL_DRIFT",
        "missing_voices": missing_voices,
        "missing_models": missing_models,
        "auto_substitution": False,
    }


def scoped_invalidation(
    dependency_map: dict[str, Iterable[str]],
    changed_keys: Iterable[str],
) -> list[str]:
    invalidated: set[str] = set()
    for key in changed_keys:
        invalidated.update(dependency_map.get(key, []))
    return sorted(invalidated)


def selective_rerender(failed_blocks: Iterable[str], known_blocks: Iterable[str]) -> list[str]:
    known = set(known_blocks)
    failed = list(failed_blocks)
    unknown = [block for block in failed if block not in known]
    if unknown:
        raise ValueError(f"UNKNOWN_BLOCKS:{','.join(sorted(unknown))}")
    return sorted(set(failed))


def promote_silent_reaction(anchor: dict[str, Any]) -> dict[str, Any]:
    required = {"anchor_id", "character_id", "trigger", "silent_action", "silence_policy"}
    if not required.issubset(anchor):
        raise ValueError("SILENT_REACTION_FIELDS_MISSING")
    out = dict(anchor)
    out["spoken_unit_delta"] = 0
    return out


def compile_functional_pause(
    functions: list[str],
    *,
    duration_hypotheses_ms: list[int] | None = None,
) -> dict[str, Any]:
    invalid = [function for function in functions if function not in VALID_PAUSE_FUNCTIONS]
    if invalid:
        raise ValueError(f"UNSUPPORTED_PAUSE_FUNCTION:{','.join(invalid)}")
    return {
        "functions": list(functions),
        "duration_hypotheses_ms": list(duration_hypotheses_ms or []),
        "absolute_time": None,
        "timing_status": "SEMANTIC_UNTIL_ALIGNMENT",
    }


def compile_reply_latency(trigger: str, response: str, state: str) -> dict[str, Any]:
    if state not in LATENCY_STATES:
        raise ValueError("UNSUPPORTED_LATENCY_STATE")
    return {
        "trigger": trigger,
        "response": response,
        "state": state,
        "absolute_time": None,
    }


def compile_microphone_choreography(
    role: str,
    perspective: str,
    *,
    movement_path: list[str] | None = None,
    mono_fallback: str = "CENTER_PRESERVED",
) -> dict[str, Any]:
    if perspective not in MIC_PERSPECTIVES:
        raise ValueError("UNSUPPORTED_MIC_PERSPECTIVE")
    return {
        "role": role,
        "perspective": perspective,
        "movement_path": list(movement_path or []),
        "mono_fallback": mono_fallback,
        "extreme_pan_required": False,
    }


def ai_tell_flags(
    line_endings: list[str],
    pause_intervals: list[float],
    breath_intervals: list[float],
) -> dict[str, Any]:
    """Advisory only. Machine flags may never auto-reject a performance."""
    flags: list[str] = []
    if len(line_endings) >= 4:
        normalized = [re.sub(r"\W+", "", value.lower()) for value in line_endings]
        if len(set(normalized)) <= max(1, len(normalized) // 2):
            flags.append("REPEATED_ENDINGS")
    for label, values in (
        ("PAUSE_REGULARITY", pause_intervals),
        ("BREATH_REGULARITY", breath_intervals),
    ):
        if len(values) >= 4 and statistics.mean(values) > 0:
            coefficient = statistics.pstdev(values) / statistics.mean(values)
            if coefficient < 0.06:
                flags.append(label)
    return {
        "flags": flags,
        "authoritative": False,
        "auto_reject": False,
    }


def performance_lock_gate(
    evidence: dict[str, bool],
    *,
    pair_required: bool = True,
) -> dict[str, Any]:
    required = ["multi_state", "pronunciation", "fatigue", "human_review"]
    if pair_required:
        required.append("pair")
    missing = [key for key in required if not evidence.get(key)]
    return {
        "status": "LOCKED" if not missing else "HOLD",
        "missing": missing,
        "machine_may_auto_lock": False,
    }


def orchestration_acceptance(results: dict[str, bool]) -> dict[str, Any]:
    required = ["clean_build", "resume", "scoped_invalidation", "selective_rerender", "fail_closed"]
    missing = [key for key in required if not results.get(key)]
    return {
        "status": "PASS_CANDIDATE" if not missing else "HOLD",
        "missing": missing,
        "promotion": "REQUIRES_PRODUCTION_AND_LIVE_REVIEW",
    }
