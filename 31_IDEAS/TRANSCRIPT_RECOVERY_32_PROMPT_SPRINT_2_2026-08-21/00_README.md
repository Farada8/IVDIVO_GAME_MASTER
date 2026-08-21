# IVDIVO — FULL CHAT RECOVERY 32-PROMPT SPRINT 2 — 2026-08-21

**Status:** EXECUTED R&D / SELF-IMPROVEMENT INPUT — NOT STORY CANON AND NOT AUTOMATIC CURRENT ENGINE AUTHORITY.

## Purpose

Second-cycle 32-prompt pass on abrupt-chat/full-transcript recovery. This sprint does **not** repeat the first 32→64 pass. It rebases against the verified 18B protocol + v1 extractor, current Self-Improvement v2, registry-family architecture, SI-0009 / draft PR #67, parser-hardening candidate work, and the sibling whole-system PR #68.

## Core question

How do we move from safe first-pass extraction to reliable semantic recovery that can verify persisted claims, separate projects, reconstruct the real frontier, persist chat-only work transactionally, update learning, and only then hand control back to the normal next-action resolver?

## GitHub files

- `01_PROMPTS_N01_N32.md` — 32 prompts executed sequentially.
- `02_EXECUTION_RESULTS_N01_N32.md` — result/disposition of every prompt.
- `03_SYNTHESIS_AND_UPGRADE_DECISIONS.md` — integrated analysis and promotion boundaries.
- `04_NEXT_64_PROMPTS_v2.md` — exactly 64 next-generation prompts derived from the second-cycle findings.
- `05_MACHINE_CONTRACTS_OR_SCHEMAS.json` — compact candidate contracts extracted from the sprint.
- `06_SPRINT_STATE.json` — machine-readable sprint state/counts/frontier.

## Google Drive mirror

Folder: `IVDIVO — FULL CHAT RECOVERY 32-PROMPT SPRINT 2 — 2026-08-21`  
Folder ID: `1CT1zgdpDqw6X4mOO2tk_7A_yhaRrTwkH`

Files:
- `00_MASTER — TRANSCRIPT RECOVERY SPRINT 2 — 32 EXECUTED + SYNTHESIS v1.0` — `1aqWMj9oejsoGBapII06L1Wy0JfuXsRCbKiehW3HSsqw`
- `01_PROMPTS — TRANSCRIPT RECOVERY SPRINT 2 — N01-N32 v1.0` — `1K_2W-yScEd9a8Bi_lc0XFG0b_nj52rsbuvZq5BbngEg`
- `02_NEXT 64 PROMPTS — TRANSCRIPT RECOVERY SPRINT 2 v2` — `1nny6HmvCHc0LUibZf7hb_fILLBj4X5hareOkVFmCaDs`
- `03_MACHINE CONTRACTS + SPRINT STATE — TRANSCRIPT RECOVERY SPRINT 2 v1.0` — `18YcVXupeVa5GKqEGv8Ad_1TqDcxxeHlgUNi8p_fhiO4`

## Self-Improvement write-through

The sprint generated three explicit registry-family candidates rather than leaving conclusions only in prose:
- `SI-0009_RECONCILED_RECOVERY_STATE_V2.json` — READY_FOR_PILOT; PR #67 remains candidate/not CURRENT.
- `SI-0010_REGISTRY_SHARD_COMPACTION_TRANSACTION.json` — DEVELOPING.
- `SI-0011_REAL_CORPUS_RECOVERY_ADVERSARIAL_PILOT.json` — READY_FOR_PILOT.

`CURRENT_IMPROVEMENT_REGISTRY_FAMILY.json` was updated to schema 1.1 to route SI-0008…SI-0011. Visibility in the registry family is **not** promotion to CURRENT authority.

## Governing truth boundary

`EXTRACTION CONFIDENCE ≠ SOURCE AUTHORITY ≠ PERSISTENCE VERIFICATION ≠ CANON/LOCK STATUS`.

A transcript may tell us what a model **claimed**. It does not prove that a file was saved, a gate passed, a provider rendered, a human approved, a market validated, or a Founder locked anything.

## Primary result

The next bottleneck is not another larger regex extractor. It is the chain:

`RECOVERY LEDGER v1 -> RECONCILED RECOVERY STATE v2 -> PROJECT PARTITION -> CLAIM/EVIDENCE VERIFICATION -> AUTHORITY/SUPERSESSION -> TRANSACTIONAL WRITE + READBACK -> RECOVERY COMPLETE -> NORMAL NEXT ACTION`.

The first real large copied chat remains the decisive production pilot. Prompt-count expansion must not outrank that evidence gate.
