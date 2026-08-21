#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, sys

EXPECTED_OCCURRENCES = 269
EXPECTED_TOKENS = 1494
FORBIDDEN_BRANCH_TERMS = [
    "Dr Adrian Mercer", "Nate Calder", "C-17", "THE LAMP AFTER 916",
]
LABELS = ["COMMENTATOR","ISLA","LEO","LEO — RECORDING","VIVIAN","SECURITY OFFICER","SECURITY OFFICER — PHONE"]

def episode_one(text):
    a = text.index("EPISODE 1 — THE CONFESSION")
    b = text.index("END OF EPISODE", a) + len("END OF EPISODE")
    return text[a:b]

def parse(e01):
    pat = re.compile(r'^(%s):\s*(.*)$' % '|'.join(map(re.escape, sorted(LABELS,key=len,reverse=True))))
    out=[]
    for ln,line in enumerate(e01.splitlines(),1):
        m=pat.match(line.strip())
        if m:
            out.append({"occurrence_id":len(out)+1,"source_line":ln,"speaker":m.group(1),"exact_text":m.group(2)})
    return out

def no_branch_fallback(text):
    hits=[t for t in FORBIDDEN_BRANCH_TERMS if t in text]
    if hits:
        raise AssertionError("FAIL_NO_BRANCH_FALLBACK: "+", ".join(hits))

def classify_diff(old, new):
    old_e,new_e=episode_one(old),episode_one(new)
    po,pn=parse(old_e),parse(new_e)
    if [(x["speaker"],x["exact_text"]) for x in po] != [(x["speaker"],x["exact_text"]) for x in pn]:
        return "PROSE_CHANGE_REQUIRES_AUTHORITY"
    if old_e != new_e:
        return "NON_SPOKEN_EPISODE_METADATA_OR_CUE_CHANGE"
    if old != new:
        return "NON_RECORDED_LEDGER_OR_OUTSIDE_E01_CHANGE"
    return "NO_CHANGE"

def main(path):
    raw=Path(path).read_bytes()
    text=raw.decode("utf-8-sig")
    e01=episode_one(text)
    no_branch_fallback(e01)
    rows=parse(e01)
    tokens=sum(len(r["exact_text"].split()) for r in rows)
    assert len(rows)==EXPECTED_OCCURRENCES, (len(rows),EXPECTED_OCCURRENCES)
    assert tokens==EXPECTED_TOKENS, (tokens,EXPECTED_TOKENS)
    assert all(not r["exact_text"].startswith(("SFX:","MUSIC:","SCENE ","CAST:")) for r in rows)
    print(json.dumps({"status":"PASS","occurrences":len(rows),"tokens":tokens,"source_sha256":hashlib.sha256(raw).hexdigest()},indent=2))

if __name__=="__main__":
    main(sys.argv[1])
