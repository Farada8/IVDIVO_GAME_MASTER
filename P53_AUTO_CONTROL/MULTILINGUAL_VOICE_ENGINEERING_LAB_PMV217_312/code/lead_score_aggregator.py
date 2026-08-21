#!/usr/bin/env python3
import json,sys
from pathlib import Path
def score(rows,contract):
    weights=contract["weights"]; out=[]
    for r in rows:
        hard=[x for x in r.get("hard_fails",[]) if x]
        total=sum(float(r["scores"].get(k,0))*w for k,w in weights.items())/sum(weights.values())
        decision="REJECT" if hard or total<70 else "HOLD" if total<80 else "CALLBACK" if total<88 else "PROVISIONAL_ELIGIBLE"
        out.append({"candidate_id":r["candidate_id"],"weighted_score":round(total,2),"hard_fails":hard,"decision":decision})
    return {"artifact":"BODYGUARD_RU_LEAD_SCORE_AGGREGATE_v1","results":out}
if __name__=="__main__":
    rows=json.loads(Path(sys.argv[1]).read_text())["rows"]; c=json.loads(Path(sys.argv[2]).read_text())
    Path(sys.argv[3]).write_text(json.dumps(score(rows,c),indent=2))
