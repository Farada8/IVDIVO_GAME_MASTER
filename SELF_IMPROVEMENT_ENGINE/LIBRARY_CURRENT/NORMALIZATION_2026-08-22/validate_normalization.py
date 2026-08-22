#!/usr/bin/env python3
"""Fail-closed consistency checks for derived systems RAW normalization.

This validator checks persisted metadata/count relationships only. It does not have raw
copyrighted book bytes and therefore does not re-prove the SHA-256 values themselves.
"""
from __future__ import annotations
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / "RAW_MANIFEST_35.json").read_text(encoding="utf-8"))
dedup = json.loads((ROOT / "BYTE_DEDUP_AND_QUARANTINE.json").read_text(encoding="utf-8"))
canon = json.loads((ROOT / "CANONICAL_WORK_MAP.json").read_text(encoding="utf-8"))
proof = json.loads((ROOT / "NORMALIZATION_PROOF.json").read_text(encoding="utf-8"))

entries = manifest["entries"]
assert len(entries) == 35
assert len({e["drive_id"] for e in entries}) == 35
assert all(len(e["sha256"]) == 64 for e in entries)

valid = [e for e in entries if e["integrity"].startswith("VALID")]
quar = [e for e in entries if e["integrity"].startswith("QUARANTINE")]
assert len(valid) == 26
assert len(quar) == 9

hash_counts = Counter(e["sha256"] for e in entries)
assert len(hash_counts) == 30
assert sum(1 for n in hash_counts.values() if n > 1) == 2
assert len({e["sha256"] for e in valid}) == 26
assert len({e["sha256"] for e in quar}) == 4

assert dedup["summary"]["exact_duplicate_groups"] == 2
assert set(dedup["quarantine_drive_ids"]) == {e["drive_id"] for e in quar}
for group in dedup["exact_duplicate_groups"]:
    assert len(group["drive_ids"]) > 1
    for drive_id in group["drive_ids"]:
        item = next(e for e in entries if e["drive_id"] == drive_id)
        assert item["sha256"] == group["sha256"]
        assert item["integrity"].startswith("QUARANTINE")

canonical_valid = [e["canonical"] for e in valid]
assert all(canonical_valid)
assert len(set(canonical_valid)) == 24
assert canon["counts"]["resolved_canonical_works"] == 24
assert canon["counts"]["resolved_work_families"] == 23
assert canon["counts"]["unresolved_valid_entries"] == 0

checks = {c["gate"]: c["result"] for c in proof["checks"]}
for gate in ["N09_MANIFEST_COVERAGE","N10_HASH_COVERAGE","N11_EXACT_DUPLICATE_DETECTION","N12_QUARANTINE","N13_CANONICAL_ALIAS_MAP","N14_SOURCE_PASSPORTS","N15_CONCENTRATION_RISK"]:
    assert checks[gate].startswith("PASS"), (gate, checks[gate])
assert checks["N16_CURRENT_REGISTRY_UPDATE"].startswith("PENDING")
assert proof["raw_copyrighted_bytes_published_to_github"] is False

print("SYSTEMS_RAW_NORMALIZATION_INTERNAL_CONSISTENCY_PASS")
print("35 physical / 26 valid / 9 quarantine / 30 hashes / 24 works / 23 families")
