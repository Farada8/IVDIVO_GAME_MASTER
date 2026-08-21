# IVDIVO — NEXT 64 PROMPTS v1.0

Derived from the completed 32-prompt Full Chat Recovery / Cross-Dialog / Self-Improvement sprint.
Status: NEXT-WORK TASK BANK — NOT A MANDATORY RITUAL SEQUENCE
Date: 2026-08-21

Use only the prompts relevant to the current bottleneck. Story/audio production remains higher priority unless a recovery-system MAJOR/FATAL blocks continuity.

---

# WORKSTREAM A — RECONCILED RECOVERY STATE v2

## N01 — v2 state model
Design `RECONCILED_RECOVERY_STATE_SCHEMA_v2` from the 18B minimum ledger plus sprint findings. Separate extraction, authority, persistence verification, disposition, write-through and completion state.

## N02 — authority class enum
Define a minimal non-overlapping authority taxonomy for Founder directives, locked canon, project authority, domain authority, current state, working candidates, external findings and transcript-only claims.

## N03 — verification state machine
Design claim states from UNCHECKED through VERIFIED/MISSING/SUPERSEDED/CONFLICT/UNRECOVERABLE. Specify legal transitions and fail-closed illegal transitions.

## N04 — project partition model
Design `project_partitions[]` for multi-project transcripts, including project identity resolution, unknown project handling and contamination prevention.

## N05 — conflict graph
Represent conflicts between recovered directives, current artifacts and competing branches as a graph with source, authority, chronology and resolution state.

## N06 — unknowns contract
Define `UNKNOWN` categories so missing exact details, unavailable stores, incomplete transcript sections and unresolved chronology remain explicit rather than silently reconstructed.

## N07 — recovery completion contract
Specify the exact Boolean and evidence conditions for `INGESTION_COMPLETE`. Make it impossible to set completion with unresolved material items or unread accepted writes.

## N08 — schema migration
Design migration from Extract Ledger v1 to Reconciled State v2 without mutating or invalidating existing v1 evidence artifacts.

---

# WORKSTREAM B — CLAIM / EVIDENCE VERIFICATION

## N09 — claim evidence registry
Create a registry mapping claim types (`SAVED`, `LOCKED`, `PASS`, `RENDERED`, `HUMAN_APPROVED`, etc.) to required evidence classes.

## N10 — Founder lock proof
Define the evidence contract for `FOUNDER_LOCK` and distinguish it from assistant `ready for lock`, gate PASS, project status and filename `FINAL`.

## N11 — test PASS proof
Define test evidence requirements: command, exact source identity, fixture/version, result counts, exit status, environment and readback.

## N12 — provider execution proof
Define when audio/image/video/provider claims can be marked rendered/generated/paid/executed. Separate dry-run manifests from real provider artifacts.

## N13 — human evidence proof
Define valid human reader/listener/editor evidence and prevent AI-generated reviews from being misclassified as human signal.

## N14 — market evidence proof
Define real market/platform evidence versus forecasts, synthetic scores and model speculation.

## N15 — artifact verification adapter
Design a store-neutral verification interface for GitHub, Drive, File Library and provider artifact checks with consistent result codes.

## N16 — supersession verifier
Design automatic detection that a found artifact exists but is no longer current because a later authority/gate explicitly superseded it.

---

# WORKSTREAM C — PARSER / LARGE-CORPUS ROBUSTNESS

## N17 — nested quotation fixture
Create adversarial fixtures where user messages quote old assistant/user turns. Ensure outer role and embedded role are not confused.

## N18 — markdown/code fixture
Test speaker-like labels, filenames, commands and secrets inside fenced code, blockquotes, JSON and markdown tables.

## N19 — multilingual role fixture
Test Russian/English/Ukrainian/mixed language directives and speaker labels without relying on English-only keywords.

## N20 — malformed transcript fixture
Test missing colons, broken turn separators, duplicated turns, truncation, garbled Unicode and pasted UI chrome.

## N21 — fake artifact fixture
Test invented Drive IDs, file-like strings, URLs, hashes and filenames inside fiction/code so they do not become verified artifacts.

## N22 — large-file checkpoint engine
Implement source-hash-bound chunk checkpoints with byte ranges, overlap hashes, findings hashes and final-tail proof.

## N23 — resume-after-abrupt-stop
Simulate the recovery process itself being interrupted, then restarted from persisted chunk checkpoints with zero skipped/duplicated material items.

## N24 — parser property tests
Define invariants/property tests: secrets never appear in output excerpts; assistant claims never self-verify; source hash stable; rerun deterministic; no completion from extractor alone.

---

# WORKSTREAM D — PERSISTENCE / CONCURRENCY / IDEMPOTENCE

## N25 — recovery write transaction
Design `recovery_id`-scoped write sets with previous pointer snapshot, intended mutations, result refs and rollback/repair status.

## N26 — idempotent candidate persistence
Design content fingerprints and identity keys so rerunning one transcript never creates duplicate candidate artifacts.

## N27 — GitHub stale-write adapter
Formalize SHA-aware write/rebase/branch+PR fallback. Define when retry is safe and when conflict must escalate.

## N28 — Drive revision adapter
Use Drive revision/write-control semantics to prevent overwriting concurrent edits and define rebase behavior for native Docs.

## N29 — partial-write recovery
Simulate failure after some GitHub/Drive writes. Reconstruct touched surfaces and repair without rolling back unrelated sibling progress.

## N30 — two-chat concurrency test
Run two recovery workers against overlapping state and verify no lost update, no duplicate promotion and correct final frontier.

## N31 — atomic Improvement Registry redesign
Compare monolithic JSON, shard+index and transactional utility approaches. Select the safest design and migration path for SI candidates.

