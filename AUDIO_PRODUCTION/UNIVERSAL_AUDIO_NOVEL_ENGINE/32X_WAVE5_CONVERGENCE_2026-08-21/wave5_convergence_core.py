from __future__ import annotations
from typing import Any
from hashlib import sha256
import json

AUTHORITY_RANK={"FOUNDER_DIRECTIVE":100,"CURRENT_MAIN_AUTHORITY":90,"MERGED_VERIFIED_CURRENT":80,"MERGED_CANDIDATE":70,"MAIN_BASED_DRAFT_PR":60,"STACKED_DRAFT_PR":50,"DRIVE_MIRROR":40,"CHAT_ONLY":10}
PORTABLE_CLASSES={"MECHANISM","SCHEMA","NEGATIVE_FIXTURE","QC_GATE","EVIDENCE_GATE"}
PROJECT_ONLY_CLASSES={"VOICE_ID","STORY_FACT","CHARACTER","PROJECT_ASSET","PROJECT_TIMELINE","PROJECT_ACOUSTIC_VALUE"}

def canonical_hash(obj:Any)->str:return sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def authority_rank(kind:str)->int:return AUTHORITY_RANK.get(kind,0)
def choose_authority(candidates):
    if not candidates: raise ValueError("NO_AUTHORITY_CANDIDATES")
    return max(candidates,key=lambda x:(authority_rank(x.get("kind","")),x.get("freshness",0)))
def freshness_graph(items):
    risks=[]
    for x in items:
        if x.get("state")=="OPEN" and x.get("base")!="main":risks.append((x["id"],"STACKED_OPEN"))
        if x.get("behind_main",0)>0:risks.append((x["id"],"STALE_BASE"))
        if x.get("mergeable") is False and x.get("state")=="OPEN":risks.append((x["id"],"MERGE_FRESHNESS_RECHECK"))
    return {"risks":risks,"requires_final_freshness_read":bool(risks)}
def dedupe_mechanisms(records):
    groups={}
    for r in records:
        key=r["mechanism"].strip().lower().replace("-","_").replace(" ","_");groups.setdefault(key,[]).append(r)
    out={}
    for k,rs in groups.items():
        canonical=max(rs,key=lambda r:(authority_rank(r.get("kind","")),r.get("freshness",0),r.get("evidence",0)))
        out[k]={"canonical":canonical,"duplicates":[r for r in rs if r is not canonical]}
    return out
def classify_delta(item):
    if item.get("superseded"):return "SUPERSEDED"
    if item.get("duplicate"):return "DUPLICATE"
    if item.get("class") in PORTABLE_CLASSES:return "PORTABLE_MECHANISM"
    if item.get("class") in PROJECT_ONLY_CLASSES:return "PROJECT_SPECIFIC_DO_NOT_TRANSFER"
    return "REVIEW_REQUIRED"
def convergence_manifest(items):return {"items":[{**i,"disposition":classify_delta(i)} for i in items],"new_runtime_allowed":False,"integration_target":"audio/studio/runtime","promotion_requires_fresh_file_read":True}
def source_fingerprint_gate(got,expected):
    required=("authority_revision","source_sha256","occurrence_ledger_sha256","request_sha256")
    missing=[k for k in required if not got.get(k)];mismatched=[k for k in required if expected.get(k) and got.get(k)!=expected.get(k)]
    return {"status":"PASS" if not missing and not mismatched else "FAIL_CLOSED","missing":missing,"mismatched":mismatched}
def no_branch_fallback(authority_ok,fingerprint_ok,fallback_requested):return "BLOCK_DISPATCH" if fallback_requested or not authority_ok or not fingerprint_ok else "ALLOW_PREFLIGHT_ONLY"
def master_asset_alias_gate(master_hash,replay_hash,rerender_requested):
    if rerender_requested:return {"status":"FAIL_RERENDER_FORBIDDEN"}
    if master_hash!=replay_hash:return {"status":"FAIL_REPLAY_DRIFT"}
    return {"status":"PASS_ALIAS_REUSE"}
def replay_drift(master,replay):return [k for k in ("audio_sha256","source_hash","voice_binding","model","post_chain") if master.get(k)!=replay.get(k)]
def one_listen_fact_gate(facts,masked,duplicated_conflicts=None):
    f=set(facts);m=set(masked);c=set(duplicated_conflicts or [])
    return {"status":"PASS" if f and not(f&m) and not(f&c) else "FAIL_INFORMATION_PRIORITY","masked":sorted(f&m),"conflicted":sorted(f&c)}
def project_leakage_gate(payload,forbidden_tokens):
    text=json.dumps(payload,ensure_ascii=False).lower();hits=sorted({t for t in forbidden_tokens if t.lower() in text})
    return {"status":"PASS" if not hits else "FAIL_PROJECT_LEAKAGE","hits":hits}
