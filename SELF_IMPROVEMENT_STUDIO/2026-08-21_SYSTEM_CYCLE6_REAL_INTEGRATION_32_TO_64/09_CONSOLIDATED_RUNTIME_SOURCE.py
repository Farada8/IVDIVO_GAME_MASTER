# Cycle 6 consolidated source for review
# Full reproducible package is mirrored in Drive; this is the GitHub review surface.

# ===== audio_replication.py =====
def compare(a,b):
    if a.get("mechanism_contract_hash")!=b.get("mechanism_contract_hash"):return {"status":"HOLD_NOT_SAME_MECHANISM"}
    if a.get("project_id")==b.get("project_id"):return {"status":"HOLD_NOT_INDEPENDENT"}
    if a.get("human_result")!="PASS" or b.get("human_result")!="PASS":return {"status":"HOLD_HUMAN_EVIDENCE"}
    if a.get("result")!="PASS" or b.get("result")!="PASS":return {"status":"HOLD_REPLICATION_RESULT"}
    return {"status":"SECOND_AUDIO_PROJECT_PASS","domain_promotion":"ELIGIBLE_FOR_REVIEW"}

# ===== book_replication_ingest.py =====
def book_replication(e):
    if e["positive_fixture"]["observed_hits"]!=e["positive_fixture"]["expected_hits"]:return {"status":"FAIL_POSITIVE_CONTROL"}
    if e["repaired_no_change_fixture"]["observed_hits"]!=e["repaired_no_change_fixture"]["expected_hits"]:return {"status":"FAIL_REPAIRED_CONTROL"}
    if e["false_positive_control"]["observed_hits"]!=0:return {"status":"FAIL_FALSE_POSITIVE"}
    if e.get("locked_story_mutated"):return {"status":"FAIL_LOCK_MUTATION"}
    return {"status":"SECOND_BOOK_REPLICATION_PASS","scope":"BOOK_DOMAIN_REVIEW_ONLY","universal":False}

# ===== book_scope_reconciler.py =====
def book_scope(replication_status,overlap):
    if overlap=="EXACT":return {"status":"MERGE_WITH_EXISTING","new_candidate":False}
    if replication_status=="SECOND_BOOK_REPLICATION_PASS":return {"status":"ACCEPT_WITH_SCOPE_REVIEW","scope":"BOOK_DOMAIN","new_candidate":False}
    return {"status":"HOLD_FOR_MORE_EVIDENCE","new_candidate":False}

# ===== durable_txn_interface.py =====
VALID={"PREPARED","APPLIED","COMMITTED_VERIFIED","REPAIR_REQUIRED","QUARANTINED"}
def reconcile(txn_id,stores):
    rows=[x for x in stores if x.get("txn_id")==txn_id]
    if not rows:return {"status":"HOLD_NO_TXN"}
    if any(x.get("state") not in VALID for x in rows):return {"status":"FAIL_UNKNOWN_STATE"}
    if any(x.get("paid_or_irreversible") and x.get("state")!="COMMITTED_VERIFIED" for x in rows):return {"status":"QUARANTINED","replay_allowed":False}
    if all(x.get("state")=="COMMITTED_VERIFIED" for x in rows):return {"status":"COMPLETE","replay_allowed":False}
    return {"status":"REPAIR_REQUIRED","repair":[x["store"] for x in rows if x.get("state")!="COMMITTED_VERIFIED"],"replay_allowed":True}

# ===== economics_evidence.py =====
def economics(r):
    need=["provider_spend","human_minutes","generated_minutes","accepted_minutes","human_hourly_cost"]
    m=[k for k in need if r.get(k) is None]
    if m:return {"status":"HOLD_MISSING_MEASURED_DATA","missing":m}
    if r["accepted_minutes"]<=0:return {"status":"FAIL_ACCEPTED_MINUTES"}
    total=r["provider_spend"]+r["human_minutes"]/60*r["human_hourly_cost"]
    return {"status":"PASS_MEASURED","total_cost":round(total,4),"cost_per_accepted_minute":round(total/r["accepted_minutes"],4),"regeneration_waste_minutes":max(0,r["generated_minutes"]-r["accepted_minutes"])}

