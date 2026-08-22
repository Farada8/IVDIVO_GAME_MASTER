#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def main()->int:
 ap=argparse.ArgumentParser(description='Resolve ROOM917 semantic sound anchors only from trusted accepted timing events')
 ap.add_argument('--usage-map',required=True,type=Path);ap.add_argument('--timing-map',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);a=ap.parse_args()
 usage=load(a.usage_map);tim=load(a.timing_map);errors=[];holds=[];resolved={}
 if usage.get('schema_version')!='room917.e01_sound_asset_semantic_usage/1.0': errors.append('USAGE_MAP_SCHEMA_INVALID')
 if tim.get('schema_version') not in ('room917.accepted_semantic_timing/1.0','room917.live_timeline_semantic_events/1.0'): errors.append('TIMING_MAP_SCHEMA_NOT_ACCEPTED')
 if tim.get('authority_status')!='ACCEPTED': errors.append('TIMING_AUTHORITY_NOT_ACCEPTED')
 anchors=usage.get('anchors',{})
 if not isinstance(anchors,dict) or not anchors: errors.append('USAGE_ANCHORS_EMPTY_OR_INVALID');anchors={}
 events={}
 for e in tim.get('events',[]):
  if isinstance(e,dict): events.setdefault(e.get('anchor_id'),[]).append(e)
 for aid,row in anchors.items():
  if not isinstance(row,dict): holds.append({'asset_id':aid,'reason':'USAGE_ANCHOR_ROW_INVALID'});continue
  anchor=row.get('anchor_id');matches=events.get(anchor,[])
  if not anchor: holds.append({'asset_id':aid,'reason':'ANCHOR_ID_MISSING'});continue
  if len(matches)==0: holds.append({'asset_id':aid,'anchor_id':anchor,'reason':'ANCHOR_NOT_FOUND'});continue
  if len(matches)>1 and row.get('multiplicity') in ('ONCE','ONCE_PER_WAKE','ONE_SHORT_SEQUENCE','ONE_SCAN_SEQUENCE','ONE_DOUBLE_RING_EVENT','EXACTLY_ONE_TWO_PART_EVENT','ONE_RETURN_SEQUENCE'):
   holds.append({'asset_id':aid,'anchor_id':anchor,'reason':'AMBIGUOUS_MULTIPLE_MATCHES','match_count':len(matches)});continue
  good=[]
  for e in matches:
   try:s=float(e['start_seconds']);en=float(e.get('end_seconds',s))
   except Exception: holds.append({'asset_id':aid,'anchor_id':anchor,'reason':'INVALID_NUMERIC_TIMING'});good=[];break
   if s<0 or en<s: holds.append({'asset_id':aid,'anchor_id':anchor,'reason':'INVALID_RANGE'});good=[];break
   if e.get('source_status') not in ('ACCEPTED_ALIGNMENT','LIVE_TIMELINE','FOUNDER_LOCKED_TIMING'): holds.append({'asset_id':aid,'anchor_id':anchor,'reason':'UNTRUSTED_EVENT_SOURCE'});good=[];break
   good.append({'start_seconds':s,'end_seconds':en,'source_status':e.get('source_status'),'source_ref':e.get('source_ref')})
  if good: resolved[aid]={'anchor_id':anchor,'relation':row.get('relation'),'multiplicity':row.get('multiplicity'),'events':good,'timing_status':'RESOLVED_FROM_ACCEPTED_SOURCE'}
 complete=bool(anchors) and not errors and not holds and set(resolved)==set(anchors)
 status='PASS' if complete else ('FAIL' if errors else 'HOLD')
 production_resolved=resolved if complete else {}
 out={'schema_version':'room917.e01_sound_asset_resolved_timing/1.1','status':status,'production_timing_ready':complete,'requested_asset_ids':sorted(anchors),'resolved':resolved,'production_resolved':production_resolved,'diagnostic_resolved_count':len(resolved),'production_resolved_count':len(production_resolved),'holds':holds,'errors':errors,'law':'No timestamp is inferred from semantics. Partial resolution may remain visible only as diagnostic evidence. Production timing output is atomic across the requested usage map: any missing, ambiguous, invalid, or untrusted anchor suppresses production_resolved and returns HOLD/FAIL.'}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(status+' diagnostic_resolved='+str(len(resolved))+' production_resolved='+str(len(production_resolved))+' holds='+str(len(holds)));return 0 if complete else 4
if __name__=='__main__': raise SystemExit(main())
