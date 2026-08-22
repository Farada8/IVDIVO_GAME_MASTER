#!/usr/bin/env python3
"""Compile the locked ROOM917 RU E01 recording script into dialogue units.

Zero-spend, no provider calls, no script writes. The compiler extracts only
speaker-labelled dialogue from the authoritative Markdown script, preserves the
spoken text exactly as written, assigns stable order-based IDs, and records
SHA-256 hashes so downstream block rendering can prove source identity.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from typing import Any

SCENE_RE = re.compile(r"^#\s+SCENE\s+(\d+)\s*[—-]\s*(.+?)\s*$", re.IGNORECASE)
LABEL_RE = re.compile(r"^\*\*(.+?):\*\*\s*$")

ROLE_ALIASES = {
    "ЭЛЕНА": "ELENA",
    "ЕЛЕНА": "ELENA",
    "ДЖУЛИАН": "JULIAN",
    "МИНА": "MINA",
    "КЕЙТ": "CATE",
    "CATE": "CATE",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_label(label: str) -> str:
    label = label.strip()
    label = re.sub(r"\s*\([^)]*\)\s*", " ", label)
    label = " ".join(label.split())
    return label.upper()


def role_from_label(label: str) -> str | None:
    normalized = normalize_label(label)
    for alias, role in ROLE_ALIASES.items():
        if normalized == alias or normalized.startswith(alias + " "):
            return role
    return None


def clean_dialogue_lines(lines: list[str]) -> str:
    # Dialogue body is preserved lexically. Only Markdown's explicit hard-line
    # break trailing spaces are removed before joining continuation lines.
    cleaned = [line.rstrip() for line in lines]
    return "\n".join(cleaned).strip()


def word_count(text: str) -> int:
    return len(re.findall(r"[\wЁёА-Яа-я’-]+", text, flags=re.UNICODE))


def compile_units(script_path: Path) -> dict[str, Any]:
    raw = script_path.read_bytes()
    text = raw.decode("utf-8-sig")
    lines = text.splitlines()

    current_scene: int | None = None
    current_scene_title = ""
    scene_ordinals: dict[int, int] = {}
    units: list[dict[str, Any]] = []

    i = 0
    while i < len(lines):
        line = lines[i]
        scene_match = SCENE_RE.match(line.strip())
        if scene_match:
            current_scene = int(scene_match.group(1))
            current_scene_title = scene_match.group(2).strip()
            scene_ordinals.setdefault(current_scene, 0)
            i += 1
            continue

        label_match = LABEL_RE.match(line.strip())
        if not label_match or current_scene is None:
            i += 1
            continue

        role = role_from_label(label_match.group(1))
        if role is None:
            i += 1
            continue

        body: list[str] = []
        j = i + 1
        while j < len(lines):
            candidate = lines[j]
            if candidate.strip() == "":
                break
            if SCENE_RE.match(candidate.strip()) or LABEL_RE.match(candidate.strip()):
                break
            body.append(candidate)
            j += 1

        spoken = clean_dialogue_lines(body)
        if spoken:
            scene_ordinals[current_scene] += 1
            ordinal = scene_ordinals[current_scene]
            unit_id = f"RU_E01_DLG_S{current_scene:02d}_{ordinal:03d}_{role}"
            wc = word_count(spoken)
            units.append(
                {
                    "unit_id": unit_id,
                    "episode": "E01",
                    "scene": current_scene,
                    "scene_title": current_scene_title,
                    "scene_dialogue_ordinal": ordinal,
                    "global_dialogue_ordinal": len(units) + 1,
                    "character": role,
                    "speaker_label_source": label_match.group(1).strip(),
                    "text": spoken,
                    "text_sha256": sha256_text(spoken),
                    "word_count": wc,
                    "estimated_seconds_reference_only": round((wc / 150.0) * 60.0, 3),
                    "source_line_start_1_based": i + 2,
                    "source_line_end_1_based": i + 1 + len(body),
                }
            )
        i = max(j, i + 1)

    if not units:
        raise ValueError("No dialogue units extracted")

    role_counts = {role: 0 for role in set(ROLE_ALIASES.values())}
    scene_counts: dict[str, int] = {}
    for unit in units:
        role_counts[unit["character"]] = role_counts.get(unit["character"], 0) + 1
        scene_key = str(unit["scene"])
        scene_counts[scene_key] = scene_counts.get(scene_key, 0) + 1

    return {
        "schema_version": "ivdivo.room917_ru_e01_dialogue_units/1.0",
        "generated_at": utc_now(),
        "project_id": "ROOM917",
        "episode": "E01",
        "locale": "ru-RU",
        "story_status": "LOCKED",
        "status": "COMPILED_FROM_AUTHORITATIVE_SCRIPT",
        "source_script": str(script_path),
        "source_script_sha256": sha256_bytes(raw),
        "story_or_dialogue_changed": False,
        "provider_calls": 0,
        "paid_synthesis_calls": 0,
        "unit_count": len(units),
        "role_counts": role_counts,
        "scene_counts": scene_counts,
        "estimated_seconds_are_authority": False,
        "downstream_law": {
            "unit_text_must_match_text_sha256": True,
            "unit_order_must_not_be_reordered_to_change_scene_meaning": True,
            "block_compiler_may_group_adjacent_units_only": True,
            "full_episode_single_pass_forbidden": True,
            "selective_rerender_must_reference_unit_ids": True,
        },
        "units": units,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    result = compile_units(args.script)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "unit_count": result["unit_count"], "role_counts": result["role_counts"], "scene_counts": result["scene_counts"], "out": str(args.out)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
