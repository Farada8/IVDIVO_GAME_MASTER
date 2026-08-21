import sys
import unittest
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))

from external_evidence_trust import DurableArtifactReceipt, ReadbackStrength, TransactionRecoveryReceipt
from live_lineage_escrow import (
    compile_exact_escrow,
    compile_lineage,
    compile_recovery_proof,
    lineage_recovery_hashes,
    verify_escrow,
    verify_lineage,
)
from provider_snapshot_contract import SCHEMA_VERSION, seal_snapshot


class LiveLineageEscrowTests(unittest.TestCase):
    SOURCE = sha256(b"source").hexdigest()

    @staticmethod
    def h(value: str) -> str:
        return sha256(value.encode("utf-8")).hexdigest()

    def durable(self, *, kind, content_hash, tx, metadata=None, artifact_id=None):
        return DurableArtifactReceipt(
            artifact_id=artifact_id or f"{kind}-{content_hash[:8]}",
            artifact_kind=kind,
            storage_provider="GOOGLE_DRIVE",
            source_ref=f"gdrive://{kind.lower()}/{content_hash[:10]}",
            content_hash=content_hash,
            size_bytes=256,
            written_at="2026-08-21T17:45:00+00:00",
            readback_at="2026-08-21T17:46:00+00:00",
            readback_hash=content_hash,
            readback_strength=ReadbackStrength.CONTENT_HASH_VERIFIED.value,
            transaction_id=tx,
            metadata=metadata or {},
        )

    def provider_payload(self, block_id):
        snapshot = seal_snapshot({
            "schema_version": SCHEMA_VERSION,
            "provider": "generic-provider",
            "status": "PASS",
            "authentication": {
                "state": "AUTHENTICATED",
                "method": "RUNTIME_AUTH",
                "credential_persisted": False,
            },
            "provenance": {
                "captured_at": "2026-08-21T17:30:00+00:00",
                "capture_method": "DIRECT_AUTHENTICATED_READ_ONLY_API",
                "capture_engine": "test-provider-acquirer/1.0",
                "source": [{"path": "/capabilities", "http_status": 200}],
            },
            "account": {"fingerprint_sha256": self.h("account")},
            "voices": {"v1": {"name": "Voice"}},
            "models": {"m1": {"name": "Model"}},
        })
        durable = self.durable(
            kind="PROVIDER_SNAPSHOT",
            content_hash=snapshot["snapshot_hash"],
            tx=f"SNAP-{block_id}",
        )
        return {"snapshot": snapshot, "durable_receipt": durable}

    def lineage(self, block_id="RB001", request_hash=None, state="ACCEPTED", *, response_binding_override=None):
        request_hash = request_hash or self.h(f"request:{block_id}")
        tx = f"TX-{block_id}"
        result_hash = self.h(f"provider-result:{block_id}:{state}")
        request_receipt = self.durable(
            kind="PROVIDER_REQUEST",
            content_hash=request_hash,
            tx=tx,
            metadata={
                "project_id": "P1",
                "block_id": block_id,
                "request_hash": request_hash,
                "source_hash": self.SOURCE,
            },
        )
        result_meta = {
            "block_id": block_id,
            "request_hash": request_hash,
            "provider_state": state,
        }
        if state == "ACCEPTED":
            result_meta["provider_request_id"] = f"provider://{block_id}"
        result_receipt = self.durable(
            kind="PROVIDER_RESULT",
            content_hash=result_hash,
            tx=tx,
            metadata=result_meta,
        )
        spend_meta = {
            "block_id": block_id,
            "request_hash": request_hash,
            "provider_state": state,
        }
        if state == "ACCEPTED":
            spend_meta["charge_ref"] = f"charge://{block_id}"
        spend_receipt = self.durable(
            kind="SPEND_LEDGER_ENTRY",
            content_hash=self.h(f"spend:{block_id}:{state}"),
            tx=tx,
            metadata=spend_meta,
        )
        live_receipt = None
        alignment_receipt = None
        if state == "ACCEPTED":
            audio_hash = self.h(f"audio:{block_id}")
            live_receipt = self.durable(
                kind="RAW_AUDIO",
                content_hash=audio_hash,
                tx=tx,
                metadata={
                    "project_id": "P1",
                    "request_hash": request_hash,
                    "provider_response_hash": response_binding_override or result_hash,
                },
            )
            alignment_receipt = self.durable(
                kind="ALIGNMENT",
                content_hash=self.h(f"alignment:{block_id}"),
                tx=tx,
                metadata={
                    "audio_hash": audio_hash,
                    "source_hash": self.SOURCE,
                    "coverage_complete": True,
                },
            )
        return compile_lineage({
            "project_id": "P1",
            "episode_id": "CANARY",
            "block_id": block_id,
            "source_hash": self.SOURCE,
            "request_hash": request_hash,
            "provider": "generic-provider",
            "provider_state": state,
            "dispatch_at": "2026-08-21T18:00:00+00:00",
            "provider_auth_receipt": self.provider_payload(block_id),
            "request_receipt": request_receipt,
            "provider_result_receipt": result_receipt,
            "spend_receipt": spend_receipt,
            "live_audio_receipt": live_receipt,
            "alignment_receipt": alignment_receipt,
        })

    def exact_rows(self):
        return [self.lineage("RB001"), self.lineage("RB002"), self.lineage("RB003")]

    def expected_hashes(self):
        return {block: self.h(f"request:{block}") for block in ("RB001", "RB002", "RB003")}

    def recovery(self, lineage, *, omit_hash=None, duplicate_charges=0):
        hashes = [value for value in lineage_recovery_hashes(lineage) if value != omit_hash]
        return TransactionRecoveryReceipt(
            transaction_id=lineage["transaction_id"],
            recovered_at="2026-08-21T18:30:00+00:00",
            recovered_content_hashes=hashes,
            durable_readback_strength=ReadbackStrength.TRANSACTION_RECOVERABLE.value,
            duplicate_provider_calls=0,
            duplicate_charges=duplicate_charges,
            unresolved_ambiguities=0,
            recovery_manifest_ref=f"gdrive://recovery/{lineage['block_id']}",
            recovery_manifest_hash=self.h(f"recovery:{lineage['block_id']}"),
            synthetic_fixture=False,
        )

    def test_accepted_lineage_is_receipt_bound_but_not_take_accepted(self):
        row = self.lineage()
        self.assertEqual(verify_lineage(row)["status"], "PASS")
        self.assertEqual(row["provider_state"], "ACCEPTED")
        self.assertEqual(row["production_take_status"], "NOT_ACCEPTED")
        self.assertFalse(row["take_lock"])
        self.assertFalse(row["machine_may_replay_paid_request"])

    def test_bare_provider_verified_flag_cannot_enter_lineage(self):
        block = "RB001"
        request_hash = self.h(f"request:{block}")
        tx = f"TX-{block}"
        with self.assertRaisesRegex(ValueError, "PROVIDER_AUTH_RECEIPT_INVALID"):
            compile_lineage({
                "project_id": "P1", "episode_id": "CANARY", "block_id": block,
                "source_hash": self.SOURCE, "request_hash": request_hash,
                "provider": "generic-provider", "provider_state": "AMBIGUOUS",
                "dispatch_at": "2026-08-21T18:00:00+00:00",
                "provider_auth_receipt": {"verified": True},
                "request_receipt": self.durable(kind="PROVIDER_REQUEST", content_hash=request_hash, tx=tx,
                    metadata={"project_id": "P1", "block_id": block, "request_hash": request_hash, "source_hash": self.SOURCE}),
                "provider_result_receipt": self.durable(kind="PROVIDER_RESULT", content_hash=self.h("result"), tx=tx,
                    metadata={"block_id": block, "request_hash": request_hash, "provider_state": "AMBIGUOUS"}),
                "spend_receipt": self.durable(kind="SPEND_LEDGER_ENTRY", content_hash=self.h("spend"), tx=tx,
                    metadata={"block_id": block, "request_hash": request_hash, "provider_state": "AMBIGUOUS"}),
            })

    def test_audio_must_bind_exact_provider_result_hash(self):
        with self.assertRaisesRegex(ValueError, "LIVE_AUDIO_PROVIDER_RESULT_BINDING_MISMATCH"):
            self.lineage(response_binding_override=self.h("wrong-provider-result"))

    def test_exact_three_lineages_pass(self):
        escrow = compile_exact_escrow(
            self.exact_rows(),
            expected_block_ids=["RB001", "RB002", "RB003"],
            expected_source_hash=self.SOURCE,
            expected_request_hashes=self.expected_hashes(),
        )
        self.assertEqual(escrow["status"], "PASS_EXACT_ESCROW")
        self.assertEqual(verify_escrow(escrow)["status"], "PASS")
        self.assertFalse(escrow["auto_retry_allowed"])

    def test_unknown_fourth_and_duplicate_request_fail_closed(self):
        rows = self.exact_rows() + [self.lineage("RB004")]
        escrow = compile_exact_escrow(
            rows,
            expected_block_ids=["RB001", "RB002", "RB003"],
            expected_source_hash=self.SOURCE,
        )
        self.assertEqual(escrow["status"], "HOLD")
        self.assertEqual(escrow["issues"]["unknown_block_ids"], ["RB004"])

        dup = [self.lineage("RB001"), self.lineage("RB002", request_hash=self.h("request:RB001")), self.lineage("RB003")]
        escrow2 = compile_exact_escrow(
            dup,
            expected_block_ids=["RB001", "RB002", "RB003"],
            expected_source_hash=self.SOURCE,
        )
        self.assertEqual(escrow2["status"], "HOLD")
        self.assertEqual(escrow2["issues"]["duplicate_request_hashes"], [self.h("request:RB001")])

    def test_ambiguous_lineage_keeps_exact_escrow_on_hold(self):
        rows = [self.lineage("RB001"), self.lineage("RB002", state="AMBIGUOUS"), self.lineage("RB003")]
        escrow = compile_exact_escrow(
            rows,
            expected_block_ids=["RB001", "RB002", "RB003"],
            expected_source_hash=self.SOURCE,
        )
        self.assertEqual(escrow["status"], "HOLD")
        self.assertEqual(escrow["issues"]["nonaccepted_block_ids"], ["RB002"])
        self.assertFalse(escrow["machine_may_replay_paid_request"])

    def test_recovery_requires_transaction_recoverable_hash_coverage(self):
        rows = self.exact_rows()
        escrow = compile_exact_escrow(
            rows,
            expected_block_ids=["RB001", "RB002", "RB003"],
            expected_source_hash=self.SOURCE,
            expected_request_hashes=self.expected_hashes(),
        )
        receipts = [self.recovery(row) for row in rows]
        good = compile_recovery_proof(escrow, receipts)
        self.assertEqual(good["status"], "PASS_TRANSACTION_RECOVERABLE")
        self.assertFalse(good["auto_replay_provider"])

        missing_hash = lineage_recovery_hashes(rows[1])[0]
        bad_receipts = [self.recovery(rows[0]), self.recovery(rows[1], omit_hash=missing_hash), self.recovery(rows[2])]
        bad = compile_recovery_proof(escrow, bad_receipts)
        self.assertEqual(bad["status"], "HOLD")
        self.assertIn(rows[1]["transaction_id"], bad["issues"]["uncovered_content_hashes"])

    def test_recovery_receipt_with_duplicate_charge_is_not_accepted(self):
        rows = self.exact_rows()
        escrow = compile_exact_escrow(
            rows,
            expected_block_ids=["RB001", "RB002", "RB003"],
            expected_source_hash=self.SOURCE,
        )
        receipts = [self.recovery(rows[0]), self.recovery(rows[1], duplicate_charges=1), self.recovery(rows[2])]
        out = compile_recovery_proof(escrow, receipts)
        self.assertEqual(out["status"], "HOLD")
        self.assertEqual(out["issues"]["invalid_transaction_receipts"], [rows[1]["transaction_id"]])


if __name__ == "__main__":
    unittest.main()
