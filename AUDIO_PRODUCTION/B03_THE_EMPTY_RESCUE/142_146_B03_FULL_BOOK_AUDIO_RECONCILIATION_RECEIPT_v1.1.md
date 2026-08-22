# B03 — FULL-BOOK AUDIO RECONCILIATION RECEIPT — 142–146 v1.1

**Date:** 2026-08-22  
**Story authority:** FOUNDER-LOCKED CH01–29  
**Story text mutation:** 0 bytes  
**CH30:** not authorized

## Result

The full-book offline audio routing chain has been rebuilt against the current chapter-local speaker authority rather than the superseded 120/121 ancestry.

### 142 — full speaker manifest rebuild
- actual cast speech: **3714 / 3714**
- UNKNOWN speaker ownership: **0**
- exact-text hash mismatches: **0**
- stale 120 speaker-label / ownership divergences found: **291**
- Drive current manifest: `1qry9Pr2iW3qtlu19PAe-lm14tue4QC2T`
- Drive stale-120 diff: `1FkYxNZW3rEHZwqWj84zVhyp5YDRtHMUR`

### 143 — voice roster normalization
- acoustic speaker IDs: **119**
- cast slots: **28**
- ensemble slot collisions: **0**
- provider voice IDs assigned: **0**
- CH24 Packet 1 / Packet 2 remain separate source identities; relationship UNKNOWN
- CH27 S0136: source author `TAREN_SOR`, acoustic reader `SMITH`
- Drive architecture: `13Go1HxW86AmYf7dfptH8o1QzihCqexSL`
- Drive gate: `1p2A29eLYryoAKE3DAOjNMbYj8DVGxDs9`
- Drive package: `1L_EjMpS-RrjI9pKjrHZBF4RbcMwN1ztw`
- package SHA-256: `376d75e7aa80fe0d54f75f03f28bf572c9f7da32bb2ba8b942c16a2ce463fe11`

### 144 — performance chain reconciliation
Repaired only authority-dependent fields; exact text remained immutable.

- speaker fields repaired: **291**
- cast-slot fields repaired: **287**
- performance-profile fields repaired: **88**
- delivery-mode fields repaired: **73**
- exact-text changes: **0**
- Drive baseline: `1GRn1qMGtRlXIh7U-ILkLQu2RbtqeB4CM`
- Drive manifest: `1cagXHO9RYgClgb9J193tNl6vYQ_0OITh`
- Drive gate: `1nH0qdcKr3l-ki5HT49pDuhzxwXEIYSbg`
- Drive package: `1flgkma50KX9efc5rBOfbosGcNsmXSRRq`
- package SHA-256: `a8702f3f03dda46d409f7eef9b0ff0d9fbffc0dfde0e3b53e09270a9b8abe0e2`

### 145 — SFX / acoustic / asset linkage
SFX and acoustic semantics were retained where speaker-independent; production pointers were rebound to the current speaker/roster authority.

- SFX architecture Drive: `1anh7qx2GpVv5bNJaNl07hWop1SrBpizm`
- asset/acoustic manifest Drive: `1E_qiZgVExCOdMt3HvhvON1EfRo2Zf8Dw`

### 146 — dry render reconciliation
- exact-text units: **7465 / 7465**
- speech units: **3714**
- narration units: **3751**
- hash mismatches: **0**
- unmapped cast slots: **0**
- Drive manifest: `16N5TX8c5NBOX7hC0F7zvX5QQKB5Rqr-b`
- Drive gate: `1tL8pvpB_F6feFB4SoBTRyh_vDEJjIHk-`
- Drive package: `1Y6t6QE0DTLGUDrLbKehy3TO7Lhz1piyE`
- package SHA-256: `6574f2ed49acdcf9662aa552cf8eb91aaf9063d934ce0dc5927924bedf6db7cc`

## Superseded production routing

The following historical artifacts remain available for provenance but must not seed current production:
- 120 full speaker manifest / gate
- 121 voice-map architecture / gate
- 122 old performance baseline
- 123 old segment-level performance manifest / package / gate
- 126 old dry-render manifest / package

## Authority boundary

`599` is the deterministic engine-verified subset.  
`3714/3714` is the chapter-local production speaker authority.  
These are separate evidence layers and must never be conflated.

## Current frontier

**OFFLINE FULL-BOOK AUDIO ROUTING = RECONCILED.**

Next authorized gate:
`147 — CASTING MANIFEST + SLOVENIAN PRONUNCIATION ADJUDICATION QUEUE`

Requirements:
- 28 cast slots
- `voice_id = null` until real casting evidence
- no invented accent / IPA
- no bulk render
- only bounded S0 auditions after provider inventory, source-hash recheck and pronunciation adjudication
- no API keys or secrets in GitHub or Drive
