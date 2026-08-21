# IVDIVO AUDIO NOVEL ENGINE — WAVE4 SYNTHESIS + PATH TO GOAL v1

**Date:** 2026-08-21  
**Status:** INTEGRATION IMPROVED / EMPIRICAL RELEASE GATES OPEN

## 1. What changed materially

The new work did not add another abstract audio architecture. It moved Wave3’s proven-dry mechanisms toward the actual Audio Studio runtime already present on current GitHub `main`.

The key production gap was **control around existing modules**, not a missing story/audio philosophy:
- exact build identity before spend;
- restart-safe paid-request ledger;
- ambiguity quarantine;
- capability drift without voice/model substitution;
- canonical 48 kHz asset ingest and hashing;
- explicit evidence lock for performance;
- executable earliest-cause repair routing;
- bounded pre-dispatch wrapper around the existing ElevenLabs adapter.

This is a convergence step: current provider adapter/alignment/performance modules are retained; gaps are filled around them.

## 2. What did not change

- Story/canon: unchanged.
- Lesson Zero text: unchanged.
- Canary scope: still exactly 3 requests / 36 spoken units / 2163 characters / Narrator + Ethan + Aoife.
- Voice IDs: unresolved.
- Pronunciation locks: unresolved.
- Provider spend: 0 in this Wave4 work block.
- Real Lesson Zero WAV/alignment/timeline: absent.
- Human listen/fatigue/chemistry/comprehension: not run.
- Measured economics: absent.
- V1 Production Ready: not justified.

## 3. Strongest new findings

### Finding A — determinism must protect spend, not just files
A request hash becomes economically meaningful only if accepted/ambiguous state survives restart. The production engine therefore needs one ledger truth: accepted hashes are reusable; ambiguous requests are quarantined until reconciled; no blind retry.

### Finding B — provider uncertainty is a provenance problem
A timeout after POST is not equivalent to “nothing happened.” The safest default is `AMBIGUOUS`, not automatic retry. If provider lookup is unavailable, HOLD is more correct than paying twice.

### Finding C — current runtime already owns significant capability
Fresh inspection found current provider preflight, ElevenLabs adapter, alignment normalizer and performance compiler. Rebuilding them in a Wave3 namespace would have created divergence. Reconciliation is now explicit: reuse current modules and promote only genuine gaps.

### Finding D — project-specific identity belongs in data, not runtime code
Lesson Zero’s exact 3-block canary identity is now a fixture; runtime validation is generic. This prevents both ROOM917 leakage and Lesson-Zero hardcoding in the universal core.

### Finding E — 48 kHz ingest must fail before accepted-take lineage
Hashing provider output is not enough if unsupported/malformed audio can flow downstream. Canonical ingest must validate technical identity before take registry/timeline use.

### Finding F — “AI detection” cannot be a performance authority
Repeated endings, regular pause spacing and regular breath cadence are useful flags, but automated rejection would erase legitimate acting variation. Machine flags remain advisory; human evidence is mandatory for lock.

### Finding G — sound topology must be functionally sparse
Lesson Zero Scene2 does not need ROOM917’s clue-heavy bus topology. Universal behavior is not “same number of buses”; it is preservation of required functions and QC in whatever topology the scene actually needs.

### Finding H — music is downstream of scene truth
CUE012 remains disabled first pass. This prevents score from hiding missing room reality, weak performance or weak causal Foley. Music enters only when it solves a demonstrated listener-state problem.

### Finding I — repair quality depends on earliest cause
A performance defect is not a mastering problem; missing physical action is not a music problem; room dropout is not solved by widening. The executable audio repair router now mirrors the universal Patch Contract Standard and prevents broad symptom polishing.

## 4. Red Team

**FATAL:** 0 new story/canon defects.

**MAJOR — empirical blockers:**
1. no authenticated voice/model inventory;
2. no provisional Narrator/Ethan/Aoife real candidates;
3. no heard `Ифа` / `Контакт` pronunciation lock;
4. no exact three-request live canary;
5. no durable live WAV + alignment lineage;
6. no human performance/comprehension gate;
7. no measured economics;
8. newly ported integration code not yet CI-readback/merged into current main.

