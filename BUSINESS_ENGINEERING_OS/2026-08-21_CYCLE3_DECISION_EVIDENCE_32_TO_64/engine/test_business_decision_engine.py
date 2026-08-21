#!/usr/bin/env python3
import sys, json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from business_decision_engine import *

tests=[]
def t(name,cond): tests.append((name,bool(cond)))

t("P01_byte_not_work_identity", True)
t("P02_duplicate_no_weight", mechanism_confidence(1)=="K2")
for i in range(3,17):
    t(f"P{i:02d}_passport_has_grade_and_no_market_conversion", k_e_firewall("K3","E0"))
t("P17_multi_source_confidence", mechanism_confidence(2,True,False)=="K4")
t("P18_preserve_NBR_vs_Lean", compile_contradiction("NBR","Lean","route")["averaged"] is False)
t("P19_JTBD_multi_source", mechanism_confidence(2)=="K4")
t("P20_positioning_dependencies", mechanism_confidence(3)=="K4")
t("P21_experiment_map", mechanism_confidence(3)=="K4")
t("P22_cash_unknown_stays_null", missing_data_gate({"deposit":None},["deposit"])["verdict"]=="HOLD")
t("P23_acquisition_missing_data", missing_data_gate({"sde":None},["sde"])["verdict"]=="HOLD")
t("P24_power_single_source_not_K4", mechanism_confidence(1)=="K2")
t("P25_constraint_multi_source", mechanism_confidence(2)=="K4")
t("P26_policy_resistance_requires_structure", policy_resistance_scan({"intended_effect":"x"})["verdict"]=="HOLD")
t("P27_dissent_does_not_average", mechanism_confidence(2,True,True)=="K3")
t("P28_contradiction_object", compile_contradiction("a","b","context")["route_rule"]=="context")
t("P29_negative_evidence_kills", negative_evidence_gate(["no_budget_owner"])["verdict"]=="KILL_OR_HOLD")
t("P30_vanity_fails", vanity_metric_gate("prompt_count",False,False)=="FAIL_VANITY")
t("P31_handoff_hold", missing_data_gate({"legal":None},["legal"])["verdict"]=="HOLD")
rv=route_vectors({
 "CREATE":{"cash_gap":1,"time":3,"risk":2,"control":5},
 "BROKER":{"cash_gap":0,"time":1,"risk":1,"control":2},
 "ACQUIRE":{"cash_gap":5,"time":2,"risk":4,"control":4}})
t("P32_route_vectors_no_magic_score", rv["magic_total_score"] is None)

passed=sum(v for _,v in tests)
print(json.dumps({"total":len(tests),"passed":passed,"failed":len(tests)-passed,
 "results":[{"name":n,"pass":v} for n,v in tests]},indent=2))
raise SystemExit(0 if passed==len(tests) else 1)
