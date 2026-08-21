#!/usr/bin/env python3
from __future__ import annotations
import argparse,subprocess,sys,json
from pathlib import Path

def run(cmd):
    print("+"," ".join(map(str,cmd)))
    subprocess.run(list(map(str,cmd)),check=True)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--master",required=True); ap.add_argument("--expected-sha256",required=True); ap.add_argument("--semantic-lineage",required=True); ap.add_argument("--timing-map",required=True); ap.add_argument("--analyzer",required=True,help="Path to existing P003A2 analyzer"); ap.add_argument("--outdir",required=True); args=ap.parse_args()
    od=Path(args.outdir); od.mkdir(parents=True,exist_ok=True); here=Path(__file__).resolve().parent; resolved=od/"01_resolved_lineage.json"
    run([sys.executable,here/"lineage_timing_resolver.py","--semantic-lineage",args.semantic_lineage,"--timing-map",args.timing_map,"--out",resolved])
    lin=json.loads(resolved.read_text())
    if lin.get("timing_state")!="RESOLVED_COMPLETE": raise SystemExit("Timing map incomplete: production interval classification is blocked.")
    analysis=od/"02_p003a2_intervals.json"; csv=od/"02_p003a2_intervals.csv"
    run([sys.executable,args.analyzer,args.master,"--segment-start","0","--segment-end","444.980","--window-ms","100","--thresholds","-85","-50","-45","--expected-sha256",args.expected_sha256,"--output-json",analysis,"--output-csv",csv])
    classified=od/"03_classified_intervals.json"; run([sys.executable,here/"interval_classifier.py","--intervals",analysis,"--lineage",resolved,"--out",classified])
    plan=od/"04_selective_repair_plan.json"; run([sys.executable,here/"selective_repair_planner.py","--classified",classified,"--lineage",resolved,"--master-sha256",args.expected_sha256,"--out",plan])
    print(json.dumps({"status":"PASS_TO_REPAIR_PLAN","outputs":[str(resolved),str(analysis),str(classified),str(plan)]},indent=2))
if __name__=="__main__": main()
