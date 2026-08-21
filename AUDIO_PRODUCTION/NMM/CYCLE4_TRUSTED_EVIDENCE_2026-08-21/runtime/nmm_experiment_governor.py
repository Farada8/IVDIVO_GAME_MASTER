"""Value-of-information governor preventing architecture/meta-work starvation."""
from __future__ import annotations
PRIORITY={"REAL_PROVIDER":100,"REAL_HUMAN":95,"SPECIALIST":80,"MEASURED_ECONOMICS":75,"DETERMINISTIC_GAP":60,"NEW_SCHEMA":20,"GENERIC_ARCHITECTURE":10}
def choose(actions:list[dict])->dict:
    eligible=[a for a in actions if not a.get("blocked")]
    if not eligible: return {"gate":"HOLD","reason":"ALL_ACTIONS_BLOCKED"}
    ranked=sorted(eligible,key=lambda a:(PRIORITY.get(a.get("class"),0)+float(a.get("info_gain",0))-float(a.get("cost",0))),reverse=True)
    best=ranked[0]
    if best.get("class")=="GENERIC_ARCHITECTURE" and not best.get("demonstrated_gap"):
        return {"gate":"REFUSE_META_WORK","reason":"NO_DEMONSTRATED_GENERIC_GAP"}
    return {"gate":"EXECUTE","selected":best,"ranked_ids":[a.get("id") for a in ranked]}
