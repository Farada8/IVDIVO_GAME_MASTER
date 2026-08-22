# IVDIVO — BOOK INTELLIGENCE — ALL-ENGINE ADAPTER + INTEGRATION CONTRACT v1.0

**Status:** CURRENT INTEGRATION CONTRACT  
**Established:** 2026-08-22

## 1. Mandatory gateway

When any IVDIVO engine materially uses a book/manual/paper/script/long-form reference to make a production or architecture decision, route through:

`BOOK_INTELLIGENCE_ENGINE/00_BOOK_INTELLIGENCE_ENGINE_CANON_v1.0.md`.

Existing domain book modules are implementations/subsystems, not competing top-level authorities.

## 2. Call contract

Input:
- `domain`
- `active_project`
- `task`
- `current_authority`
- `protected_invariants`
- `evidence_needed`
- `max_mechanisms` default 3.

Book Engine returns:
- selected `source_ids`;
- selected `mechanism_ids`;
- lifecycle/disposition of each;
- evidence locators;
- failure modes / contraindications;
- explicit unknowns;
- test and rollback;
- whether a fresh raw-source read is actually necessary.

No production engine consumes raw book text as an untyped blob when a current MechanismCard exists.

## 3. Domain bindings

| Domain | Existing layer retained | New rule |
|---|---|---|
| Story/Narrative | Reference Intelligence, Source Passports, Mechanism Banks, strict craft lifecycle | all fresh reference use enters via Book Engine then Story Adapter |
| Audio | Audio Reference Intelligence / production evidence | books can suggest mechanisms; provider/render/listener evidence remains separate |
| Business | B01–B08 library/source modules and later Business Engineering modules | B01–B08 become Business-side implementation of universal SourcePassport/Mechanism contracts |
| Self-Improvement | Learning Ledger, Improvement Registry, v2 engine | book-derived architecture changes require Book Engine provenance + bounded pilot |
| Research | project-specific research methods | use claim/evidence/contradiction/provenance objects; never promote hypothesis by repetition |
| Game/Visual/Operations | local reference packs | use shared AdapterPacket contract and domain-specific validation |

## 4. Story adapter contract

`task -> retrieve current mechanism bank -> max 3 -> verify source status -> bind to scene/chapter problem -> preserve project authority -> run local story gate -> return result evidence`.

Forbidden:
- copying a reference scene;
- reopening a locked book solely because a new source exists;
- replacing story judgment with mechanism counts.

## 5. Audio adapter contract

Book evidence may inform:
- performance direction;
- acoustic workflow;
- reliability;
- evaluation design;
- sound dramaturgy.

Book evidence cannot prove:
- voice quality;
- pronunciation;
- provider capability;
- render correctness;
- listener comprehension;
- commercial audio quality.

Those require the appropriate live evidence.

## 6. Business adapter contract

Book evidence may inform:
- opportunity framing;
- experiment design;
- unit economics models;
- systems/constraint analysis;
- acquisition structure;
- decision hygiene.

Book evidence cannot prove:
- current tender requirement;
- bidder eligibility;
- customer demand;
- willingness to pay;
- payment;
- repeat purchase;
- current legal/tax/company status.

`KNOWLEDGE PROOF != MARKET/TRANSACTION PROOF`.

## 7. Self-Improvement adapter contract

Book-derived improvement path:

`observed production defect`
→ `retrieve mechanism`
→ `architecture/process candidate`
→ `dedupe against current registry`
→ `bounded implementation`
→ `verification`
→ `real project validation`
→ `second-project replication`
→ `promotion`.

Do not create a new engine because a book has an attractive taxonomy. Prefer modifying/reusing existing modules unless an interface gap is demonstrated.

## 8. Research adapter contract

Every nontrivial source claim must preserve:
`CLAIM -> LOCATOR -> SOURCE -> ACCESS -> INTERPRETATION -> ALTERNATIVE -> CORROBORATION`.

Differentiate:
- source says X;
- model infers Y from X;
- project hypothesizes Z;
- experiment supports/refutes Z.

## 9. Failure handling

If:
- source missing -> `SOURCE_UNAVAILABLE`;
- book only indexed -> `NOT_FULL_READ`;
- claim lacks locator -> `UNBOUND_CLAIM`;
- duplicate copy -> `DUPLICATE_ZERO_WEIGHT`;
- source conflict -> `CONTRADICTION_SET_REQUIRED`;
- rights unclear -> `NO_REDISTRIBUTION`;
- project evidence absent -> `LOCAL_TEST/PILOT_READY`, never universal;
- FATAL/MAJOR regression -> `REJECT_OR_ROLLBACK`.

## 10. Write-through targets

Accepted universal book-engine improvements must update, as applicable:
1. Book Engine canon/schema/runtime/tests;
2. affected domain router;
3. `CURRENT_IVDIVO_SYSTEM_STATE.json`;
4. Self-Improvement Learning Ledger / Improvement Registry when the change is a reusable learning;
5. current prompts/runbooks;
6. Drive working mirror/index;
7. readback verification.

## 11. Migration rule

Legacy book/reference outputs are not invalidated wholesale.

They are classified:
- `COMPATIBLE_CURRENT`
- `NEEDS_SOURCE_PASSPORT_BACKFILL`
- `NEEDS_LOCATOR_BACKFILL`
- `DUPLICATE`
- `STALE`
- `REJECT`.

Migration is lazy/problem-targeted unless a missing provenance field is blocking a real decision.

## 12. Acceptance

This integration is considered engineering-ready when:
- universal canon exists;
- schema exists;
- source manifest exists;
- 32-pass prompt program exists;
- runtime tool exists;
- contract tests exist;
- Narrative reference router points to Book Engine;
- aggregate system state points to Book Engine;
- Drive mirror exists;
- at least one real domain pilot remains explicitly scheduled rather than simulated.

**BOOKS FEED MECHANISMS. MECHANISMS FEED ADAPTERS. ADAPTERS FEED REAL WORK. REAL RESULTS FEED LEARNING.**
