#!/usr/bin/env python3
import json,hashlib,sys

def h(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()
def check(req_path,line_map_path):
    req=json.load(open(req_path,encoding='utf-8'))['requests']
    lm=json.load(open(line_map_path,encoding='utf-8'))['lines']
    issues=[]
    if len(req)!=len(lm): issues.append({'issue':'COUNT','expected':len(req),'actual':len(lm)})
    for i,(s,t) in enumerate(zip(req,lm),1):
        if s['block_id']!=t['block_id']: issues.append({'line':i,'issue':'BLOCK_ID'})
        if s['exact_text']!=t['source_text_en']: issues.append({'line':i,'issue':'SOURCE_TEXT_DRIFT'})
        if h(s['exact_text'])!=s['exact_text_sha256']: issues.append({'line':i,'issue':'SOURCE_HASH_BAD'})
        if h(t['text_ru'])!=t['text_ru_sha256']: issues.append({'line':i,'issue':'TARGET_HASH_BAD'})
    return {'artifact':'SEMANTIC_STATIC_PREFLIGHT','expected':len(req),'mapped':len(lm),'issues':issues,'verdict':'PASS' if not issues else 'FAIL','note':'Static integrity cannot replace human semantic/native QA.'}
if __name__=='__main__': print(json.dumps(check(sys.argv[1],sys.argv[2]),ensure_ascii=False,indent=2))
