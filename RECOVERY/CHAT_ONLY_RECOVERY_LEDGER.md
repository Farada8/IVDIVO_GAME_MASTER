# CHAT-ONLY / UNRECORDED RECOVERY LEDGER — 2026-08-22

**Purpose:** preserve known chat-only decisions and unresolved fragments so chat deletion does not erase their existence.  
**Authority rule:** `RECOVERED_CONTEXT != CANON`.  
**Promotion rule:** every entry remains `CANDIDATE`, `UNRECORDED`, `CONFLICTED`, or `TO_RECOVER` until reconciled with the relevant project authority.

## A. Portals: Ireland

Source evidence: Library `PORTALS_IRELAND_IDEA_REGISTER_v0_1.csv`.

| Recovery ID | Original idea ID | Recovered content | Original status | Recovery action | Authority effect |
|---|---|---|---|---|---|
| PORT-R01 | IDEA-003 | **Card-only physical base**; latest Founder correction overrides map-and-pawn prototype | `CONFIRMED_NOT_RECORDED` | reconcile against latest game authority and persist as Founder decision if still intended | NONE until reconciliation |
| PORT-R02 | IDEA-010 | tourist route through three Dublin locations; vertical-slice/tutorial candidate | `CHAT_ONLY` | recover exact three locations and scenario flow from source chat if available | NONE |
| PORT-R03 | IDEA-014 | science-fiction cards: small base presence, deeper Future expansion | `CHAT_ONLY` | persist as candidate content policy only after founder confirmation/current-version reconciliation | NONE |
| PORT-R04 | IDEA-016 | **Place Verbs** core design asset | `TO_RECOVER` | recover full raw dictionary; current register explicitly says it is missing | NONE; raw asset absent |
| PORT-R05 | IDEA-017 | Seals optional module; function unresolved | `CHAT_ONLY` | recover intended function or mark abandoned | NONE |
| PORT-R06 | IDEA-020 | Leprechaun character/system; avoid caricature; role unresolved | `CHAT_ONLY` | recover exact role or keep out of base canon | NONE |
| PORT-R07 | IDEA-025 | **24 Portals + 40 Memory Places** content architecture | `CONFIRMED_NOT_RECORDED` | reconcile against IDEA-024 `64 locations` conflicted architecture before promotion | NONE |
| PORT-R08 | IDEA-024 | 64 locations | `CONFLICTED` | do not produce content before resolving against 24+40 architecture and current core proof | NONE |

Additional Portals visual/output risk recovered from current work context:
- recent card production was being generated **one card per sheet/output** rather than collage sheets;
- the user repeatedly required **real/consistent dimensions** after size mismatches;
- recent place sequence included **Carna, Barna, Ballyvaghan/Ballyvagan** and nearby cards;
- descriptions above are recovery metadata only. Exact final image bytes, prompts and dimensions must be verified from Library/Drive/source chats before deletion.

`PORTALS_DELETE_GATE = BLOCKED`

## B. Ireland visual cards / murals

Known durable Library examples include:
- `Винтажные туристические постеры Дублина.png`;
- `Концепты фресок Шиллега и Уиклоу.png`;
- individual mural/card PNGs such as the Shillelagh Cartographer’s Room and Dublin location cards.

Known durable style/content metadata includes:
- Ireland vintage travel-poster direction;
- Shillelagh/Wicklow mural concept system;
- Metaphysical-Renaissance-related mural styling exists in durable concept imagery/text.

Recovery gap:
- **complete final binary inventory is not proven**;
- chat-generated variants may include unique images not present in Library/Drive;
- do not infer that a visual is archived merely because its prompt or description survives.

Required closure:
`WANTED_FINAL_IMAGE -> FILE_ID/DRIVE_ID + HASH/NAME + DIMENSIONS + PROJECT/PLACE + CURRENT/REJECTED`.

`VISUAL_DELETE_GATE = ARCHIVE_CHECK_REQUIRED`

## C. Numerical orders / numeral-system research

The following are recovered as **research hypotheses/methodological constraints**, not established mathematics:

### MATH-R01 — representation boundary
`NUMBER != NUMERAL_REPRESENTATION`

