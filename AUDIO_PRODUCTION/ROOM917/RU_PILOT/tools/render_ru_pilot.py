#!/usr/bin/env python3
"""ROOM917 Russian ElevenLabs audition renderer.

Dry-run by default. Live mode requires:
  ELEVENLABS_API_KEY
  ROOM917_RU_VOICE_ELENA
  ROOM917_RU_VOICE_JULIAN
  ROOM917_RU_VOICE_MINA
  ROOM917_RU_VOICE_CATE

The script intentionally renders audition units only. It does not auto-render full
E01/E02 before the voice-binding gate is passed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = HERE.parent / "ROOM917_RU_E01_E02_ELEVENLABS_V3_MANIFEST_v1.0.json"
API_BASE = "https://api.elevenlabs.io/v1"


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def voice_id_for(manifest: dict, character: str) -> str | None:
    binding = manifest["voice_bindings"][character]
    return os.getenv(binding["voice_id_env"])


def request_tts(api_key: str, voice_id: str, text: str, model_id: str, output_format: str) -> bytes:
    query = urllib.parse.urlencode({"output_format": output_format})
    url = f"{API_BASE}/text-to-speech/{urllib.parse.quote(voice_id)}?{query}"
    body = json.dumps({"text": text, "model_id": model_id}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"ElevenLabs HTTP {exc.code}: {detail}") from exc


def safe_name(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--out", type=Path, default=HERE.parent / "_renders" / "auditions")
    parser.add_argument("--live", action="store_true", help="Dispatch paid ElevenLabs requests.")
    parser.add_argument("--character", choices=["ELENA", "JULIAN", "MINA", "CATE"])
    parser.add_argument("--unit", help="Render only one audition unit id.")
    parser.add_argument("--sleep", type=float, default=0.35, help="Seconds between provider requests.")
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    model_id = manifest["provider"]["primary_dialogue_model"]
    output_format = manifest["provider"]["audition_output_format"]
    units = manifest["audition_units"]

    if args.character:
        units = [u for u in units if u["character"] == args.character]
    if args.unit:
        units = [u for u in units if u["id"] == args.unit]
    if not units:
        print("No audition units selected.", file=sys.stderr)
        return 2

    required_characters = sorted({u["character"] for u in units})
    missing_voice_bindings = [c for c in required_characters if not voice_id_for(manifest, c)]

    plan = {
        "mode": "LIVE" if args.live else "DRY_RUN",
        "model_id": model_id,
        "output_format": output_format,
        "selected_units": len(units),
        "characters": required_characters,
        "missing_voice_bindings": missing_voice_bindings,
    }
    print(json.dumps(plan, ensure_ascii=False, indent=2))

    if not args.live:
        for unit in units:
            print(f"\n[{unit['id']}] {unit['character']} x{unit.get('takes', 1)}")
            print(f"FUNCTION: {unit['function']}")
            print(f"DIRECTION: {unit['direction']}")
            print(f"TEXT: {unit['text']}")
        return 0

    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("LIVE blocked: ELEVENLABS_API_KEY is not set.", file=sys.stderr)
        return 3
    if missing_voice_bindings:
        print(
            "LIVE blocked: missing current RU voice bindings for " + ", ".join(missing_voice_bindings),
            file=sys.stderr,
        )
        return 4

    args.out.mkdir(parents=True, exist_ok=True)
    registry = []

    for unit in units:
        character = unit["character"]
        voice_id = voice_id_for(manifest, character)
        assert voice_id
        takes = int(unit.get("takes", 1))

        for take in range(1, takes + 1):
            audio = request_tts(api_key, voice_id, unit["text"], model_id, output_format)
            digest = hashlib.sha256(audio).hexdigest()
            filename = f"{safe_name(unit['id'])}__{character}__T{take:02d}.mp3"
            out_path = args.out / filename
            out_path.write_bytes(audio)
            registry.append(
                {
                    "unit_id": unit["id"],
                    "character": character,
                    "take": take,
                    "voice_id": voice_id,
                    "model_id": model_id,
                    "output_format": output_format,
                    "filename": filename,
                    "sha256": digest,
                    "bytes": len(audio),
                }
            )
            print(f"WROTE {out_path} sha256={digest}")
            time.sleep(max(args.sleep, 0.0))

    registry_path = args.out / "AUDITION_RENDER_REGISTRY.json"
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Registry: {registry_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