# ===== evidence_graph.py =====
def evidence_families(events):
    d={}
    for e in events:d.setdefault(e.get("root_evidence") or e.get("source_hash") or e["id"],[]).append(e["id"])
    return d

def independent_count(events):return len(evidence_families(events))

def claim_ceiling(events):
    c={e.get("evidence_class") for e in events}
    if "HUMAN_SIGNAL" in c:return "HUMAN_SUPPORTED"
    if "LIVE_PROVIDER" in c:return "PROVIDER_SUPPORTED"
    if "PERSISTED_READBACK" in c:return "PERSISTENCE_SUPPORTED"
    return "ENGINEERING_ONLY"

# ===== frontier_replay.py =====
def frontier_choose(frontiers):
    valid=[f for f in frontiers if f.get("persisted")]
    if not valid:return {"status":"HOLD_NO_PERSISTED_FRONTIER"}
    winner=max(valid,key=lambda f:(f.get("observed_at",""),f.get("episode",0)))
    return {"status":"PASS","winner":winner,"superseded":[f for f in valid if f!=winner]}

def stale_work(current,proposed):return {"status":"FAIL_STALE_WORK" if proposed<current else "PASS"}

# ===== human_gate.py =====
def human_gate(packet_ready,raw_responses,participant_count,coached=False):
    if not packet_ready:return {"status":"HOLD_PACKET_NOT_READY"}
    if not raw_responses or participant_count<=0:return {"status":"HOLD_HUMAN_SIGNAL_NOT_RUN"}
    if coached:return {"status":"FAIL_COACHED_SAMPLE"}
    return {"status":"HUMAN_SIGNAL_CAPTURED_NOT_YET_SYNTHESIZED","participants":participant_count}

def evidence_source_class(source):return "HUMAN_SIGNAL" if source=="REAL_PARTICIPANT" else ("FOUNDER_SIGNAL" if source=="FOUNDER" else "MODEL_REVIEW")

# ===== interruption_observer.py =====
def interruption_record(before,after):
    req=("main_sha","state_revision","material_boundary")
    if any(k not in before or k not in after for k in req):return {"status":"HOLD_INCOMPLETE_OBSERVATION"}
    lost=max(0,before.get("durable_units",0)-after.get("durable_units",0));dup=after.get("duplicate_units",0)
    return {"status":"PASS_OBSERVATION","lost_units":lost,"duplicate_units":dup,"claim_scope":"INCIDENT_ONLY","improvement_candidate":bool(lost or dup)}

# ===== live_governor.py =====
def live_governor(opts):
    a=[o for o in opts if o.get("authorized",True) and not o.get("blocked",False)]
    if not a:return {"status":"HOLD_NO_ADMISSIBLE"}
    best=max(a,key=lambda o:(o.get("priority",0),o.get("information_value",0),-o.get("effort",0)))
    real=[o for o in a if o.get("kind") in {"BOOK","AUDIO","HUMAN_EVIDENCE","PROVIDER_EVIDENCE","MEASURED_ECONOMICS"}]
    if best.get("kind")=="META" and real:
        rb=max(real,key=lambda o:(o.get("priority",0),o.get("information_value",0),-o.get("effort",0)))
        if rb.get("priority",0)>=best.get("priority",0) and rb.get("information_value",0)>best.get("information_value",0):return {"status":"ROUTE_REAL_EVIDENCE","selected":rb["id"],"meta_deferred":best["id"]}
    return {"status":"PASS","selected":best["id"]}

# ===== package_promotion.py =====
def package_decide(package_sha,cold_pass,manifest_match,post_package_main_extensions):
    if not package_sha or not cold_pass or not manifest_match:return {"status":"HOLD_PACKAGE_PROOF"}
    if post_package_main_extensions:return {"status":"NEW_PACKAGE_REQUIRED","relabel_old":False}
    return {"status":"PACKAGE_IDENTITY_VERIFIED","relabel_old":False}