def clean_first_gate(provider_fx,downstream_fx):
    forbidden={"AMBIENCE","MUSIC","FINAL_REVERB","PHONE_EQ","BROADCAST_EQ","SCENE_MIX"};hits=sorted(forbidden & {x.upper() for x in provider_fx})
    return {"status":"PASS" if not hits else "FAIL_BAKED_PROCESSING","forbidden_baked":hits,"downstream_fx":downstream_fx}
def route_render_block(*,speakers,chars,clue_identity,device_domain=False,ttd_ceiling=1800):
    if chars<=0:raise ValueError("EMPTY_BLOCK")
    if clue_identity or device_domain or speakers<=1:return {"route":"ISOLATED_TTS","reason":"SELECTIVE_REGEN_OR_DOMAIN_ISOLATION"}
    if chars>ttd_ceiling:return {"route":"SPLIT_TTD","reason":"PROJECT_TTD_CEILING"}
    return {"route":"TTD_BLOCK","reason":"CONVERSATIONAL_COHERENCE"}
def canary_identity_gate(requests,units,chars):return {"status":"PASS" if (requests,units,chars)==(3,36,2163) else "FAIL_CANARY_DRIFT","expected":{"requests":3,"units":36,"chars":2163}}
def spend_decision(existing_state,response_started=False,reconcile_proven=False):
    if existing_state=="ACCEPTED":return "REUSE_ACCEPTED"
    if existing_state=="AMBIGUOUS" and not reconcile_proven:return "RECONCILE_REQUIRED"
    if response_started and existing_state in (None,"PLANNED","SENT"):return "QUARANTINE_AMBIGUOUS"
    if reconcile_proven and existing_state=="AMBIGUOUS":return "RESOLVE_THEN_DECIDE"
    return "MAY_SEND_ONCE"
def normalize_provider_error(status,code="",message=""):
    c=(code or "").upper();m=(message or "").upper()
    if status in (401,403) or "AUTH" in c:cat,retry="AUTH",False
    elif "VOICE" in c:cat,retry="VOICE",False
    elif "MODEL" in c:cat,retry="MODEL",False
    elif "ALIGN" in c:cat,retry="ALIGNMENT",False
    elif "FORMAT" in c:cat,retry="FORMAT",False
    elif "QUOTA" in c or "CREDIT" in m:cat,retry="QUOTA",False
    elif status==429 or "RATE" in c:cat,retry="RATE_LIMIT",True
    elif status in (408,504) or "TIMEOUT" in c:cat,retry="TIMEOUT",True
    elif status in (400,404,422) or "INVALID" in c:cat,retry="INVALID_REQUEST",False
    else:cat,retry="PROVIDER",status in (500,502,503)
    return {"category":cat,"retryable":retry}
def capability_snapshot_gate(expected,snapshot):
    mv=[x for x in expected.get("voice_ids",[]) if x not in snapshot.get("voice_ids",[])];mm=[x for x in expected.get("model_ids",[]) if x not in snapshot.get("model_ids",[])]
    return {"status":"PASS" if not mv and not mm else "FAIL_CAPABILITY_DRIFT","missing_voices":mv,"missing_models":mm,"auto_substitution":False}
def alignment_coverage_gate(unit_ids,alignment,synthetic=False):
    if synthetic:return {"status":"FAIL_SYNTHETIC_TIMING"}
    seen=[]
    for a in alignment:
        if not isinstance(a.get("start"),(int,float)) or not isinstance(a.get("end"),(int,float)) or a["end"]<a["start"]:return {"status":"FAIL_ALIGNMENT_INTERVAL"}
        seen.append(a.get("unit_id"))
    return {"status":"PASS" if sorted(seen)==sorted(unit_ids) and len(seen)==len(set(seen)) else "FAIL_ALIGNMENT_COVERAGE","missing":sorted(set(unit_ids)-set(seen)),"duplicates":sorted({u for u in seen if seen.count(u)>1})}
def acoustic_passport_gate(p):
    req={"domain_id","space_type","foreground_priority","ambience_policy","silence_policy","project_id"};missing=sorted(req-set(p));return {"status":"PASS" if not missing else "FAIL_PASSPORT","missing":missing}
def causal_foley_gate(e):
    req=("physical_cause","action","sound","listener_function");missing=[k for k in req if not e.get(k)];return {"status":"PASS" if not missing else "FAIL_DECORATIVE_OR_UNCAUSED","missing":missing}
def protected_silence_gate(window,events):
    forbidden={"MUSIC","FOLEY","AMBIENCE_FILL","REVERB_TAIL","SFX"};hits=[];a,b=window["start"],window["end"]
    for e in events:
        if e.get("kind") in forbidden and e.get("start",10**9)<b and e.get("end",-1)>a:hits.append(e.get("id","?"))
    return {"status":"PASS" if not hits else "FAIL_SILENCE_MASK","hits":hits}
def stem_topology_gate(source_channels,stem_channels,mono_intended=False):
    if source_channels==2 and stem_channels==1 and not mono_intended:return "FAIL_UNEXPECTED_STEREO_TO_MONO"
    if source_channels not in (1,2) or stem_channels not in (1,2):return "FAIL_UNSUPPORTED_CHANNELS"
    return "PASS"