Changing numeral base changes representation/encoding of a number; it does not by itself create a new mathematical object or prove a new physical order.

### MATH-R02 — 16-system scheme evidence ceiling
The proposed 16-system / 16-based order architecture is a **search hypothesis**, not an established theorem or empirical fact. Related 32/64/256/4096/16384 structures may be explored, but representation, combinatorial structure, source doctrine and mathematical theorem must remain separate evidence classes.

### MATH-R03 — synthesis-as-new-element growth hypothesis
Recovered current hypothesis: combining a set of elements may produce a synthesis that is treated as a new element which re-enters a higher-order system as an equal participant. Examples discussed conversationally included “two elements -> third” and a whole/synthesis becoming the next element.

Status: `HYPOTHESIS / FORMALIZATION_REQUIRED`.

Required formalization:
- define element set/domain;
- define synthesis operator;
- define whether synthesis is associative/commutative/idempotent;
- define embedding/re-entry map;
- distinguish cardinality growth from representation change;
- specify invariants;
- identify counterexamples;
- test whether the proposed next-tier operation is mathematically nontrivial.

### MATH-R04 — tier/order iteration hypothesis
Recovered idea: a complete whole at one tier can participate in a new synthesis at the next tier, iteratively producing a hierarchy/order structure.

Status: `HYPOTHESIS / NOT YET FORMAL MODEL`.

Do not write `MATH-R03` or `MATH-R04` as proven facts in future work.

Library evidence relevant to this research includes Paradigma source text and working reports such as `Механика_тонких_тел_и_64_видов_материи_IVDIVO_v0_1`, which itself explicitly treats some 16,384 structures as research architecture rather than established anatomy.

`MATH_DELETE_GATE = BLOCKED_UNTIL_CURRENT_RESEARCH_NOTE_IS_ACCEPTED`

## D. IVDIVO cosmology / synthetic-life / consciousness-transfer research

Recovered project themes that should not be lost if chats disappear:
- artificial/synthetic life and specially created bodies;
- possible embodiment/transfer of consciousness into engineered carriers;
- bodies adapted for vacuum/ocean/extreme environments;
- AI/robotic/synthetic embodiment as a technological branch;
- layered civilisational/world architecture;
- distinction between sourced doctrine, authored extrapolation, speculative engineering and fiction/worldbuilding.

Authority boundary:
`SOURCE_QUOTE != USER_HYPOTHESIS != ENGINEERING_POSSIBILITY != FICTION_CANON`.

The Library contains durable related research, but a single definitive current state was not verified in this audit. Preserve this entry as a recovery pointer, not a doctrinal truth claim.

## E. Website / physical-business chat recovery

### painters-dublin.ie
Known project-level recovery metadata:
- service-business website for Dublin painting/insulation work;
- WordPress + Elementor Pro direction;
- portfolio/reviews/contact/WhatsApp/GBP/Stripe integration concepts existed in planning.

No current export/config handoff was verified in this audit. Never store passwords, API keys, cookies or private credentials in this ledger/GitHub.

### FARADA modular buildings / windows-doors
Detailed generated spreadsheet artifacts survive in Library, including RFQ/BOM data. The project is therefore not chat-only, but its canonical CURRENT pointer remains to be created if promoted to active production.

## F. Audio binary safety

Text authority does not prove that wanted audio binaries are archived.

Before deleting audio-production chats, verify for each wanted render:
- project/episode/chapter;
- provider/request id if applicable;
- WAV/MP3 file outside chat;
- alignment/QC file if required;
- hash or stable Drive/File Library id;
- current/rejected status.

Projects explicitly affected: B03 audio, ROOM917, D01 and any other live audio adaptation.

## G. Global deletion guard

`KNOWN_CHAT_ONLY_COUNT > 0 -> DELETE_ALL_CHATS = BLOCKED`

Current known blockers include Portals items and incomplete binary inventory for visual/audio outputs.

The existence of this ledger protects **knowledge that a gap exists**. It does not recreate missing raw files.

`CHAT_ONLY_RECOVERY_MARKER: IVDIVO-CHAT-ONLY-RECOVERY-20260822-V1-NO-AUTO-CANON`
