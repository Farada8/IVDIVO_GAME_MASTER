# IVDIVO — FULL CHAT TRANSCRIPT RECOVERY — RUNTIME VERIFICATION

**Date:** 2026-08-21  
**Authority:** `IVDIVO_NARRATIVE_OS/18B_FULL_CHAT_TRANSCRIPT_RECOVERY_AND_INGESTION_PROTOCOL_v1.0.md`  
**Implementation:** `tools/ivdivo_transcript_recovery.py`  
**Schema:** `schemas/IVDIVO_TRANSCRIPT_RECOVERY_LEDGER_SCHEMA_v1.json`  
**Tests:** `tests/test_transcript_recovery.py`

## Verification result

The deterministic first-pass transcript-recovery implementation was tested before GitHub integration and then verified by exact Git blob identity after merge.

- local pytest smoke: **5 passed / 0 failed**;
- tested tool Git-blob SHA: `79b9cd9f9b8e60f65a7ec156dc23689a194233a6`;
- GitHub `main` readback tool Git-blob SHA: `79b9cd9f9b8e60f65a7ec156dc23689a194233a6`;
- identity result: **MATCH**;
- integration PR: **#59**;
- PR result: **MERGED**;
- merge commit: `1e3bd068771135f8f1bf470269f2e9243af8f797`.

## Tested contracts

1. secrets such as API credentials are redacted before ledger excerpts are persisted;
2. Founder/user directive candidates are extracted separately from assistant/model claims;
3. assistant/model claims such as `saved`, `locked`, `PASS`, `verified` remain `UNVERIFIED`;
4. artifact references are extracted into a persisted-source verification queue;
5. full-file processing sets `final_tail_processed=true` and records source SHA-256;
6. recovered system-improvement material begins as `DISCOVERY_ONLY`, not automatic CURRENT/CANON;
7. generated ledgers remain `EXTRACTED_UNVERIFIED` and `ingestion_complete=false` until semantic reconciliation, persisted-source verification, disposition and readback occur.

## Scope boundary

This utility is a deterministic **first-pass extractor**, not a replacement for AI/editorial reconciliation. It does not:
- decide canon;
- verify Google Drive or GitHub claims by itself;
- promote a chat-only artifact;
- certify Human Signal, provider execution or market evidence;
- mark a recovery `INGESTION_COMPLETE`.

Those stages remain governed by 18B + current Cross-Conversation Autopilot + Self-Improvement v2.

## Packaging status

The implementation is **VERIFIED_CURRENT on GitHub main as a post-v11.2 extension**. It is **not retroactively claimed to exist inside `IVDIVO_ENGINE_v11_2_CONTINUOUS_EXECUTION_CURRENT.zip`**. Inclusion in the next engine ZIP requires a new full-package regression before the package can be promoted.

## Concurrency evidence

Direct fast-forward writes to `main` repeatedly failed while sibling dialogs were advancing the repository. The integration therefore switched to a dedicated branch + PR and merged without force overwrite. This is additional production evidence for the existing `CONCURRENT_DIALOG_REBASE / STALE_WORK_GATE` law.
