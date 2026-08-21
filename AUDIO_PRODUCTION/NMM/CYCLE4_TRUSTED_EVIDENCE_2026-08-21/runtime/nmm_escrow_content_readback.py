"""Content-level escrow readback: locator presence alone is never persistence proof."""
from __future__ import annotations
import hashlib
from pathlib import Path

def sha256_file(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def verify_escrow(record:dict, materialized_path=None)->dict:
    if not record.get("locator") or not record.get("expected_sha256"):
        return {"gate":"FAIL","reason":"MISSING_LOCATOR_OR_HASH"}
    if materialized_path is None:
        return {"gate":"METADATA_ONLY","reason":"CONTENT_NOT_READ_BACK"}
    p=Path(materialized_path)
    if not p.exists(): return {"gate":"FAIL","reason":"READBACK_MISSING"}
    actual=sha256_file(p); ok=actual==record["expected_sha256"]
    return {"gate":"CONTENT_READBACK_PASS" if ok else "FAIL","actual_sha256":actual,"expected_sha256":record["expected_sha256"]}
