#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--state",required=True); ap.add_argument("--master-path"); ap.add_argument("--lineage-compiled"); ap.add_argument("--interval-analysis"); ap.add_argument("--classified"); ap.add_argument("--patch-plan"); ap.add_argument("--patched-master"); ap.add_argument("--regression"); ap.add_argument("--out",required=True); args=ap.parse_args()
    state=json.loads(Path(args.state).read_text(encoding="utf-8")); stages=[]; exists=lambda x: bool(x and Path(x).exists()); master_ok=exists(args.master_path); lineage_ok=exists(args.lineage_compiled); analysis_ok=exists(args.interval_analysis); class_ok=exists(args.classified); plan_ok=exists(args.patch_plan); patched_ok=exists(args.patched_master); reg_ok=False
    if exists(args.regression):
        try: reg_ok=json.loads(Path(args.regression).read_text()).get("status")=="PASS"
        except Exception: pass
    stages += [
      {"stage":"MASTER_BYTE_ESCROW","status":"PASS_LOCAL_BYTES_PRESENT" if master_ok else "BLOCKED","next":"Provide exact immutable full-master bytes" if not master_ok else None},
      {"stage":"SEMANTIC_CUE_LINEAGE","status":"PASS" if lineage_ok else "READY","next":"Compile semantic lineage" if not lineage_ok else None},
      {"stage":"P003A2_INTERVAL_ANALYSIS","status":"PASS" if analysis_ok else ("READY" if master_ok else "BLOCKED")},
      {"stage":"INTERVAL_CLASSIFICATION","status":"PASS" if class_ok else ("READY" if analysis_ok and lineage_ok else "BLOCKED")},
      {"stage":"P004A_SELECTIVE_REPAIR_PLAN","status":"PASS" if plan_ok else ("READY" if class_ok else "BLOCKED")},
      {"stage":"PATCH_RENDER","status":"PASS" if patched_ok else ("READY_EXTERNAL_MIX_ACTION" if plan_ok else "BLOCKED")},
      {"stage":"REGRESSION_GATE","status":"PASS" if reg_ok else ("READY" if patched_ok else "BLOCKED")},
      {"stage":"P003B_HUMAN_LISTEN","status":"REQUIRED_NOT_SIMULATED"},
      {"stage":"COMMERCIAL_ABC","status":"BLOCKED_UNTIL_TECHNICAL_REPAIR_AND_HUMAN_GATE"}]
    out={"schema_version":"room917.post_render_router/1.0","project":"ROOM917","episode":"E01","state_status":state.get("status"),"stages":stages}; Path(args.out).write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8"); print("ROUTED")
if __name__=="__main__": main()
