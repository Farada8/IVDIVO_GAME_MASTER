# IVDIVO AUDIO NOVEL ENGINE — WAVE6 POST-RENDER HARDENING

**Date:** 2026-08-21  
**Status:** ACTIVE ENGINEERING CYCLE / 32 SEQUENTIAL TASKS  
**Canonical runtime target:** `audio/studio/runtime`  
**No new parallel engine is authorized.**

## Why Wave6 exists

Fresh parallel readback changed the task while work was underway:
- Wave4 production-control has merged to `main`.
- Studio Evidence has merged to `main`.
- Wave5 convergence has merged to `main` with 32 prior convergence prompts and a 64-item Wave6 evidence bank.
- ROOM917 post-render engineering v2 now exists as a real project pilot.
- Self-Improvement has captured that pilot as `SI-0009` with `PILOT_PASS`, but domain promotion remains blocked by second-project replication and real human evidence.

Therefore Wave6 does **not** invent another architecture. It hardens concrete weaknesses exposed by the project pilot and converts only reusable mechanisms into project-neutral runtime contracts.

## Engineering thesis

`CLASSIFIER CANDIDATE != PATCH AUTHORIZATION`

A candidate repair may change accepted audio bytes only after:

`MASTER SHA`
→ `ACCEPTED TIMING`
→ `PROTECTED TIMING COMPLETE`
→ `ONE BED DOMAIN`
→ `ASSET SHA + RIGHTS + 48K + CHANNELS + EXPLICIT GAIN`
→ `HEADROOM PASS`
→ `DETERMINISTIC AUTHORIZATION HASH`
→ `PATCH LEDGER`
→ `BOUNDED RENDER`
→ `PROJECT-NEUTRAL BYTE REGRESSION`
→ `PCM CLIP/SEAM QC`
→ `REAL HUMAN LISTEN`.

## Current concrete deltas implemented in this branch

Universal runtime candidates:
- `audio/studio/runtime/post_render_contracts.py`
- `audio/studio/runtime/post_render_engineering.py`
- `audio/studio/runtime/post_render_learning.py`
- `audio/studio/runtime/post_render_pcm_qc.py`

Universal machine-contract family:
- `audio/studio/contracts/post_render/`

Regression suites:
- `test_post_render_contracts.py`
- `test_post_render_engineering.py`
- `test_post_render_learning.py`
- `test_post_render_pcm_qc.py`
- `test_post_render_universal_leakage.py`

## Evidence firewall

This cycle may prove deterministic engineering behavior. It may **not** claim:
- real ROOM917 repair timing where accepted timing is absent;
- human P003B listening;
- provider quality or voice locks;
- real economics not measured from provider evidence;
- domain promotion from a single project;
- Production Ready.

## Cycle output

1. parallel delta analysis;
2. 32 sequential engineering prompts + execution report;
3. concrete modules and JSON contracts;
4. CI + Red Team;
5. Self-Improvement reconciliation;
6. path to the next empirical gate;
7. 64 follow-up prompts derived from actual Wave6 outcomes;
8. GitHub + Google Drive mirror/readback.