def media_state_gate(world_id,bed_world_id,medium_changed,explicit_exposition_required):
    if world_id!=bed_world_id:return "FAIL_WORLD_IDENTITY"
    if not medium_changed:return "FAIL_MEDIA_STATE_NOT_DISTINCT"
    if explicit_exposition_required:return "FAIL_INFERENCE_NOT_AUDIBLE"
    return "PASS"
def music_function_gate(*,dialogue_space_pass,human_gain,overlaps_protected_silence,masks_fact,premature_answer):
    if not dialogue_space_pass:return "HOLD_GENERATE_LAST"
    if overlaps_protected_silence or masks_fact or premature_answer:return "FAIL_FUNCTION"
    if not human_gain:return "REJECT_NO_FUNCTIONAL_GAIN"
    return "PASS_OPTIONAL"
def information_priority_gate(facts):
    bad=[f["id"] for f in facts if f.get("masked") or f.get("ambiguous_due_to_mix")];return {"status":"PASS" if not bad else "FAIL_INFORMATION_LOSS","facts":bad}
CAUSE_ROUTE={"wrong_intention":"PERFORMANCE","wrong_status":"PERFORMANCE","unclear_position":"STAGING","body_action_gap":"FOLEY_STAGING","cue_time":"ALIGNMENT_TIMELINE","stereo_collapse":"STEM_RENDER_ROUTING","music_masks_fact":"MIX_MUSIC","global_loudness":"MASTERING","pronunciation":"VOICE_PRONUNCIATION","source_mismatch":"AUTHORITY_SOURCE","duplicate_charge":"PROVIDER_SPEND"}
def earliest_cause_route(defect):return CAUSE_ROUTE.get(defect,"DIAGNOSE_BEFORE_REPAIR")
DEPENDENCIES={"VOICE_PRONUNCIATION":["VOICE_BINDING","AFFECTED_SPEECH_BLOCKS"],"PERFORMANCE":["AFFECTED_TAKES"],"ALIGNMENT_TIMELINE":["TIMELINE","DEPENDENT_CUES","MIX"],"STEM_RENDER_ROUTING":["AFFECTED_STEM","MIX","MASTER"],"MIX_MUSIC":["MIX","MASTER"],"MASTERING":["MASTER"],"AUTHORITY_SOURCE":["ALL_DOWNSTREAM"]}
def selective_repair_plan(cause):return {"earliest_cause":cause,"invalidate":DEPENDENCIES.get(cause,["LOCAL_REVIEW"]),"full_chapter_rerender_default":False}
def abc_benchmark_gate(variants):
    if {v.get("mode") for v in variants}!={"NARRATED","MULTI_VOICE","DRAMATIZED"}:return {"status":"FAIL_VARIANT_SET"}
    if len({v.get("source_hash") for v in variants})!=1:return {"status":"FAIL_SOURCE_MISMATCH"}
    if {v.get("loudness_matched") for v in variants}!={True}:return {"status":"FAIL_LOUDNESS_MATCH"}
    if not all(v.get("human_score") is not None for v in variants):return {"status":"HOLD_HUMAN"}
    return {"status":"PASS"}
def performance_human_gate(e,pair_required=True):
    req=["multi_state","pronunciation","fatigue","human_blind"]+(["pair"] if pair_required else []);missing=[k for k in req if not e.get(k)]
    return {"status":"PASS" if not missing else "HOLD","missing":missing,"machine_auto_lock":False}
def economics_gate(m):
    req=("provider_cost_actual","accepted_minutes_actual","human_minutes_actual");missing=[k for k in req if m.get(k) is None]
    if missing:return {"status":"HOLD_MEASURED","missing":missing}
    if m["accepted_minutes_actual"]<=0:return {"status":"FAIL_ZERO_ACCEPTED"}
    return {"status":"PASS_MEASURED","provider_cost_per_accepted_minute":m["provider_cost_actual"]/m["accepted_minutes_actual"],"human_minutes_per_accepted_minute":m["human_minutes_actual"]/m["accepted_minutes_actual"],"projection_is_actual":False}
def anti_bloat_gate(items):
    actionable=[i for i in items if i.get("new_information") or i.get("unblocks_dependency") or i.get("real_evidence")]
    return {"status":"PASS" if actionable else "STOP_NO_INFORMATION_GAIN","actionable_ids":[i.get("id") for i in actionable],"defer_or_dedupe":[i.get("id") for i in items if i not in actionable]}
def release_matrix(gates):
    mandatory=["canonical_runtime","source_integrity","provider_live","alignment_live","human_performance","economics_measured","portability_live"];bad={k:gates.get(k,"MISSING") for k in mandatory if gates.get(k)!="PASS"}
    return {"status":"GO" if not bad else "HOLD","blocking":bad,"test_count_is_quality_proof":False}
