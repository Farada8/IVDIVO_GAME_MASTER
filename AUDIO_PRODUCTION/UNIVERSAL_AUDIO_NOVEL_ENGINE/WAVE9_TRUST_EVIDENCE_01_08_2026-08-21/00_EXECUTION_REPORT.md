# AUDIO NOVEL ENGINE — WAVE9 TRUST / EVIDENCE 01–08

Date: 2026-08-21
Status: `01_08_ENGINEERING_COMPLETE / FRESH_CI_PASS / MERGE_PENDING / 09_PLUS_EXTERNAL_HOLD`

## Authority / freshness

Branch cut from current GitHub `main` `0a3fcaa37b7774382013230e5eacc26b61e175c1`, which includes merged Self-Improvement Cycle6 and earlier SI-0014/Run33 recovery plus provider snapshot hardening PR #122.

Canonical runtime remains `audio/studio/runtime`. No second Audio Engine was created.

## Fresh defect

`audio/studio/runtime/studio_evidence.py` still accepted caller-supplied booleans for external evidence fields. A caller could construct values such as `human_review=True`, `provider_preflight_pass=True` or an all-True release matrix without the original authenticated provider snapshot, trusted human submission, content readback, live-audio lineage, real alignment, measured economics or recovery provenance.

This was a real promotion/evidence-laundering defect even though the provider dispatch boundary itself had already been hardened by PR #122.

## Wave9 01–08 disposition

### 01 — FRESH MAIN READBACK
`PASS_ENGINEERING`.

Current branch base at execution: `0a3fcaa37b7774382013230e5eacc26b61e175c1`.

### 02 — FRESH-MAIN FUNCTION DIFF
`PASS_ENGINEERING`.

Reuse current ProviderSnapshot validator, current canonical runtime, SI-0014/Run33 recovery semantics and Cycle6 evidence discipline. Do not duplicate those systems.

### 03 — WAVE8 DOC / SCHEMA SYNC
`PASS_BOUNDED` for the active trust surface.

Runtime evidence semantics now distinguish class-specific source validation and four durable readback strengths. Historical Wave8 provenance remains provenance; this package is the current implementation/readback delta.

### 04 — PROOF SOURCE-VALIDATOR CONTRACT
`PASS_ENGINEERING / CI_PASS`.

Added `external_evidence_trust.py`. A bare bool, generic `verified=True`, pointer or hash cannot satisfy an external evidence class. Classes route to distinct validators.

### 05 — HUMAN ATTESTATION CONTRACT
`PASS_ENGINEERING / CI_PASS`.

Trusted reviewer identity class, submission ref/hash, task-pack hash, artifact hash, candidate hash, timestamp, review scope, durable submission readback and `synthetic_fixture=False` are required. Synthetic fixtures cannot satisfy HUMAN_REVIEW.

Performance eligibility now requires separate trusted human evidence families for multi-state, pronunciation, fatigue and performance review; pair evidence is required when the pair gate is active. Machine still cannot set `voice_lock=True`.

### 06 — DURABLE CONTENT READBACK CONTRACT
`PASS_ENGINEERING / CI_PASS`.

Readback strengths are explicit:

`POINTER_PRESENT < POINTER_READABLE < CONTENT_HASH_VERIFIED < TRANSACTION_RECOVERABLE`.

Pointer-only durability cannot satisfy production evidence. Content/readback hashes must bind and readback timestamps must postdate the write. Recovery additionally requires transaction-recoverable strength, zero duplicate provider calls, zero duplicate charges and zero unresolved ambiguities.

### 07 — PROVIDER PREFLIGHT SOURCE BINDING
`PASS_ENGINEERING / CI_PASS`.

The adapter reuses `provider_snapshot_contract.validate_provider_snapshot`; it does not invent a parallel provider validator. Provider evidence must pass the current authenticated snapshot contract and a durable PROVIDER_SNAPSHOT receipt whose logical content hash binds to the validated snapshot hash.

### 08 — FRESH MERGE-RESULT CI GATE
`PASS_ENGINEERING` for PR #132 merge result at the recorded run.

GitHub Actions workflow: `Audio Studio Runtime Tests`
Run ID: `32521002618`
Run number: `117`
Merge-result checkout SHA: `f1248e3feacf7cd00f8113c8ab31e39d2d32a499`
Dedicated Audio Novel runtime: `4/4 PASS`
Full Audio Studio discovery: `186/186 PASS`
Job ID: `96892943790`

This proves engineering/regression readiness only. It does not prove provider, human, audio quality, economics or market claims.

## New release-boundary law

Internal deterministic facts may remain explicit booleans. External release classes may not.

The production release matrix now requires class-specific receipt validation for:

- AUTH_PROVIDER;
- LIVE_AUDIO;
- REAL_ALIGNMENT;
- HUMAN_REVIEW / PERFORMANCE;
- HUMAN_REVIEW / BLIND_LISTENER;
- MEASURED_ECONOMICS;
- DURABLE_RAW_ASSET;
- DURABLE_RECOVERY;
- CROSS_PROJECT_LIVE.

An all-True boolean release matrix now returns HOLD.

Even when every receipt is valid, the machine returns only `GO_FOR_FOUNDER_RELEASE_DECISION`; `production_ready` remains false and the machine may not self-promote.

## Evidence ceiling

Provider/account reads in this work block: 0.
Paid synthesis calls: 0.
Real human review claims: 0.
Real voice locks: 0.
Pronunciation locks: 0.
Real Lesson Zero live WAV/alignment: none created in this work block.
Measured Lesson Zero economics: none.
Cross-project live replication: none newly claimed.
Story/source mutations: 0.

## Exact next dependency

Wave9 09+ remains external evidence work:

`authenticated provider access -> first real secret-free snapshot -> current bound voice/model inventory -> Narrator/Ethan/Aoife candidates -> heard Ифа/Контакт -> multi-state/pair/fatigue -> human/founder lock -> exact pre-spend GO -> RB001...`

If trusted provider access is unavailable, status remains `BLOCKED_EXTERNAL`; do not compensate with another generic architecture cycle.