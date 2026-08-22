#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path


def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''): h.update(b)
 return h.hexdigest()
def resolve_key(key, group, label):
 m=key.get('mapping',{}).get(group)
 if isinstance(m,dict): return m.get(label)
 return None
def all_true(row,skip=('selected_variant','notes')):
 vals=[v for k,v in row.items() if k not in skip and isinstance(v,bool)]
 return bool(vals) and all(vals)
def main()->int:
 ap=argparse.ArgumentParser(description='Compile frozen ROOM917 blind sound-audition results without inventing gain or binding')
 ap.add_argument('--result',required=True,type=Path);ap.add_argument('--room-bed-key',type=Path);ap.add_argument('--critical-key',type=Path);ap.add_argument('--support-key',type=Path);ap.add_argument('--room-bed-dir',type=Path);ap.add_argument('--critical-dir',type=Path);ap.add_argument('--support-dir',type=Path);ap.add_argument('--out',required=True,type=Path);a=ap.parse_args()
 r=load(a.result); errors=[]; selected={}; holds=[]
 if r.get('schema_version')!='room917.e01_sound_asset_blind_audition_result/1.1': errors.append('RESULT_SCHEMA_NOT_1_1')
 # Room beds X/Y
 rb=r.get('room_bed_pass',{})
 if rb and rb.get('first_pass_notes_frozen'):
  if not a.room_bed_key or not a.room_bed_dir: errors.append('ROOM_BED_KEY_OR_DIR_MISSING')
  else:
   key=load(a.room_bed_key)
   for label in ('X','Y'):
    row=rb.get(label,{})
    if row.get('verdict')!='PASS_CANDIDATE': continue
    req=['realism','false_clue','loop_seam','mono_survival','phone_survival']
    if not all(row.get(k) is True for k in req): holds.append({'group':'ROOM_BED','label':label,'reason':'HUMAN_GATES_NOT_ALL_PASS'}); continue
    ident=resolve_key(key,label,label) or key.get('mapping',{}).get(label)
    if not ident: holds.append({'group':'ROOM_BED','label':label,'reason':'IDENTITY_KEY_MAPPING_MISSING'}); continue
    aid=ident['contract_asset_id']; cid=ident['candidate_id']; p=a.room_bed_dir/(cid+'.wav')
    if not p.is_file() or sha(p)!=ident['source_sha256']: holds.append({'asset_id':aid,'reason':'BYTES_OR_SHA_MISMATCH'}); continue
    selected[aid]={'candidate_id':cid,'path':str(p.resolve()),'sha256':ident['source_sha256'],'audition_status':'PASS','mono_status':'PASS','phone_proxy_status':'PASS','loop_seam_status':'PASS','false_clue_audit_status':'PASS','gain_db':None,'promotion_status':'HOLD_CONTEXT_GAIN_REQUIRED'}
 elif rb:
  holds.append({'group':'ROOM_BED','reason':'FIRST_PASS_NOTES_NOT_FROZEN'})
 # Generic A/B/C groups
 for section,key_path,root in [('critical_sfx_pass',a.critical_key,a.critical_dir),('support_sfx_music_pass',a.support_key,a.support_dir)]:
  sec=r.get(section,{})
  if not sec: continue
  if not sec.get('first_pass_notes_frozen'): holds.append({'group':section,'reason':'FIRST_PASS_NOTES_NOT_FROZEN'}); continue
  if not key_path or not root: errors.append(section.upper()+'_KEY_OR_DIR_MISSING'); continue
  key=load(key_path)
  for aid,row in sec.get('functions',{}).items():
   label=row.get('selected_variant')
   if label not in ('A','B','C'): continue
   if not all_true(row): holds.append({'asset_id':aid,'reason':'HUMAN_GATES_NOT_ALL_PASS'}); continue
   ident=resolve_key(key,aid,label)
   if not ident: holds.append({'asset_id':aid,'reason':'IDENTITY_KEY_MAPPING_MISSING'}); continue
   cid=ident['candidate_id']; p=root/(cid+'.wav')
   if not p.is_file() or sha(p)!=ident['source_sha256']: holds.append({'asset_id':aid,'reason':'BYTES_OR_SHA_MISMATCH'}); continue
   selected[aid]={'candidate_id':cid,'path':str(p.resolve()),'sha256':ident['source_sha256'],'audition_status':'PASS','mono_status':'PASS' if row.get('mono_survival') is True else 'HOLD','phone_proxy_status':'PASS' if row.get('phone_survival') is True else 'HOLD','gain_db':None,'promotion_status':'HOLD_CONTEXT_GAIN_REQUIRED'}
 if 'S14_UNMARKED_GLASS_LAMP_PING' in selected and 'S11_GLASS_LAMP_916_PING' not in selected:
  holds.append({'asset_id':'S14_UNMARKED_GLASS_LAMP_PING','reason':'S11_REFERENCE_NOT_SELECTED'}); selected.pop('S14_UNMARKED_GLASS_LAMP_PING',None)
 status='FAIL' if errors else ('READY_FOR_CONTEXT_GAIN' if selected else 'HOLD')
 out={'schema_version':'room917.sound_asset_audition_compilation/1.0','status':status,'selected':selected,'holds':holds,'errors':errors,'law':'Human blind selection can lock candidate identity but cannot invent production gain. sound_asset_binding_gate remains downstream and requires explicit gain plus all required translation/asset-class gates.'}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(status+' selected='+str(len(selected))+' holds='+str(len(holds)))
 return 0 if status=='READY_FOR_CONTEXT_GAIN' else 4
if __name__=='__main__': raise SystemExit(main())
