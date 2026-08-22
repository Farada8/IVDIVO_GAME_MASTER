#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, subprocess, sys, tempfile, wave
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from post_render_router import pick_frontier

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def wav(p):
    with wave.open(str(p),'wb') as w:
        w.setnchannels(2);w.setsampwidth(3);w.setframerate(48000);w.writeframes(b'\x00'*(2*3*480))
def run(cmd): return subprocess.run([sys.executable,*map(str,cmd)],capture_output=True,text=True)
def test_router_secondary():
    ctx={'mainline_ready':False,'authority_ok':True,'asset_contract_exists':True,'asset_canary_receipt_exists':True,'asset_audition_contract_exists':True,'release_qc_profile_exists':True,'provenance_contract_exists':True,'master_ok':False,'timing_ok':False,'secondary_safe_work_remaining':True}
    assert pick_frontier(ctx)['frontier']=='DOCUMENTED_SECONDARY_RISK_REDUCTION'
def test_router_recovery_when_secondary_exhausted():
    ctx={'mainline_ready':False,'authority_ok':True,'asset_contract_exists':True,'asset_canary_receipt_exists':True,'asset_audition_contract_exists':True,'release_qc_profile_exists':True,'provenance_contract_exists':True,'master_ok':False,'timing_ok':False,'secondary_safe_work_remaining':False}
    assert pick_frontier(ctx)['frontier']=='RECOVERY_SEARCH_FOR_MISSING_BYTES_OR_TIMING'
def test_policy():
    p=json.loads((HERE/'CONTINUATION_POLICY_v1.json').read_text())
    assert p['blocked_is_not_stop'] is True and p['mode']=='FAIL_CLOSED_NON_STOP'
def test_blind_builder_and_tamper():
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); src=td/'src';out=td/'out';src.mkdir();
        rows=[]
        for aid in ('A01_TEST','A02_TEST'):
            p=src/(aid+'_CAND.wav');wav(p);rows.append({'contract_asset_id':aid,'candidate_id':aid+'_CAND','filename':p.name,'sha256':sha(p),'duration_seconds':0.01})
        rec=td/'receipt.json';rec.write_text(json.dumps({'assets':rows}))
        q=run([HERE/'build_sound_asset_blind_package.py','--receipt',rec,'--canary-dir',src,'--outdir',out,'--package-id','TEST','--room-bed-mode'])
        assert q.returncode==0,(q.stdout,q.stderr)
        assert (out/'PUBLIC_BLIND'/'ROOM_BED_X.wav').is_file() and (out/'INTERNAL_IDENTITY_KEY_SEALED.json').is_file()
        rows[0]['sha256']='0'*64;rec.write_text(json.dumps({'assets':rows}));out2=td/'out2'
        q=run([HERE/'build_sound_asset_blind_package.py','--receipt',rec,'--canary-dir',src,'--outdir',out2,'--package-id','TEST2','--room-bed-mode'])
        assert q.returncode==4

def test_audition_compiler_gain_fail_closed():
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); audio=td/'audio';audio.mkdir();p=audio/'S07_TEST.wav';wav(p);h=sha(p)
        key={'mapping':{'S07_TRANSFORMER_WAKE':{'A':{'candidate_id':'S07_TEST','source_sha256':h}}}}
        kp=td/'key.json';kp.write_text(json.dumps(key))
        result={'schema_version':'room917.e01_sound_asset_blind_audition_result/1.1','critical_sfx_pass':{'first_pass_notes_frozen':True,'functions':{'S07_TRANSFORMER_WAKE':{'selected_variant':'A','ordinary_technical':True,'not_music_or_horror':True,'mono_survival':True,'phone_survival':True,'notes':'ok'}}}}
        rp=td/'result.json';rp.write_text(json.dumps(result));op=td/'compiled.json'
        q=run([HERE/'compile_sound_asset_audition_result.py','--result',rp,'--critical-key',kp,'--critical-dir',audio,'--out',op])
        assert q.returncode==0,(q.stdout,q.stderr)
        data=json.loads(op.read_text());row=data['selected']['S07_TRANSFORMER_WAKE'];assert row['gain_db'] is None and row['promotion_status']=='HOLD_CONTEXT_GAIN_REQUIRED'

def main():
    tests=[test_router_secondary,test_router_recovery_when_secondary_exhausted,test_policy,test_blind_builder_and_tamper,test_audition_compiler_gain_fail_closed]
    for t in tests:t();print('PASS',t.__name__)
    print('5/5 PASS')
if __name__=='__main__':main()
