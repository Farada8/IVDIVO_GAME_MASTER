from __future__ import annotations
import hashlib,re
SECRET_PATTERNS=[re.compile(r"sk-[A-Za-z0-9_-]{16,}"),re.compile(r"(?i)(api[_-]?key|password|secret)\s*[:=]\s*\S+")]
def sha(data:bytes): return hashlib.sha256(data).hexdigest()
def preflight(*,path:str,current:bytes,expected_hash:str,new:bytes,allowed_prefixes:list[str],irreversible=False,approval=False):
    if sha(current)!=expected_hash:return {"decision":"STOP","reason":"STALE_HASH"}
    if not any(path.startswith(p) for p in allowed_prefixes):return {"decision":"STOP","reason":"UNAUTHORIZED_PATH"}
    txt=new.decode("utf-8",errors="ignore")
    if any(p.search(txt) for p in SECRET_PATTERNS):return {"decision":"STOP","reason":"SECRET_SCAN_FAIL"}
    if current==new:return {"decision":"STOP","reason":"NO_EFFECT"}
    if irreversible and not approval:return {"decision":"STOP","reason":"APPROVAL_REQUIRED"}
    return {"decision":"ALLOW","new_hash":sha(new)}
def postflight(expected:bytes,readback:bytes):
    return {"status":"COMMITTED_VERIFIED" if expected==readback else "REPAIR_REQUIRED","expected_hash":sha(expected),"readback_hash":sha(readback)}
