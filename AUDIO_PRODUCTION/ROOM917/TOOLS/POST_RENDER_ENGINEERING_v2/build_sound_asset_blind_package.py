#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, random, shutil
from pathlib import Path


def sha256_file(p: Path, block_size: int = 8 * 1024 * 1024) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(block_size),b''): h.update(b)
    return h.hexdigest()

def load(p: Path): return json.loads(p.read_text(encoding='utf-8'))
def normalize_rows(receipt: dict):
    rows=[]; assets=receipt.get('assets')
    if isinstance(assets,list):
        for r in assets:
            if 'contract_asset_id' in r: rows.append(r)
    elif isinstance(assets,dict):
        for aid,variants in assets.items():
            for item in variants:
                if isinstance(item,list):
                    rows.append({'contract_asset_id':aid,'candidate_id':item[0],'sha256':item[1],'duration_seconds':item[2],'filename':item[0]+'.wav'})
                else:
                    r=dict(item); r.setdefault('contract_asset_id',aid); rows.append(r)
    return rows

def main()->int:
    ap=argparse.ArgumentParser(description='Build blind ROOM917 sound-asset audition package from verified canary bytes')
    ap.add_argument('--receipt',required=True,type=Path); ap.add_argument('--canary-dir',required=True,type=Path); ap.add_argument('--outdir',required=True,type=Path); ap.add_argument('--package-id',required=True); ap.add_argument('--seed',type=int,default=91720260822); ap.add_argument('--room-bed-mode',action='store_true'); a=ap.parse_args()
    rec=load(a.receipt); rows=normalize_rows(rec); errors=[]; by={}
    for r in rows:
        aid=r['contract_asset_id']; p=a.canary_dir/(r.get('filename') or (r['candidate_id']+'.wav'))
        if not p.is_file(): errors.append('MISSING:'+str(p)); continue
        observed=sha256_file(p)
        if observed!=str(r.get('sha256','')).lower(): errors.append('SHA_MISMATCH:'+r['candidate_id']); continue
        rr=dict(r); rr['source_path']=str(p.resolve()); by.setdefault(aid,[]).append(rr)
    if errors:
        print('HOLD '+';'.join(errors)); return 4
    rnd=random.Random(a.seed); a.outdir.mkdir(parents=True,exist_ok=True); public=a.outdir/'PUBLIC_BLIND'; public.mkdir(exist_ok=True); internal={}; manifest={'schema_version':'room917.sound_asset_blind_package/1.0','package_id':a.package_id,'status':'READY_FOR_HUMAN_LISTEN','rules':['LISTEN_BEFORE_OPENING_INTERNAL_KEY','FREEZE_NOTES_BEFORE_REVEAL','NO_PRODUCTION_BINDING_FROM_PACKAGE_ALONE'],'groups':{}}
    if a.room_bed_mode:
        if len(by)!=2 or any(len(v)!=1 for v in by.values()):
            print('HOLD room-bed mode requires exactly two assets with one candidate each'); return 4
        aids=list(by); rnd.shuffle(aids)
        for label,aid in zip(['X','Y'],aids):
            r=by[aid][0]; dst=public/f'ROOM_BED_{label}.wav'; shutil.copy2(r['source_path'],dst); manifest['groups'][label]={'file':dst.name,'sha256':sha256_file(dst)}; internal[label]={'contract_asset_id':aid,'candidate_id':r['candidate_id'],'source_sha256':r['sha256']}
    else:
        for aid,variants in sorted(by.items()):
            variants=list(variants); rnd.shuffle(variants); labels='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            if len(variants)>len(labels): raise SystemExit('too many variants')
            group=[]; imap={}
            for label,r in zip(labels,variants):
                dst=public/f'{aid}__{label}.wav'; shutil.copy2(r['source_path'],dst); group.append({'label':label,'file':dst.name,'sha256':sha256_file(dst)}); imap[label]={'candidate_id':r['candidate_id'],'source_sha256':r['sha256']}
            manifest['groups'][aid]=group; internal[aid]=imap
    (public/'LISTENER_MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    key={'schema_version':'room917.sound_asset_blind_identity_key/1.0','package_id':a.package_id,'receipt_sha256':sha256_file(a.receipt),'mapping':internal,'law':'Keep sealed until first-pass notes are frozen.'}
    (a.outdir/'INTERNAL_IDENTITY_KEY_SEALED.json').write_text(json.dumps(key,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('PASS groups='+str(len(manifest['groups']))+' files='+str(sum(1 for _ in public.glob('*.wav')))); return 0
if __name__=='__main__': raise SystemExit(main())
