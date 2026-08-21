# WAVE8 — PARALLEL GITHUB + GOOGLE DRIVE DELTA ANALYSIS

## Fresh surfaces inspected

### GitHub current-main / merged work
- PR #103 post-render hardening is merged; merge commit `0219586858797bf646ca2e7f020bf6a9ff662fc0`.
- Final PR103 evidence: dedicated runtime 4/4 PASS; full Audio Studio 158/158 PASS.
- current universal post-render modules are on `main`: authorization/headroom/protected timing, verified artifact routing, PCM/seam QC, learning bridge and Founder-review promotion eligibility.
- Session Resilience Run32 is merged and adds SI-0010 checkpoint/resume logic with `RESUME_EXACT / REBASE_FIRST / RECOVER_VOLATILE_FIRST / STOP`.
- PMV177–208 multilingual voice engineering provides reusable mechanisms: credential-safe preflight, review-to-lock firewall, baseline-before-challenger, bounded slice before full render, evidence contracts and expected-information-gain routing.

### Google Drive
Wave7 already exists and was not repeated blindly. Its execution report states 32/32 prompts processed, provider calls=0, human claims=0, voice/pronunciation locks=0. It identifies authenticated provider inventory + casting + human-heard pronunciation/performance as the real external bottleneck.

Wave8 64-prompt bank already exists in Drive. This cycle consumes the smallest decisive subset and hardens only missing contracts before external spend.

## Function-by-function disposition

### REUSE CURRENT
- `audio/studio/provider_preflight.py`: credential-safe read-only provider access.
- `audio/studio/controlled_provider_dispatch.py`: identity + authenticated capability live gates, idempotent spend ledger, ambiguous response quarantine.
- `audio/studio/runtime/studio_evidence.py`: human/economics/release evidence concepts and no-machine-lock law.
- `tools/ivdivo_session_checkpoint.py`: hashed restart classification.
- post-render Wave6 runtime: byte-touch authorization and regression.

### UNIQUE DELTAS FOUND
1. **Provider Snapshot Contract**  
   Existing preflight is a request-time report. Missing: deterministic stable/volatile separation, inventory scope declaration, snapshot hashes and a formal rule that TARGETED voice verification cannot be presented as account-wide inventory.

2. **Human Review Provenance Ledger**  
   Existing Studio Evidence has boolean evidence states. Missing: append-only review events tied to source/audio hashes, reviewer type/time, evidence family, hard fails and a hash-chain ledger that supports audit/restart without allowing machine lock.

3. **Live Evidence Escrow**  
   Provider dispatch, spend, alignment and session recovery exist separately. Missing: one exact lineage binding request hash, provider request ID, capability snapshot hash, audio/alignment hashes, durable refs and spend evidence, plus exact-N lineage validation and no-paid-replay recovery.

4. **Typed Proof Manifest**  
   The repository increasingly uses PASS labels from different evidence domains. Missing: machine-readable prevention of `PASS_CODE/CI` being interpreted as provider/human/live/economics proof.

## Explicit non-transfer

Do not transfer project story facts, cast IDs, voices, ROOM917 timings, BODYGUARD terminology, NMM asset identities or Lesson Zero text into universal runtime. Only mechanisms/contracts cross project boundaries.

## Architecture decision

`ONE CANONICAL AUDIO RUNTIME, BOUNDED CONTRACT DELTAS ONLY.`

Generic architecture remains frozen. New shared code is justified only by the four concrete gaps above. After these close and regressions are green, the next useful information requires actual authenticated provider/human/live evidence.
