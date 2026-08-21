from __future__ import annotations
import hashlib

CURRENT_ROLES = {"ISLA_GRANT", "LEO_HART", "VIVIAN_CROSS"}

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def source_revision_gate(*, expected_revision: str, observed_revision: str, expected_slice_sha: str, observed_slice_sha: str) -> dict:
    if observed_revision != expected_revision:
        return {"status":"REEXPORT_REQUIRED","reason":"SOURCE_REVISION_DRIFT"}
    if observed_slice_sha != expected_slice_sha:
        return {"status":"FAIL_CLOSED","reason":"SOURCE_SLICE_HASH_DRIFT"}
    return {"status":"PASS","revision":observed_revision,"slice_sha256":observed_slice_sha}

def bind_exact_line(*, role: str, exact_text: str, authoritative_excerpt: str, source_locator: str, source_slice_sha256: str) -> dict:
    if role not in CURRENT_ROLES:
        return {"status":"STALE_ROLE_BINDING","role":role,"current_roles":sorted(CURRENT_ROLES)}
    if not exact_text or exact_text not in authoritative_excerpt:
        return {"status":"FAIL_CLOSED","reason":"EXACT_TEXT_NOT_IN_AUTHORITY","role":role}
    return {"status":"PASS","role":role,"exact_text":exact_text,"line_sha256":sha256_text(exact_text),"source_locator":source_locator,"source_slice_sha256":source_slice_sha256,"text_lock":True}
