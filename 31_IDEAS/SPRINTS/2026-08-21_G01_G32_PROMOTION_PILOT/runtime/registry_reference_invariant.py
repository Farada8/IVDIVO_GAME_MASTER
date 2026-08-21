#!/usr/bin/env python3
import json,sys
registry=json.load(open(sys.argv[1],encoding='utf-8'))
refs=json.load(open(sys.argv[2],encoding='utf-8'))
ids=[c['candidate_id'] for c in registry['candidates']]
errors=[]
for candidate_id in refs['referenced_candidates']:
    if ids.count(candidate_id)!=1:
        errors.append(f'{candidate_id}:COUNT={ids.count(candidate_id)}')
for c in registry['candidates']:
    if c.get('status')=='VERIFIED_CURRENT' and not c.get('verification_evidence'):
        errors.append(f"{c['candidate_id']}:VERIFIED_WITHOUT_EVIDENCE")
print('PASS' if not errors else 'FAIL',errors)
raise SystemExit(1 if errors else 0)
