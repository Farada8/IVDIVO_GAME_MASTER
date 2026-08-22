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
 sel=load(a.selected);gl=load(a.gain_lock);errors=[];holds=[];out={}
 if sel.get('schema_version')!='room917.sound_asset_audition_compilation/1.0': errors.append('SELECTED_SCHEMA_INVALID')
 if gl.get('schema_version')!='room917.e01_context_gain_lock/1.0': errors.append('GAIN_LOCK_SCHEMA_INVALID')
 if gl.get('source_selected_compilation_sha256')!=sha(a.selected): errors.append('SELECTED_COMPILATION_SHA_MISMATCH')
 for aid,row in sel.get('selected',{}).items():
  lock=gl.get('entries',{}).get(aid)
  if not lock: holds.append({'asset_id':aid,'reason':'GAIN_LOCK_ENTRY_MISSING'});continue
  if lock.get('candidate_id')!=row.get('candidate_id'): holds.append({'asset_id':aid,'reason':'CANDIDATE_ID_MISMATCH'});continue
  try: gain=float(lock.get('gain_db'))
  except (TypeError,ValueError): holds.append({'asset_id':aid,'reason':'GAIN_DB_NOT_NUMERIC'});continue
  required=['context_status','dialogue_intelligibility','function_readability','no_overstatement','mono_context','phone_context']
  if any(lock.get(k)!='PASS' for k in required): holds.append({'asset_id':aid,'reason':'CONTEXT_GATES_NOT_ALL_PASS'});continue
  p=Path(row.get('path',''))
  if not p.is_file() or sha(p)!=row.get('sha256'): holds.append({'asset_id':aid,'reason':'SELECTED_ASSET_BYTES_OR_SHA_MISMATCH'});continue
  meta=wav_meta(p)
  out[aid]={'asset_id':aid,'candidate_id':row['candidate_id'],'path':str(p.resolve()),'sha256':row['sha256'],'size_bytes':meta['size_bytes'],'sample_rate_hz':meta['sample_rate_hz'],'bit_depth':meta['bit_depth'],'channels':meta['channels'],'gain_db':gain,'audition_status':'PASS','mono_status':'PASS','phone_proxy_status':'PASS','loop_seam_status':row.get('loop_seam_status'),'false_clue_audit_status':row.get('false_clue_audit_status'),'context_gain_lock':'PASS'}
 status='FAIL' if errors else ('PASS' if out and not holds else ('PASS_WITH_HOLDS' if out else 'HOLD'))
 result={'schema_version':'room917.e01_context_gain_compilation/1.0','status':status,'candidates':out,'holds':holds,'errors':errors,'source_selected_sha256':sha(a.selected),'source_gain_lock_sha256':sha(a.gain_lock),'law':'Only explicit context-auditioned numeric gain is emitted. This output still must pass sound_asset_binding_gate before mix.'}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(status+' candidates='+str(len(out))+' holds='+str(len(holds)));return 0 if out and not errors else 4
if __name__=='__main__': raise SystemExit(main())
