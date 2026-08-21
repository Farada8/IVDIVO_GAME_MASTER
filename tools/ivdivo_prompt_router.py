#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

DEFAULT_CONFIG = Path(__file__).resolve().parents[1] / "PROMPT_ROUTER_CONFIG_v1.json"
RANK = {"P0":0,"P1":1,"P2":2,"P3":3,"P4":4,"P5":5,"P6":6}
TITLES = {
1:"PORTFOLIO FRONTIER REBASE + TRUE NEXT BOOK OBLIGATION",
2:"CURRENT BOOK AUTHORITY + SOURCE TRUTH RESTORATION",
3:"STORY ENGINE / PREMISE COMPETITION REDISCOVERY GATE",
4:"STORY CORE + CHARACTER PRESSURE SYSTEM",
5:"CAUSAL ARCHITECTURE + CHAPTER/EPISODE MAP",
6:"SCENE / DIALOGUE / VOICE EXECUTION SYSTEM",
7:"DEVELOPMENT + RED TEAM + TARGETED REPAIR",
8:"FINAL STORY GATE + FOUNDER LOCK PACKET + LEARNING EXTRACTION",
9:"AUDIO INGEST + SOURCE HASH + TEXT-PROTECTION CONTRACT",
10:"LISTENER CONTRACT + DRAMATIC FORCE MAP",
11:"CASTING / VOICE AUDITION / BINDING CASCADE",
12:"PERFORMANCE DIRECTOR SCORE + MICROPHONE CHOREOGRAPHY",
13:"FOLEY / SFX / AMBIENCE / MUSIC DRAMATURGY",
14:"PROVIDER PREFLIGHT + RENDER BLOCKS + CANARY",
15:"ALIGNMENT / TIMELINE / MIX / MASTER / QC",
16:"HUMAN LISTEN + RELEASE + AUDIO LEARNING RETURN",
17:"PRODUCTION BOTTLENECK MINER",
18:"GENERAL PROBLEM-SOLVING KERNEL",
19:"ENGINE-WORTHINESS GATE",
20:"ENGINE ARCHITECTURE / STATE / DAG DESIGN",
21:"ENGINE / CODE IMPLEMENTATION + ADVERSARIAL TEST SUITE",
22:"PROMPT SYSTEM OPTIMIZER / ANTI-BLOAT PASS",
23:"MULTI-AI ORCHESTRATION / SOURCE-PARITY CELL",
24:"PRODUCTIVITY / COST / SAFE AUTOMATION OPTIMIZER",
25:"IMPROVEMENT REGISTRY SWEEP + BEST-CANDIDATE ROUTER",
26:"REFERENCE LIBRARY MECHANISM MINING",
27:"FRESH RESEARCH RADAR: MODELS / TOOLS / AUDIO / PUBLISHING / MARKET",
28:"EXPERIMENT / CANARY DESIGNER",
29:"EVALUATION MATRIX / EVIDENCE CLASSIFIER",
30:"PORTABILITY / UNIVERSALIZATION / WRITE-THROUGH GATE",
31:"KNOWLEDGE COMPACTION / PRUNING / SUPERSESSION PASS",
32:"META-AUDIT + NEXT CONTINUOUS CYCLE"
}

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def match(state, cond):
    return all(state.get(k) == expected for k, expected in cond.items())

def route(state, cfg):
    valid_domains={"BOOK","AUDIO","FACTORY","ENGINE","RESEARCH","SELF_IMPROVEMENT"}
    if state.get("domain") not in valid_domains:
        return {"status":"FAIL","code":"INVALID_DOMAIN","domain":state.get("domain")}
    if "authority_clean" not in state:
        return {"status":"FAIL","code":"MISSING_AUTHORITY_CLEAN"}

    candidates=[]; stops=[]
    for idx,rule in enumerate(cfg["routing_rules"]):
        if match(state,rule["when"]):
            item=dict(rule); item["_order"]=idx
            if "stop" in rule: stops.append(item)
            else: candidates.append(item)

    if stops:
        s=stops[0]
        return {"status":"STOP","stop_condition":s["stop"],"rule_id":s["id"],
                "selected_prompt":None,
                "reason":"Real authority/Founder gate outranks executable prompt routing."}

    pc=state.get("portfolio_context") or {}
    production_open=bool(pc.get("unblocked_p1_or_p2"))
    direct_prereq=bool(state.get("direct_prerequisite"))
    if production_open and not direct_prereq:
        candidates=[r for r in candidates if RANK.get(r.get("priority","P6"),99)<=RANK["P2"]]

    if not candidates:
        return {"status":"STOP","stop_condition":"NO_MATCHING_UNBLOCKED_PROMPT",
                "selected_prompt":None,
                "reason":"State does not justify a prompt; rebase or supply next obligation."}

    candidates.sort(key=lambda r:(RANK.get(r.get("priority","P6"),99),r["_order"]))
    primary=candidates[0]

    parallel=[]
    for p in state.get("independent_parallel_branches",[]):
        if not isinstance(p,dict):
            continue
        sub=route({**p,"independent_parallel_branches":[]},cfg)
        if sub.get("status")=="ROUTE" and sub.get("selected_prompt")!=primary.get("prompt"):
            parallel.append(sub["selected_prompt"])

    num=primary["prompt"]
    return {
        "status":"ROUTE",
        "rule_id":primary["id"],
        "priority":primary["priority"],
        "selected_prompt":num,
        "selected_title":TITLES.get(num),
        "parallel_prompts":parallel,
        "guard":"P1/P2 production outranks unrelated meta-work unless blocked or meta-work is a direct prerequisite.",
        "next_after_pass":"RELOAD_CURRENT_STATE_AND_ROUTE_AGAIN"
    }

def main():
    ap=argparse.ArgumentParser(description="IVDIVO 32 RUN CARD Prompt Router")
    ap.add_argument("state")
    ap.add_argument("--config",default=str(DEFAULT_CONFIG))
    args=ap.parse_args()
    try:
        out=route(load(args.state),load(args.config))
    except Exception as e:
        print(json.dumps({"status":"FAIL","code":"ROUTER_EXCEPTION","error":str(e)},ensure_ascii=False))
        return 2
    print(json.dumps(out,ensure_ascii=False,indent=2))
    return 0 if out["status"] in {"ROUTE","STOP"} else 1

if __name__=="__main__":
    raise SystemExit(main())
