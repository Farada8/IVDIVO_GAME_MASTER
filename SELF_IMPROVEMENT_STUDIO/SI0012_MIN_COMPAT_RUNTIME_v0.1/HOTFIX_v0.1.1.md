# SI-0012 v0.1.1 — LIVE-SCHEMA HOTFIX

**Status:** PILOT HOTFIX / NOT CURRENT AUTHORITY  
**Trigger:** real concurrent D04 state advance after v0.1 packaging.

D04 advanced to schema 1.4:
- G0 internal preflight PASS / external binding blocked;
- G4 transfer prototype `MACHINE_PASS_HUMAN_LISTENER_PACKET_READY`;
- current blocker `HUMAN_SIGNAL_REQUIRED_FOR_G4_PERCEPTUAL_PASS`;
- `next_action` changed from a dict-shaped execution contract to a **string** instruction.

This exposed a real compatibility defect: v0.1 assumed `(next_action or {}).get(...)` and could not consume the new shape.

## v0.1.1 repair
1. Accept dict or string `next_action` without flattening semantics.
2. `HUMAN` / `LISTENER` blocker -> `HUMAN_EVIDENCE_REQUIRED`.
3. `PROVIDER` blocker -> `EXTERNAL_PROVIDER_REQUIRED`.
4. Retain exact protected audio facts, including `Hold the second transfer.`.
5. Never promote machine metrics to Human Signal.

## Regression
- v0.1.1 warm: **40/40 PASS**.
- v0.1.1 final cold extraction: **40/40 PASS**.
- New real D04 v1.4 fixture correctly STOPs on Human Signal instead of replaying the now-stale zero-cost preflight obligation.

## Durable package
Drive folder: `1Z8vbvdpsSbTXYWoCPryFMOonr659tzsb`  
ZIP Drive ID: `1oacUip8tDABFePzjdAx-8Xn-7BJDLSYM`  
ZIP SHA256: `530e2d3414bdc7fa8e1b6ef4909d826389cf947d46451cad6820fbb84808e287`

v0.1 remains immutable historical package evidence; v0.1.1 is its compatibility hotfix.