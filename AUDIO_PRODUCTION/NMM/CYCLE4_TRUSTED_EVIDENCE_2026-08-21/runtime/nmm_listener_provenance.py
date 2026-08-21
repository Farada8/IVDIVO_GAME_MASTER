"""Human-listening provenance validator. A record can prove declaration, not inner experience."""
from __future__ import annotations
import re
REQ=("listener_id","listener_declaration","captured_at","artifact_sha256","protocol_sha256","device","methodology","raw_response_hash")
def validate_human_record(rec:dict)->dict:
    missing=[k for k in REQ if not rec.get(k)]
    if missing: return {"gate":"FAIL","missing":missing,"evidence_class":"UNUSABLE"}
    if rec.get("listener_declaration") not in {"I_LISTENED_ONCE","I_LISTENED_AS_PROTOCOL_DIRECTED"}:
        return {"gate":"FAIL","reason":"INVALID_DECLARATION","evidence_class":"UNUSABLE"}
    if not re.fullmatch(r"[0-9a-f]{64}",str(rec.get("artifact_sha256"))):
        return {"gate":"FAIL","reason":"BAD_ARTIFACT_HASH","evidence_class":"UNUSABLE"}
    if not re.fullmatch(r"[0-9a-f]{64}",str(rec.get("protocol_sha256"))):
        return {"gate":"FAIL","reason":"BAD_PROTOCOL_HASH","evidence_class":"UNUSABLE"}
    return {"gate":"PROVENANCE_COMPLETE","evidence_class":"DECLARED_HUMAN_REVIEW",
            "law":"This proves a complete declared review record; it cannot independently prove subjective listening occurred."}
