#!/usr/bin/env python3
from __future__ import annotations
import json,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent

def run(args): return subprocess.run([sys.executable,*map(str,args)],capture_output=True,text=True)
def main():
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        usage={'schema_version':'room917.e01_sound_asset_semantic_usage/1.0','anchors':{'S10_SELECTOR_916':{'anchor_id':'ACTION_SELECT_916','relation':'SYNC','multiplicity':'ONCE'},'S13_INTERNAL_DOUBLE_RING_OLD':{'anchor_id':'EVENT_IMPOSSIBLE_INTERNAL_DOUBLE_RING','relation':'FOREGROUND_EVENT','multiplicity':'ONE_DOUBLE_RING_EVENT'}}}
        up=td/'usage.json';up.write_text(json.dumps(usage));out=td/'out.json'
        accepted={'schema_version':'room917.accepted_semantic_timing/1.0','authority_status':'ACCEPTED','events':[{'anchor_id':'ACTION_SELECT_916','start_seconds':12.1,'end_seconds':12.2,'source_status':'ACCEPTED_ALIGNMENT','source_ref':'test'},{'anchor_id':'EVENT_IMPOSSIBLE_INTERNAL_DOUBLE_RING','start_seconds':18.0,'end_seconds':18.8,'source_status':'LIVE_TIMELINE','source_ref':'test'}]}
        tp=td/'timing.json';tp.write_text(json.dumps(accepted));q=run([HERE/'resolve_sound_asset_semantic_timing.py','--usage-map',up,'--timing-map',tp,'--out',out]);assert q.returncode==0,(q.stdout,q.stderr);d=json.loads(out.read_text());assert d['status']=='PASS' and len(d['resolved'])==2
        accepted['events'].append({'anchor_id':'ACTION_SELECT_916','start_seconds':13.0,'end_seconds':13.1,'source_status':'LIVE_TIMELINE','source_ref':'duplicate'});tp.write_text(json.dumps(accepted));q=run([HERE/'resolve_sound_asset_semantic_timing.py','--usage-map',up,'--timing-map',tp,'--out',out]);assert q.returncode==0;d=json.loads(out.read_text());assert d['status']=='PASS_WITH_HOLDS' and any(h['reason']=='AMBIGUOUS_MULTIPLE_MATCHES' for h in d['holds'])
        bad={'schema_version':'room917.accepted_semantic_timing/1.0','authority_status':'HOLD_UNTIL_REAL_TIMING_IMPORTED','events':[]};tp.write_text(json.dumps(bad));q=run([HERE/'resolve_sound_asset_semantic_timing.py','--usage-map',up,'--timing-map',tp,'--out',out]);assert q.returncode==4
    print('3/3 PASS semantic timing: accepted resolves; ambiguity HOLD; unaccepted timing FAIL')
if __name__=='__main__':main()
