# IVDIVO AUDIO NOVEL ENGINE — WAVE8 EVIDENCE FRONTIER

**Date:** 2026-08-21  
**Status:** ACTIVE ENGINEERING CYCLE / NO LIVE OR HUMAN CLAIMS  
**Canonical runtime target:** `audio/studio/runtime` only. No second Audio Engine is authorized.

## Why Wave8 exists

Wave6 post-render hardening is already merged to `main` through PR #103 with 158/158 full Audio Studio regression PASS. Wave7 then processed 32/32 tasks and proved that the primary remaining bottleneck is no longer generic architecture: it is authenticated provider evidence, real casting, human-heard pronunciation/performance, exact live canary provenance, real alignment/mix, human listener evidence and measured economics.

Fresh parallel analysis exposed three bounded engineering gaps immediately before that external frontier:

1. current `provider_preflight.py` verifies requested models/voices but does not produce a stable-vs-volatile, scope-explicit reusable provider snapshot;
2. current Studio Evidence has human-gate booleans but not an append-only provenance/hash-chain review ledger that can support a formal review-to-lock firewall;
3. session recovery and provider dispatch exist, but accepted request/audio/alignment/spend evidence is not yet bound into one exact, restart-safe live lineage escrow.

A fourth control was added because the project now has many kinds of PASS: typed proof manifests prevent CI/code evidence from being presented as human/live/provider/economics evidence.

## New bounded modules

- `audio/studio/runtime/provider_snapshot.py`
- `audio/studio/runtime/human_review_evidence.py`
- `audio/studio/runtime/live_evidence_escrow.py`
- `audio/studio/runtime/evidence_proof.py`

## New contract family

`audio/studio/contracts/evidence_frontier/`

Contracts cover provider snapshot, human review event, live evidence escrow and typed proof manifest.

## Protected laws

- no credential persistence;
- TARGETED provider verification != account-wide inventory;
- no auto voice/model substitution;
- provider ACCEPTED != production take ACCEPTED != voice/performance lock;
- human review may create eligibility, never machine lock;
- ambiguous provider response is quarantined, never blindly retried;
- exact canary means exactly the expected lineages, no fourth paid lineage;
- recovery reads durable evidence and never replays paid work;
- PASS_CODE / PASS_CI / PASS_PROVIDER / PASS_LIVE / PASS_HUMAN / PASS_MEASURED remain distinct;
- no new Self-Improvement universal authority from code agreement alone.

## Evidence boundary

This Wave8 cycle has not authenticated an ElevenLabs account, selected a real voice, rendered paid audio, heard pronunciation, produced real alignment, performed human listening or measured real provider economics. Those remain explicit HOLD gates until actual evidence exists.
