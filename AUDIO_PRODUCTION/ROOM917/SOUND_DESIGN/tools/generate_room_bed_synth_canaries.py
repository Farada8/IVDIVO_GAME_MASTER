#!/usr/bin/env python3
"""Generate deterministic ROOM917 A01/A02 ambience canaries.

These outputs are SYNTHETIC_REFERENCE_ONLY. They are listening/engineering
candidates and can never become production-bound merely because this script
runs. Production binding still requires the sound asset identity gate, blind
human audition, mono/phone checks, false-clue audit, and explicit accepted
SHA-256.

No story text is changed. No provider is called. No paid synthesis occurs.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48_000
DURATION_S = 30.0
OVERLAP_S = 2.0
PREROLL_S = 5.0
SEED = 91720260824


def colored_noise(rng: np.random.Generator, beta: float, n: int) -> np.ndarray:
    white = rng.standard_normal(n)
    spectrum = np.fft.rfft(white)
    freqs = np.fft.rfftfreq(n, 1 / SR)
    scale = np.ones_like(freqs)
    scale[1:] = 1 / np.maximum(freqs[1:], 1.0) ** (beta / 2)
    signal = np.fft.irfft(spectrum * scale, n)
    return signal / (np.max(np.abs(signal)) + 1e-12)


def band(signal: np.ndarray, lo: float | None = None, hi: float | None = None, order: int = 4) -> np.ndarray:
    nyquist = SR / 2
    if lo and hi:
        sos = butter(order, [lo / nyquist, hi / nyquist], btype="band", output="sos")
    elif lo:
        sos = butter(order, lo / nyquist, btype="high", output="sos")
    else:
        sos = butter(order, hi / nyquist, btype="low", output="sos")
    return sosfilt(sos, signal)


def seamless_from_long(signal: np.ndarray, n_out: int, overlap_s: float) -> np.ndarray:
    length = int(overlap_s * SR)
    if len(signal) < n_out + length:
        raise ValueError("source too short for overlap loop")
    output = signal[:n_out].copy()
    t = np.linspace(0, 1, length, endpoint=False)[:, None]
    fade_out = np.cos(t * np.pi / 2) ** 2
    fade_in = np.sin(t * np.pi / 2) ** 2
    # Start of the loop is crossfaded from the post-tail continuation into the
    # actual head. Therefore the end -> start boundary follows a continuous
    # source trajectory rather than a hard splice.
    output[:length] = signal[n_out:n_out + length] * fade_out + signal[:length] * fade_in
    return output


def events(rng: np.random.Generator, n: int, rate_hz: float, amp_range: tuple[float, float],
           freqs: list[float], decay_s: float, spread: float = 0.5, edge_s: float = 0.0) -> np.ndarray:
    output = np.zeros((n, 2), dtype=np.float64)
    duration = n / SR
    count = max(1, int(rate_hz * duration))
    for event_time in rng.uniform(edge_s, duration - edge_s, count):
        start = int(event_time * SR)
        size = min(int(decay_s * SR), n - start)
        index = np.arange(size)
        event = np.zeros(size)
        for freq in freqs:
            event += np.sin(2 * np.pi * freq * index / SR + rng.uniform(0, 2 * np.pi)) * np.exp(
                -index / (SR * decay_s * 0.25)
            )
        event /= len(freqs)
        pan = rng.uniform(-spread, spread)
        left = np.sqrt((1 - pan) / 2)
        right = np.sqrt((1 + pan) / 2)
        amplitude = rng.uniform(*amp_range)
        output[start:start + size, 0] += amplitude * left * event
        output[start:start + size, 1] += amplitude * right * event
    return output


def generate(kind: str, rng: np.random.Generator) -> np.ndarray:
    n_raw = int((DURATION_S + OVERLAP_S + PREROLL_S) * SR)
    if kind == "A01":
        rain = np.stack([
            band(colored_noise(rng, 0.35, n_raw), 650, 9500),
            band(colored_noise(rng, 0.35, n_raw), 650, 9500),
        ], axis=1)
        rain /= np.max(np.abs(rain))
        rain *= 0.10
        wind = band(colored_noise(rng, 1.8, n_raw), 30, 380)
        wind /= np.max(np.abs(wind))
        wind = np.stack([wind, np.roll(wind, int(0.019 * SR))], axis=1) * 0.042
        body = band(colored_noise(rng, 1.1, n_raw), 75, 1300)
        body /= np.max(np.abs(body))
        body = np.stack([body, np.roll(body, int(0.009 * SR))], axis=1) * 0.016
        signal = rain + wind + body
        # Sparse non-clue material: thermal/radiator ticks and very distant
        # cutlery-like material. Intentionally quiet and non-rhythmic.
        signal += events(rng, n_raw, 0.18, (0.004, 0.011), [1250, 2300, 3600], 0.06, 0.6, 1.0)
        signal += events(rng, n_raw, 0.08, (0.0025, 0.006), [1900, 3200, 4900], 0.10, 0.8, 1.0)
        for delay_s, gain in [(0.032, 0.075), (0.058, 0.050), (0.094, 0.028)]:
            signal += np.roll(signal, int(delay_s * SR), axis=0) * gain
        target_peak = 0.36
    elif kind == "A02":
        rain = np.stack([
            band(colored_noise(rng, 0.5, n_raw), 900, 6500),
            band(colored_noise(rng, 0.5, n_raw), 900, 6500),
        ], axis=1)
        rain /= np.max(np.abs(rain))
        rain *= 0.043
        body = band(colored_noise(rng, 1.8, n_raw), 38, 430)
        body /= np.max(np.abs(body))
        body = np.stack([body, np.roll(body, int(0.006 * SR))], axis=1) * 0.025
        wood = band(colored_noise(rng, 1.5, n_raw), 110, 720)
        wood /= np.max(np.abs(wood))
        wood = np.stack([wood, np.roll(wood, int(0.004 * SR))], axis=1) * 0.013
        signal = rain + body + wood
        for delay_s, gain in [(0.014, 0.05), (0.027, 0.03)]:
            signal += np.roll(signal, int(delay_s * SR), axis=0) * gain
        mid = signal.mean(axis=1)
        side = (signal[:, 0] - signal[:, 1]) * 0.25
        signal = np.stack([mid + side / 2, mid - side / 2], axis=1)
        target_peak = 0.25
    else:
        raise ValueError(f"unknown kind: {kind}")

    signal = signal[int(PREROLL_S * SR):]
    output = seamless_from_long(signal, int(DURATION_S * SR), OVERLAP_S)
    output /= max(1.0, np.max(np.abs(output)) / target_peak)
    return output


def main() -> int:
    output_dir = Path("ROOM917_ROOM_BED_SYNTH_CANARIES")
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    assets = []
    for kind, name in [
        ("A01", "A01_GREYHAVEN_LOBBY_30S_LOOP_CANDIDATE_SYNTH02"),
        ("A02", "A02_SWITCHBOARD_ALCOVE_30S_LOOP_CANDIDATE_SYNTH02"),
    ]:
        audio = generate(kind, rng)
        path = output_dir / f"{name}.wav"
        sf.write(path, audio, SR, subtype="PCM_24")
        data = path.read_bytes()
        delta = np.diff(audio, axis=0)
        seam = audio[0] - audio[-1]
        diff_rms = np.sqrt(np.mean(delta * delta, axis=0))
        seam_db = 20 * np.log10((np.abs(seam) + 1e-12) / (diff_rms + 1e-12))
        assets.append({
            "asset_id": name,
            "path": str(path),
            "sha256": hashlib.sha256(data).hexdigest(),
            "size_bytes": len(data),
            "sample_rate_hz": SR,
            "bit_depth": 24,
            "channels": 2,
            "duration_s": DURATION_S,
            "seam_vs_internal_diff_rms_db_lr": [float(v) for v in seam_db],
            "status": "CANDIDATE_HOLD_HUMAN_AUDITION_REQUIRED",
            "origin": "PROCEDURAL_SYNTHETIC_REFERENCE_ONLY",
            "production_binding": False,
        })
    receipt = {
        "schema_version": "room917.room_bed_synthetic_canary_receipt/2.0",
        "date": "2026-08-22",
        "seed": SEED,
        "assets": assets,
        "laws": [
            "NOT_PRODUCTION_BINDING",
            "HUMAN_BLIND_LISTEN_REQUIRED",
            "NO_STORY_CHANGE",
            "NO_PROVIDER_SPEND",
        ],
    }
    (output_dir / "ROOM917_E01_ROOM_BED_SYNTHETIC_CANARY_RECEIPT_v2.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
