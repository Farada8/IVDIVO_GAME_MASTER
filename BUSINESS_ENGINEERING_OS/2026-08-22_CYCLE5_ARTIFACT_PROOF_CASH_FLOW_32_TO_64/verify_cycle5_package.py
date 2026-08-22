from pathlib import Path
import json, re
r=Path(__file__).parent
ledger=(r/'02_RUN32_P65_P96_EXECUTION_LEDGER.md').read_text()
next64=(r/'07_NEXT64_P97_P160.md').read_text()
contracts=(r/'contracts'/'CONTRACTS_C153_C184.md').read_text()
assert len(re.findall(r'^\| P(?:6[5-9]|[7-8][0-9]|9[0-6]) \|', ledger, re.M)) == 32
assert len(re.findall(r'^P(?:9[7-9]|1[0-5][0-9]|160)\.', next64, re.M)) == 64
assert len(re.findall(r'^C(?:15[3-9]|1[6-7][0-9]|18[0-4]) `', contracts, re.M)) == 32
for p in r.rglob('*.json'):
    json.load(open(p,encoding='utf-8'))
for name in ['OP01_TENDER_DECISION_BRIEF_SAMPLE.md','OP03_RETROFIT_QUALIFICATION_PACK_SAMPLE.md','OP19_AI_WORKFLOW_DIAGNOSTIC_SAMPLE.md']:
    assert (r/'artifacts'/name).exists()
print('PACKAGE_STRUCTURE_PASS: run32=32 next64=64 contracts=32 json=valid artifacts=3')
