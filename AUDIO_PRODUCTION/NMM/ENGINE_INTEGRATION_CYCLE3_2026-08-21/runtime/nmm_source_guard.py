from __future__ import annotations
import hashlib,json,re
from pathlib import Path
LABELS=["COMMENTATOR","ISLA","LEO","LEO — RECORDING","VIVIAN","SECURITY OFFICER","SECURITY OFFICER — PHONE"]
FORBIDDEN=["Dr Adrian Mercer","Nate Calder","C-17","THE LAMP AFTER 916"]
EXPECTED_OCC=269; EXPECTED_TOKENS=1494

def episode1(text):
 a=text.index("EPISODE 1 — THE CONFESSION"); b=text.index("END OF EPISODE",a)+len("END OF EPISODE"); return text[a:b]
def parse(e01):
 pat=re.compile(r'^(%s):\s*(.*)$' % '|'.join(map(re.escape,sorted(LABELS,key=len,reverse=True))))
 out=[]
 for ln,line in enumerate(e01.splitlines(),1):
  m=pat.match(line.strip())
  if m: out.append({"occurrence_id":len(out)+1,"source_line":ln,"speaker":m.group(1),"exact_text":m.group(2)})
 return out
def fingerprint(path):
 raw=Path(path).read_bytes(); txt=raw.decode('utf-8-sig'); e=episode1(txt); rows=parse(e)
 hits=[x for x in FORBIDDEN if x in e]
 return {"source_sha256":hashlib.sha256(raw).hexdigest(),"e01_sha256":hashlib.sha256(e.encode()).hexdigest(),"ledger_sha256":hashlib.sha256(json.dumps(rows,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest(),"occurrences":len(rows),"tokens":sum(len(x['exact_text'].split()) for x in rows),"forbidden_hits":hits}
def gate(path,expected):
 got=fingerprint(path); fails=[]
 for k in ["source_sha256","e01_sha256","ledger_sha256","occurrences","tokens"]:
  if expected.get(k)!=got.get(k): fails.append(k)
 if got['forbidden_hits']: fails.append('forbidden_hits')
 return {"gate":"PASS" if not fails else "FAIL","fails":fails,"got":got,"expected":expected}
