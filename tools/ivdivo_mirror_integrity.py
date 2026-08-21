#!/usr/bin/env python3
"""IVDIVO GitHub<->Drive logical mirror integrity checker.

The checker compares explicit mirror manifests. It never chooses canon by mtime and
never assumes native Google Docs bytes equal Git blob bytes. Exact-byte mirrors may
opt into raw hash comparison; semantic mirrors compare declared frontier/status/
authority tokens and canonical content fingerprints.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

def _index(records):
    out, errors = {}, []
    for r in records:
        if not isinstance(r, dict) or not r.get("logical_id"):
            errors.append("INVALID_MIRROR_RECORD")
            continue
        lid = str(r["logical_id"])
        if lid in out:
            errors.append(f"DUPLICATE_LOGICAL_ID:{lid}")
        else:
            out[lid] = r
    return out, errors

def compare(payload: dict) -> dict:
    left = payload.get("github_records", [])
    right = payload.get("drive_records", [])
    if not isinstance(left, list) or not isinstance(right, list):
        return {"status":"FAIL_CLOSED","errors":["INVALID_RECORD_ARRAYS"],"items":[]}
    gh, errors = _index(left)
    dr, e2 = _index(right); errors += e2
    items=[]
    for lid in sorted(set(gh) | set(dr)):
        a, b = gh.get(lid), dr.get(lid)
        issues=[]
        if a is None:
            issues.append("MISSING_GITHUB_MIRROR")
        if b is None:
            issues.append("MISSING_DRIVE_MIRROR")
        if a is not None and b is not None:
            if a.get("authority_epoch") != b.get("authority_epoch"):
                issues.append("AUTHORITY_EPOCH_DIVERGENCE")
            if a.get("frontier_token") != b.get("frontier_token"):
                issues.append("FRONTIER_DIVERGENCE")
            if a.get("status_token") != b.get("status_token"):
                issues.append("STATUS_DIVERGENCE")
            mode = a.get("mirror_mode") or b.get("mirror_mode") or "SEMANTIC"
            if mode != (b.get("mirror_mode") or mode):
                issues.append("MIRROR_MODE_DIVERGENCE")
            if mode == "EXACT_BYTES":
                if not a.get("raw_sha256") or not b.get("raw_sha256"):
                    issues.append("RAW_HASH_REQUIRED")
                elif a.get("raw_sha256") != b.get("raw_sha256"):
                    issues.append("RAW_HASH_MISMATCH")
            else:
                fa, fb = a.get("content_fingerprint"), b.get("content_fingerprint")
                if fa and fb and fa != fb:
                    issues.append("SEMANTIC_FINGERPRINT_MISMATCH")
            # Revision/mtime are evidence of freshness, never authority selectors.
            if a.get("source_revision") and b.get("source_revision") and a.get("expected_peer_revision"):
                if a.get("expected_peer_revision") != b.get("source_revision"):
                    issues.append("EXPECTED_DRIVE_REVISION_STALE")
            if b.get("expected_peer_revision") and a.get("source_revision"):
                if b.get("expected_peer_revision") != a.get("source_revision"):
                    issues.append("EXPECTED_GITHUB_REVISION_STALE")
        item_status = "PASS" if not issues else "ISSUES_FOUND"
        items.append({"logical_id":lid,"status":item_status,"issues":issues})
    if errors:
        status="FAIL_CLOSED"
    elif any(i["status"]!="PASS" for i in items):
        status="ISSUES_FOUND"
    else:
        status="PASS"
    return {"status":status,"errors":errors,"items":items,
            "policy":"NEVER_SELECT_AUTHORITY_BY_MTIME; RECONCILE_USING_DECLARED_AUTHORITY_AND_FRONTIER"}

def main():
    p=argparse.ArgumentParser(); p.add_argument("input",type=Path); a=p.parse_args()
    try: payload=json.loads(a.input.read_text(encoding="utf-8"))
    except Exception as exc:
        print(json.dumps({"status":"FAIL_CLOSED","errors":[f"INPUT_ERROR:{exc}"]})); return 2
    out=compare(payload); print(json.dumps(out,indent=2,ensure_ascii=False,sort_keys=True))
    return 0 if out["status"] in {"PASS","ISSUES_FOUND"} else 1
if __name__=="__main__": raise SystemExit(main())