## N32 — registry compaction builder
Design deterministic build/validate/compact process that assembles candidate shards into a canonical registry without data loss.

---

# WORKSTREAM E — FRONTIER / NEXT-ACTION / PRODUCTION COUPLING

## N33 — frontier compiler
Build a formal frontier compiler from verified completed artifacts, current authority, gates, blockers, do-not-repeat list and next legal action.

## N34 — transcript frontier vs persisted frontier
Create adversarial cases where the transcript ends earlier/later than current persisted project state and verify correct rebase.

## N35 — do-not-repeat derivation
Design rules for deriving `do_not_repeat` from completed gates/version reconciliation rather than from assistant prose.

## N36 — next-action recovery gate
Extend next-action resolver so `EXTRACTED_UNVERIFIED` and `RECONCILING` stop state-changing work, while clean `INGESTION_COMPLETE` can pass normal action gates.

## N37 — decision-gate minimization
Design a classifier that asks Founder only for irreducible creative/canon choices, not recoverable file/state questions.

## N38 — project queue rebase
When recovery updates one project frontier, recompute portfolio queue without reopening locked or external-evidence-held work.

## N39 — production-first budget
Define a time/tool-call/research budget so transcript recovery and meta-learning cannot consume an active story/audio session indefinitely.

## N40 — recovery-to-continuation handoff
Design the final handoff object: `what recovered / what verified / what changed / unresolved / exact next action / stop reason if any` for another dialog/model.

---

# WORKSTREAM F — SELF-IMPROVEMENT / LEARNING / MULTI-AI

## N41 — recovery learning event schema
Define Learning Ledger event types for stale-write collision, false saved claim, successful chat-only recovery, duplicate prevented, secret blocked and frontier correction.

## N42 — candidate creation threshold
Define when a recovery observation deserves an Improvement Registry candidate versus a one-off Learning Ledger event.

## N43 — system-candidate dedupe
Test whether new recovery improvements duplicate SI-0001/2/4/7/8 or truly require a new candidate.

## N44 — recovery success mining
Identify successful patterns from completed recoveries, not only failures, and define promotion criteria for them.

## N45 — multi-AI recovery roles
Assign Claude/Grok/GPT/Codex bounded orthogonal roles for large-corpus recovery without creating parallel canons.

## N46 — same-source independent review
Design a protocol where two models independently reconcile the same transcript/source without seeing each other's verdict, then compare disagreement.

## N47 — diagnosis/fix separation
Require external models to return diagnosis before proposed persistence/canon repair so confident fixes cannot hide faulty diagnosis.

## N48 — learning compaction
Define when old recovery rules/candidates should be merged, narrowed, superseded or archived to keep the Self-Improvement stack usable.

---

# WORKSTREAM G — REAL PILOT / SECURITY / EVALUATION

## N49 — first real corpus pilot card
Create an exact run card for the next pasted long conversation: source capture, baseline, extractor, reconciliation, verification, writes, readback, frontier and metrics.

## N50 — manual gold set
For the first pilot, create a small human-reviewed material-item gold set to measure missed/false directives, claims and artifacts without requiring manual reconstruction of the entire chat.

## N51 — secret attack corpus
Construct synthetic transcripts containing common API-key/token/password/link patterns and ambiguous non-secret lookalikes. Measure leaks and false positives.

## N52 — authority attack corpus
Construct transcripts where assistant falsely claims Founder approval, lock, PASS and file persistence; verify zero promotion without external evidence.

## N53 — stale-transcript attack corpus
Use an old transcript against newer project authority and confirm no rollback of current state.

## N54 — multi-project contamination corpus
Mix D09, ROOM917, Smith and tooling material in one synthetic transcript and measure partition leakage.

## N55 — recovery efficiency baseline
Compare assisted recovery versus manual Founder reconstruction on elapsed actions/questions, not on artificial prompt count.

## N56 — acceptance scorecard
Design a non-fake-precision PASS/FAIL scorecard for the real pilot: zero false authority promotion, zero secret persistence, material coverage, correct frontier, idempotence and bounded Founder questions.

---

# WORKSTREAM H — PACKAGING / RED TEAM / ROLLOUT

## N57 — v11.3 candidate manifest
Draft the next engine package manifest including v11.2 base plus verified transcript-recovery extensions and no retroactive history rewrite.

## N58 — full-package regression plan
Specify clean-unzip tests covering existing 290 v11.2 tests plus new recovery tests, schema validation and pointer consistency.

## N59 — migration compatibility audit
Check that existing project states/chat starters/audio boots still operate when recovery v2 is added and that no locked project is reopened.

## N60 — security Red Team
Attack secret handling, malicious pasted instructions, embedded prompt injection, private links, oversized inputs and accidental persistence.

## N61 — authority Red Team
Attack chronology, paraphrase, duplicated Founder statements, stale locks, competing branches, external model claims and misleading `FINAL/PASS` filenames.

## N62 — concurrency Red Team
Stress branch/PR fallback, Drive write conflicts, partial writes and two-dialog simultaneous updates.

## N63 — production starvation Red Team
Measure whether recovery/self-improvement becomes ritual overhead. Remove or defer controls that do not materially prevent loss/error.

## N64 — promotion decision
After real-pilot evidence and full regression, issue a strict GO / HOLD / NO-GO decision for promoting the recovery stack into the next packaged engine release, with application map and rollback path.

---

## Final use law

The 64 prompts are a prioritized reservoir. Do not execute all 64 merely to create volume. Select by the current bottleneck, run the smallest decisive set, persist results, update state, then return to production when the real gate is closed.
