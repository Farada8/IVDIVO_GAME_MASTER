# WAVE6 — PARALLEL DEVELOPMENT DELTA ANALYSIS

## Freshness boundary

Wave6 was rebased conceptually against `main` at commit `46f9a133530fd3a86b7e9ef83556c9b51e249371` after fresh-read discovery that multiple audio lines had advanced concurrently.

## What parallel work already solved

### Production control — merged
PR #94 merged into `main` at `49a4d0e455b62dfd68932bf7c60ca4dee7df7b68`.
It supplies paid-dispatch identity/capability gates, spend/idempotency, ambiguous-response quarantine, provider-vs-production acceptance separation, 48 kHz ingest and related tests.

### Studio Evidence — merged
Commit `6929402fe8b299b1b715b473853e6ae73504c754` merged evidence-only three-mode benchmarking, human performance/review gates, measured economics and Founder-routed release evidence without replacing director/provider/alignment/repair authorities.

### Wave5 convergence — merged
Commit `ef021949d7f9d10d1159ee6e93dcbdeddc96427e` records 32 convergence prompts, 68 deterministic Wave5 tests, 64 next evidence prompts and the rule `ONE CANONICAL AUDIO RUNTIME, MANY PROJECT OVERLAYS`.

### ROOM917 post-render engineering v2 — project pilot
The project package implements semantic cue lineage, accepted timing resolution, signal intervals, classification, selective repair planning, room-bed patching, regression, routing and a self-improvement adapter.

### Self-Improvement — SI-0009 captured
Commit `46f9a133530fd3a86b7e9ef83556c9b51e249371` records `SI-0009` as a `PILOT_PASS` candidate: Evidence-gated post-render repair compiler + executable persistence enforcement. Domain promotion remains blocked by a second independent locked audio project and human listen evidence.

## Concrete gaps remaining after dedupe

### G1 — classifier/authorization conflation — MAJOR
ROOM917 `interval_classifier.py` emits `patch_authorized=true` for one machine-classified condition. That is too strong for universal use because the classifier does not itself prove:
- immutable master identity;
- exact coverage of every protected semantic pause;
- asset hash/rights;
- explicit production gain;
- headroom;
- one-bed-domain containment;
- final human evidence.

Wave6 correction: classifier output is treated as **nomination/candidate only**. A separate deterministic authorization artifact controls permission to touch bytes.

### G2 — path existence treated as state evidence — MAJOR
ROOM917 `post_render_router.py` mainly advances stages by `Path.exists()`. A stale, wrong-schema, wrong-hash, semantic-HOLD file can therefore look superficially present.

Wave6 correction: artifact evidence must verify bytes/hash/schema/semantic status. Existence alone never advances the universal state machine.

### G3 — renderer can silently clip — MAJOR
ROOM917 renderer applies `np.clip` before writing PCM. That prevents numeric overflow but can hide a failed mix/headroom decision.

Wave6 correction: universal contract forbids silent clipping. Headroom is preflight evidence; post-render PCM QC explicitly reports near/full-scale clipping and boundary discontinuities. Candidate output may be HOLD but never silently accepted.

### G4 — source-master identity not rechecked at byte-touch point — MAJOR
Patch plan carries a master SHA, but the project renderer does not independently verify that the bytes supplied as `--master` match that SHA before applying the patch.

Wave6 correction: master identity is part of authorization and patch ledger lineage. Mismatch = HOLD before accepted lineage can advance.

### G5 — asset binding provenance too weak — MAJOR
Project renderer currently needs `path + gain_db`; universal production use also needs asset hash, rights state, sample rate and channel declaration.

Wave6 correction: explicit `asset_binding` contract requires SHA-256, rights status, 48 kHz, mono/stereo, explicit non-positive gain.

### G6 — regression has a project-specific default timestamp — MAJOR for universalization
ROOM917 `regression_gate.py` carries a default Scene3 start time. Valid for that project pilot, invalid as universal authority.

Wave6 correction: universal regression consumes project overlay `authorized_ranges`, `protected_ranges` and measured `changed_ranges`; no story/scene/timestamp constant exists in runtime code.

### G7 — protected semantic silence can remain unresolved — MAJOR
ROOM917 correctly keeps some silence semantic-only until real timing exists. Universal auto-repair must not patch around that unresolved protected beat as though its range were known.

Wave6 correction: if any declared protected pause lacks accepted/live absolute timing, machine patch authorization is HOLD.

### G8 — project pilot learning needs stronger normalized write-through — MEDIUM/MAJOR
SI-0009 exists, but the universal bridge needs normalized metrics and explicit project-leakage defense so repeated project evidence does not become accidental lore/canon transfer.

Wave6 correction: `post_render_learning.py` emits mechanism-level self-improvement events, normalized provider/human/rework metrics, collapses duplicate evidence families and forbids automatic authority mutation.

## Non-duplication decision

Wave6 does NOT add:
- another provider adapter;
- another alignment engine;
- another Automatic Director;
- another three-mode benchmark/economics engine;
- another global audio runtime;
- project story facts in universal modules.

It extends the existing runtime only at the evidence/authorization boundary proven weak by actual project integration.

## Current real frontier

Internal hardening can be tested now. Domain promotion still requires:
1. immutable real second-project master bytes;
2. project-native semantic cue contracts;
3. accepted/live timing;
4. at least one real bounded defect and selective repair;
5. positive regression + deliberate negative fixture;
6. real human listen;
7. false-positive/manual-override measurement.
