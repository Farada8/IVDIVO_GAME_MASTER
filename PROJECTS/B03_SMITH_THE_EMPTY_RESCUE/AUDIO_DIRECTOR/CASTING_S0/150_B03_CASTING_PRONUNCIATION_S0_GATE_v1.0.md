# 150_B03 — CASTING + PRONUNCIATION + BOUNDED S0 GATE v1.0

**Status:** PASS — PROVIDER-NEUTRAL PREPARATION COMPLETE / LIVE PROVIDER EXECUTION NOT RUN  
**Story authority:** FOUNDER-LOCKED CH01–29  
**Locked prose mutation:** 0 bytes  
**Provider voice IDs assigned:** 0  
**Provider dispatch:** false  
**Voice lock:** false

## Authorities
- Full Speaker Gate v1.2 — Drive `1lFmVbEZJSMnCZMn65nAEV5U-rESC-qFX`.
- Rebuilt speaker manifest v1.1 — Drive `1qry9Pr2iW3qtlu19PAe-lm14tue4QC2T`.
- Voice roster/cast architecture v1.1 — Drive `13Go1HxW86AmYf7dfptH8o1QzihCqexSL`.
- Segment-level performance v1.1 reconciled — Drive `1nH0qdcKr3l-ki5HT49pDuhzxwXEIYSbg`.
- Dry Render Manifest v1.2 reconciled — Drive `1tL8pvpB_F6feFB4SoBTRyh_vDEJjIHk-`.
- Full-book Scene-Bed Routing Gate v1.0 — Drive `1EJm6hG81a3a4MXebpDtro-8o0-II2hEc`.
- Provider Execution Bridge v1 — Drive `1sIQNV0p12f1XRtwSRQCnps2kBMB6DTTl`.
- Exact segmentation package SHA-256 `4f7f779fc42007f384512cb1e1cef84a98ef0c0756f010404a835e204e05c0ac`.

## New artifacts
- `147_B03_CASTING_MANIFEST_v1.0_PROVIDER_NEUTRAL.json` — 28 cast slots, all `provider_voice_id=null`; SHA-256 `b36ea4b852cc35a7d046604d85ba98b1e41488f85c0c947787d0083b8b5e8ea2`; 45307 bytes.
- `148_B03_SLOVENIAN_PRONUNCIATION_EVIDENCE_LEDGER_v1.0.json` — 15 locked-text terms, 0 accepted pronunciations, no invented IPA; SHA-256 `9c7667de2aee46e83f0ad66c2a4b0e9a7cea74cb79a7c6e04d493f0e2157ca57`; 6469 bytes.
- `149_B03_S0_BOUNDED_REQUEST_PACKET_v1.0.json` — exactly 4 prepared jobs, dispatch false; SHA-256 `9415e7887b5aaac8679c14c24f3db1164b906be889c720cc4e934a1800a6808c`; 5389 bytes.

## S0 selection
The four S0 jobs are selected by **current delivery volume**, not taste:
1. `V_NARRATOR` / NARRATOR — 3751 delivery segments.
2. `V_D02` / JANA_KOVAC — 912 speech segments.
3. `V_D01` / SMITH — 817 speech segments.
4. `V_D03` / NIKA_ZUPAN — 423 speech segments.

This is a cost-control engineering choice for the first bounded provider test. It is **not** a cast lock.

## Pronunciation boundary
No IPA, phonetic hint, accent or dialect is invented. Every listed term remains `OPEN_TRUSTED_NATIVE_EVIDENCE_REQUIRED` until a trusted/native source, a real provider candidate take and human listening adjudication exist.

## Red Team
PASS:
- 28/28 cast slots present.
- 0 non-null provider voice IDs.
- 4/4 S0 jobs prepared; no fifth job.
- Selected S0 slots are delivery-volume ranks 1–4.
- All three dialogue S0 samples match current speaker authority.
- All S0 sample exact-text hashes recomputed from locked segmentation.
- CH24 packet source separation remains untouched.
- CH27 source-author/acoustic-speaker law remains untouched.
- CH29 current speaker repairs remain upstream authority.
- Provider/model enumeration not claimed.
- Provider dispatch false.
- Bulk render false.
- Story text mutation 0 bytes.

## Next allowed action
Authenticate a real provider context, enumerate actual workspace voices/models **read-only**, bind temporary audition candidates to S0 only, recheck hashes, and dispatch **exactly four** S0 jobs. Human listening + pronunciation adjudication is required before any voice lock or CH01 Hard Pilot.
