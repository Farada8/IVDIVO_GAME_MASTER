# SI-0012 v0.1 — TEST + REAL PERSISTED-STATE PILOT REPORT

**Status:** ENGINEERING PASS / CANDIDATE EVIDENCE ONLY  
**Date:** 2026-08-21

## Regression history

Initial suite: **35/36 PASS**. The failed negative test proved that the State Adapter accepted an unknown domain instead of failing closed. The implementation was changed; the test was not weakened.

Rerun: **36/36 PASS**.  
Final cold-extraction rerun from the packaged ZIP: **36/36 PASS**.

Covered contracts include Founder gates, authority/frontier split, WORKING PR freshness, protected audio facts, parallel branches, ROOM917 tool blocker, assertion grades, stale/no-effect transaction rejection, readback mismatch -> `REPAIR_REQUIRED`, package identity immutability and unsupported-domain fail-closed.

## Real persisted-state routing pilots

### D09 — THE MAN WHO CAME BACK
Result: `STOP / FOUNDER_DECISION_REQUIRED`.
Protected result: no E25; no reopening passed Final Story Gate.

### D10 — BLOODBOUND
Fresh state used: E01-E24 text complete; Final Story Gate PASS; Founder Lock not issued.
Result: `STOP / FOUNDER_DECISION_REQUIRED`.
Protected result: no more D10 prose/E25.

### THE WIFE AT HIS WEDDING
Authority source: merged-main project execution state.
Fresher compatible work frontier: PR #85 `wife/wave2-e91-95-32x64-2026-08-21` (`WORKING_SYNC_PENDING`).
Result: main remains authority; PR #85 becomes work frontier; route = `RUN_WAVE3_PROMPT_01_FRESHNESS_DESCENDANT_REUSE_GATE`.
Regression prevented: runtime does not fall back to old E91 drafting instruction.
Human Signal / jurisdiction-specific legal review / real listener validation remain external.

### D04 — SEVEN NIGHTS BEFORE CODE BLUE
Source: `PROJECT_STATES/D04_SEVEN_NIGHTS_BEFORE_CODE_BLUE_CURRENT_STATE.json`.
Result: route to provider-neutral casting auditions + zero-cost audio preflight.
Protected facts carried upstream into task packet, including exact radio line `Hold the second transfer.` and required transfer contrast in mono/phone playback.
Live provider evidence is explicitly absent; no live render or voice lock is claimed.

### ROOM917
Source: `AUDIO_PRODUCTION/ROOM917/CURRENT_EXECUTION_STATE.json` v3.3.
Result: `STOP / TOOL_RUNTIME_LIMITATION` at `P003A2_PRE_SCENE3_INTERVAL_LOCALIZATION`.
Protected result: does not restart S0/S1, does not blanket-fill low-level windows, does not use music as substitute for missing room bed/causal Foley.

### Package-vs-main identity
`IVDIVO_ENGINE_v11_2_CONTINUOUS_EXECUTION_CURRENT.zip` remains the exact 290/290 package. Newer GitHub-main extensions are not silently relabeled as contents of v11.2. A new package build/checksum is required before advancing the package pointer.

## Claim limits

These results prove bounded routing/execution-contract behavior only. They do **not** prove literary quality, Human Signal, live-provider quality, casting, alignment/mix, economics, market demand or two-model parity.