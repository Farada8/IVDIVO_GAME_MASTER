#!/usr/bin/env python3
import argparse,json
from pathlib import Path

DEFAULT_WEIGHTS={"uncertainty_reduction":0.35,"downstream_unlock":0.30,"cost_inverse":0.15,"irreversibility_inverse":0.10,"evidence_authority":0.10}

def score(x,w): return round(sum(float(x.get(k,0))*v for k,v in w.items()),4)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--backlog",type=Path,required=True); ap.add_argument("--out",type=Path,required=True); args=ap.parse_args()
    items=json.loads(args.backlog.read_text(encoding="utf-8"))["items"]; ranked=[]
    for x in items:
        if x.get("blocked_by"):
            x["score"]=0; x["routing"]="BLOCKED"
        else:
            x["score"]=score(x,DEFAULT_WEIGHTS); x["routing"]="ELIGIBLE"
        ranked.append(x)
    ranked.sort(key=lambda z:z["score"],reverse=True)
    out={"artifact":"IVDIVO_EXPECTED_INFORMATION_GAIN_ROUTER_RESULT_v1","weights":DEFAULT_WEIGHTS,"ranked":ranked}
    args.out.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
    print(ranked[0]["id"] if ranked else "EMPTY")

if __name__=="__main__": main()
