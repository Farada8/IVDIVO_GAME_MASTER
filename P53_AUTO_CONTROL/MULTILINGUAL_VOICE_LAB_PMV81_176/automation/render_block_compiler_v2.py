#!/usr/bin/env python3
import json,re,hashlib,sys

def parse_md(path):
    scene=None; out=[]
    for line in open(path,encoding='utf-8'):
        line=line.rstrip('\n')
        if line.startswith('## S'): scene=line[3:].strip()
        m=re.match(r'^\*\*(.+?):\*\*\s*(.*)$',line)
        if m:
            speaker=m.group(1).strip()
            if speaker.upper() in {'STATUS','SOURCE','SUPERSEDES','PATCH BASIS'}: continue
            out.append({'scene_id':scene,'speaker':speaker,'text_ru':m.group(2)})
    return out

def voice_role(s):
    s=s.upper()
    if 'NAOMI' in s: return 'NAOMI_PARK'
    if 'ELI' in s: return 'ELI_KWON'
    if 'TALIA' in s: return 'TALIA_WYNN'
    if 'CAL' in s: return 'CAL_MERCER'
    if 'VOICE IN IEM' in s: return 'THREAT_VOICE'
    return s.replace(' ','_')

def compile_plan(md_path,req_path):
    ru=parse_md(md_path); src=json.load(open(req_path,encoding='utf-8'))['requests']; assert len(ru)==len(src)
    clue={10,46,51,61,120,135,137,152,160,161,180,186,188,190}; blocks=[]; cur=[]
    def flush():
        nonlocal cur
        if not cur:return
        mode='TTD_BLOCK' if len(cur)>1 else 'ISOLATED_TTS'; bid=f"RU_E01_V2_{'TTD' if mode=='TTD_BLOCK' else 'ISO'}_{len(blocks)+1:03d}"
        blocks.append({'render_block_id':bid,'render_mode':mode,'status':'CANDIDATE_NOT_RENDERABLE','scene_id':cur[0]['scene_id'],'inputs':cur}); cur=[]
    for i,(r,s) in enumerate(zip(ru,src),1):
        item={'source_speech_index':i,'block_id':s['block_id'],'speaker':r['speaker'],'voice_role':voice_role(r['speaker']),'text_ru':r['text_ru'],'text_ru_sha256':hashlib.sha256(r['text_ru'].encode()).hexdigest(),'source_en_sha256':s['exact_text_sha256'],'scene_id':r['scene_id'],'acoustic_domain':s.get('acoustic_domain'),'post_chain':s.get('post_chain')}
        force_iso=(i in clue or 'V.O.' in r['speaker'] or 'VOICE IN IEM' in r['speaker'] or 'REPORTER' in r['speaker'] or 'MEDIA' in r['speaker'])
        if force_iso: flush(); cur=[item]; flush(); continue
        if cur and (cur[-1]['scene_id']!=item['scene_id'] or cur[-1]['acoustic_domain']!=item['acoustic_domain'] or cur[-1]['post_chain']!=item['post_chain'] or len(cur)>=6): flush()
        cur.append(item)
    flush(); covered=[i['source_speech_index'] for b in blocks for i in b['inputs']]
    return {'artifact':'BODYGUARD_RU_E01_RENDER_BLOCK_PLAN_v0_2','status':'CANDIDATE_PENDING_TTD_TTS_AB','block_count':len(blocks),'blocks':blocks,'coverage':{'expected':len(src),'covered':len(covered),'unique':len(set(covered)),'ordered':covered==list(range(1,len(src)+1)),'pass':len(covered)==len(src)==len(set(covered)) and covered==list(range(1,len(src)+1))},'law':'TTD only candidate for contiguous same-domain conversation; clue/VO/media/performance-risk isolated.'}
if __name__=='__main__': print(json.dumps(compile_plan(sys.argv[1],sys.argv[2]),ensure_ascii=False,indent=2))
