#!/usr/bin/env python3
import argparse,json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--patch",type=Path,required=True); ap.add_argument("--evidence",type=Path,nargs="+",required=True); ap.add_argument("--out",type=Path,required=True); args=ap.parse_args()
    patch=json.loads(args.patch.read_text(encoding="utf-8")); ev=[json.loads(p.read_text(encoding="utf-8")) for p in args.evidence]
    high=[e for e in ev if e.get("status")=="PASS" and e.get("authority_weight",0)>=70]
    independent={(e.get("source_type"),e.get("provenance",{}).get("source_id")) for e in high}
    decision="HOLD"
    if len(independent)>=2 and patch.get("decision") in ["CANDIDATE","ACCEPT_WITH_MODIFICATION"]:
        decision="ACCEPT_WITH_MODIFICATION"
    out={"artifact":"IVDIVO_LEARNING_PROMOTION_DECISION_v1","patch_id":patch["patch_id"],"high_authority_pass_count":len(high),"independent_evidence_count":len(independent),"decision":decision,"law":"No AI/model vote promotes canon or universal runtime without independent evidence."}
    args.out.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8"); print(decision)

if __name__=="__main__": main()
