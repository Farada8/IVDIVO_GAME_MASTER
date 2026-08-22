#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, wave
from pathlib import Path


def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''): h.update(b)
 return h.hexdigest()
def wav_meta(p):
 with wave.open(str(p),'rb') as w:
  return {'size_bytes':Path(p).stat().st_size,'sample_rate_hz':w.getframerate(),'bit_depth':w.getsampwidth()*8,'channels':w.getnchannels()}

def main()->int:
 ap=argparse.ArgumentParser(description='Apply explicit human context gain lock to selected ROOM917 sound candidates')
 ap.add_argument('--selected',required=True,type=Path);ap.add_argument('--gain-lock',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);a=ap.parse_args()
 sel=load(a.selected);gl=load(a.gain_lock);errors=[];holds=[];staged={}
 if sel.get('schema_version')!='room917.sound_asset_audition_compilation/1.0': errors.append('SELECTED_SCHEMA_INVALID')
 if gl.get('schema_version')!='room917.e01_context_gain_lock/1.0': errors.append('GAIN_LOCK_SCHEMA_INVALID')
 if gl.get('source_selected_compilation_sha256')!=sha(a.selected): errors.append('SELECTED_COMPILATION_SHA_MISMATCH')
 selected=sel.get('selected',{})
 entries=gl.get('entries',{})
 if not isinstance(selected,dict) or not selected: errors.append('SELECTED_SET_EMPTY_OR_INVALID');selected={}
 if not isinstance(entries,dict): errors.append('GAIN_LOCK_ENTRIES_INVALID');entries={}
 if set(entries)!=set(selected): errors.append('GAIN_LOCK_ASSET_SET_MISMATCH')
 for aid,row in selected.items():
  lock=entries.get(aid)
  if not lock: holds.append({'asset_id':aid,'reason':'GAIN_LOCK_ENTRY_MISSING'});continue
  if lock.get('candidate_id')!=row.get('candidate_id'): holds.append({'asset_id':aid,'reason':'CANDIDATE_ID_MISMATCH'});continue
  try: gain=float(lock.get('gain_db'))
  except (TypeError,ValueError): holds.append({'asset_id':aid,'reason':'GAIN_DB_NOT_NUMERIC'});continue
  required=['context_status','dialogue_intelligibility','function_readability','no_overstatement','mono_context','phone_context']
  if any(lock.get(k)!='PASS' for k in required): holds.append({'asset_id':aid,'reason':'CONTEXT_GATES_NOT_ALL_PASS'});continue
  p=Path(row.get('path',''))
  if not p.is_file() or sha(p)!=row.get('sha256'): holds.append({'asset_id':aid,'reason':'SELECTED_ASSET_BYTES_OR_SHA_MISMATCH'});continue
  meta=wav_meta(p)
  staged[aid]={'asset_id':aid,'candidate_id':row['candidate_id'],'path':str(p.resolve()),'sha256':row['sha256'],'size_bytes':meta['size_bytes'],'sample_rate_hz':meta['sample_rate_hz'],'bit_depth':meta['bit_depth'],'channels':meta['channels'],'gain_db':gain,'audition_status':'PASS','mono_status':'PASS','phone_proxy_status':'PASS','loop_seam_status':row.get('loop_seam_status'),'false_clue_audit_status':row.get('false_clue_audit_status'),'context_gain_lock':'PASS'}
 atomic_ready=bool(selected) and not errors and not holds and set(staged)==set(selected)
 out=staged if atomic_ready else {}
 status='PASS' if atomic_ready else ('FAIL' if errors else 'HOLD')
 result={'schema_version':'room917.e01_context_gain_compilation/1.1','status':status,'requested_asset_ids':sorted(selected),'candidates':out,'staged_pass_count':len(staged),'renderer_candidate_set_atomic':True,'candidates_suppressed_on_any_hold':not atomic_ready,'holds':holds,'errors':errors,'source_selected_sha256':sha(a.selected),'source_gain_lock_sha256':sha(a.gain_lock),'law':'Context gain promotion is atomic across the entire selected audition set. One missing/failed context gate suppresses all downstream candidate output. Only explicit context-auditioned numeric gain is eligible, and the complete output still must pass sound_asset_binding_gate before mix.'}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(status+' staged='+str(len(staged))+' emitted='+str(len(out))+' holds='+str(len(holds)));return 0 if atomic_ready else 4
if __name__=='__main__': raise SystemExit(main())