# ===== promotion_bundle.py =====
PROMOTION_REQ={"application_target","regression","readback","rollback","evidence_boundary","source_identity"}
def promotion_check(x):
    m=sorted(PROMOTION_REQ-set(x))
    if m:return {"status":"HOLD_MISSING_PROOF","missing":m}
    if x["regression"]!="PASS" or x["readback"]!="PASS":return {"status":"HOLD_FAILED_GATE"}
    if x.get("external_required") and not x.get("external_evidence"):return {"status":"HOLD_EXTERNAL"}
    return {"status":"READY_FOR_HUMAN_AUTHORITY_REVIEW","auto_promote":False}

# ===== proof_ledger_compaction.py =====
def proof_compact(rs):
    d={}
    for r in rs:
        k=(r["claim_id"],r["source_ref"],r["evidence_class"])
        if k not in d or r.get("revision",0)>d[k].get("revision",0):d[k]=r
    return list(d.values())

def proof_validate(rs):
    for r in rs:
        if r.get("claim_class")=="HUMAN_SIGNAL" and r.get("evidence_class")!="HUMAN_SIGNAL":return {"status":"FAIL_EVIDENCE_SUBSTITUTION"}
    return {"status":"PASS","count":len(rs)}

# ===== registry_reservation_scan.py =====
import re
def registry_scan(main_ids,reserved):
    m=set(main_ids);r=set(reserved);allx=m|r
    nums=[int(x.split("-")[1]) for x in allx if re.fullmatch(r"SI-\d{4}",x)]
    return {"status":"HOLD_COLLISION" if m&r else "PASS","collisions":sorted(m&r),"next_unreserved":f"SI-{max(nums or [0])+1:04d}","main_ids":sorted(m),"reserved_ids":sorted(r)}

def registry_allocate(snapshot,complete):
    if not complete:return {"status":"HOLD_PARTIAL_VISIBILITY","candidate_id":None}
    if snapshot["status"]!="PASS":return {"status":"HOLD_COLLISION","candidate_id":None}
    return {"status":"ELIGIBLE_ID_ONLY_NOT_PROMOTED","candidate_id":snapshot["next_unreserved"]}

# ===== restart_classifier.py =====
def restart_classify(cp,main_sha,state_rev,blocker=None):
    if blocker:return {"status":"STOP","reason":"BLOCKER_PRESENT"}
    if cp.get("hash_valid") is not True:return {"status":"STOP","reason":"CHECKPOINT_TAMPER"}
    if cp.get("main_sha")!=main_sha or cp.get("state_revision")!=state_rev:return {"status":"REBASE_FIRST","reason":"AUTHORITY_OR_STATE_DRIFT"}
    if cp.get("volatile_artifacts"):return {"status":"RECOVER_VOLATILE_FIRST"}
    return {"status":"RESUME_EXACT"}

# ===== telemetry_accumulator.py =====
TELEMETRY_REQ={"event_id","project_id","kind","evidence_class","decision"}
def telemetry_validate(e):
    m=sorted(TELEMETRY_REQ-set(e))
    if m:return {"status":"FAIL_MISSING_FIELDS","missing":m}
    for k in ("provider_spend","human_minutes","generated_minutes","accepted_minutes"):
        if e.get(k)==0 and e.get(k+"_measured") is False:return {"status":"FAIL_FALSE_ZERO","field":k}
    return {"status":"PASS"}

def telemetry_aggregate(events):
    g=[e for e in events if telemetry_validate(e)["status"]=="PASS"]
    return {"events":len(g),"measured_provider_spend":sum(e["provider_spend"] for e in g if isinstance(e.get("provider_spend"),(int,float)) and e.get("provider_spend_measured") is True),"human_minutes_known":sum(e["human_minutes"] for e in g if isinstance(e.get("human_minutes"),(int,float)) and e.get("human_minutes_measured") is True)}
