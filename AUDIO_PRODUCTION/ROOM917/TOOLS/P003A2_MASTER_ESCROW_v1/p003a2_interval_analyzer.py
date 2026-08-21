#!/usr/bin/env python3
"""ROOM917 / IVDIVO P003A2 exact low-level interval analyzer.

Fail-closed design:
- Operates only on real PCM WAV bytes.
- Measures fixed-size RMS windows (default 100 ms) in dBFS.
- Extracts contiguous runs under one or more thresholds.
- NEVER promotes a low-level interval to a story/mix defect from level alone.
  Classification defaults to UNKNOWN_REQUIRES_LISTEN_OR_LIVE_TIMELINE unless an
  authoritative cue map explicitly supplies a class.

Python 3.10+; dependency: numpy.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, Sequence
import wave

import numpy as np

ALLOWED_CLASSES = {
    "PROTECTED_AUTHORED_PAUSE",
    "VALID_LOW_DENSITY",
    "MISSING_ROOM_OR_AMBIENCE_SUPPORT",
    "MISSING_CAUSAL_OVERLAP_CANDIDATE",
    "UNKNOWN_REQUIRES_LISTEN_OR_LIVE_TIMELINE",
}
DEFAULT_CLASS = "UNKNOWN_REQUIRES_LISTEN_OR_LIVE_TIMELINE"


def sha256_file(path: Path, block_size: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(block_size)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def decode_pcm(raw: bytes, sampwidth: int, channels: int) -> np.ndarray:
    """Return float64 PCM samples shaped (frames, channels), normalized to [-1, 1)."""
    if not raw:
        return np.empty((0, channels), dtype=np.float64)
    if sampwidth == 1:
        a = np.frombuffer(raw, dtype=np.uint8).astype(np.float64) - 128.0
        scale = 128.0
    elif sampwidth == 2:
        a = np.frombuffer(raw, dtype="<i2").astype(np.float64)
        scale = 32768.0
    elif sampwidth == 3:
        u = np.frombuffer(raw, dtype=np.uint8)
        if len(u) % 3:
            raise ValueError("24-bit PCM byte count is not divisible by 3")
        b = u.reshape(-1, 3).astype(np.int32)
        v = b[:, 0] | (b[:, 1] << 8) | (b[:, 2] << 16)
        v = np.where(v & 0x800000, v - 0x1000000, v)
        a = v.astype(np.float64)
        scale = 8388608.0
    elif sampwidth == 4:
        a = np.frombuffer(raw, dtype="<i4").astype(np.float64)
        scale = 2147483648.0
    else:
        raise ValueError(f"Unsupported PCM sample width: {sampwidth} bytes")
    if a.size % channels:
        raise ValueError("PCM sample count is not divisible by channel count")
    return (a / scale).reshape(-1, channels)


def rms_dbfs(samples: np.ndarray) -> float:
    if samples.size == 0:
        return float("-inf")
    ms = float(np.mean(np.square(samples), dtype=np.float64))
    if ms <= 0.0:
        return float("-inf")
    return 10.0 * math.log10(ms)


@dataclass
class Window:
    index: int
    start_seconds: float
    end_seconds: float
    rms_dbfs: float


@dataclass
class Interval:
    threshold_dbfs: float
    start_seconds: float
    end_seconds: float
    duration_seconds: float
    window_count: int
    min_rms_dbfs: float | None
    mean_rms_dbfs: float | None
    classification: str = DEFAULT_CLASS
    evidence_ids: list[str] | None = None
    notes: list[str] | None = None


def iter_windows(
    path: Path,
    *,
    start_seconds: float = 0.0,
    end_seconds: float | None = None,
    window_ms: float = 100.0,
) -> tuple[dict, list[Window]]:
    with wave.open(str(path), "rb") as wf:
        if wf.getcomptype() != "NONE":
            raise ValueError(f"Only PCM WAV is supported; got {wf.getcomptype()}")
        channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        rate = wf.getframerate()
        total_frames = wf.getnframes()
        duration = total_frames / rate
        if channels < 1:
            raise ValueError("Invalid channel count")
        if rate <= 0:
            raise ValueError("Invalid sample rate")
        if window_ms <= 0:
            raise ValueError("window_ms must be > 0")
        start_seconds = max(0.0, float(start_seconds))
        if end_seconds is None:
            end_seconds = duration
        end_seconds = min(float(end_seconds), duration)
        if end_seconds <= start_seconds:
            raise ValueError("end_seconds must be greater than start_seconds")

        start_frame = int(round(start_seconds * rate))
        end_frame = int(round(end_seconds * rate))
        end_frame = min(end_frame, total_frames)
        frames_per_window = max(1, int(round(rate * window_ms / 1000.0)))
        wf.setpos(start_frame)

        windows: list[Window] = []
        frame_pos = start_frame
        idx = 0
        while frame_pos < end_frame:
            n = min(frames_per_window, end_frame - frame_pos)
            raw = wf.readframes(n)
            if not raw:
                break
            arr = decode_pcm(raw, sampwidth, channels)
            actual_frames = arr.shape[0]
            if actual_frames == 0:
                break
            s = frame_pos / rate
            e = (frame_pos + actual_frames) / rate
            windows.append(Window(idx, s, e, rms_dbfs(arr)))
            frame_pos += actual_frames
            idx += 1

    meta = {
        "channels": channels,
        "sample_width_bytes": sampwidth,
        "sample_rate_hz": rate,
        "total_frames": total_frames,
        "duration_seconds": round(duration, 6),
        "segment_start_seconds": round(start_seconds, 6),
        "segment_end_seconds": round(end_seconds, 6),
        "window_ms": float(window_ms),
    }
    return meta, windows


def _finite_mean(vals: Sequence[float]) -> float | None:
    finite = [v for v in vals if math.isfinite(v)]
    return (sum(finite) / len(finite)) if finite else None


def extract_intervals(
    windows: Sequence[Window], threshold: float, *, merge_gap_ms: float = 0.0
) -> list[Interval]:
    below = [w for w in windows if w.rms_dbfs < threshold]
    if not below:
        return []
    groups: list[list[Window]] = []
    cur = [below[0]]
    for w in below[1:]:
        if w.index == cur[-1].index + 1:
            cur.append(w)
        else:
            groups.append(cur)
            cur = [w]
    groups.append(cur)

    if merge_gap_ms > 0 and len(groups) > 1:
        merged: list[list[Window]] = [groups[0]]
        max_gap = merge_gap_ms / 1000.0
        for g in groups[1:]:
            gap = g[0].start_seconds - merged[-1][-1].end_seconds
            if gap <= max_gap + 1e-9:
                merged[-1].extend(g)
            else:
                merged.append(g)
        groups = merged

    out: list[Interval] = []
    for g in groups:
        vals = [w.rms_dbfs for w in g]
        finite = [v for v in vals if math.isfinite(v)]
        minv = min(finite) if finite else None
        meanv = _finite_mean(vals)
        s = g[0].start_seconds
        e = g[-1].end_seconds
        out.append(
            Interval(
                threshold_dbfs=float(threshold),
                start_seconds=round(s, 6),
                end_seconds=round(e, 6),
                duration_seconds=round(e - s, 6),
                window_count=len(g),
                min_rms_dbfs=None if minv is None else round(minv, 4),
                mean_rms_dbfs=None if meanv is None else round(meanv, 4),
                evidence_ids=[],
                notes=[],
            )
        )
    return out


def load_cue_map(path: Path | None) -> list[dict]:
    if path is None:
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    cues = data.get("cues", data if isinstance(data, list) else [])
    if not isinstance(cues, list):
        raise ValueError("cue map must be a list or {'cues': [...]} object")
    for cue in cues:
        if "start_seconds" not in cue or "end_seconds" not in cue:
            raise ValueError("each cue requires start_seconds and end_seconds")
        if "classification" in cue and cue["classification"] not in ALLOWED_CLASSES:
            raise ValueError(f"invalid classification: {cue['classification']}")
    return cues


def overlap_seconds(a0: float, a1: float, b0: float, b1: float) -> float:
    return max(0.0, min(a1, b1) - max(a0, b0))


def apply_authoritative_classification(intervals: Iterable[Interval], cues: list[dict]) -> None:
    for iv in intervals:
        overlaps = []
        for cue in cues:
            ov = overlap_seconds(iv.start_seconds, iv.end_seconds, float(cue["start_seconds"]), float(cue["end_seconds"]))
            if ov > 0:
                overlaps.append((cue, ov))
        if not overlaps:
            continue
        iv.evidence_ids = [str(c.get("id", "UNNAMED_CUE")) for c, _ in overlaps]
        explicit = {c.get("classification") for c, _ in overlaps if c.get("classification")}
        if len(explicit) == 1:
            cls = next(iter(explicit))
            covered = sum(ov for c, ov in overlaps if c.get("classification") == cls)
            if covered >= iv.duration_seconds - 1e-6:
                iv.classification = cls
            else:
                iv.notes.append("Explicit classification covers only part of interval; kept UNKNOWN")
        elif len(explicit) > 1:
            iv.notes.append("Conflicting explicit classifications overlap interval; kept UNKNOWN")


def write_csv(path: Path, intervals: Sequence[Interval]) -> None:
    fields = [
        "threshold_dbfs", "start_seconds", "end_seconds", "duration_seconds",
        "window_count", "min_rms_dbfs", "mean_rms_dbfs", "classification",
        "evidence_ids", "notes",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for iv in intervals:
            d = asdict(iv)
            d["evidence_ids"] = ";".join(d["evidence_ids"] or [])
            d["notes"] = ";".join(d["notes"] or [])
            w.writerow(d)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("wav", type=Path)
    ap.add_argument("--segment-start", type=float, default=0.0)
    ap.add_argument("--segment-end", type=float, default=None)
    ap.add_argument("--window-ms", type=float, default=100.0)
    ap.add_argument("--thresholds", type=float, nargs="+", default=[-85.0, -50.0, -45.0])
    ap.add_argument("--merge-gap-ms", type=float, default=0.0)
    ap.add_argument("--cue-map", type=Path, default=None)
    ap.add_argument("--expected-sha256", default=None)
    ap.add_argument("--output-json", type=Path, required=True)
    ap.add_argument("--output-csv", type=Path, required=True)
    ap.add_argument("--skip-sha256", action="store_true")
    args = ap.parse_args()

    wav = args.wav.resolve()
    if not wav.is_file():
        raise SystemExit(f"WAV not found: {wav}")
    digest = None if args.skip_sha256 else sha256_file(wav)
    if args.expected_sha256 and digest != args.expected_sha256.lower():
        raise SystemExit(f"SHA256 mismatch: expected {args.expected_sha256}, got {digest}")

    meta, windows = iter_windows(
        wav,
        start_seconds=args.segment_start,
        end_seconds=args.segment_end,
        window_ms=args.window_ms,
    )
    cues = load_cue_map(args.cue_map)
    all_intervals: list[Interval] = []
    summary = {}
    for t in args.thresholds:
        ivs = extract_intervals(windows, t, merge_gap_ms=args.merge_gap_ms)
        apply_authoritative_classification(ivs, cues)
        all_intervals.extend(ivs)
        summary[str(t)] = {
            "interval_count": len(ivs),
            "below_threshold_seconds": round(sum(i.duration_seconds for i in ivs), 6),
        }

    result = {
        "schema_version": "ivdivo.room917.p003a2_interval_analysis/1.0",
        "status": "MEASURED_NOT_AUTOMATICALLY_PATCH_AUTHORIZED",
        "source": {
            "filename": wav.name,
            "size_bytes": wav.stat().st_size,
            "sha256": digest,
        },
        "analysis_basis": meta | {
            "thresholds_dbfs": args.thresholds,
            "merge_gap_ms": args.merge_gap_ms,
            "classification_law": sorted(ALLOWED_CLASSES),
            "fail_closed_rule": "LEVEL_ONLY_NEVER_PROVES_DEFECT",
        },
        "summary": summary,
        "intervals": [asdict(i) for i in all_intervals],
        "next_required_step": "JOIN_TO_ACCEPTED_SCENE_CUE_LINEAGE_AND_HUMAN_LISTEN_BEFORE_PATCH_AUTHORIZATION",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(args.output_csv, all_intervals)
    print(json.dumps({"status": "PASS", "summary": summary, "sha256": digest}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
