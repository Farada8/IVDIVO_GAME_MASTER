"""Score NMM blind whistle trials after answers are frozen; predeclared thresholds are hash-bound."""
from __future__ import annotations
import hashlib, json

def canonical_hash(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def seal_protocol(protocol:dict)->dict:
    out=dict(protocol); out["sealed_protocol_sha256"]=canonical_hash(protocol); return out

def verify_protocol_seal(sealed:dict)->bool:
    x=dict(sealed); h=x.pop("sealed_protocol_sha256",None); return h==canonical_hash(x)

def score_rows(rows:list[dict], answer_key:dict, sealed_protocol:dict)->dict:
    if not verify_protocol_seal(sealed_protocol): return {"gate":"FAIL_PROTOCOL_MUTATED"}
    min_accuracy=float(sealed_protocol["min_accuracy"]); min_realism=float(sealed_protocol["min_mean_realism"])
    correct=0; scored=0; realism=[]; unknown=[]
    for r in rows:
        trial=str(r.get("trial","")).zfill(2); dev=str(r.get("device_pass","")).upper()
        key=f"{dev}:{trial}"; ans=answer_key.get(key)
        if ans is None: unknown.append(key); continue
        guess=str(r.get("shorter_sound_guess_FIRST_SECOND_CANNOT_TELL","")).upper()
        if guess in {"FIRST","SECOND","CANNOT_TELL"}:
            scored+=1; correct += int(guess==ans)
        try:
            rv=float(r.get("realism_1_5",""))
            if 1<=rv<=5: realism.append(rv)
        except Exception: pass
    acc=(correct/scored) if scored else None; mr=(sum(realism)/len(realism)) if realism else None
    pass_gate= acc is not None and mr is not None and acc>=min_accuracy and mr>=min_realism and not unknown
    return {"gate":"PASS" if pass_gate else "HOLD_OR_FAIL","scored_trials":scored,"accuracy":acc,"mean_realism":mr,"unknown_keys":unknown,
            "thresholds":{"min_accuracy":min_accuracy,"min_mean_realism":min_realism}}
