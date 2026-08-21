#!/usr/bin/env python3
"""Build a durable AUTH_PROVIDER receipt after artifact write/readback.

The script never reads provider credentials. It consumes an already secret-free
snapshot twice: the source file and the copy read back from durable storage.
Both must independently satisfy ProviderSnapshotContract, have identical logical
snapshot hashes and identical file bytes. The resulting payload is validated by
the canonical external_evidence_trust AUTH_PROVIDER adapter before persistence.
"""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any
import argparse
import json

HERE = Path(__file__).resolve().parent
RUNTIME = HERE / "runtime"
import sys
for path in (HERE, RUNTIME):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from external_evidence_trust import validate_provider_auth_receipt
from provider_snapshot_contract import validate_provider_snapshot


def _load(path: str | Path) -> tuple[dict[str, Any], bytes]:
    raw = Path(path).read_bytes()
    return json.loads(raw.decode("utf-8")), raw


def _normalize_time(value: str) -> str:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("PROVIDER_RECEIPT_TIMEZONE_REQUIRED")
    return parsed.astimezone(timezone.utc).isoformat()


def build_provider_auth_receipt(
    snapshot_path: str | Path,
    readback_snapshot_path: str | Path,
    *,
    artifact_id: str,
    storage_provider: str,
    source_ref: str,
    written_at: str,
    transaction_id: str | None = None,
    artifact_digest: str | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    source, source_bytes = _load(snapshot_path)
    readback, readback_bytes = _load(readback_snapshot_path)
    source_validation = validate_provider_snapshot(
        source, expected_provider="elevenlabs", max_age_seconds=21600, now=now
    )
    readback_validation = validate_provider_snapshot(
        readback, expected_provider="elevenlabs", max_age_seconds=21600, now=now
    )
    if not source_validation.get("verified"):
        raise ValueError(f"SOURCE_PROVIDER_SNAPSHOT_INVALID:{source_validation.get('status')}")
    if not readback_validation.get("verified"):
        raise ValueError(f"READBACK_PROVIDER_SNAPSHOT_INVALID:{readback_validation.get('status')}")
    if source_validation["snapshot_hash"] != readback_validation["snapshot_hash"]:
        raise ValueError("PROVIDER_SNAPSHOT_LOGICAL_HASH_DRIFT")

    source_file_hash = sha256(source_bytes).hexdigest()
    readback_file_hash = sha256(readback_bytes).hexdigest()
    if source_file_hash != readback_file_hash:
        raise ValueError("PROVIDER_SNAPSHOT_FILE_HASH_DRIFT")

    logical_hash = source_validation["snapshot_hash"]
    readback_at = (now or datetime.now(timezone.utc)).astimezone(timezone.utc).isoformat()
    durable_receipt = {
        "artifact_id": artifact_id,
        "artifact_kind": "PROVIDER_SNAPSHOT",
        "storage_provider": storage_provider,
        "source_ref": source_ref,
        "content_hash": logical_hash,
        "size_bytes": len(readback_bytes),
        "written_at": _normalize_time(written_at),
        "readback_at": readback_at,
        "readback_hash": readback_validation["snapshot_hash"],
        "readback_strength": "CONTENT_HASH_VERIFIED",
        "transaction_id": transaction_id,
        "metadata": {
            "source_file_sha256": source_file_hash,
            "readback_file_sha256": readback_file_hash,
            "artifact_digest": artifact_digest,
            "provider": "elevenlabs",
        },
    }
    payload = {"snapshot": readback, "durable_receipt": durable_receipt}
    trust = validate_provider_auth_receipt(
        payload, expected_provider="elevenlabs", max_age_seconds=21600, now=now
    )
    if not trust.get("verified"):
        raise ValueError(f"AUTH_PROVIDER_RECEIPT_INVALID:{trust.get('status')}")
    payload["_ivdivo_validation"] = trust
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(prog="ivdivo-provider-snapshot-receipt")
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--readback-snapshot", required=True)
    parser.add_argument("--artifact-id", required=True)
    parser.add_argument("--storage-provider", required=True)
    parser.add_argument("--source-ref", required=True)
    parser.add_argument("--written-at", required=True)
    parser.add_argument("--transaction-id")
    parser.add_argument("--artifact-digest")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    payload = build_provider_auth_receipt(
        args.snapshot,
        args.readback_snapshot,
        artifact_id=args.artifact_id,
        storage_provider=args.storage_provider,
        source_ref=args.source_ref,
        written_at=args.written_at,
        transaction_id=args.transaction_id,
        artifact_digest=args.artifact_digest,
    )
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validation = payload["_ivdivo_validation"]
    print(json.dumps({
        "status": "PASS",
        "evidence_class": "AUTH_PROVIDER",
        "snapshot_hash": validation["snapshot_hash"],
        "readback_strength": validation["readback_strength"],
        "artifact": str(out),
    }, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
