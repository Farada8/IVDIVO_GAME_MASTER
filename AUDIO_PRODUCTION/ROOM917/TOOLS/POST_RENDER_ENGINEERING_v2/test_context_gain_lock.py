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
def main():
    with tempfile.TemporaryDirectory() as td:
        td=Path(td);audio=td/'a.wav';wav(audio);h=sha(audio)
        selected={'schema_version':'room917.sound_asset_audition_compilation/1.0','selected':{'S07_TRANSFORMER_WAKE':{'candidate_id':'S07_TEST','path':str(audio),'sha256':h,'audition_status':'PASS','mono_status':'PASS','phone_proxy_status':'PASS','gain_db':None,'promotion_status':'HOLD_CONTEXT_GAIN_REQUIRED'}}}
        sp=td/'selected.json';sp.write_text(json.dumps(selected))
        base={'schema_version':'room917.e01_context_gain_lock/1.0','source_selected_compilation_sha256':sha(sp),'entries':{'S07_TRANSFORMER_WAKE':{'candidate_id':'S07_TEST','gain_db':None,'context_status':'PASS','dialogue_intelligibility':'PASS','function_readability':'PASS','no_overstatement':'PASS','mono_context':'PASS','phone_context':'PASS'}}}
        gp=td/'gain.json';gp.write_text(json.dumps(base));out=td/'out.json'
        q=run([HERE/'apply_context_gain_lock.py','--selected',sp,'--gain-lock',gp,'--out',out]);assert q.returncode==4
        base['entries']['S07_TRANSFORMER_WAKE']['gain_db']=-12.5;gp.write_text(json.dumps(base));q=run([HERE/'apply_context_gain_lock.py','--selected',sp,'--gain-lock',gp,'--out',out]);assert q.returncode==0,(q.stdout,q.stderr)
        data=json.loads(out.read_text());assert data['candidates']['S07_TRANSFORMER_WAKE']['gain_db']==-12.5
        base['entries']['S07_TRANSFORMER_WAKE']['dialogue_intelligibility']='HOLD';gp.write_text(json.dumps(base));q=run([HERE/'apply_context_gain_lock.py','--selected',sp,'--gain-lock',gp,'--out',out]);assert q.returncode==4
    print('3/3 PASS context gain lock: missing gain HOLD; explicit PASS; failed context gate HOLD')
if __name__=='__main__':main()
