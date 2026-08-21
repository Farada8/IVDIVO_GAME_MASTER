#!/usr/bin/env python3
"""Deterministic first-pass recovery ledger builder for pasted/exported IVDIVO chats.

This tool does NOT decide canon, verify Drive/GitHub claims, or promote recovered
content. It only converts a complete local transcript file into a structured,
secret-redacted recovery ledger that downstream AI/human reconciliation can use.

Authority: IVDIVO_NARRATIVE_OS/18B_FULL_CHAT_TRANSCRIPT_RECOVERY_AND_INGESTION_PROTOCOL_v1.0.md
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

COMPLETENESS = {
    "FULL_TRANSCRIPT",
    "PARTIAL_TRANSCRIPT",
    "UNKNOWN_COMPLETENESS",
    "MULTI_TRANSCRIPT_BUNDLE",
}

ROLE_RE = re.compile(
    r"^\s*(user|assistant|system|developer|founder|claude|grok|chatgpt|codex)\s*[:：]\s*(.*)$",
    re.IGNORECASE,
)
URL_RE = re.compile(r"https?://[^\s<>\])}]+")
DRIVE_ID_RE = re.compile(r"\b[1-9A-Za-z_-]{25,}\b")
FILE_RE = re.compile(
    r"(?<![\w.-])(?:[\w.-]+/)*[\w.-]+\.(?:md|json|txt|docx|pdf|zip|py|yaml|yml|csv|wav|mp3|m4a)\b",
    re.IGNORECASE,
)

SECRET_PATTERNS = [
    re.compile(
        r"(?i)\b(?:api[_ -]?key|password|passwd|secret|access[_ -]?token|bearer)"
        r"\s*[:=]\s*['\"]?([^\s'\";,]{6,})"
    ),
    re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
]
WORK_CLAIM_RE = re.compile(
    r"(?i)\b(?:saved|created|updated|wrote|uploaded|committed|merged|locked|passed|verified|"
    r"сохранил|создал|обновил|записал|загрузил|внес|закоммитил|прош[её]л|проверил|зафиксировал)\b"
)
DIRECTIVE_RE = re.compile(
    r"(?i)\b(?:do|make|create|continue|use|save|write|update|check|must|should|"
    r"надо|нужно|сделай|делай|продолжай|сохрани|запиши|внеси|обнови|проверь|используй|внедри|интегрируй|пусть|должен|обязан)\b"
)
AUTHORITY_RE = re.compile(
    r"(?i)\b(?:canon|canonical|authority|current|locked|final|superseded|rejected|"
    r"канон|канонич|авторитет|текущ|зафиксир|лок|финал|отклон|заменен|заменён)\b"
)
NEXT_RE = re.compile(
    r"(?i)\b(?:next action|next step|next obligation|next gate|дальше|следующ(?:ий|ая|ее)|"
    r"следующий шаг|следующая задача|что дальше)\b"
)
SYSTEM_IMPROVEMENT_RE = re.compile(
    r"(?i)\b(?:engine|protocol|router|prompt|program|schema|workflow|self[- ]?improv|"
    r"движок|протокол|роутер|промт|программ|схем|процесс|самосоверш)\b"
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def redact_secrets(text: str) -> tuple[str, int]:
    out = text
    count = 0
    for pattern in SECRET_PATTERNS:
        while True:
            match = pattern.search(out)
            if not match:
                break
            count += 1
            out = out[: match.start()] + "[REDACTED_SECRET]" + out[match.end() :]
    return out, count


def split_turns(text: str) -> list[dict[str, str]]:
    turns: list[dict[str, str]] = []
    role = "unknown"
    buffer: list[str] = []

    for line in text.splitlines():
        match = ROLE_RE.match(line)
        if match:
            if buffer:
                body = "\n".join(buffer).strip()
                if body:
                    turns.append({"role": role, "text": body})
            role = match.group(1).lower()
            buffer = [match.group(2)]
        else:
            buffer.append(line)

    if buffer:
        body = "\n".join(buffer).strip()
        if body:
            turns.append({"role": role, "text": body})

    return turns


def excerpt(text: str, limit: int = 500) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    return compact[:limit] + ("…" if len(compact) > limit else "")


def find_artifacts(text: str) -> list[str]:
    found: list[str] = []
    found.extend(match.group(0) for match in URL_RE.finditer(text))
    found.extend(match.group(0) for match in FILE_RE.finditer(text))
    found.extend(match.group(0) for match in DRIVE_ID_RE.finditer(text))

    seen: set[str] = set()
    result: list[str] = []
    for item in found:
        if item == "REDACTED_SECRET" or item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def build_ledger(
    text: str,
    *,
    completeness: str = "UNKNOWN_COMPLETENESS",
    source_model: str | None = None,
    source_chat: str | None = None,
    source_date: str | None = None,
) -> dict[str, Any]:
    if completeness not in COMPLETENESS:
        raise ValueError(f"invalid completeness: {completeness}")
    if not text or not text.strip():
        raise ValueError("empty transcript")

    redacted, secret_count = redact_secrets(text)
    turns = split_turns(redacted)

    directives: list[dict[str, Any]] = []
    work_claims: list[dict[str, Any]] = []
    authority_claims: list[dict[str, Any]] = []
    next_claims: list[dict[str, Any]] = []
    improvements: list[dict[str, Any]] = []
    artifacts: list[dict[str, Any]] = []

    for turn_number, turn in enumerate(turns, 1):
        role = turn["role"]
        body = turn["text"]

        for reference in find_artifacts(body):
            artifacts.append(
                {
                    "turn": turn_number,
                    "role": role,
                    "reference": reference,
                    "verification_status": "UNVERIFIED",
                }
            )

        if role in {"user", "founder"} and DIRECTIVE_RE.search(body):
            directives.append(
                {
                    "turn": turn_number,
                    "role": role,
                    "excerpt": excerpt(body),
                    "authority_status": "SOURCE_DIRECTIVE_CANDIDATE",
                }
            )

        if role in {"assistant", "claude", "grok", "chatgpt", "codex", "unknown"} and WORK_CLAIM_RE.search(body):
            work_claims.append(
                {
                    "turn": turn_number,
                    "role": role,
                    "excerpt": excerpt(body),
                    "claim_status": "UNVERIFIED",
                }
            )

        if AUTHORITY_RE.search(body):
            authority_claims.append(
                {
                    "turn": turn_number,
                    "role": role,
                    "excerpt": excerpt(body),
                    "claim_status": "UNVERIFIED",
                }
            )

        if NEXT_RE.search(body):
            next_claims.append(
                {
                    "turn": turn_number,
                    "role": role,
                    "excerpt": excerpt(body),
                    "claim_status": "UNVERIFIED",
                }
            )

        if SYSTEM_IMPROVEMENT_RE.search(body) and (
            DIRECTIVE_RE.search(body) or WORK_CLAIM_RE.search(body)
        ):
            improvements.append(
                {
                    "turn": turn_number,
                    "role": role,
                    "excerpt": excerpt(body),
                    "candidate_status": "DISCOVERY_ONLY",
                }
            )

    deduped_artifacts: list[dict[str, Any]] = []
    seen_refs: set[str] = set()
    for item in artifacts:
        if item["reference"] in seen_refs:
            continue
        seen_refs.add(item["reference"])
        deduped_artifacts.append(item)

    return {
        "schema_version": "1.0",
        "recovery_status": "EXTRACTED_UNVERIFIED",
        "source": {
            "model": source_model,
            "chat": source_chat,
            "date": source_date,
            "completeness": completeness,
            "sha256": sha256_text(text),
            "bytes": len(text.encode("utf-8")),
            "turns_detected": len(turns),
            "final_tail_processed": True,
        },
        "secret_firewall": {
            "secrets_detected": secret_count,
            "secrets_persisted": False,
        },
        "founder_directives": directives,
        "work_completed_claims": work_claims,
        "canon_or_authority_claims": authority_claims,
        "artifact_references": deduped_artifacts,
        "next_action_claims": next_claims,
        "system_improvement_candidates": improvements,
        "verification_queue": [
            {
                "kind": "ARTIFACT_REFERENCE",
                "reference": item["reference"],
                "required_action": "VERIFY_IN_PERSISTED_SOURCE",
            }
            for item in deduped_artifacts
        ],
        "hard_fails": [],
        "completion_gate": {
            "ingestion_complete": False,
            "reason": (
                "Semantic reconciliation, persisted-source verification, dispositions "
                "and readback remain required."
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a fail-closed IVDIVO transcript-recovery ledger."
    )
    parser.add_argument("transcript", type=Path, help="UTF-8 transcript text/markdown file")
    parser.add_argument("--output", type=Path, help="Write ledger JSON to this path")
    parser.add_argument(
        "--completeness",
        choices=sorted(COMPLETENESS),
        default="UNKNOWN_COMPLETENESS",
    )
    parser.add_argument("--source-model")
    parser.add_argument("--source-chat")
    parser.add_argument("--source-date")
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()

    try:
        text = args.transcript.read_text(encoding="utf-8")
        ledger = build_ledger(
            text,
            completeness=args.completeness,
            source_model=args.source_model,
            source_chat=args.source_chat,
            source_date=args.source_date,
        )
    except Exception as exc:
        print(
            json.dumps(
                {"recovery_status": "FAIL_CLOSED", "error": str(exc)},
                ensure_ascii=False,
            )
        )
        return 2

    payload = json.dumps(
        ledger,
        ensure_ascii=False,
        indent=None if args.compact else 2,
        separators=(",", ":") if args.compact else None,
    )
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
