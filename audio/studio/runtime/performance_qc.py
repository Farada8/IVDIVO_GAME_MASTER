#!/usr/bin/env python3
"""IVDIVO Audio Novel Studio — mechanical performance QC.

This module does NOT claim to judge acting by waveform alone. It measures timing,
pause structure, activity and level dynamics, then compares them with authored
rhythm requirements or a regression fixture. Human/AI-director listening remains
mandatory for artistic acceptance.
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
import wave
from array import array
from pathlib import Path
from typing import Any, Dict, List, Tuple

EPS = 1e-12


def dbfs(value: float) -> float:
    return 20.0 * math.log10(max(abs(value), EPS))


def percentile(values: List[float], p: float) -> float | None:
    if not values:
        return None
    xs = sorted(values)
    if len(xs) == 1:
        return xs[0]
    rank = (len(xs) - 1) * p
    lo = int(math.floor(rank)); hi = int(math.ceil(rank))
    if lo == hi:
        return xs[lo]
    frac = rank - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


def _decode_pcm(raw: bytes, sampwidth: int) -> List[float]:
    out: List[float] = []
    if sampwidth == 1:
        out = [(b - 128) / 128.0 for b in raw]
    elif sampwidth == 2:
        a = array("h"); a.frombytes(raw)
        import sys
        if sys.byteorder != "little": a.byteswap()
        out = [v / 32768.0 for v in a]
    elif sampwidth == 3:
        scale = float(1 << 23)
        for i in range(0, len(raw) - 2, 3):
            b0, b1, b2 = raw[i], raw[i + 1], raw[i + 2]
            v = b0 | (b1 << 8) | (b2 << 16)
            if v & 0x800000: v -= 1 << 24
            out.append(v / scale)
    elif sampwidth == 4:
        a = array("i"); a.frombytes(raw)
        import sys
        if sys.byteorder != "little": a.byteswap()
        out = [v / 2147483648.0 for v in a]
    else:
        raise ValueError(f"Unsupported PCM sample width: {sampwidth} bytes")
    return out


def load_wav_mono(path: Path) -> Tuple[List[float], Dict[str, Any]]:
    with wave.open(str(path), "rb") as wf:
        nch = wf.getnchannels(); sw = wf.getsampwidth(); sr = wf.getframerate(); n = wf.getnframes(); comptype = wf.getcomptype()
        if comptype != "NONE": raise ValueError(f"Compressed WAV unsupported: {comptype}")
        raw = wf.readframes(n)
    samples = _decode_pcm(raw, sw)
    if nch > 1:
        mono: List[float] = []
        for i in range(0, len(samples) - nch + 1, nch):
            mono.append(sum(samples[i:i+nch]) / nch)
        samples = mono
    return samples, {"sample_rate": sr, "channels": nch, "sample_width_bytes": sw, "frame_count": n, "duration_s": n / sr if sr else 0.0}


def frame_rms_db(samples: List[float], sr: int, frame_ms: int) -> List[float]:
    size = max(1, int(sr * frame_ms / 1000.0))
    out: List[float] = []
    for i in range(0, len(samples) - size + 1, size):
        frame = samples[i:i+size]
        out.append(dbfs(math.sqrt(sum(v*v for v in frame) / len(frame) + EPS)))
    return out


def pause_segments(db_frames: List[float], frame_ms: int, threshold_dbfs: float, min_pause_s: float) -> List[Dict[str, float]]:
    silent = [v < threshold_dbfs for v in db_frames]
    segments: List[Dict[str, float]] = []
    i = 0; frame_s = frame_ms / 1000.0
    while i < len(silent):
        if not silent[i]: i += 1; continue
        j = i + 1
        while j < len(silent) and silent[j]: j += 1
        dur = (j - i) * frame_s
        if dur >= min_pause_s:
            segments.append({"start_s": round(i * frame_s, 6), "end_s": round(j * frame_s, 6), "duration_s": round(dur, 6)})
        i = j
    return segments


def analyze_wav(path: Path, silence_threshold_dbfs: float = -45.0) -> Dict[str, Any]:
    samples, meta = load_wav_mono(path); sr = int(meta["sample_rate"])
    peak = max((abs(v) for v in samples), default=0.0)
    rms = math.sqrt(sum(v*v for v in samples) / max(1, len(samples)) + EPS)
    db20 = frame_rms_db(samples, sr, 20); db100 = frame_rms_db(samples, sr, 100)
    active100 = [v for v in db100 if v > -40.0]
    pauses = pause_segments(db20, 20, silence_threshold_dbfs, 0.08); durations = [p["duration_s"] for p in pauses]
    pause_mean = statistics.mean(durations) if durations else 0.0
    pause_std = statistics.pstdev(durations) if len(durations) > 1 else 0.0
    active_p10 = percentile(active100, 0.10); active_p90 = percentile(active100, 0.90)
    metrics = {
        **meta,
        "peak_dbfs": round(dbfs(peak), 4), "rms_dbfs": round(dbfs(rms), 4),
        "active_ratio": round(sum(1 for v in db100 if v > -40.0) / len(db100), 6) if db100 else 0.0,
        "active_level_spread_db": round(active_p90 - active_p10, 4) if active_p10 is not None and active_p90 is not None else None,
        "silence_threshold_dbfs": silence_threshold_dbfs,
        "pause_count_ge_0_08": len(durations),
        "pause_median_s": round(statistics.median(durations), 4) if durations else 0.0,
        "pause_mean_s": round(pause_mean, 4), "pause_std_s": round(pause_std, 4),
        "pause_cv": round(pause_std / pause_mean, 4) if pause_mean > 0 else 0.0,
        "pause_p10_s": round(percentile(durations, 0.10) or 0.0, 4),
        "pause_p90_s": round(percentile(durations, 0.90) or 0.0, 4),
        "pause_max_s": round(max(durations), 4) if durations else 0.0,
        "pause_count_ge_0_5": sum(1 for d in durations if d >= 0.5),
        "pause_count_ge_0_8": sum(1 for d in durations if d >= 0.8),
        "pause_count_ge_1_0": sum(1 for d in durations if d >= 1.0),
        "silence_total_s_ge_0_08": round(sum(durations), 4),
    }
    diagnostics: List[Dict[str, Any]] = []
    p90 = percentile(durations, 0.90) or 0.0; p10 = percentile(durations, 0.10) or 0.0
    if len(durations) >= 20 and p90 - p10 < 0.20:
        diagnostics.append({"severity":"MEDIUM","code":"LOW_PAUSE_VARIATION_RISK","evidence":{"pause_p10_s":round(p10,3),"pause_p90_s":round(p90,3),"count":len(durations)},"note":"Mechanical timing is highly clustered. Artistic verdict still requires plan/listening context."})
    if durations and max(durations) < 0.5:
        diagnostics.append({"severity":"MEDIUM","code":"NO_LONG_PAUSE_SIGNAL","evidence":{"pause_max_s":round(max(durations),3)},"note":"No silence >=0.5s detected. This is only a defect if authored rhythm requires it."})
    if meta["channels"] == 1:
        diagnostics.append({"severity":"INFO","code":"MONO_SOURCE","evidence":{"channels":1},"note":"Acceptable for dry dialogue; not a spatial/mastering failure by itself."})
    return {"schema":"IVDIVO_PERFORMANCE_QC_MECHANICAL_v1","file":str(path),"metrics":metrics,"diagnostics":diagnostics,"artistic_scope_warning":"Waveform metrics cannot prove believable acting. Human/AI-director listening gate remains required."}


def _plan_expectations(plan: Dict[str, Any]) -> Dict[str, Any]:
    events = plan.get("events") or []; protected=[]; planned_long=0
    for e in events:
        rng=e.get("pause_range_ms")
        if e.get("protected_silence"): protected.append(e)
        if isinstance(rng,dict):
            target=rng.get("target_ms") or rng.get("minimum_ms")
            try:
                if target is not None and float(target)>=500: planned_long+=1
            except (TypeError,ValueError): pass
    return {"protected_silence_events":len(protected),"planned_pause_events_ge_500ms":planned_long}


def evaluate_plan(report: Dict[str, Any], plan: Dict[str, Any]) -> List[Dict[str, Any]]:
    expectations=_plan_expectations(plan); metrics=report["metrics"]; issues=[]
    expected_long=expectations["planned_pause_events_ge_500ms"]; actual_long=metrics.get("pause_count_ge_0_5",0)
    if expected_long>0 and actual_long<expected_long:
        issues.append({"severity":"MAJOR","code":"AUTHORED_LONG_PAUSE_REQUIREMENTS_NOT_VISIBLE","expected_min_count":expected_long,"actual_count":actual_long,"smallest_repair":"EDIT_ONLY or selective rerender around authored pause anchors; do not add music to hide the timing defect."})
    return issues


def evaluate_baseline(report: Dict[str, Any], baseline: Dict[str, Any]) -> List[Dict[str, Any]]:
    metrics=report["metrics"]; rules=baseline.get("candidate_acceptance_rules") or []; issues=[]
    for rule in rules:
        metric=rule.get("metric"); op=rule.get("op"); target=rule.get("value"); actual=metrics.get(metric); passed=False
        if isinstance(actual,(int,float)) and isinstance(target,(int,float)):
            if op==">=": passed=actual>=target
            elif op==">": passed=actual>target
            elif op=="<=": passed=actual<=target
            elif op=="<": passed=actual<target
            elif op=="==": passed=actual==target
        if not passed:
            issues.append({"severity":rule.get("severity","MAJOR"),"code":"REGRESSION_RULE_FAIL","metric":metric,"op":op,"target":target,"actual":actual,"reason":rule.get("reason")})
    return issues


def main() -> None:
    p=argparse.ArgumentParser(description="Mechanical performance QC for IVDIVO audio")
    p.add_argument("wav"); p.add_argument("--plan"); p.add_argument("--baseline"); p.add_argument("--output"); p.add_argument("--silence-threshold-dbfs",type=float,default=-45.0)
    args=p.parse_args(); report=analyze_wav(Path(args.wav),args.silence_threshold_dbfs); gate_issues=[]
    if args.plan:
        plan=json.loads(Path(args.plan).read_text(encoding="utf-8")); report["plan_expectations"]=_plan_expectations(plan); gate_issues.extend(evaluate_plan(report,plan))
    if args.baseline:
        baseline=json.loads(Path(args.baseline).read_text(encoding="utf-8")); report["baseline_id"]=baseline.get("baseline_id"); gate_issues.extend(evaluate_baseline(report,baseline))
    report["gate_issues"]=gate_issues
    report["gate"]="FAIL" if any(i.get("severity") in {"FATAL","MAJOR"} for i in gate_issues) else "PASS_WITH_HUMAN_LISTEN_REQUIRED"
    text=json.dumps(report,ensure_ascii=False,indent=2)+"\n"
    if args.output: Path(args.output).write_text(text,encoding="utf-8")
    else: print(text,end="")
    raise SystemExit(2 if report["gate"]=="FAIL" else 0)


if __name__ == "__main__":
    main()
