#!/usr/bin/env python3
"""
BODYGUARD FOR THE FALLEN IDOL — E01 ElevenLabs rough-render driver v1.0

Default behavior is DRY RUN.
Execution requires:
  --execute
  ELEVENLABS_API_KEY
  non-null voice_id + model_id for every used voice role

The driver never edits story text. It validates the locked spoken-sequence hash
before any network request.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import httpx


EXPECTED_WORDS = 1344
EXPECTED_BLOCKS = 190
EXPECTED_SPOKEN_SHA256 = "2af60ca3b58bc90a2863e8f6dbee2bf7541d6b1f2315e78704f12ca214da9149"
DEFAULT_BASE_URL = "https://api.elevenlabs.io"
DEFAULT_TIMEOUT = 90.0


class RenderFailure(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def spoken_words(text: str) -> int:
    return len(text.split())


def validate_request_manifest(requests: dict[str, Any]) -> None:
    rows = requests.get("requests", [])
    if len(rows) != EXPECTED_BLOCKS:
        raise RenderFailure(f"Expected {EXPECTED_BLOCKS} request blocks, found {len(rows)}.")

    ordered = "\n".join(row["exact_text"] for row in rows)
    total_words = sum(spoken_words(row["exact_text"]) for row in rows)
    digest = sha256_text(ordered)

    if total_words != EXPECTED_WORDS:
        raise RenderFailure(f"Expected {EXPECTED_WORDS} spoken words, found {total_words}.")
    if digest != EXPECTED_SPOKEN_SHA256:
        raise RenderFailure(
            "Locked spoken-sequence SHA mismatch. "
            f"Expected {EXPECTED_SPOKEN_SHA256}, found {digest}."
        )

    ids = [row["block_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise RenderFailure("Duplicate block_id detected.")

    for row in rows:
        if sha256_text(row["exact_text"]) != row["exact_text_sha256"]:
            raise RenderFailure(f"Text hash mismatch in {row['block_id']}.")


def used_roles(requests: dict[str, Any]) -> set[str]:
    return {row["voice_role"] for row in requests["requests"]}


def validate_voice_map(requests: dict[str, Any], voice_map: dict[str, Any], execute: bool) -> None:
    roles = voice_map.get("roles", {})
    missing = []
    incomplete = []

    for role in sorted(used_roles(requests)):
        if role not in roles:
            missing.append(role)
            continue
        voice_id = roles[role].get("voice_id")
        model_id = roles[role].get("model_id")
        if execute and (not voice_id or not model_id):
            incomplete.append(role)

    if missing:
        raise RenderFailure(f"Voice map missing roles: {', '.join(missing)}.")
    if incomplete:
        raise RenderFailure(
            "Execution blocked. Bind voice_id and model_id for: "
            + ", ".join(incomplete)
        )


def validate_take_manifest(requests: dict[str, Any], takes: dict[str, Any]) -> None:
    expected = {
        f"{row['block_id']}_T{n:02d}"
        for row in requests["requests"]
        for n, _ in enumerate(row["take_plan"], start=1)
    }
    actual = {row["take_id"] for row in takes.get("take_rows", [])}

    if expected != actual:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise RenderFailure(
            f"Take-ledger mismatch. missing={len(missing)} extra={len(extra)}"
        )


def find_request_by_block(requests: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["block_id"]: row for row in requests["requests"]}


def build_payload(
    req: dict[str, Any],
    voice_binding: dict[str, Any],
    take_type: str,
) -> dict[str, Any]:
    """
    Exact text is always copied from the locked request manifest.

    Director intent is kept in local metadata. It is not injected into spoken text.
    Optional provider-specific voice settings can be supplied under:
      voice_binding["voice_settings_by_take"][take_type]
    or voice_binding["voice_settings"].
    """
    payload: dict[str, Any] = {
        "text": req["exact_text"],
        "model_id": voice_binding["model_id"],
    }

    settings_by_take = voice_binding.get("voice_settings_by_take") or {}
    settings = settings_by_take.get(take_type) or voice_binding.get("voice_settings")
    if settings:
        payload["voice_settings"] = settings

    return payload


def endpoint(base_url: str, voice_id: str) -> str:
    return f"{base_url.rstrip('/')}/v1/text-to-speech/{voice_id}"


def request_audio(
    client: httpx.Client,
    base_url: str,
    api_key: str,
    voice_id: str,
    payload: dict[str, Any],
    output_format: str | None,
    max_attempts: int,
) -> tuple[bytes, dict[str, str]]:
    url = endpoint(base_url, voice_id)
    params = {}
    if output_format:
        params["output_format"] = output_format

    headers = {
        "xi-api-key": api_key,
        "accept": "audio/mpeg",
        "content-type": "application/json",
    }

    last_error = None
    for attempt in range(1, max_attempts + 1):
        try:
            response = client.post(url, params=params, headers=headers, json=payload)
        except httpx.HTTPError as exc:
            last_error = f"network error: {exc}"
            retryable = True
        else:
            if 200 <= response.status_code < 300:
                meta = {
                    "request_id": response.headers.get("request-id")
                    or response.headers.get("x-request-id")
                    or "",
                    "content_type": response.headers.get("content-type", ""),
                }
                return response.content, meta

            last_error = f"HTTP {response.status_code}: {response.text[:500]}"
            retryable = response.status_code == 429 or response.status_code >= 500

        if not retryable or attempt == max_attempts:
            raise RenderFailure(last_error or "Unknown provider error.")

        time.sleep(min(2 ** (attempt - 1), 16))

    raise RenderFailure(last_error or "Provider request failed.")


def choose_extension(content_type: str, fallback: str = ".mp3") -> str:
    c = (content_type or "").lower()
    if "wav" in c:
        return ".wav"
    if "mpeg" in c or "mp3" in c:
        return ".mp3"
    return fallback


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--requests", type=Path, required=True)
    parser.add_argument("--voice-map", type=Path, required=True)
    parser.add_argument("--take-manifest", type=Path, required=True)
    parser.add_argument("--ledger-out", type=Path, default=None, help="Working ledger output. Defaults to <take-manifest>.working.json when executing.")
    parser.add_argument("--output-dir", type=Path, default=Path("renders/E01"))
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--only-block", action="append", default=[])
    parser.add_argument("--base-url", default=os.getenv("ELEVENLABS_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--output-format", default=os.getenv("ELEVENLABS_OUTPUT_FORMAT"))
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--max-attempts", type=int, default=4)
    args = parser.parse_args()

    requests = load_json(args.requests)
    voice_map = load_json(args.voice_map)
    take_manifest = load_json(args.take_manifest)

    validate_request_manifest(requests)
    validate_voice_map(requests, voice_map, execute=args.execute)
    validate_take_manifest(requests, take_manifest)

    print("AUTHORITY PASS")
    print(f"  blocks: {EXPECTED_BLOCKS}")
    print(f"  spoken words: {EXPECTED_WORDS}")
    print(f"  spoken SHA-256: {EXPECTED_SPOKEN_SHA256}")

    req_by_block = find_request_by_block(requests)
    rows = take_manifest["take_rows"]

    if args.only_block:
        allowed = set(args.only_block)
        unknown = allowed - set(req_by_block)
        if unknown:
            raise RenderFailure(f"Unknown --only-block IDs: {sorted(unknown)}")
        rows = [row for row in rows if row["block_id"] in allowed]

    if args.limit is not None:
        rows = rows[: args.limit]

    if not args.execute:
        print("DRY RUN — no provider calls will be made.")
        for row in rows:
            req = req_by_block[row["block_id"]]
            role = req["voice_role"]
            binding = voice_map["roles"][role]
            print(
                f"{row['take_id']} | {role} | {row['take_type']} | "
                f"{req['processing']['acoustic_domain']} | "
                f"{spoken_words(req['exact_text'])} words | "
                f"voice_id={binding.get('voice_id')!r} model_id={binding.get('model_id')!r}"
            )
        print(f"Planned rows: {len(rows)}")
        return 0

    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RenderFailure("ELEVENLABS_API_KEY is required for --execute.")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    ledger_path = args.ledger_out
    if ledger_path is None:
        ledger_path = args.take_manifest.with_name(args.take_manifest.stem + ".working.json")
    updated = copy.deepcopy(take_manifest)
    updated["status"] = "RENDER_IN_PROGRESS"
    updated_by_take = {row["take_id"]: row for row in updated["take_rows"]}

    with httpx.Client(timeout=args.timeout) as client:
        for n, row in enumerate(rows, start=1):
            ledger_row = updated_by_take[row["take_id"]]
            req = req_by_block[row["block_id"]]
            role = req["voice_role"]
            binding = voice_map["roles"][role]

            exact_text = req["exact_text"]
            if sha256_text(exact_text) != ledger_row["exact_text_sha256"]:
                raise RenderFailure(f"Exact-text hash failed before {row['take_id']}.")

            payload = build_payload(req, binding, row["take_type"])
            audio, provider_meta = request_audio(
                client=client,
                base_url=args.base_url,
                api_key=api_key,
                voice_id=binding["voice_id"],
                payload=payload,
                output_format=args.output_format,
                max_attempts=args.max_attempts,
            )

            ext = choose_extension(provider_meta.get("content_type", ""))
            filename = Path(row["local_filename"]).with_suffix(ext).name
            audio_path = args.output_dir / filename
            audio_path.write_bytes(audio)

            meta_path = audio_path.with_suffix(audio_path.suffix + ".meta.json")
            meta = {
                "take_id": row["take_id"],
                "block_id": row["block_id"],
                "voice_role": role,
                "voice_id": binding["voice_id"],
                "model_id": binding["model_id"],
                "take_type": row["take_type"],
                "exact_text_sha256": req["exact_text_sha256"],
                "raw_audio_sha256": sha256_bytes(audio),
                "provider_request_id": provider_meta.get("request_id") or None,
                "acoustic_domain": req["processing"]["acoustic_domain"],
                "post_chain": req["processing"]["post_chain"],
                "absolute_timestamp": None,
            }
            meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

            ledger_row["voice_id"] = binding["voice_id"]
            ledger_row["render_status"] = "RENDERED"
            ledger_row["provider_request_id"] = provider_meta.get("request_id") or None
            ledger_row["local_filename"] = filename
            ledger_row["raw_audio_sha256"] = meta["raw_audio_sha256"]

            atomic_write_json(ledger_path, updated)
            print(f"[{n}/{len(rows)}] RENDERED {row['take_id']} -> {audio_path}")

    updated["status"] = "RAW_RENDER_BATCH_COMPLETE"
    atomic_write_json(ledger_path, updated)
    print("RAW RENDER BATCH COMPLETE")
    print(f"Working ledger: {ledger_path}")
    print("QC / take selection / alignment are still pending.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RenderFailure as exc:
        print(f"FAIL-CLOSED: {exc}", file=sys.stderr)
        raise SystemExit(2)
