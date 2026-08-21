from __future__ import annotations
from typing import Any
from hashlib import sha256
import json

def compile_acoustic_passport(domain_id:str,poa:str,topology:list[str],movement:list[str],occlusion:list[str],stereo_policy:str,mono_policy:str,inherited_project_specific:list[str]|None=None)->dict[str,Any]:
    inherited=inherited_project_specific or []
    forbidden=[x for x in inherited if "ROOM917" in x.upper() or any(t in x.lower() for t in ["greyhaven","917","cate","lullaby"])]
    return {"domain_id":domain_id,"poa":poa,"topology":topology,"movement":movement,"occlusion":occlusion,"stereo_policy":stereo_policy,"mono_policy":mono_policy,"status":"FAIL_PROJECT_LEAK" if forbidden else "PASS_PLAN","forbidden_leaks":forbidden}

def ambience_variation_gate(duration_s:float,loop_period_s:float|None,repeated_signatures:int,protected_fill_seconds:float)->dict[str,Any]:
    failures=[]
    if loop_period_s and duration_s/max(loop_period_s,1e-9)>=3 and repeated_signatures>=2: failures.append("OBVIOUS_SHORT_LOOP")
    if protected_fill_seconds>0: failures.append("PROTECTED_SILENCE_DECORATIVELY_FILLED")
    return {"status":"PASS" if not failures else "FAIL","failures":failures}

def foley_causality_gate(events:list[dict[str,Any]])->dict[str,Any]:
    bad=[]
    for e in events:
        if not all(e.get(k) for k in ("physical_cause","action","sound","listener_function")): bad.append(e.get("cue_id","UNKNOWN"))
    return {"status":"PASS" if not bad else "FAIL","uncausal":bad}

def diegetic_recorder_contract(base_bed_id:str,capture_id:str,medium_change_markers:list[str])->dict[str,Any]:
    if base_bed_id==capture_id: return {"status":"FAIL","reason":"CAPTURE_NOT_DISTINCT_FROM_CONTINUOUS_BED"}
    if not medium_change_markers: return {"status":"HOLD","reason":"NO_MEDIA_IDENTITY_MARKERS"}
    return {"status":"PASS_PLAN","base_bed":base_bed_id,"capture":capture_id,"markers":medium_change_markers}

def music_causality_gate(dialogue_space_pass:bool,functional_gain:bool,invades_protected:bool,wallpaper:bool=False,premature_answer:bool=False)->dict[str,Any]:
    if not dialogue_space_pass: return {"status":"DEFER","admit_music":False,"reason":"DIALOGUE_SPACE_NOT_PROVEN"}
    failures=[]
    if not functional_gain: failures.append("NO_FUNCTIONAL_GAIN")
    if invades_protected: failures.append("PROTECTED_SILENCE_INVASION")
    if wallpaper: failures.append("WALLPAPER")
    if premature_answer: failures.append("PREMATURE_ANSWER")
    return {"status":"PASS" if not failures else "FAIL","admit_music":not failures,"failures":failures}

def validate_musical_fact_contract(c:dict[str,Any])->dict[str,Any]:
    req={"musical_fact_id","story_function","listener_must_infer","bindings","verification"}; missing=sorted(req-set(c))
    if missing: return {"status":"FAIL","missing":missing}
    ids=[]
    for _,events in c.get("bindings",{}).items():
        for e in events: ids.append(e.get("musical_fact_id"))
    if ids and any(i!=c["musical_fact_id"] for i in ids): return {"status":"FAIL","reason":"IDENTITY_SPLIT"}
    if c["verification"].get("result") not in ("PASS","PENDING"): return {"status":"FAIL","reason":"VERIFICATION_INVALID"}
    return {"status":"PASS" if c["verification"].get("result")=="PASS" else "HOLD","missing":[]}

def spatial_mono_safety(headphone_perspective_score:float,mono_comprehension:float,extreme_pan:bool)->dict[str,Any]:
    failures=[]
    if headphone_perspective_score<0.7: failures.append("PERSPECTIVE_WEAK")
    if mono_comprehension<0.9: failures.append("MONO_INFORMATION_LOSS")
    if extreme_pan: failures.append("EXTREME_PANNING_DEPENDENCY")
    return {"status":"PASS" if not failures else "FAIL","failures":failures}

def abc_mini_mix_gate(real_alignment:bool,human_blind_scores:dict[str,dict[str,float]]|None)->dict[str,Any]:
    if not real_alignment: return {"status":"HOLD","winner":None,"reason":"REAL_ALIGNMENT_REQUIRED"}
    if not human_blind_scores: return {"status":"HOLD","winner":None,"reason":"HUMAN_BLIND_REQUIRED"}
    dims=("comprehension","acting","space","desire_to_continue")
    avg={k:sum(v.get(d,0) for d in dims)/len(dims) for k,v in human_blind_scores.items()}
    winner=max(avg,key=avg.get); return {"status":"PASS","winner":winner,"averages":avg}

