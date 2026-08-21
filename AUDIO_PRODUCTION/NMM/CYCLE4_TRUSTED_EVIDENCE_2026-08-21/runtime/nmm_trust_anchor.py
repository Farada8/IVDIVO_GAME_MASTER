"""NMM trusted-evidence anchors. Integrity is not external truth."""
from __future__ import annotations
import hashlib
from pathlib import Path

EXTERNAL_CLASSES={"AUTHENTICATED_PROVIDER","HEARD_HUMAN","QUALIFIED_SPECIALIST","MEASURED_ECONOMICS"}

def sha256_bytes(data: bytes)->str: return hashlib.sha256(data).hexdigest()
def sha256_file(path)->str: return sha256_bytes(Path(path).read_bytes())

def classify_anchor(record: dict)->dict:
    evidence_class=str(record.get("evidence_class","INTERNAL_ENGINEERING"))
    integrity=bool(record.get("artifact_sha256")) and bool(record.get("protocol_sha256"))
    provenance=all(record.get(k) for k in ("captured_at","producer_declaration"))
    external=evidence_class in EXTERNAL_CLASSES
    authenticated = bool(record.get("authenticated_source")) if evidence_class=="AUTHENTICATED_PROVIDER" else True
    gate="EXTERNAL_TRUTH_ELIGIBLE" if integrity and provenance and external and authenticated else "INTERNAL_ONLY"
    return {"integrity":integrity,"provenance_complete":provenance,"external_class":external,"authenticated":authenticated,"gate":gate,
            "law":"Hash integrity proves identity/integrity only; it never proves an external event occurred."}

def verify_artifact(path, expected_sha256): return sha256_file(path)==expected_sha256
