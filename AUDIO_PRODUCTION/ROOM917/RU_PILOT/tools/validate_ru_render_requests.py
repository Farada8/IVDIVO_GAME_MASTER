#!/usr/bin/env python3
"""Validate ROOM917 RU Eleven v3 render requests before any provider call.

This validator is zero-spend. It protects locked dialogue while permitting
bounded Eleven v3 performance-tag experiments and punctuation-only variants.
It never calls ElevenLabs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

TAG_RE = re.compile(r"\[[^\[\]]+\]")
WORD_RE = re.compile(r"[\wЁёА-Яа-я]+", re.UNICODE)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_ws(text: str) -> str:
    return " ".join(text.split())


def strip_tags(text: str) -> str:
    return TAG_RE.sub("", text)


def lexical_tokens(text: str) -> list[str]:
    return [m.group(0).casefold() for m in WORD_RE.finditer(strip_tags(text))]


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected object in {path}")
    return data


def policy_sets(policy: dict[str, Any]) -> tuple[set[str], set[str], set[str]]:
    classes = policy.get("tag_classes") or {}
    allowed = set(classes.get("ALLOW_FOR_BOUNDED_CANARY") or [])
    conditional = set(classes.get("CONDITIONAL_SOURCE_ACTION_REQUIRED") or [])
    forbidden = set(classes.get("ROOM917_DEFAULT_FORBIDDEN") or [])
    return allowed, conditional, forbidden


def validate_request(
    req: dict[str, Any],
    unit_map: dict[str, dict[str, Any]],
    allowed: set[str],
    conditional: set[str],
    forbidden: set[str],
) -> list[str]:
    errors: list[str] = []
    unit_id = str(req.get("unit_id") or "")
    if unit_id not in unit_map:
        return [f"UNKNOWN_UNIT_ID:{unit_id or '<empty>'}"]

    unit = unit_map[unit_id]
    source_text = str(unit.get("text") or "")
    character = str(unit.get("character") or "")

    if req.get("character") != character:
        errors.append(f"CHARACTER_MISMATCH:{req.get('character')}!={character}")

    expected_source_hash = sha256_text(source_text)
    if req.get("source_text_sha256") != expected_source_hash:
        errors.append("SOURCE_TEXT_HASH_MISMATCH")

    voice_id = str(req.get("voice_id") or "").strip()
    if not voice_id:
        errors.append("VOICE_ID_MISSING")

    if req.get("model_id") != "eleven_v3":
        errors.append("MODEL_MUST_BE_ELEVEN_V3")

    if req.get("language_code") != "ru":
        errors.append("LANGUAGE_CODE_MUST_BE_RU")

    text = str(req.get("text") or "")
    if not text:
        errors.append("REQUEST_TEXT_MISSING")
        return errors

    if re.search(r"<\s*break\b", text, flags=re.IGNORECASE):
        errors.append("SSML_BREAK_FORBIDDEN_IN_V3")

    extracted_tags = TAG_RE.findall(text)
    declared_tags = req.get("performance_tags") or []
    if extracted_tags != declared_tags:
        errors.append("DECLARED_TAGS_DO_NOT_MATCH_REQUEST_TEXT")

    conditional_authorized = bool(req.get("conditional_tag_authorized"))
    for tag in extracted_tags:
        if tag in forbidden:
            errors.append(f"ROOM917_FORBIDDEN_TAG:{tag}")
        elif tag in conditional:
            if not conditional_authorized:
                errors.append(f"CONDITIONAL_TAG_REQUIRES_SOURCE_ACTION_AUTH:{tag}")
        elif tag not in allowed:
            errors.append(f"UNAPPROVED_TAG:{tag}")

    mode = req.get("text_variant_mode", "EXACT_PLUS_TAGS")
    stripped = normalize_ws(strip_tags(text))
    source_norm = normalize_ws(source_text)
    if mode == "EXACT_PLUS_TAGS":
        if stripped != source_norm:
            errors.append("DIALOGUE_MUTATION_EXACT_MODE")
    elif mode == "PUNCTUATION_ONLY":
        if lexical_tokens(text) != lexical_tokens(source_text):
            errors.append("LEXICAL_MUTATION_IN_PUNCTUATION_ONLY_MODE")
        if not str(req.get("variant_reason") or "").strip():
            errors.append("PUNCTUATION_VARIANT_REASON_REQUIRED")
    else:
        errors.append(f"UNSUPPORTED_TEXT_VARIANT_MODE:{mode}")

    locators = req.get("pronunciation_dictionary_locators") or []
    if len(locators) > 3:
        errors.append("MORE_THAN_3_PRONUNCIATION_DICTIONARY_LOCATORS")
    for idx, loc in enumerate(locators):
        if not isinstance(loc, dict):
            errors.append(f"DICTIONARY_LOCATOR_{idx}_NOT_OBJECT")
            continue
        if not str(loc.get("pronunciation_dictionary_id") or "").strip():
            errors.append(f"DICTIONARY_LOCATOR_{idx}_ID_MISSING")
        if not str(loc.get("version_id") or "").strip():
            errors.append(f"DICTIONARY_LOCATOR_{idx}_VERSION_MISSING")

    if req.get("request_text_sha256") != sha256_text(text):
        errors.append("REQUEST_TEXT_HASH_MISMATCH")

    return errors


def validate_bundle(
    manifest: dict[str, Any],
    policy: dict[str, Any],
    bundle: dict[str, Any],
) -> dict[str, Any]:
    units = manifest.get("audition_units") or []
    unit_map = {str(u.get("id")): u for u in units if u.get("id")}
    allowed, conditional, forbidden = policy_sets(policy)

    errors: list[dict[str, Any]] = []
    requests = bundle.get("requests") or []
    if not isinstance(requests, list) or not requests:
        errors.append({"request_index": None, "unit_id": None, "errors": ["REQUESTS_EMPTY"]})
        requests = []

    seen_ids: set[str] = set()
    for idx, req in enumerate(requests):
        if not isinstance(req, dict):
            errors.append({"request_index": idx, "unit_id": None, "errors": ["REQUEST_NOT_OBJECT"]})
            continue
        request_id = str(req.get("request_id") or "")
        if not request_id:
            req_errors = ["REQUEST_ID_MISSING"]
        elif request_id in seen_ids:
            req_errors = ["DUPLICATE_REQUEST_ID"]
        else:
            seen_ids.add(request_id)
            req_errors = []
        req_errors.extend(validate_request(req, unit_map, allowed, conditional, forbidden))
        if req_errors:
            errors.append({"request_index": idx, "request_id": request_id, "unit_id": req.get("unit_id"), "errors": req_errors})

    result = {
        "schema_version": "ivdivo.room917_ru_render_request_validation/1.0",
        "project_id": "ROOM917",
        "locale": "ru-RU",
        "provider_calls": 0,
        "paid_synthesis_calls": 0,
        "request_count": len(requests),
        "status": "PASS_ZERO_SPEND_PRE_PROVIDER" if not errors else "FAIL_CLOSED",
        "errors": errors,
        "full_episode_render_allowed": False,
        "cast_lock_changed": False,
    }
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--tag-policy", type=Path, required=True)
    ap.add_argument("--bundle", type=Path, required=True)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()

    result = validate_bundle(load_json(args.manifest), load_json(args.tag_policy), load_json(args.bundle))
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["status"] == "PASS_ZERO_SPEND_PRE_PROVIDER" else 2


if __name__ == "__main__":
    sys.exit(main())