def protected_silence_postfx_gate(forbidden_energy_dbfs:float|None,threshold_dbfs:float=-80)->dict[str,Any]:
    if forbidden_energy_dbfs is None: return {"status":"HOLD","reason":"NO_POSTFX_MEASUREMENT"}
    return {"status":"PASS" if forbidden_energy_dbfs<=threshold_dbfs else "FAIL_COLLISION","measured_dbfs":forbidden_energy_dbfs,"threshold_dbfs":threshold_dbfs}

def stereo_source_stem_integrity(source_corr:float,stem_corr:float,source_side_db:float,stem_side_db:float)->dict[str,Any]:
    source_is_wide=(source_corr<0.95 and source_side_db>-60); collapsed=(stem_corr>0.999 and stem_side_db<-90)
    return {"status":"FAIL_STEREO_SOURCE_TO_MONO_STEM" if source_is_wide and collapsed else "PASS","source_is_wide":source_is_wide,"collapsed":collapsed}

def information_audibility_gate(dialogue:float,clue:float,space:float,music:float)->dict[str,Any]:
    ok=dialogue>=clue>=space>=music
    return {"status":"PASS" if ok else "FAIL_PRIORITY","values":{"dialogue":dialogue,"clue":clue,"space":space,"music":music}}

def earliest_cause_router(symptom:str)->dict[str,str]:
    m={"wrong_intention":"PERFORMANCE","flat_status_change":"PERFORMANCE","unclear_position":"STAGING","missing_body_action":"FOLEY_STAGING","wrong_cue_time":"ALIGNMENT_TIMELINE","music_masks_clue":"MIX_MUSIC","stereo_source_collapsed":"STEM_RENDER_ROUTING","global_loudness":"MASTERING","bad_pronunciation":"VOICE_PRONUNCIATION"}
    return {"symptom":symptom,"earliest_layer":m.get(symptom,"DIAGNOSE_BEFORE_REPAIR")}

def edit_before_regen(defect:str)->dict[str,str]:
    edit={"long_pause","crossfade_click","clip_trim","tail_overlap","level_balance"}; regen={"wrong_identity","wrong_intention","mispronunciation_uneditable","corrupt_source"}
    if defect in edit: return {"route":"EDIT_ONLY"}
    if defect in regen: return {"route":"SELECTIVE_RERENDER"}
    return {"route":"DIAGNOSE"}

def runtime_reconciliation_map(main_symbols:set[str],candidate_symbols:set[str])->dict[str,Any]:
    overlap=sorted(main_symbols & candidate_symbols); gaps=sorted(candidate_symbols-main_symbols)
    return {"status":"GAPS_REQUIRE_REVIEW" if gaps else "NO_GAPS","overlap":overlap,"candidate_gaps":gaps,"parallel_engine_authorized":False}

def sound_gate_state(assets_generated:bool,real_alignment:bool,human_listen:bool)->dict[str,str]:
    return {"acoustic_passports":"PASS_PLAN","ambience_asset_density":"PASS_CODE" if not assets_generated else "READY_AUDIO_TEST","recorder_foley_graph":"PASS_PLAN","diegetic_media_identity":"PASS_PLAN","music_entry":"HOLD_AUDIO" if not human_listen else "READY_A_B","mono_mobile":"HOLD_AUDIO" if not assets_generated else "READY_PROXY","abc_mix":"HOLD_LIVE_ALIGNMENT_AUDIO_HUMAN" if not (real_alignment and human_listen) else "READY","earliest_cause_router":"PASS_CODE"}

def secret_scan_classification(github_matches:int,drive_literal_matches:int,scope_note:str)->dict[str,Any]:
    return {"status":"PASS_CURRENT_SEARCH_SCOPE" if github_matches==0 and drive_literal_matches==0 else "REVIEW_REQUIRED","github_literal_matches":github_matches,"drive_literal_matches":drive_literal_matches,"scope_note":scope_note,"exhaustive_binary_revision_scan":False}

def third_project_dry_portability(project:str,locked:bool,dry_manifest_valid:bool,project_leaks:list[str])->dict[str,Any]:
    return {"status":"PASS_DRY" if locked and dry_manifest_valid and not project_leaks else "HOLD","project":project,"live_proof":False,"project_leaks":project_leaks}

def release_decision(gates:dict[str,str])->dict[str,Any]:
    mandatory=("architecture","dry_portability","authenticated_casting","live_portability","real_timeline","human_performance","economics","durable_provenance","release_qc")
    bad={k:gates.get(k,"MISSING") for k in mandatory if gates.get(k)!="PASS"}
    return {"status":"GO" if not bad else "HOLD","open_gates":bad}

def canonical_json_sha(obj:Any)->str:
    return sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
