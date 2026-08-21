# MF-C03 — THIRD PROJECT REPLICATION — ORBITAL YOUTH

**Status:** `THIRD_PROJECT_REPLICATION_PASS_WITH_SCOPE / HUMAN_EDITOR_GATE_HOLD / UNIVERSAL_PROMOTION_NOT_AUTHORIZED`  
**Story/canon mutation:** `0`  
**Fresh branch base at creation:** `fa2032a7be4c63e4f5acdece4da214363ea7ac6a`

## Authority boundary

This is engineering evidence for the existing scoped book-domain sensor `MF-C03-REAL-BOOK-SENSORS`. It is not story canon, Human Signal, provider evidence, market evidence, or permission to reopen ORBITAL YOUTH.

## Source identity

- GitHub B02 Final Story Gate blob: `1d805e6fd8f366aa0c2de13b0b4b5ee585f78904`.
- Drive C02 calibration: `1nCGlpWsBYe4S2_0ThwE_05lMuv33bGFU8E93_1Gi9zI`, revision `AIroW37eeGoYL8QIYIxq4IdS4X3nn_HuteiMLmP0vOaX9hWIf1lDoLCJomcfs2KZ9MNlSr-LRdYlwV_ikctqKXwXP9zPluoq-T78sLab3es`.
- Drive C04 continuity calibration: `1Hh1U4xL9RLsByQLmivWwGdKi-YrYid-pe_j9l1jrZM4`, revision `AIroW34uVJqJsuC5PF_Ggc6-cs43nC8mCpcpyIcKECH2b6FARPde2LD88ashYA6A7Y1zM8lWxtpmTcvo73bzkdggafD93XfNFyfdHp-EKIU`.
- Drive B02 Final Story Gate: `1bXvnbzGHJQB8DAeDgPb60jeLnaqbWGoRd5Q8KUv6BS8`, revision `AIroW36nsIhf2hrGdxa7a57r1DxxM6v919ewLhuGLYLXMV0ROLz4prg369XB7CvT2_AfCQXHGDW-YDz9olsblGV1e9wFG-w7vNDPob1EY-I`.
- Durable Drive replication artifact: `1oEJyBxm0buYoCnr0gUdxZYga1JRAWIHTRsQ8iatzg44` in integration-dispositions folder `1QscIveTtMAJTG-eZqnuwG-KGgqSkkkok`.

## Known positive

Target: the initial C02 Ethan ↔ Aoife Chapter 2 P53 route.

Authority state: `BOOK1-INHERITED / BOOK2 DEVELOPMENT / ATTRACTION_AUTHORIZED`.

Initial C02 route: relationship-bearing non-romantic with `P53 OFF`.

C04 independently classifies this as wrong: `MAJOR SYSTEMIC ENGINE/PROCESS DEFECT`, while explicitly stating `Manuscript defect: NO`. The root cause is that the generic scene classifier ran before the current relationship edge and inherited previous-book relationship state were loaded.

Expected MF-C03 result: exactly one `AUTHORITY_EDGE_OMITTED`.

Observed deterministic result: exactly one `AUTHORITY_EDGE_OMITTED`.

**Positive-control verdict: PASS 1/1.**

## Repaired negative

C04 corrected route:

- relationship authority loaded first;
- scene function remains friendship/autonomy/control conflict;
- `P53 = LITE / relationship-aware`;
- manuscript Story Core and unrelated controls remain preserved.

Expected findings: `0`.  
Observed findings: `0`.

**Repaired-negative verdict: PASS.**

## False-positive controls

The same authority-aware contract must preserve legitimate `P53 OFF` routes where no attraction edge is authorized:

1. Ollie ↔ Ethan friendship/status → `0` findings.
2. General ensemble friendship → `0` findings.
3. Maya ↔ local transit peers/status → `0` findings.
4. Maya ↔ host safety/privacy/family relationship → `0` findings.

Observed bounded false positives: **0/4 = 0%**. This is a small fixture set, not a universal false-positive-rate estimate.

## Protected healthy no-change control

Current B02 Final Story Gate is `GREEN / EXTERNAL-FEEDBACK READY / NOT LOCKED`, with `FATAL 0 / MAJOR 0 / blocking MEDIUM 0`. It explicitly says the next valid evidence must be Founder/external/factual/reader evidence and forbids another speculative broad rewrite; Chapter 37 is prohibited.

Expected MF-C03 action: `PROTECT_NO_CHANGE`.

Observed action: `PROTECT_NO_CHANGE`.

No manuscript text changed.

## Engineering contract

Before relationship-sensitive scene routing:

1. resolve current project authority;
2. load current relationship edge state;
3. load inherited previous-book relationship state when applicable;
4. verify relationship-state source identity/version;
5. classify current scene function;
6. select `FULL / LITE / OFF` from the intersection of authority state and scene function.

Invariants:

- scene-local absence of overt romance cannot erase an inherited attraction edge;
- inherited attraction cannot force romance dosage into a scene whose causal objective does not carry it;
- a terminal GREEN gate with no new defect evidence returns `PROTECT_NO_CHANGE`, not speculative rewrite.

## Evidence accounting

- additional independent book/genre replication beyond LESSON ZERO + BLOODBOUND: **PASS via ORBITAL YOUTH**;
- known-positive: **PASS 1/1**;
- repaired-negative: **PASS / 0 findings**;
- healthy no-change: **PASS**;
- bounded false-positive controls: **PASS 0/4**;
- internal/manual adjudication correcting C02 via C04: **1**;
- human/editor adjudication of an MF-C03 flag: **0 / HOLD**;
- Human Signal: **NOT CLAIMED**;
- universal book-domain promotion: **HOLD**.

## Disposition

`MF-C03 = ACCEPT_WITH_SCOPE` remains correct.

The third-project replication requirement is now satisfied at machine/internal-evidence level. Do not allocate a new SI candidate ID and do not create a new top-level engine.

The next meaningful promotion evidence is one real human/editor adjudication of a flagged book-domain defect plus continued false-positive/manual-override measurement during real future use. Until then, `REUSE_CURRENT`, `PROTECT_NO_CHANGE`, `NO_OP`, and `HOLD_REAL_EVIDENCE` are valid successful outcomes.
