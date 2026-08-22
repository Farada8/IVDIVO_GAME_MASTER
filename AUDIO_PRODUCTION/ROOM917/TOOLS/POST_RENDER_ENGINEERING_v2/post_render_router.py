#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from authority_hygiene_guard import PASS, evaluate_authority


def exists(path): return bool(path and Path(path).exists())
def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))

def resolve_authority(explicit,lineage,rules_path):
    if exists(explicit): return load(explicit)
    if exists(lineage): return evaluate_authority(load(lineage).get("source_authority",{}),load(rules_path))
    return {"status":"HOLD_UNVERIFIED_AUTHORITY","reasons":["no_lineage_or_explicit_authority_preflight"]}

def stage(stage,status,**kw):
    row={"stage":stage,"status":status}; row.update(kw); return row

def pick_frontier(ctx):
    # Never bypass a blocked gate. Instead choose the nearest independent safe frontier.
    if ctx["mainline_ready"]: return {"frontier":"MAINLINE_NEXT_READY_STAGE","mode":"EXECUTE_NOW","reason":"All prerequisites for the next mainline stage are present."}
    if not ctx["authority_ok"]: return {"frontier":"AUTHORITY_HYGIENE_AND_CONTAMINATION_TESTS","mode":"EXECUTE_NOW","reason":"No downstream work may proceed without exact current authority."}
    if not ctx["asset_contract_exists"]: return {"frontier":"ASSET_CONTRACT_COMPLETION","mode":"EXECUTE_NOW","reason":"Current-branch sound assets need a machine-readable contract independent of master timing."}
    if not ctx["asset_canary_receipt_exists"]: return {"frontier":"ASSET_GENERATION_AND_MACHINE_PREFLIGHT","mode":"EXECUTE_NOW","reason":"Generate isolated canaries without touching locked story or unavailable master."}
    if not ctx["asset_audition_contract_exists"]: return {"frontier":"ASSET_BLIND_AUDITION_PACKAGING","mode":"EXECUTE_NOW","reason":"Existing canaries can be packaged for blind evaluation without production binding."}
    if not ctx["release_qc_profile_exists"]: return {"frontier":"QC_TOOLING_AND_NEGATIVE_TESTS","mode":"EXECUTE_NOW","reason":"Release/translation QC can be hardened independently of master recovery."}
    if not ctx["provenance_contract_exists"]: return {"frontier":"PROVENANCE_AND_ESCROW_HARDENING","mode":"EXECUTE_NOW","reason":"Derived-master evidence chain can be implemented without changing audio."}
    if not ctx["master_ok"] or not ctx["timing_ok"]:
        if ctx["secondary_safe_work_remaining"]:
            return {"frontier":"DOCUMENTED_SECONDARY_RISK_REDUCTION","mode":"EXECUTE_NOW","reason":"Mainline bytes/timing blocked; continue on remaining isolated sound assets, Foley, QC, or recovery-hardening work."}
        return {"frontier":"RECOVERY_SEARCH_FOR_MISSING_BYTES_OR_TIMING","mode":"EXECUTE_NOW","reason":"No closer independent engineering work remains; retry evidence recovery without inventing substitutes."}
    return {"frontier":"SELF_IMPROVEMENT_SIGNAL","mode":"EXECUTE_NOW","reason":"No mainline bypass is legal; capture tooling gap and search for another safe frontier."}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--state",required=True); ap.add_argument("--master-path"); ap.add_argument("--lineage-compiled"); ap.add_argument("--timing-map"); ap.add_argument("--authority-hygiene"); ap.add_argument("--authority-rules"); ap.add_argument("--interval-analysis"); ap.add_argument("--classified"); ap.add_argument("--patch-plan"); ap.add_argument("--patched-master"); ap.add_argument("--regression"); ap.add_argument("--asset-contract"); ap.add_argument("--asset-canary-receipt"); ap.add_argument("--asset-audition-contract"); ap.add_argument("--release-qc-profile"); ap.add_argument("--provenance-contract"); ap.add_argument("--secondary-safe-work-remaining",choices=["true","false"],default="true"); ap.add_argument("--continuation-policy"); ap.add_argument("--out",required=True)
    a=ap.parse_args(); state=load(a.state); here=Path(__file__).resolve().parent
    rules=Path(a.authority_rules) if a.authority_rules else here/"AUTHORITY_HYGIENE_RULES_v1.json"
    policy=Path(a.continuation_policy) if a.continuation_policy else here/"CONTINUATION_POLICY_v1.json"
    continuation=load(policy) if policy.exists() else {"law":"DO_NOT_STOP_AT_A_BLOCKED_GATE_IF_ANY_INDEPENDENT_SAFE_FRONTIER_REMAINS_EXECUTABLE","mode":"FAIL_CLOSED_NON_STOP"}
    authority=resolve_authority(a.authority_hygiene,a.lineage_compiled,rules); authority_ok=authority.get("status")==PASS
    master_ok=exists(a.master_path); lineage_exists=exists(a.lineage_compiled); lineage_ok=lineage_exists and authority_ok; timing_ok=exists(a.timing_map); analysis_ok=exists(a.interval_analysis); class_ok=exists(a.classified); plan_ok=exists(a.patch_plan); patched_ok=exists(a.patched_master); reg_ok=False
    if exists(a.regression):
        try: reg_ok=load(a.regression).get("status")=="PASS"
        except Exception: reg_ok=False
    missing=[]
    if not authority_ok: missing.append("AUTHORITY_HYGIENE")
    if not lineage_ok: missing.append("SEMANTIC_CUE_LINEAGE")
    if not timing_ok: missing.append("LIVE_ACCEPTED_TIMING")
    if not analysis_ok: missing.append("P003A2_INTERVAL_ANALYSIS")
    stages=[
      stage("AUTHORITY_HYGIENE","PASS" if authority_ok else authority.get("status","HOLD_UNVERIFIED_AUTHORITY"),details=authority),
      stage("MASTER_BYTE_ESCROW","PASS_LOCAL_BYTES_PRESENT" if master_ok else "BLOCKED",next=None if master_ok else "Provide exact immutable full-master bytes"),
      stage("SEMANTIC_CUE_LINEAGE","PASS" if lineage_ok else ("HOLD_AUTHORITY_PREFLIGHT" if lineage_exists else "READY")),
      stage("LIVE_ACCEPTED_TIMING","PASS" if timing_ok else "BLOCKED"),
      stage("P003A2_INTERVAL_ANALYSIS","PASS" if analysis_ok else ("READY" if master_ok else "BLOCKED_MASTER_BYTES")),
      stage("INTERVAL_CLASSIFICATION","PASS" if class_ok else ("READY" if authority_ok and lineage_ok and timing_ok and analysis_ok else "BLOCKED"),missing_prerequisites=[] if class_ok else missing),
      stage("P004A_SELECTIVE_REPAIR_PLAN","PASS" if plan_ok else ("READY" if class_ok else "BLOCKED")),
      stage("PATCH_RENDER","PASS" if patched_ok else ("READY_EXTERNAL_MIX_ACTION" if plan_ok else "BLOCKED")),
      stage("REGRESSION_GATE","PASS" if reg_ok else ("READY" if patched_ok else "BLOCKED")),
      stage("P003B_HUMAN_LISTEN","REQUIRED_NOT_SIMULATED"),
      stage("COMMERCIAL_ABC","BLOCKED_UNTIL_TECHNICAL_REPAIR_AND_HUMAN_GATE")]
    ctx={
      "authority_ok":authority_ok,"master_ok":master_ok,"timing_ok":timing_ok,
      "mainline_ready":authority_ok and lineage_ok and timing_ok and analysis_ok and not class_ok,
      "asset_contract_exists":exists(a.asset_contract),"asset_canary_receipt_exists":exists(a.asset_canary_receipt),"asset_audition_contract_exists":exists(a.asset_audition_contract),"release_qc_profile_exists":exists(a.release_qc_profile),"provenance_contract_exists":exists(a.provenance_contract),"secondary_safe_work_remaining":a.secondary_safe_work_remaining=="true"}
    frontier=pick_frontier(ctx)
    out={"schema_version":"room917.post_render_router/1.2","project":"ROOM917","episode":"E01","state_status":state.get("status"),"authority_hygiene":authority,"continuation_policy":continuation,"stages":stages,"non_stop_decision":{"blocked_is_not_stop":True,"selected":frontier,"hard_stop":False,"law":"Do not bypass evidence gates; continue on the nearest independent safe frontier."}}
    Path(a.out).write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("ROUTED authority="+authority.get("status","UNKNOWN")+" next="+frontier["frontier"])

if __name__=="__main__": main()
