# IVDIVO AUDIO NOVEL ENGINE — WAVE7 PROMPTS 01–32 SEQUENTIAL EXECUTION

Source: first 32 prompts from the Wave7 bank produced by Wave6 PR #99.
Method: execute in order after fresh parallel-development reconciliation. `REUSE_CURRENT` means the requested behavior is already present in fresher verified main and was checked rather than rebuilt.

Result vocabulary:
- `PASS` — evidence closed for this prompt.
- `REUSE_CURRENT / PASS_CODE` — current verified mechanism already closes the engineering requirement; no duplicate implementation created.
- `PASS_DESIGN / HUMAN_OR_AUDIO_PENDING` — execution package/contract can be completed, but result depends on real human/audio evidence.
- `BLOCKED_EXTERNAL` — requires authenticated provider/account access not available here.
- `DEPENDENCY_BLOCKED` — truthful downstream work cannot precede its missing upstream evidence.
- `NO_GO_CORRECT` — the prompt was executed and correctly denied spend/advance because mandatory evidence is missing.

## A — FRESH RUNTIME / CI / SAFETY

### 01 FRESH MAIN HEAD SNAPSHOT — PASS
Fresh integration point after parallel sweep: `0219586858797bf646ca2e7f020bf6a9ff662fc0`, merge of Audio Studio post-render hardening on top of session-resilience and PMV/current-main work. Wave7 branch was created from this SHA. No alternate runtime root was created.

### 02 EXACT-HEAD AUDIO STUDIO CI — PASS AT MERGE-RESULT EQUIVALENT
PR #103 merge-result was rebuilt against then-current `main` including session-resilience. GitHub Actions run `32513420831`, job `96869536778`: dedicated Audio Novel runtime 4/4 PASS; full `audio/studio/tests` discovery 158/158 PASS. The tested merge-result was exactly the same PR head merged over current main immediately before the final merge.

### 03 CI NEGATIVE FIXTURE AUDIT — PASS + TWO REAL DEFECTS REPAIRED
Negative coverage exists for identity drift, capability/voice absence, duplicate spend/restart, ambiguous post-response, malformed/44.1k/raw PCM, unknown alignment schema, unresolved timeline anchors, protected pauses, stereo collapse, project leakage, master hash mismatch, asset rights, headroom, clipping and patch boundaries.
This prompt also exposed two live CI inconsistencies in #103:
1. stale test expected `DOMAIN_PROMOTED` instead of `DOMAIN_PROMOTION_ELIGIBLE`;
2. learning bridge only accepted impossible `DOMAIN_PROMOTED`, so an eligible two-project result still returned HOLD.
Repairs preserve `machine_may_change_current_authority=false` and route eligibility only to Founder review.

### 04 CONTROLLED DISPATCH DRY TRACE — REUSE_CURRENT / PASS_CODE
Current tests prove default dispatch is dry/no provider call; new live dispatch requires both exact identity and authenticated capability evidence. Restart-safe ledger and ambiguous-response quarantine are already current. Wave7 provider calls remain 0.

### 05 HASH SEMANTICS REGRESSION — REUSE_CURRENT / PASS_CODE
Current production-control tests prove canonical hash reproducibility and fail on scalar/block hash drift. Post-render authorization also binds master SHA, asset SHA and authorization hash. No protected Lesson Zero text/request semantics were changed in Wave7.

### 06 ALIGNMENT SINGLE-AUTHORITY TEST — REUSE_CURRENT / PASS_CODE
Current alignment normalizer accepts known TTD voice-segment and TTS character-alignment shapes and fails closed on unknown schemas. Timeline assembler fails on missing alignment/unresolved anchors. No synthetic alignment was accepted as real timing.

### 07 CLEAN-ENV IMPORT/CLI TEST — PASS_WITH_LIMIT
GitHub Actions executes the runtime on a clean hosted runner and current CLI/recovery tests pass there, proving tested modules do not depend on this chat or an existing local workspace. This does not prove every undocumented operator command; current documented/tested entrypoints are green.

### 08 INTERNAL FREEZE DECISION — PASS
Decision: `GENERIC_RUNTIME_ARCHITECTURE_FROZEN_UNTIL_CONCRETE_FAILURE`.
Reason: current shared runtime + production control + Studio Evidence + post-render hardening + session resilience are CI-green. Further generic architecture would add complexity without closing the actual provider/human gate.

## B — AUTHENTICATED INVENTORY / CAST SEARCH

### 09 SECRET-FREE ELEVENLABS SNAPSHOT — BLOCKED_EXTERNAL
Fresh PMV work provides a credential-safe preflight that can call user/subscription/voice inventory without persisting the API key. However this ChatGPT environment has no authenticated ElevenLabs connector/API credential. No inventory was fabricated.

### 10 SNAPSHOT DRIFT POLICY LIVE TEST — REUSE_CURRENT / PASS_CODE
Current production control already proves missing/changed voice capability blocks dispatch and prohibits automatic substitution. PMV preflight adds a practical authenticated snapshot route. Real account drift remains untested until prompt 09 can run.

### 11 NARRATOR SEARCH — DEPENDENCY_BLOCKED
Requires fresh authenticated voice inventory. Role criteria remain available, but historical/unverified voices are not promoted as current candidates.

### 12 ETHAN SEARCH — DEPENDENCY_BLOCKED
Requires prompt 09. No adult-leading-man voice is guessed into the role.

### 13 AOIFE SEARCH — DEPENDENCY_BLOCKED
Requires prompt 09. No therapist/flirt/adult cadence candidate is invented.

### 14 NARRATOR DIRECTION-CHANGE MICROTEST — DEPENDENCY_BLOCKED
Requires real candidate audio in natural/private/pressure/technical states.

