#!/usr/bin/env python3
"""IVDIVO dialogue naturalism static audit.

Heuristic only. This tool never decides canon or rewrites prose. It surfaces
repetition / house-style / speaker-convergence signals for human/model review.

Usage:
    python tools/dialogue_naturalism_audit.py manuscript.txt
    python tools/dialogue_naturalism_audit.py script.txt --script-format
    python tools/dialogue_naturalism_audit.py manuscript.txt --json report.json
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

DEFAULT_FRAMES = {
    "i_know": r"\bi know\b",
    "that_is": r"\bthat is\b",
    "that_is_not": r"\bthat is not\b",
    "not_the_question": r"\b(?:that (?:was|is) )?not the question\b",
    "apparently": r"\bapparently\b",
    "technically": r"\btechnically\b",
    "exactly": r"\bexactly\b",
    "actually": r"\bactually\b",
    "you_mean": r"\byou mean\b",
    "i_didnt_say": r"\bi (?:did not|didn't) say\b",
}

DIALOGUE_QUOTE_RE = re.compile(r"[\u201c\"]([^\u201d\"]+)[\u201d\"]")
SCRIPT_SPEAKER_RE = re.compile(r"^\s*([A-Z][A-Z0-9 _'\-]{1,40}):\s*(.*)$")
TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z'\-]*")


def words(text: str) -> list[str]:
    return [m.group(0).lower() for m in TOKEN_RE.finditer(text)]


def extract_dialogue(text: str, script_format: bool) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    if script_format:
        for line in text.splitlines():
            m = SCRIPT_SPEAKER_RE.match(line)
            if m and m.group(2).strip():
                rows.append((m.group(1).strip(), m.group(2).strip()))
        return rows

    for i, m in enumerate(DIALOGUE_QUOTE_RE.finditer(text), start=1):
        rows.append((f"UNKNOWN_{i}", m.group(1).strip()))
    return rows


def phrase_counts(text: str, frames: dict[str, str]) -> dict[str, int]:
    low = text.lower()
    return {name: len(re.findall(pattern, low, flags=re.I)) for name, pattern in frames.items()}


def lexical_profile(lines: Iterable[str]) -> dict[str, float | int]:
    toks = [w for line in lines for w in words(line)]
    if not toks:
        return {"tokens": 0, "types": 0, "type_token_ratio": 0.0, "mean_line_words": 0.0}
    line_list = list(lines) if not isinstance(lines, list) else lines
    return {
        "tokens": len(toks),
        "types": len(set(toks)),
        "type_token_ratio": round(len(set(toks)) / len(toks), 4),
        "mean_line_words": round(sum(len(words(x)) for x in line_list) / max(len(line_list), 1), 2),
    }


def jaccard_top_words(a: list[str], b: list[str], n: int = 30) -> float:
    ca, cb = Counter(words(" ".join(a))), Counter(words(" ".join(b)))
    sa = {w for w, _ in ca.most_common(n)}
    sb = {w for w, _ in cb.most_common(n)}
    if not sa or not sb:
        return 0.0
    return round(len(sa & sb) / len(sa | sb), 4)


def consecutive_polish_signals(dialogue: list[tuple[str, str]]) -> list[dict[str, object]]:
    """Very conservative signal for neat correction/comeback clusters."""
    flags = []
    markers = re.compile(
        r"\b(that is not|that was not|not the question|i know|exactly|technically|actually|you mean)\b",
        re.I,
    )
    streak: list[tuple[int, str, str]] = []
    for idx, (speaker, line) in enumerate(dialogue):
        if markers.search(line) and len(words(line)) <= 18:
            streak.append((idx, speaker, line))
        else:
            if len(streak) >= 3:
                flags.append({"start": streak[0][0], "end": streak[-1][0], "lines": streak})
            streak = []
    if len(streak) >= 3:
        flags.append({"start": streak[0][0], "end": streak[-1][0], "lines": streak})
    return flags


def audit(text: str, script_format: bool) -> dict[str, object]:
    dialogue = extract_dialogue(text, script_format)
    by_speaker: dict[str, list[str]] = defaultdict(list)
    for speaker, line in dialogue:
        by_speaker[speaker].append(line)

    speaker_profiles = {}
    for speaker, lines in sorted(by_speaker.items()):
        speaker_profiles[speaker] = {
            **lexical_profile(lines),
            "frame_counts": phrase_counts("\n".join(lines), DEFAULT_FRAMES),
        }

    pair_similarity = []
    speakers = sorted(s for s in by_speaker if not s.startswith("UNKNOWN_"))
    for i, a in enumerate(speakers):
        for b in speakers[i + 1 :]:
            pair_similarity.append({
                "a": a,
                "b": b,
                "top_word_jaccard": jaccard_top_words(by_speaker[a], by_speaker[b]),
            })
    pair_similarity.sort(key=lambda x: x["top_word_jaccard"], reverse=True)

    return {
        "tool": "IVDIVO_DIALOGUE_NATURALISM_AUDIT",
        "version": "1.0",
        "disclaimer": "Heuristic signal only; frequency is not a defect and cannot authorize rewriting.",
        "document": {
            "characters": len(text),
            "words": len(words(text)),
            "dialogue_units": len(dialogue),
        },
        "global_frame_counts": phrase_counts(text, DEFAULT_FRAMES),
        "speaker_profiles": speaker_profiles,
        "highest_speaker_lexical_similarity": pair_similarity[:20],
        "cleverness_cluster_signals": consecutive_polish_signals(dialogue),
        "required_next_step": "Human/LLM naturalism review using HUMAN_SCENE_DIALOGUE_QC_v1; do not auto-rewrite from this report.",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("--script-format", action="store_true", help="Parse SPEAKER: line format")
    ap.add_argument("--json", type=Path, dest="json_path")
    args = ap.parse_args()

    text = args.input.read_text(encoding="utf-8")
    report = audit(text, args.script_format)
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_path:
        args.json_path.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
