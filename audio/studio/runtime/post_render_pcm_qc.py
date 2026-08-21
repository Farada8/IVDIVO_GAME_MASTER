#!/usr/bin/env python3
"""PCM-level QC for candidate post-render patches.

This module never fixes audio. It detects full-scale clipping and abrupt patch-boundary
sample discontinuities so renderers cannot hide defects by silently clipping.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable
import math
import wave

import numpy as np

from post_render_contracts import canonical_interval


def read_pcm_wav(path: str | Path) -> tuple[dict[str, Any], np.ndarray]:
    with wave.open(str(path), "rb") as wav:
        channels = wav.getnchannels()
        width = wav.getsampwidth()
        rate = wav.getframerate()
        frames = wav.getnframes()
        compression = wav.getcomptype()
        raw = wav.readframes(frames)
    if compression != "NONE":
        raise ValueError("PCM_QC_COMPRESSED_WAV_UNSUPPORTED")
    if width not in (2, 3):
        raise ValueError("PCM_QC_SAMPLE_WIDTH_UNSUPPORTED")
    if channels not in (1, 2):
        raise ValueError("PCM_QC_CHANNEL_COUNT_UNSUPPORTED")
    if rate != 48000:
        raise ValueError("PCM_QC_SAMPLE_RATE_NOT_CANONICAL")
    if width == 2:
        values = np.frombuffer(raw, dtype="<i2").astype(np.float64) / 32768.0
    else:
        b = np.frombuffer(raw, dtype=np.uint8)
        if b.size % 3:
            raise ValueError("PCM_QC_PCM24_MALFORMED")
        b = b.reshape(-1, 3)
        u = b[:, 0].astype(np.int32) | (b[:, 1].astype(np.int32) << 8) | (b[:, 2].astype(np.int32) << 16)
        signed = np.where(u & 0x800000, u | ~0xFFFFFF, u).astype(np.int32)
        values = signed.astype(np.float64) / 8388608.0
    return {
        "sample_rate_hz": rate,
        "channels": channels,
        "sample_width_bytes": width,
        "frame_count": frames,
        "duration_seconds": frames / float(rate),
    }, values.reshape(-1, channels)


def signal_qc(path: str | Path, *, clipping_threshold: float = 0.9995) -> dict[str, Any]:
    meta, audio = read_pcm_wav(path)
    peak = float(np.max(np.abs(audio))) if audio.size else 0.0
    clip_count = int(np.count_nonzero(np.abs(audio) >= clipping_threshold))
    peak_dbfs = 20.0 * math.log10(max(peak, 1e-12))
    return {
        "status": "PASS" if clip_count == 0 else "FAIL_CLIPPING",
        "sample_peak": peak,
        "sample_peak_dbfs": peak_dbfs,
        "clip_sample_count": clip_count,
        "clipping_threshold": clipping_threshold,
        "meta": meta,
    }


def patch_boundary_qc(
    path: str | Path,
    ranges: Iterable[dict[str, Any]],
    *,
    max_boundary_jump: float = 0.35,
) -> dict[str, Any]:
    """Flag abrupt sample jumps at patch boundaries; human/auditory review still decides audibility."""
    meta, audio = read_pcm_wav(path)
    rate = meta["sample_rate_hz"]
    findings: list[dict[str, Any]] = []
    for index, item in enumerate(ranges):
        interval = canonical_interval(item)
        for label, seconds in (("START", interval["start_seconds"]), ("END", interval["end_seconds"])):
            frame = int(round(seconds * rate))
            if frame <= 0 or frame >= len(audio):
                continue
            jump = float(np.max(np.abs(audio[frame] - audio[frame - 1])))
            if jump > max_boundary_jump:
                findings.append({
                    "range_index": index,
                    "boundary": label,
                    "seconds": seconds,
                    "sample_jump": jump,
                })
    return {
        "status": "PASS" if not findings else "HOLD_BOUNDARY_DISCONTINUITY",
        "findings": findings,
        "max_boundary_jump": max_boundary_jump,
        "machine_may_auto_repair": False,
    }


def candidate_render_qc(path: str | Path, ranges: Iterable[dict[str, Any]]) -> dict[str, Any]:
    signal = signal_qc(path)
    boundary = patch_boundary_qc(path, ranges)
    return {
        "status": "PASS" if signal["status"] == "PASS" and boundary["status"] == "PASS" else "HOLD",
        "signal": signal,
        "boundary": boundary,
        "silent_clipping_allowed": False,
    }
