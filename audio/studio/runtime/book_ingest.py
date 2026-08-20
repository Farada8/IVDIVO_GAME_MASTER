#!/usr/bin/env python3
"""IVDIVO Audio Novel Studio — BOOK INGEST runtime v0.1.

First executable boundary for the product flow: immutable manuscript -> stable book map.

Supported in v0.1: UTF-8/UTF-8-SIG TXT and Markdown.
Other formats must use explicit adapters later; this program will not pretend to parse
DOCX/EPUB/PDF by extension.

Outputs:
- NORMALIZED_SOURCE.txt
- BOOK_INGEST_MANIFEST.json
- CHAPTER_MAP.json
- SOURCE_UNIT_MAP.json

Normalization is deliberately minimal and evidence-preserving:
- strip UTF-8 BOM;
- normalize CRLF/CR line endings to LF;
- do NOT rewrite punctuation, whitespace inside lines, spelling, names or prose.
Both original-byte and normalized-text SHA-256 hashes are recorded.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

SUPPORTED_SUFFIXES = {".txt", ".md", ".markdown"}

# Conservative heading recognition. This is structural detection only, not literary analysis.
CHAPTER_PATTERNS = [
    re.compile(r"^(?:#{1,6}\s+)?(?:CHAPTER|ГЛАВА)\s+[0-9IVXLCDMА-ЯA-ZЁ\-–—]+(?:\s*[:.\-–—]\s*.*)?$", re.IGNORECASE),
    re.compile(r"^(?:#{1,6}\s+)?(?:PROLOGUE|EPILOGUE|ПРОЛОГ|ЭПИЛОГ)(?:\s*[:.\-–—]\s*.*)?$", re.IGNORECASE),
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def decode_source(raw: bytes) -> Tuple[str, str]:
    """Return decoded text and declared decoding. Fail rather than lossy-decode."""
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw.decode("utf-8-sig"), "utf-8-sig"
    try:
        return raw.decode("utf-8"), "utf-8"
    except UnicodeDecodeError as exc:
        raise ValueError(
            "FAIL_SOURCE_ENCODING: v0.1 accepts UTF-8/UTF-8-SIG only; "
            "convert through an explicit adapter instead of lossy decoding"
        ) from exc


def normalize_text(text: str) -> Tuple[str, List[str]]:
    changes: List[str] = []
    if "\r\n" in text or "\r" in text:
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        changes.append("LINE_ENDINGS_TO_LF")
    return text, changes


def is_chapter_heading(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    # Markdown # Title that is not explicitly a chapter is NOT automatically a chapter.
    return any(p.match(stripped) for p in CHAPTER_PATTERNS)


def line_spans(text: str) -> List[Tuple[int, int, str]]:
    """(start,end,line_without_newline) preserving offsets in normalized source."""
    out: List[Tuple[int, int, str]] = []
    pos = 0
    for chunk in text.splitlines(keepends=True):
        end = pos + len(chunk)
        line = chunk[:-1] if chunk.endswith("\n") else chunk
        out.append((pos, end, line))
        pos = end
    if not text:
        return []
    if pos < len(text):
        out.append((pos, len(text), text[pos:]))
    return out


def detect_chapters(text: str) -> List[Dict[str, Any]]:
    lines = line_spans(text)
    headings: List[Tuple[int, int, str]] = []
    for start, end, line in lines:
        if is_chapter_heading(line):
            headings.append((start, end, line.strip().lstrip("#").strip()))

    chapters: List[Dict[str, Any]] = []
    if not headings:
        chapters.append({
            "chapter_id": "CH000",
            "ordinal": 0,
            "title": "BOOK_BODY",
            "heading_start": None,
            "heading_end": None,
            "content_start": 0,
            "content_end": len(text),
            "source_start": 0,
            "source_end": len(text),
        })
        return chapters

    # Preserve any front matter before first explicit heading.
    if headings[0][0] > 0 and text[:headings[0][0]].strip():
        chapters.append({
            "chapter_id": "CH000",
            "ordinal": 0,
            "title": "FRONT_MATTER",
            "heading_start": None,
            "heading_end": None,
            "content_start": 0,
            "content_end": headings[0][0],
            "source_start": 0,
            "source_end": headings[0][0],
        })

    base = len(chapters)
    for i, (hstart, hend, title) in enumerate(headings):
        source_end = headings[i + 1][0] if i + 1 < len(headings) else len(text)
        chapters.append({
            "chapter_id": f"CH{base + i + 1:03d}",
            "ordinal": base + i + 1,
            "title": title,
            "heading_start": hstart,
            "heading_end": hend,
            "content_start": hend,
            "content_end": source_end,
            "source_start": hstart,
            "source_end": source_end,
        })
    return chapters


def paragraph_spans(text: str, start: int, end: int) -> List[Tuple[int, int]]:
    """Find non-empty paragraph spans without altering exact text."""
    segment = text[start:end]
    spans: List[Tuple[int, int]] = []
    # Paragraph = one or more nonblank lines separated by a blank-line boundary.
    # Exact content slice is retained; surrounding blank separators are not unit speech text.
    pattern = re.compile(r"(?ms)(?<!\S)(?:[^\n]*\S[^\n]*(?:\n(?!\s*\n)[^\n]*\S[^\n]*)*)")
    # Simpler robust scan by blank-line separators, preserving offsets.
    cursor = 0
    for m in re.finditer(r"\n[ \t]*\n+", segment):
        p0, p1 = cursor, m.start()
        raw = segment[p0:p1]
        if raw.strip():
            lead = len(raw) - len(raw.lstrip())
            trail = len(raw.rstrip())
            spans.append((start + p0 + lead, start + p0 + trail))
        cursor = m.end()
    raw = segment[cursor:]
    if raw.strip():
        lead = len(raw) - len(raw.lstrip())
        trail = len(raw.rstrip())
        spans.append((start + cursor + lead, start + cursor + trail))
    return spans


def build_units(text: str, chapters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    units: List[Dict[str, Any]] = []
    global_ord = 0
    for ch in chapters:
        chapter_ord = 0
        for ustart, uend in paragraph_spans(text, ch["content_start"], ch["content_end"]):
            exact = text[ustart:uend]
            if not exact.strip():
                continue
            global_ord += 1
            chapter_ord += 1
            units.append({
                "unit_id": f"{ch['chapter_id']}_U{chapter_ord:04d}",
                "global_ordinal": global_ord,
                "chapter_id": ch["chapter_id"],
                "chapter_unit_ordinal": chapter_ord,
                "unit_type": "PARAGRAPH",
                "source_start": ustart,
                "source_end": uend,
                "exact_text": exact,
                "text_sha256": sha256_text(exact),
            })
    return units


def validate_maps(text: str, chapters: List[Dict[str, Any]], units: List[Dict[str, Any]]) -> List[str]:
    errors: List[str] = []
    n = len(text)
    for ch in chapters:
        if not (0 <= ch["source_start"] <= ch["source_end"] <= n):
            errors.append(f"chapter bounds invalid: {ch['chapter_id']}")
    seen = set()
    last_start = -1
    for u in units:
        if u["unit_id"] in seen:
            errors.append(f"duplicate unit_id: {u['unit_id']}")
        seen.add(u["unit_id"])
        s, e = u["source_start"], u["source_end"]
        if not (0 <= s < e <= n):
            errors.append(f"unit bounds invalid: {u['unit_id']}")
            continue
        if text[s:e] != u["exact_text"]:
            errors.append(f"unit exact_text mismatch: {u['unit_id']}")
        if sha256_text(text[s:e]) != u["text_sha256"]:
            errors.append(f"unit hash mismatch: {u['unit_id']}")
        if s < last_start:
            errors.append(f"unit order regression: {u['unit_id']}")
        last_start = s
    return errors


def ingest(source_path: Path, project_id: str, source_version: str) -> Dict[str, Any]:
    suffix = source_path.suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise ValueError(
            f"FAIL_UNSUPPORTED_SOURCE_FORMAT: {suffix or '<none>'}; "
            "v0.1 supports TXT/MD only. Use an explicit format adapter."
        )
    raw = source_path.read_bytes()
    decoded, encoding = decode_source(raw)
    normalized, normalization_changes = normalize_text(decoded)
    chapters = detect_chapters(normalized)
    units = build_units(normalized, chapters)
    errors = validate_maps(normalized, chapters, units)
    gate = "PASS" if not errors else "FAIL"

    manifest = {
        "schema": "IVDIVO_BOOK_INGEST_MANIFEST_v1",
        "runtime_version": "0.1",
        "project_id": project_id,
        "source_version": source_version,
        "source_filename": source_path.name,
        "source_suffix": suffix,
        "source_encoding": encoding,
        "original_bytes_sha256": sha256_bytes(raw),
        "normalized_text_sha256": sha256_text(normalized),
        "normalization_changes": normalization_changes,
        "normalization_policy": "BOM_REMOVE_IF_PRESENT + LINE_ENDINGS_ONLY; NO_PROSE_REWRITE",
        "character_count": len(normalized),
        "chapter_count": len(chapters),
        "source_unit_count": len(units),
        "gate": gate,
        "errors": errors,
        "next_stage": "AUTHORITY_CANON_LOCK_AND_AUDIO_ADAPTATION_PLAN" if gate == "PASS" else None,
    }
    return {
        "normalized_text": normalized,
        "manifest": manifest,
        "chapters": {
            "schema": "IVDIVO_CHAPTER_MAP_v1",
            "project_id": project_id,
            "source_hash": manifest["normalized_text_sha256"],
            "chapters": chapters,
        },
        "units": {
            "schema": "IVDIVO_SOURCE_UNIT_MAP_v1",
            "project_id": project_id,
            "source_hash": manifest["normalized_text_sha256"],
            "unit_count": len(units),
            "units": units,
        },
    }


def main() -> None:
    p = argparse.ArgumentParser(description="IVDIVO book ingest/source normalizer v0.1")
    p.add_argument("source")
    p.add_argument("--project-id", required=True)
    p.add_argument("--source-version", required=True)
    p.add_argument("--out-dir", required=True)
    a = p.parse_args()

    src = Path(a.source).resolve()
    if not src.exists() or not src.is_file():
        raise SystemExit(f"FAIL_SOURCE_NOT_FOUND: {src}")

    try:
        result = ingest(src, a.project_id, a.source_version)
    except ValueError as exc:
        raise SystemExit(str(exc))

    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "NORMALIZED_SOURCE.txt").write_text(result["normalized_text"], encoding="utf-8", newline="\n")
    write_json(out / "BOOK_INGEST_MANIFEST.json", result["manifest"])
    write_json(out / "CHAPTER_MAP.json", result["chapters"])
    write_json(out / "SOURCE_UNIT_MAP.json", result["units"])

    print(json.dumps(result["manifest"], ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["manifest"]["gate"] == "PASS" else 2)


if __name__ == "__main__":
    main()
