# WAVE8 PROMPTS 01–32 — RECONCILED EXECUTION REPORT

Execution basis: merged Wave7 prompt bank + previously persisted Wave8 execution + fresh current-main/Drive reconciliation. No prompt was repeated when an authoritative result already existed.

Notation: `FF` fresh finding; `A` action; `R` artifacts read/changed; `E` evidence; `B` blocker; `N` exact next step.

### 01 — PASS_REPOSITORY
OBJECTIVE current-main readback. DEPENDENCIES none. FF main advanced through PMV and provider hardening. A reread main/Wave7/Drive. R Wave7 package, CURRENT_WORKSTATE. E current main `9ecb752...`. B none. N use fresh main for all descendants.

### 02 — PASS_REPOSITORY
OBJECTIVE fresh Audio CI evidence. DEPENDENCIES 01. FF PR122 has successful Audio Studio Runtime Tests run #110. A verified workflow success. R PR122/head workflow. E run `32518376484`, conclusion SUCCESS. B test-count detail not inferred. N retain CI as engineering-only evidence.

### 03 — REUSE_CURRENT
OBJECTIVE promotion semantics. DEPENDENCIES 01. FF PR103 merged semantics remain: two real projects => eligibility only. A reuse. R post-render authority/tests. E machine cannot change authority. B none. N Founder review if eligibility is ever reached.

### 04 — PASS_REPOSITORY
OBJECTIVE negative fixture coverage. DEPENDENCIES 01. FF existing Wave8 negative catalog + newer provider regression. A retain catalog, add provider legacy-weak-snapshot failure to current evidence map. R PR114 catalog, PR122 tests. E weak PASS snapshot non-authoritative. B none. N extend only on demonstrated new failure class.

### 05 — REPAIRED
OBJECTIVE provider-preflight portability crosswalk. DEPENDENCIES 01–04. FF controlled dispatch had a concrete authentication/provenance gap. A PR122 merged ProviderSnapshotContract/acquirer/dispatch enforcement. R PMV/current runtime/PR122. E fresh CI SUCCESS. B real authenticated snapshot absent. N acquire one in trusted runtime.

### 06 — REUSE_CURRENT
OBJECTIVE human review-to-lock crosswalk. DEPENDENCIES 01–04. FF PR111/Drive Red Team confirms record-integrity != proof human listened. A preserve machine-no-lock rule; require externally witnessed attestation for real HUMAN evidence. R Wave8 Red Team, Cycle5 claim ceilings. E synthetic fixture cannot satisfy HUMAN. B human submission surface not exercised. N trusted attested micro-review after real audio.

### 07 — REUSE_CURRENT
OBJECTIVE live escrow/recovery crosswalk. DEPENDENCIES 01–04. FF pointer membership is weaker than content readback; SI-0014 owns generic transaction semantics. A require content identities and adapt to SI-0014 rather than duplicate. R Wave8 Red Team, Run33. E `POINTER_PRESENT != DURABLE_RECOVERY`. B no live transaction. N verify on first real canary.

### 08 — REUSE_CURRENT
OBJECTIVE architecture re-freeze. DEPENDENCIES 01–07. FF only concrete provider defect justified bounded patch. A refreeze generic architecture. R current runtime/PR122. E no second runtime created. B none. N unfreeze only on concrete deterministic/live/human/economics/recovery/portability failure.

### 09 — BLOCKED_EXTERNAL
OBJECTIVE authenticated secret-free ElevenLabs account snapshot. DEPENDENCIES 05,08. FF acquisition code is now merged but no credential exists in this execution surface. A persist HOLD, no fake values. R provider bridge 01–04. E provider/account reads=0. B trusted runtime credential. N run read-only acquirer with ephemeral key outside chat/repo/Drive.

### 10 — BLOCKED_DEPENDENCY
OBJECTIVE snapshot reproducibility. DEPENDENCIES 09. FF none without first real snapshot. A no simulation. R snapshot contract. E no two authenticated captures. B 09. N capture second snapshot after 09.

### 11 — BLOCKED_DEPENDENCY
OBJECTIVE current model/capability compatibility. DEPENDENCIES 09. FF names are not evidence. A hold. R provider contract/PMV. E no authenticated model inventory. B 09. N validate exact required models/capabilities from real snapshot.

### 12 — BLOCKED_DEPENDENCY
OBJECTIVE Narrator real shortlist. DEPENDENCIES 09,11. FF voice IDs must come from bound current inventory. A hold. R LZ canary authority. E zero real candidate IDs. B 09/11. N shortlist 2–4 real IDs after snapshot.

### 13 — BLOCKED_DEPENDENCY
OBJECTIVE Ethan real shortlist. DEPENDENCIES 09,11. FF same. A hold. R LZ role passport. E zero IDs. B 09/11. N shortlist age/status-plausible IDs, quality still UNKNOWN until heard.

### 14 — BLOCKED_DEPENDENCY
OBJECTIVE Aoife real shortlist. DEPENDENCIES 09,11. FF same. A hold. R LZ role passport. E zero IDs. B 09/11. N shortlist peer/dry candidates after snapshot.

### 15 — PASS_DETERMINISTIC
OBJECTIVE inventory drift/no-auto-swap. DEPENDENCIES 05. FF PR122 retains missing-ID fail-closed behavior. A reuse regression. R controlled dispatch/tests. E no auto substitution. B real live drift untested. N live drift case only after authenticated inventory.

