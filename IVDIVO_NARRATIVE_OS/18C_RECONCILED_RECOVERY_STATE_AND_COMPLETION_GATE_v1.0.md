# IVDIVO — RECONCILED RECOVERY STATE + COMPLETION GATE v1.0

**Status:** WORKING CANDIDATE — SI-0009  
**Date:** 2026-08-21  
**Parents:** Founder directive -> 18B Full Chat Transcript Recovery -> Self-Improvement v2 -> 32-Prompt Transcript Recovery Sprint  
**Machine schema:** `schemas/IVDIVO_RECONCILED_RECOVERY_STATE_SCHEMA_v2.json`  
**Gate tool:** `tools/ivdivo_recovery_completion_gate.py`

## PURPOSE

Close the gap between deterministic first-pass transcript extraction and safe normal production continuation.

The current v1 extractor intentionally outputs `EXTRACTED_UNVERIFIED`. It must remain unable to decide canon, verify Drive/GitHub claims by itself, or mark recovery complete.

This contract defines the downstream semantic/project-aware state:

`RAW TRANSCRIPT -> EXTRACT LEDGER v1 -> RECONCILED RECOVERY STATE v2 -> PERSISTENCE VERIFICATION -> WRITE/READBACK -> RECOVERY COMPLETE GATE -> NORMAL NEXT-ACTION RESOLVER`.

## PRIMARY SEPARATION

Never collapse these concepts:

`EXTRACTION CONFIDENCE != SOURCE AUTHORITY != PERSISTENCE VERIFICATION != CANON/LOCK STATUS`.

A highly confident parser extraction of an assistant sentence saying “I locked the book” remains an assistant claim. A direct Founder statement recovered from transcript has Founder-source authority, but current persisted project state must still be reconciled for chronology/supersession before the system mutates current pointers.

## STATE LAYERS

### 1. Source identity
Store source SHA-256, byte size when known, completeness class, completeness basis, supplied-input tail processing and chunk lineage.

`input_tail_processed=true` means only that the supplied recovery corpus was fully processed. It does not prove that the old conversation export itself was complete.

### 2. Authority reconstruction
Distinguish direct Founder directives from assistant/model paraphrases. Preserve chronology. Any unresolved contradiction that materially changes canon/branch/lock/priority is `AUTHORITY_UNRESOLVED`.

### 3. Project partitions
One transcript may contain multiple books, audio projects, tooling lines or research tracks. Each gets its own partition with artifact claims, chat-only candidates and reconstructed frontier. No project-specific material crosses partitions without explicit reuse/universalization classification.

### 4. Persistence verification
Every material `saved / updated / created / PASS / LOCK / FINAL / rendered / human approved / market validated` claim becomes a verification task with the correct evidence class and store.

Evidence examples:
- Founder lock -> direct Founder decision evidence;
- story gate PASS -> gate artifact/result;
- automated test PASS -> exact source/command/test evidence;
- provider render -> real provider/output artifact;
- human signal -> actual human reader/listener/editor evidence;
- market validation -> real market/platform evidence.

Filename language or assistant prose never satisfies an evidence contract.

### 5. Chat-only candidate recovery
Substantial unsaved work may be persisted as a candidate with provenance/content fingerprint. Missing sections remain UNKNOWN. Candidate persistence is not canon promotion.

### 6. Frontier reconstruction
Per project:

`LAST VERIFIED COMPLETED ARTIFACT + CURRENT AUTHORITY + PASSED GATES + OPEN BLOCKERS + DO_NOT_REPEAT + NEXT LEGAL ACTION`.

The last sentence of a transcript is not the frontier.

### 7. Write-through/readback
All recovery writes carry a `recovery_id` and target. Current pointers are not considered changed safely until accepted writes are read back. Failed/partial writes move recovery to repair state rather than silent success.

### 8. Learning harvest
Reusable mechanisms may enter Improvement Registry / Learning Ledger through normal lifecycle. Project-specific plot/canon/voice/clue material does not become universal merely because it was recovered.

## LARGE-CORPUS RESUME CONTRACT

For bounded semantic processing, each chunk records:
- `source_sha256`;
- `chunk_id`;
- byte/line/turn range;
- overlap hash where used;
- findings hash;
- processed time;
- whether supplied-input tail is contained in the chunk.

If source SHA changes, previous checkpoints cannot silently resume against the new corpus.

## COMPLETION GATE

`INGESTION_COMPLETE` is legal only when:
1. supplied input tail was processed;
2. all material items have disposition;
3. all material persistence claims are terminally checked/dispositioned;
4. no material unknown remains;
5. no unresolved material conflict remains;
6. authority is unambiguous for the active frontier;
7. every project frontier is fresh;
8. accepted writes are read back;
9. no secret was persisted;
10. exact next action/blocker is identified.

Completion does **not** imply the next production action is automatically executable. It only permits handoff to the normal next-action resolver.

`can_auto_continue=true` is legal only when the recovered next action itself does not require a new Founder choice, human evidence, unavailable provider or unavailable execution environment. The normal action resolver remains the final execution gate.

## FAILURE STATES

- `EXTRACTED_UNVERIFIED` — first-pass only; no state-changing continuation.
- `RECONCILING` — semantic/persistence reconciliation in progress.
- `PARTIAL_WRITE_REPAIR_REQUIRED` — some write-through occurred but recovery is not safely complete.
- `FAIL_CLOSED` — authority/safety/integrity failure prevents continuation.
- `INGESTION_COMPLETE` — recovery layer complete; eligible for next-action resolver.

## IDEMPOTENCE LAW

Rerunning the same source should not create duplicate candidates or repeat already verified write-through. Use source hash + project/artifact identity + content fingerprint/recovery lineage to detect duplicate recovery work.

## FOUNDER QUESTION LAW

Ask the Founder only for a real irreducible choice:
- conflicting high-authority directives;
- missing exact information that materially changes canon;
- equally authorized competing creative branches;
- irreversible external action/approval.

Do not ask the Founder to locate files, repeat known state, classify obvious duplicates or resolve ordinary persistence checks that available tools can determine.

**ASK ONLY FOR REAL CHOICE, NOT RECOVERABLE STATE.**

## EVIDENCE BOUNDARY

Automated recovery tests prove machine contracts only. They do not prove literary quality, human comprehension, provider execution, market performance or canon correctness.

## PROMOTION GATE

This candidate may become CURRENT only after:
- schema/gate-tool tests pass;
- adversarial recovery fixtures pass;
- next-action integration is regression-safe;
- first real large pasted-corpus pilot produces no false authority promotion, no secret persistence and a correct reconciled frontier;
- application/readback and package regression are complete where applicable.

Until then, v1 extractor + 18B remain the verified CURRENT first-pass layer and this v2 reconciliation contract is a WORKING candidate.
