# IVDIVO — 32-PROMPT SPRINT SYNTHESIS + UPGRADE PLAN v1.0

Status: COMPLETED SYNTHESIS / WORKING UPGRADE PLAN
Date: 2026-08-21

## 1. What the 32 executions prove

The current 18B architecture is directionally correct: pasted chat is a recovery corpus, not authority; persistence claims must be verified; chat-only work may be recovered as candidate; reusable learning feeds Self-Improvement; recovery must end in a real frontier and continuation.

The executable v1 extractor is correctly bounded as first-pass `EXTRACTED_UNVERIFIED`. Its current 5/5 tests prove only the narrow deterministic contracts already documented. The sprint found no reason to weaken that boundary.

The largest remaining weakness is not extraction itself. It is the missing **semantic reconciliation state layer between extraction and resumed production**.

## 2. Target architecture

`RAW / PASTED TRANSCRIPT`
→ `EXTRACT_LEDGER_v1` — deterministic, secret-redacted, no authority promotion
→ `RECONCILED_RECOVERY_STATE_v2` — semantic/project-aware reconciliation
→ `PERSISTENCE VERIFICATION TASKS` — GitHub / Drive / Library / provider / human evidence
→ `PROJECT PARTITIONS + FRONTIER RECONSTRUCTION`
→ `CHAT_ONLY CANDIDATE WRITE-THROUGH`
→ `SYSTEM LEARNING HARVEST`
→ `READBACK / CONFLICT CHECK`
→ `RECOVERY COMPLETE GATE`
→ `NEXT-ACTION RESOLVER`
→ `CONTINUE REAL PRODUCTION`.

The most important separation is:

`EXTRACTION CONFIDENCE ≠ AUTHORITY ≠ PERSISTENCE VERIFICATION ≠ CANON STATUS`.

## 3. Five critical controls

### C1 — Reconciled Recovery State v2
Must add: recovery_id; source/chunk lineage; project partitions; direct-Founder directives vs paraphrases; authority class; verification state; conflicts/unknowns; artifact identity; verification task results; chat-only candidate disposition; superseded items; writes performed; readback; frontier; do-not-repeat; exact next action; completion gate.

### C2 — Claim-to-evidence contracts
`LOCK`, `PASS`, `GREEN`, `FINAL`, `RENDERED`, `VERIFIED`, `HUMAN APPROVED`, `MARKET VALIDATED` must each specify what evidence can satisfy the claim. Labels and assistant prose never satisfy the contract alone.

### C3 — Resumable large-corpus ingestion
For every chunk: source SHA, chunk ID, byte/line range, overlap hash, findings hash, processed timestamp, final-input-tail flag. Source mutation invalidates stale checkpoints.

### C4 — Idempotent transactional write-through
All writes carry recovery_id/content fingerprint and preserve previous CURRENT pointers. Rerunning the same source must not duplicate artifacts. Partial writes produce a repair state, not silent success.

### C5 — Recovery completion before auto-continue
Automatic production continuation is permitted only after material items are dispositioned, current frontier is fresh/unambiguous, accepted writes are read back and no material recovery conflict remains.

## 4. Red-Team severity

### FATAL
None currently demonstrated in the conceptual architecture because v1 extractor fails closed and cannot self-promote canon.

### MAJOR
1. No `RECONCILED_RECOVERY_STATE_v2` contract/schema.
2. Central Improvement Registry atomicity/sharding/index issue can create anti-loss divergence.
3. First real large pasted-corpus pilot has not yet occurred.
4. Parser/reconciliation adversarial regression set remains too small.
5. Next-action resolver does not yet formally consume a recovery-completion gate.

### MEDIUM
- source completeness basis;
- multi-project transcript partitions;
- formal artifact identity tuple;
- claim-evidence taxonomy;
- recovery observability;
- raw-context compaction/archive law.

### POLISH
CLI/report naming, human-readable dashboard, summary formatting.

## 5. Self-improvement WIP decision

To obey ANTI-BEDLAM:

**PRIMARY META-INTEGRATION:** `RECONCILED_RECOVERY_STATE_v2 + recovery-completion gate`.

**BOUNDED PILOT A:** Improvement Registry atomic/shard/index repair.

**BOUNDED PILOT B:** adversarial/large-transcript fixture suite + first real corpus monitoring design.

Everything else becomes backlog or folds into these three lines. Do not start 20 independent sub-engines.

## 6. Acceptance gates for the next upgrade

A. No transcript can become canon merely by being pasted.
B. No saved/LOCK/PASS/provider/human/market claim can become verified without evidence contract satisfaction.
C. No raw secret is written through.
D. Same source rerun is idempotent.
E. Huge transcript can resume from checkpoints without skipping final tail.
F. Multi-project corpus remains partitioned.
G. Newer persisted project authority is never overwritten by stale transcript.
H. Every material chat-only candidate gets disposition.
I. Every write gets readback.
J. Auto-continue is blocked before recovery completion and allowed after a clean completion gate if the normal next-action gates also pass.
K. First real corpus pilot produces a measurable recovery report and Learning Ledger entries.
L. Full engine package version is not promoted until complete package regression passes.

## 7. Operational metrics that matter

- material items discovered / dispositioned;
- verified, missing, superseded and conflicting persistence claims;
- chat-only candidates recovered and safely persisted;
- false authority promotions: target 0;
- secrets persisted: target 0;
- duplicate artifacts created on rerun: target 0;
- stale write conflicts safely rebased;
- project frontier corrections;
- unresolved Founder questions required;
- repeated work prevented;
- elapsed recovery effort/tool calls relative to manual reconstruction.

Do **not** use prompt count, file count or candidate count as success metrics.

## 8. Product-level conclusion

The system should not attempt to “remember everything.” It should become a **recovery-and-verification compiler**:

`conversation history -> structured claims/deltas -> verified durable state -> next executable obligation`.

That is the scalable answer to abrupt chat endings, parallel AI work and long-running IVDIVO production.

## 9. Next-work route

The next 64-prompt pack is not 64 random brainstorms. It is organized into eight workstreams:
1. Recovery State v2 semantics;
2. claim/evidence verification;
3. parser/chunking robustness;
4. persistence/concurrency/idempotence;
5. project/frontier/next-action coupling;
6. Self-Improvement/registry/learning integration;
7. real-pilot evaluation and security;
8. packaging/Red Team/production rollout.

Run those prompts only as needed by the current bottleneck; the pack is a task bank, not a ritual that must always be exhausted before story production.
