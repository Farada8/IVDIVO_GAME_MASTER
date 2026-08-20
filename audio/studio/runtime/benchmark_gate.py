#!/usr/bin/env python3
"""Evidence-based regression gate for Audio Novel Studio runtime.

Compares candidate metrics with an approved benchmark. No single synthetic metric can
lock a performance; this gate only blocks obvious regressions and records dimensions
that require human review.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

DEFAULT_DIRECTIONS={
    "mechanical_cadence_score":"LOWER_BETTER",
    "pause_variation_score":"HIGHER_BETTER",
    "speech_rate_variation_score":"HIGHER_BETTER",
    "dialogue_intelligibility_score":"HIGHER_BETTER",
    "voice_identity_score":"HIGHER_BETTER",
    "spatial_legibility_score":"HIGHER_BETTER",
    "mono_survival_score":"HIGHER_BETTER",
    "microtexture_fatigue_score":"LOWER_BETTER",
    "music_masking_score":"LOWER_BETTER",
    "human_believability_score":"HIGHER_BETTER",
    "human_want_to_continue_score":"HIGHER_BETTER"
}


def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def dump(p,d): Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")


def compare(baseline,candidate,tolerance=0.02):
    bm=baseline.get("metrics",baseline); cm=candidate.get("metrics",candidate)
    directions={**DEFAULT_DIRECTIONS,**baseline.get("directions",{}),**candidate.get("directions",{})}
    regressions=[]; improvements=[]; unavailable=[]
    for key,direction in directions.items():
        if key not in bm or key not in cm or bm.get(key) is None or cm.get(key) is None:
            unavailable.append(key); continue
        try: b=float(bm[key]); c=float(cm[key])
        except (TypeError,ValueError): unavailable.append(key); continue
        delta=c-b
        reg=(direction=="HIGHER_BETTER" and delta < -tolerance) or (direction=="LOWER_BETTER" and delta > tolerance)
        imp=(direction=="HIGHER_BETTER" and delta > tolerance) or (direction=="LOWER_BETTER" and delta < -tolerance)
        row={"metric":key,"baseline":b,"candidate":c,"delta":delta,"direction":direction}
        if reg: regressions.append(row)
        elif imp: improvements.append(row)
    critical=set(candidate.get("critical_metrics",baseline.get("critical_metrics",["dialogue_intelligibility_score","voice_identity_score","human_believability_score"])))
    critical_reg=[r for r in regressions if r["metric"] in critical]
    gate="FAIL" if critical_reg else ("REVIEW" if regressions or unavailable else "PASS")
    return {"schema":"IVDIVO_AUDIO_BENCHMARK_GATE_v1","gate":gate,"critical_regressions":critical_reg,
            "regressions":regressions,"improvements":improvements,"unavailable_metrics":unavailable,
            "law":"Synthetic improvement never replaces human listening; critical regression blocks promotion."}


def main():
    p=argparse.ArgumentParser(); p.add_argument("baseline"); p.add_argument("candidate"); p.add_argument("--output",required=True); p.add_argument("--tolerance",type=float,default=.02); a=p.parse_args()
    out=compare(load(a.baseline),load(a.candidate),a.tolerance); dump(a.output,out); print(out["gate"])
    raise SystemExit(2 if out["gate"]=="FAIL" else 0)

if __name__=="__main__": main()