### 15 ETHAN DIRECTION-CHANGE MICROTEST — DEPENDENCY_BLOCKED
Requires real candidate rendering; no age-drift PASS is claimed.

### 16 AOIFE DIRECTION-CHANGE MICROTEST — DEPENDENCY_BLOCKED
Requires real candidate rendering; no active-waiting/peer-status PASS is claimed.

## C — PRONUNCIATION / PAIR / PRE-SPEND

### 17 ИФА CANONICAL MICRO-AUDITION — DEPENDENCY_BLOCKED
Canonical target remains `Ифа`. A real bound candidate and human-heard output are required. No pronunciation lock.

### 18 КОНТАКТ CANONICAL MICRO-AUDITION — DEPENDENCY_BLOCKED
Canonical target remains `Контакт` in protected contexts. No source rewrite and no lock without heard evidence.

### 19 PRONUNCIATION LOCK PROVENANCE — PASS_DESIGN / HUMAN_OR_AUDIO_PENDING
Current evidence model plus PMV review-to-lock mechanism establishes the correct firewall: provenance, reviewer evidence and performed timing must exist before lock; unresolved HOLD prevents lock. Lesson Zero has no qualifying heard evidence yet.

### 20 ETHAN_AOIFE BLIND PAIR PACK — PASS_DESIGN / AUDIO_PENDING
A valid blind gate can hide candidate labels and score distinction, believable age, status, listening/reactivity and premature-romance drift. The pack is ready conceptually; no pair audio exists, so no pair result is claimed.

### 21 PAIR HUMAN GATE — DEPENDENCY_BLOCKED / HUMAN
Requires real pair audio and human listening. Machine evidence cannot replace it.

### 22 NARRATOR FATIGUE MINI-PREFLIGHT — DEPENDENCY_BLOCKED
Requires a real candidate and 3–5 minute mixed-state audio. This remains preferable to spending on a full chapter.

### 23 EXACT CANARY IDENTITY REVALIDATION — PASS
Lesson Zero bounded canary remains immutable:
- exactly 3 provider requests;
- 36 spoken units;
- 2163 characters;
- roles NARRATOR / ETHAN / AOIFE;
- RB001 hash `4f41805b6aa5ed0506d8c64f43bf0351993fb6b9de113bbcfaad3c10d1fddf8c`;
- RB002 hash `f991022b8c13cc7b5b071caa4f11ee8dc6bd1b5def11fdffc971a9fb18c0b572`;
- RB003 hash `425bdf23b2a02cda5f71531ca48bb5e32dfe5de777fd5bbc92c8255a1504a464`.
No story/request recompilation was authorized.

### 24 PRE-SPEND GO/NO-GO — NO_GO_CORRECT
Current verdict: `NO_GO` for paid Lesson Zero dispatch because authenticated capability snapshot, bound real voice IDs and human-heard pronunciation evidence are absent. Exact identity alone is necessary but insufficient.

## D — THREE-REQUEST LIVE CANARY

### 25 RB001 DISPATCH — BLOCKED_EXTERNAL
No authenticated provider/cast/pre-spend GO. Provider calls in Wave7 = 0. No paid request was attempted.

### 26 RB001 SANITY STOP — DEPENDENCY_BLOCKED
No RB001 audio exists. Human catastrophic age/identity/pronunciation/artifact check cannot be simulated.

### 27 RB001 AMBIGUITY RECONCILIATION — REUSE_CURRENT / PASS_CODE
The restart-safe ambiguity contract is current: a response-started/unknown provider state is quarantined and reconciled before retry, protecting against duplicate spend. No real RB001 ambiguity incident occurred.

### 28 RB002 DISPATCH — DEPENDENCY_BLOCKED
Must not precede accepted RB001 + sanity evidence.

### 29 RB002 SANITY STOP — DEPENDENCY_BLOCKED
No RB002 audio; no pair/timing result claimed.

### 30 RB003 DISPATCH — DEPENDENCY_BLOCKED
Narrator-only request remains downstream of voice/pronunciation and earlier canary gates.

### 31 EXACT THREE-LINEAGE GATE — REUSE_CURRENT / PASS_CODE, LIVE DATA ABSENT
Current identity/idempotency/ledger design can enforce exactly the expected three lineages and quarantine extras/duplicates/ambiguous responses. There are zero live Lesson Zero lineages to accept in this Wave.

### 32 LIVE PACKAGE ESCROW — PASS_PROTOCOL / LIVE PACKAGE ABSENT
Current session-resilience and chat-local-asset persistence work provide the required durability principle: request/response/audio/alignment/ledger artifacts must survive outside the producing chat and be re-readable in a fresh session. No live canary package exists yet, so the protocol is ready but empirical escrow/recovery remains downstream.

## Aggregate execution result
- Prompts processed sequentially: **32/32**.
- New real engineering defect repairs completed during this Wave: **2** promotion-semantics inconsistencies.
- PR #103 full merge-result Audio Studio regression after repair: **158/158 PASS**; dedicated runtime **4/4 PASS**.
- PR #103 merged to current `main`: **YES**, merge `0219586858797bf646ca2e7f020bf6a9ff662fc0`.
- Provider calls: **0**.
- Human-listening claims: **0**.
- Voice locks: **0**.
- Pronunciation locks: **0**.
- Story mutations: **0**.

## Sequential conclusion
Prompts 01–08 have closed the internal freeze question: generic architecture is not the bottleneck. Prompts 09–24 prove the actual gate is authenticated inventory + real casting + human-heard pronunciation/performance. Prompts 25–32 correctly remain downstream; existing dispatch/idempotency/recovery mechanisms are ready, but they cannot create live evidence by themselves.
