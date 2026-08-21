#!/usr/bin/env python3
"""IVDIVO Audio Studio canonical audio asset ingest.

Normalizes provider/local audio bytes into evidence-bearing ingest records before take
registry/timeline use. It is intentionally strict and provider-neutral.

Supported canonical ingest:
- WAV PCM, 48 kHz, mono/stereo, 16/24/32-bit integer;
- raw signed little-endian PCM16, 48 kHz, mono/stereo, wrapped losslessly to WAV.

Anything else must be converted explicitly upstream; this module never guesses a
sample rate/channel count and never silently transcodes accepted evidence.
"""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Any
import io
import wave

CANONICAL_SAMPLE_RATE = 48000
ALLOWED_CHANNELS = {1, 2}
ALLOWED_SAMPLE_WIDTH_BYTES = {2, 3, 4}


def _sha(data: bytes) -> str:
    return sha256(data).hexdigest()


def pcm_s16le_to_wav(pcm: bytes, *, sample_rate: int, channels: int) -> bytes:
    if sample_rate != CANONICAL_SAMPLE_RATE:
        raise ValueError("FAIL_AUDIO_SAMPLE_RATE")
    if channels not in ALLOWED_CHANNELS:
        raise ValueError("FAIL_AUDIO_CHANNEL_COUNT")
    frame_bytes = 2 * channels
    if not pcm or len(pcm) % frame_bytes:
        raise ValueError("FAIL_AUDIO_PCM_LENGTH")
    out = io.BytesIO()
    with wave.open(out, "wb") as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(pcm)
    return out.getvalue()


def inspect_wav(data: bytes) -> dict[str, Any]:
    try:
        with wave.open(io.BytesIO(data), "rb") as wav:
            channels = wav.getnchannels()
            sample_width = wav.getsampwidth()
            sample_rate = wav.getframerate()
            frames = wav.getnframes()
            compression = wav.getcomptype()
    except (wave.Error, EOFError) as exc:
        raise ValueError("FAIL_AUDIO_WAV_PARSE") from exc

    if compression != "NONE":
        raise ValueError("FAIL_AUDIO_WAV_COMPRESSED")
    if sample_rate != CANONICAL_SAMPLE_RATE:
        raise ValueError("FAIL_AUDIO_SAMPLE_RATE")
    if channels not in ALLOWED_CHANNELS:
        raise ValueError("FAIL_AUDIO_CHANNEL_COUNT")
    if sample_width not in ALLOWED_SAMPLE_WIDTH_BYTES:
        raise ValueError("FAIL_AUDIO_SAMPLE_WIDTH")
    if frames <= 0:
        raise ValueError("FAIL_AUDIO_ZERO_FRAMES")

    return {
        "container": "WAV",
        "codec": "PCM_INTEGER",
        "sample_rate_hz": sample_rate,
        "channels": channels,
        "sample_width_bytes": sample_width,
        "bit_depth": sample_width * 8,
        "frame_count": frames,
        "duration_seconds": frames / float(sample_rate),
    }


def ingest_audio_bytes(
    data: bytes,
    *,
    source_format: str,
    source_ref: str,
    raw_pcm_sample_rate: int | None = None,
    raw_pcm_channels: int | None = None,
) -> tuple[bytes, dict[str, Any]]:
    """Return canonical WAV bytes plus immutable ingest evidence."""
    if not data:
        raise ValueError("FAIL_AUDIO_EMPTY")
    source_sha = _sha(data)
    fmt = source_format.upper()

    if fmt == "WAV":
        canonical = data
        transformation = "NONE"
    elif fmt in {"PCM_S16LE", "PCM16LE"}:
        if raw_pcm_sample_rate is None or raw_pcm_channels is None:
            raise ValueError("FAIL_AUDIO_RAW_PCM_METADATA_REQUIRED")
        canonical = pcm_s16le_to_wav(
            data,
            sample_rate=raw_pcm_sample_rate,
            channels=raw_pcm_channels,
        )
        transformation = "LOSSLESS_CONTAINER_WRAP_PCM16LE_TO_WAV"
    else:
        raise ValueError("FAIL_AUDIO_FORMAT_UNSUPPORTED")

    technical = inspect_wav(canonical)
    canonical_sha = _sha(canonical)
    evidence = {
        "schema_version": "1.0",
        "source_ref": source_ref,
        "source_format": fmt,
        "source_bytes": len(data),
        "source_sha256": source_sha,
        "canonical_format": "WAV_PCM_48K",
        "canonical_bytes": len(canonical),
        "canonical_sha256": canonical_sha,
        "transformation": transformation,
        "technical": technical,
        "gate": "PASS",
    }
    return canonical, evidence


def persist_ingest(
    input_path: str | Path,
    output_path: str | Path,
    *,
    source_format: str = "WAV",
    raw_pcm_sample_rate: int | None = None,
    raw_pcm_channels: int | None = None,
) -> dict[str, Any]:
    inp = Path(input_path)
    data = inp.read_bytes()
    canonical, evidence = ingest_audio_bytes(
        data,
        source_format=source_format,
        source_ref=str(inp),
        raw_pcm_sample_rate=raw_pcm_sample_rate,
        raw_pcm_channels=raw_pcm_channels,
    )
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(canonical)
    evidence["canonical_path"] = str(out)
    return evidence
