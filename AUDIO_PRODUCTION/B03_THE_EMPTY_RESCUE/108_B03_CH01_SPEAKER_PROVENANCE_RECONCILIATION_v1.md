# 108 — B03 CH01 SPEAKER PROVENANCE RECONCILIATION v1

**Date:** 2026-08-22  
**Story authority:** FOUNDER-LOCKED CH01–29  
**Text policy:** IMMUTABLE EXACT TEXT  
**Result:** **PASS — 142/142 CH01 quoted turns reconciled; provider bridge preserved**

## Scope
This audit tests the private CH01 production speaker assignments independently from the rejected whole-book speaker autopass/Tier-1 maps. It does not publish the full exact-text payload.

## Evidence
- locked CH01 source SHA256: `bf92a22bf42e00a75fd9d5247b95748e463975947909eb102308800b01d50b7d`
- private CH01 segmentation/speaker map: Drive `1aw17696W4KOLVgCcnOkKxpaOJE15YRMg`
- quoted dialogue turns audited: **142/142**
- speaker conflicts found: **0**
- corrected strict explicit anchors: **6/6 agree**
- turns additionally constrained by single-speaker scene/channel ownership: **62**
- remaining multi-party turns contextually checked against local narration/turn chain: **80**

A known counterexample proves the CH01 production map did not blindly inherit the flawed whole-book autopass: old autopass assigned `What noise?` to Nika by reusing `Nika asked.` bidirectionally; the CH01 production map correctly assigns that turn to `RESCUER_FIELD_RADIO`.

## Disposition
- CH01 speaker map: **PASS**.
- CH01 downstream voice/director/render/provider-bridge artifacts: **NOT quarantined by this repair**.
- current CH01 stage remains `PROVIDER_BRIDGE_READY / LIVE EVIDENCE REQUIRED`.
- this PASS does **not** authorize extrapolation to CH02–29.

Private reconciliation evidence:
- Drive JSON `10WMtxygCb24N2XnBZeL6z0-B0PJUZZFY`
- Drive MD `1ofWRzJoeWpidY0BkOGJsOqQKHMMnygLC`

No story/prose bytes changed.