### 16 — PASS_DETERMINISTIC
OBJECTIVE baseline-before-challenger spend plan. DEPENDENCIES 09–14 for values. FF budget values remain unknown. A retain minimum-baseline-first policy. R Wave8 plan. E no spend fabricated. B actual pricing/quota absent. N fill ceilings from authenticated provider evidence.

### 17 — BLOCKED_HUMAN
OBJECTIVE heard `Ифа`. DEPENDENCIES 12–14, real render. FF machine text expectation is not heard evidence. A protocol retained only. R LZ pronunciation risks. E no audio/human submission. B provider+human. N minimal canonical audition then attested human review.

### 18 — BLOCKED_HUMAN
OBJECTIVE heard `Контакт`. DEPENDENCIES 12–14, real render. FF exact source must remain unchanged. A hold. R RB001/RB003 contexts. E no heard evidence. B provider+human. N bounded dual-context audition.

### 19 — BLOCKED_HUMAN
OBJECTIVE Narrator four-state audition. DEPENDENCIES 12,09. FF no candidate audio. A hold. R role passport. E no human score. B provider/human. N render bound states after shortlist.

### 20 — BLOCKED_HUMAN
OBJECTIVE Ethan three-state audition. DEPENDENCIES 13,09. FF no audio. A hold. R role passport. E no age/status heard evidence. B provider/human. N real audition.

### 21 — BLOCKED_HUMAN
OBJECTIVE Aoife three-state audition. DEPENDENCIES 14,09. FF no audio. A hold. R role passport. E no heard evidence. B provider/human. N real audition.

### 22 — BLOCKED_HUMAN
OBJECTIVE blinded Ethan/Aoife pair gate. DEPENDENCIES 20,21. FF randomization contract exists; result does not. A hold. R Wave8 human evidence design. E no pair audio/review. B upstream. N opaque-label pair pack after individual candidates survive.

### 23 — BLOCKED_HUMAN
OBJECTIVE narrator fatigue mini-preflight. DEPENDENCIES 19. FF no long render. A hold. R performance plan. E no 3–5 minute human listen. B upstream. N real fatigue sample before lock.

### 24 — PASS_DETERMINISTIC
OBJECTIVE human evidence lock provenance. DEPENDENCIES 17–23 for production result. FF Red Team tightened trust anchor: hash-chain integrity alone != human truth. A preserve compiler ceiling `ELIGIBLE_FOR_HUMAN_LOCK_DECISION`; require attested source for production HUMAN. R PR111/Drive Red Team/Cycle5. E machine auto-lock=false. B real events absent. N ingest only attested real reviews.

### 25 — HOLD_MISSING_EVIDENCE
OBJECTIVE exact pre-spend gate. DEPENDENCIES 09–24. FF identity still exactly 3 requests/36 units/2163 chars and immutable RB hashes; provider/cast/pronunciation missing. A revalidate dry identity only. R LZ canary authority. E dry identity PASS; live GO=false. B 09, voice/pronunciation locks. N close earliest missing provider snapshot.

### 26 — BLOCKED_DEPENDENCY
OBJECTIVE RB001 live dispatch. DEPENDENCIES 25 PASS. FF spend remains prohibited. A no dispatch. R controlled dispatch. E paid requests=0. B 25. N one RB001 request only after GO.

### 27 — BLOCKED_DEPENDENCY
OBJECTIVE RB001 human sanity. DEPENDENCIES 26. FF no audio. A hold. R human gate contract. E no listen. B 26. N catastrophic identity/age/pronunciation/artifact check after RB001.

### 28 — PASS_DETERMINISTIC
OBJECTIVE ambiguity/retry drill. DEPENDENCIES dispatch/recovery code. FF existing idempotency/quarantine behavior retained through PR122. A reuse non-billable regression. R controlled dispatch/spend logic. E ambiguous state does not blind-resend accepted hash. B real provider-history reconciliation untested. N exercise on first real ambiguous event if it occurs.

### 29 — BLOCKED_DEPENDENCY
OBJECTIVE RB002 live dispatch. DEPENDENCIES 27 PASS. FF none. A no dispatch. R canary DAG. E paid requests=0. B 27. N independent RB002 lineage after RB001 human PASS.

### 30 — BLOCKED_DEPENDENCY
OBJECTIVE RB002 human sanity. DEPENDENCIES 29. FF none. A hold. R pair gate. E no audio/listen. B 29. N pair/status/timing review.

### 31 — BLOCKED_DEPENDENCY
OBJECTIVE RB003 live dispatch. DEPENDENCIES 30 PASS. FF none. A no dispatch. R canary DAG. E paid requests=0. B 30. N narrator-only RB003 after prior gate.

### 32 — HOLD_MISSING_EVIDENCE
OBJECTIVE exact three-lineage + durable live escrow. DEPENDENCIES 26–31. FF Red Team requires content-verified readback, not pointers; SI-0014 semantics should be reused. A template/protocol retained, live PASS withheld. R Wave8 escrow/Red Team/Run33. E zero live lineages. B provider+human+audio. N prove exact three content-verified lineages after canary.

## Aggregate
32/32 prompts are processed to evidence boundary. Fresh reconciliation adds one concrete merged repair: authenticated/fresh ProviderSnapshot enforcement before live capability PASS. Provider/account reads 0; paid synthesis 0; human listens 0; voice locks 0; pronunciation locks 0; real LZ WAV/alignment/economics none; story mutations 0. `V1 = HOLD`.