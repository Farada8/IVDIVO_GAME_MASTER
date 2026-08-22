#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from datetime import date


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",required=True); args=ap.parse_args()
    signal={
      "signal_id":"SYS-20260822-ROOM917-AUDIO-CONTINUATION-002",
      "date":date.today().isoformat(),
      "project":"ROOM917",
      "domain":"AUDIO_PRODUCTION_ENGINEERING",
      "problem":"A blocked mainline gate can cause an agent/operator to stop even while independent safe engineering frontiers remain executable.",
      "evidence":[
        "Exact E01 full-master bytes and trusted timing remain unavailable, blocking P003A2/P004A mainline.",
        "Independent work remained possible and was completed: authority hygiene, asset contracts, deterministic A01/A02 canaries, 24 critical-SFX canaries, provenance hardening, release/translation QC, blind-listener packaging.",
        "Stopping at the byte/timing blocker would therefore have left real safe progress undone."
      ],
      "earliest_failure_layer":"ROUTER_CONTINUATION_POLICY",
      "existing_rule_check":{"covered":True,"authority":"CONTINUATION_POLICY_v1.json","finding":"Rule is now explicit: BLOCKED_IS_NOT_STOP. Router must select another safe frontier without bypassing the blocked evidence gate."},
      "candidate_improvement":{"title":"Fail-closed non-stop frontier router","mechanism":"When the nearest mainline stage is BLOCKED, enumerate independent safe frontiers, select the nearest executable one by priority, write through progress, and return to mainline automatically when prerequisites appear.","candidate_type":"ROUTER_AND_SELF_IMPROVEMENT_POLICY","scope":"PROJECT_NOW_DOMAIN_CANDIDATE_AFTER_REPLICATION"},
      "protected_invariants":["LOCKED_STORY","NO_FAKE_HUMAN_PASS","NO_INVENTED_TIMING","NO_FAKE_BYTES","NO_BLANKET_SILENCE_FILL","SCENE3_V1_3E_LINEAGE","NO_SCALE_UNTIL_E01_V2_PROVEN"],
      "continuation_law":"DO_NOT_STOP_AT_A_BLOCKED_GATE_IF_ANY_INDEPENDENT_SAFE_FRONTIER_REMAINS_EXECUTABLE",
      "hard_stop_conditions":["NO_SAFE_EXECUTABLE_FRONTIER_REMAINS","USER_EXPLICITLY_STOPS_WORK","REQUIRED_ACTION_WOULD_VIOLATE_AUTHORITY_OR_SAFETY","ALL_REMAINING_FRONTIERS_REQUIRE_UNAVAILABLE_HUMAN_OR_EXTERNAL_INPUT"],
      "test":{"A":"Router reports blockers only","B":"Router reports blockers plus selected independent executable frontier","acceptance":["blocked mainline is preserved as blocked","no prerequisite is fabricated","selected frontier is independent and safe","hard_stop remains false while executable work exists"]},
      "result":"PROJECT_RULE_INTEGRATED_ROUTER_V1_2",
      "decision":"ACCEPT_PROJECT_RULE_AND_CONTINUE_WORK",
      "write_through":["CONTINUATION_POLICY_v1.json","post_render_router.py","ROOM917 current sound pointer","learning ledger candidate"]
    }
    Path(args.out).write_text(json.dumps(signal,indent=2,ensure_ascii=False)+"\n",encoding="utf-8"); print("SELF_IMPROVEMENT_SIGNAL_READY_NON_STOP")

if __name__=="__main__": main()
