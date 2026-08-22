#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,subprocess,sys,tempfile,wave
from pathlib import Path
HERE=Path(__file__).resolve().parent

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def wav(p):
    with wave.open(str(p),'wb') as w:
        w.setnchannels(2);w.setsampwidth(3);w.setframerate(48000);w.writeframes(b'\x00'*(2*3*480))
def run(args): return subprocess.run([sys.executable,*map(str,args)],capture_output=True,text=True)
def lock_row(cid,gain=None):
    return {'candidate_id':cid,'gain_db':gain,'context_status':'PASS','dialogue_intelligibility':'PASS','function_readability':'PASS','no_overstatement':'PASS','mono_context':'PASS','phone_context':'PASS'}
def main():
    with tempfile.TemporaryDirectory() as td:
        td=Path(td);audio=td/'a.wav';wav(audio);h=sha(audio)
        selected={'schema_version':'room917.sound_asset_audition_compilation/1.0','selected':{'S07_TRANSFORMER_WAKE':{'candidate_id':'S07_TEST','path':str(audio),'sha256':h,'audition_status':'PASS','mono_status':'PASS','phone_proxy_status':'PASS','gain_db':None,'promotion_status':'HOLD_CONTEXT_GAIN_REQUIRED'}}}
        sp=td/'selected.json';sp.write_text(json.dumps(selected))
        base={'schema_version':'room917.e01_context_gain_lock/1.0','source_selected_compilation_sha256':sha(sp),'entries':{'S07_TRANSFORMER_WAKE':lock_row('S07_TEST')}}
        gp=td/'gain.json';gp.write_text(json.dumps(base));out=td/'out.json'

        q=run([HERE/'apply_context_gain_lock.py','--selected',sp,'--gain-lock',gp,'--out',out]);assert q.returncode==4
        data=json.loads(out.read_text());assert data['candidates']=={} and data['status']=='HOLD'

        base['entries']['S07_TRANSFORMER_WAKE']['gain_db']=-12.5;gp.write_text(json.dumps(base));q=run([HERE/'apply_context_gain_lock.py','--selected',sp,'--gain-lock',gp,'--out',out]);assert q.returncode==0,(q.stdout,q.stderr)
        data=json.loads(out.read_text());assert data['candidates']['S07_TRANSFORMER_WAKE']['gain_db']==-12.5 and data['status']=='PASS'

        base['entries']['S07_TRANSFORMER_WAKE']['dialogue_intelligibility']='HOLD';gp.write_text(json.dumps(base));q=run([HERE/'apply_context_gain_lock.py','--selected',sp,'--gain-lock',gp,'--out',out]);assert q.returncode==4
        data=json.loads(out.read_text());assert data['candidates']=={} and data['candidates_suppressed_on_any_hold'] is True

        # Regression: one good asset plus one HOLD must not emit the good subset.
        audio2=td/'b.wav';wav(audio2);h2=sha(audio2)
        selected2={'schema_version':'room917.sound_asset_audition_compilation/1.0','selected':{
            'S07_TRANSFORMER_WAKE':{'candidate_id':'S07_TEST','path':str(audio),'sha256':h,'audition_status':'PASS','mono_status':'PASS','phone_proxy_status':'PASS','gain_db':None,'promotion_status':'HOLD_CONTEXT_GAIN_REQUIRED'},
            'S08_RELAY_RIPPLE':{'candidate_id':'S08_TEST','path':str(audio2),'sha256':h2,'audition_status':'PASS','mono_status':'PASS','phone_proxy_status':'PASS','gain_db':None,'promotion_status':'HOLD_CONTEXT_GAIN_REQUIRED'},
        }}
        sp2=td/'selected2.json';sp2.write_text(json.dumps(selected2))
        gl2={'schema_version':'room917.e01_context_gain_lock/1.0','source_selected_compilation_sha256':sha(sp2),'entries':{
            'S07_TRANSFORMER_WAKE':lock_row('S07_TEST',-12.0),
            'S08_RELAY_RIPPLE':lock_row('S08_TEST',-13.0),
        }}
        gl2['entries']['S08_RELAY_RIPPLE']['function_readability']='HOLD'
        gp2=td/'gain2.json';gp2.write_text(json.dumps(gl2));out2=td/'out2.json'
        q=run([HERE/'apply_context_gain_lock.py','--selected',sp2,'--gain-lock',gp2,'--out',out2]);assert q.returncode==4,(q.stdout,q.stderr)
        data=json.loads(out2.read_text());assert data['status']=='HOLD';assert data['staged_pass_count']==1;assert data['candidates']=={};assert data['renderer_candidate_set_atomic'] is True
    print('4/4 PASS context gain lock: missing gain HOLD; explicit PASS; failed context gate HOLD; partial PASS atomically suppressed')
if __name__=='__main__':main()