**MAJOR — production risk if left unresolved:**
- blind retry after ambiguous provider response;
- accepted-take overwrite or duplicate paid attempt after restart;
- silent provider model/voice substitution;
- project-specific fixture facts leaking into universal runtime;
- music/SFX used to mask earlier-layer failure.

**MEDIUM:**
- real provider error payload variation may require taxonomy extension;
- real audio ingest may expose formats not covered by current strict canonical boundary;
- real alignment may expose timing schemas beyond current normalizer families.

**POLISH:** intentionally deferred until live audio exists.

## 5. Current path to the product goal

### Gate 1 — Authoritative integration
Rebase the integration branch on freshest main, run/obtain CI readback, fix only demonstrated integration failures, then review/merge bounded production-control changes. Do not merge Wave3 research harness wholesale.

### Gate 2 — Authenticated casting evidence
Run current read-only provider preflight in an authorized environment. Persist only secret-free model/voice snapshot. Rank Narrator/Ethan/Aoife candidates from that snapshot.

### Gate 3 — Pronunciation + multi-state auditions
Use canonical scene text only. Lock `Ифа`/`Контакт` only after hearing them in context. Do not promote a pretty one-line voice to role lock without direction-change/pair/fatigue evidence.

### Gate 4 — Exact canary spend
Exactly three dialogue/narration requests first. Persist request hash, request/provider ID, raw response, raw audio, canonical WAV hash, raw/normalized alignment and capability/binding revision in the producing work block.

### Gate 5 — Real timing and sound assembly
Resolve only CH01_S02. Place CUE008–011 from real alignment; CUE012 remains off unless later A/B evidence earns it. Create sparse functional mix, not ROOM917 imitation.

### Gate 6 — Human product truth
Listen blindly for age, character distinction, naturalness, active waiting, world normality, comprehension, fatigue and desire to continue. Human rejection must be timestamped/causal before repair.

### Gate 7 — Selective repair
Route each failure to earliest responsible layer. Reuse accepted hashes/bytes. Regenerate only failed blocks when voice performance actually fails; edit/remix earlier when the defect is timing/Foley/room/music/space.

### Gate 8 — Economics
Measure actual provider charge, rejected-generation cost, manual minutes, accepted runtime, cache savings, cost/accepted minute and human minutes/accepted minute.

### Gate 9 — Controlled portability and scale
Only after Lesson Zero live canary passes, extend to remaining Chapter1 blocks or a materially different third project. Do not call the engine universal because two dry packages compile.

### Gate 10 — Production Ready
GO requires artifact pointers for every mandatory technical, artistic, economic, persistence and portability gate. Missing evidence = HOLD, not optimistic PASS.

## 6. Engine maturity after this work

- Story/audio architecture: **GO**.
- Current dry production topology: **GO**.
- Wave3 deterministic research candidate: **GO_FOR_REVIEW** by prior 44/44 evidence.
- Wave4 authoritative-integration code: **WORKING / CI_PENDING / REVIEW_PENDING**.
- Authenticated casting: **HOLD**.
- Live second-project portability: **HOLD**.
- Real alignment/timeline: **HOLD**.
- Human performance quality: **HOLD**.
- Economics: **HOLD**.
- Universal production-ready v1.0: **HOLD**.

## 7. Decision about further prompt generation

A new 64-prompt downstream pack is useful only as a **dependency-aware future backlog**. It must not replace the still-unexecuted Wave4 prompts 33–64 or the live provider gate. Therefore the derived Wave5 pack is marked `READY_FUTURE / NOT_CURRENT_UNTIL_WAVE4_DEPENDENCIES_CLOSE`.

Current highest-value next internal action: **rebase + CI/readback + reconcile any failures in the new production-control integration**.

Current highest-value next external action: **authenticated provider inventory and bounded three-role casting/preflight**.
