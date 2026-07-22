# ENTITY_INTERACTION_CARDS_v0.1_DRAFT — note

Status: DRAFT / TO-PLAYTEST / LOCAL-FULL-TABLE-GENERATED
Date: 2026-07-22
Section: docs/04_CARDS

## Purpose

This note records the generated entity-interaction card package requested by the founder:

- 50 World Inhabitant cards;
- 36 Ally cards;
- 24 Mediator cards.

The full table was generated in the working environment as:

- `ENTITY_INTERACTION_CARDS_v0.1_DRAFT.xlsx`
- `ENTITY_INTERACTION_CARDS_v0.1_DRAFT.csv`
- `ENTITY_INTERACTION_CARDS_v0.1_DRAFT.md`

## Required columns

```text
ID, колода, название, мир/орбиталь, тип существа, что предлагает, что требует, риск, как получить помощь, как потерять, связанная колода, тестовая заметка
```

## Design rule

These cards are not simple enemies. Each card is an encounter with a choice:

```text
help / bargain / test / information / price / consequence
```

## Source grounding

The package was generated against the active 2026-07-22 state:

- PROJECT_CORE_CONTEXT_2026 v1.6: 5 vertical worlds + orbital/parallel worlds.
- WORLD_ARCHITECTURE_v0.2_APPROVED / WORLD-002: old 8-world vertical is superseded.
- WORLDS_AND_PARALLEL_WORLDS_SCHEMA_v0.1_FOUNDER_CONFIRMED: current orbital schema.
- WORLD_INHABITANTS_AND_TOOLS_v0.1_DRAFT: inhabitants are defined by origin world + scale + function + tools + abilities + limitations + influence + game role.
- CARD_TABLES_IMPORT_INDEX / PR #26: current card package context; Ecopolis replaces Shelter.

## Internal distribution

### World Inhabitants — 50 cards

- 6 Physical World inhabitants.
- 6 Thin World inhabitants.
- 6 Metagalactic World inhabitants.
- 6 Fire World inhabitants.
- 6 Synthesis World inhabitants.
- 20 orbital inhabitants across Paradise, Fey/Leprechaun world, unified lower world, Ray Teachers, Ashtar/Sirius, Angelic civilization, Arcana, Mahatmas/64/Sanat, Sephiroth/Elohim, 99 Names, Christ/Maitreya.

### Allies — 36 cards

Allies are recruitable helpers tied to Ecopolis, routes, Forms, Portals, World Laws, deckbuilding development, campaign memory, and player roles. They are not passive bonuses; each requires trust, payment, repair, protection, shared mission, or ethical conduct.

### Mediators — 24 cards

Mediators are forces between worlds. They may help, obstruct, trade, redirect routes, sell permission, demand memory, alter orbital timing, or reveal hidden transition laws. They are especially linked to the earlier founder idea of mediators between sleeping and awakened states.

## Current storage status

A full `.xlsx` and `.csv` table exists in the current GPT runtime, and a Google Drive note was created in `04_КАРТЫ_И_КОМПОНЕНТЫ`:

```text
ENTITY_INTERACTION_CARDS_v0.1_DRAFT__DRIVE_NOTE
https://docs.google.com/document/d/1rcUex-4LzjZHO4ZJW877Pvz1l7VrTZe4zuE6qYKOBpE/edit
```

However, the full raw CSV has not yet been mirrored into GitHub through the connector because this runtime connector does not accept local sandbox file paths as GitHub/Drive upload file references.

## Next required completion

1. Import `ENTITY_INTERACTION_CARDS_v0.1_DRAFT.xlsx` into Google Drive as a native Google Sheet.
2. Commit `ENTITY_INTERACTION_CARDS_v0.1_DRAFT.csv` under `docs/04_CARDS/data/`.
3. Replace this note with a full raw-data mirror once connector/file upload is available.
4. Link the final table from `CARD_TABLES_IMPORT_INDEX_v0.1.md`, `DOCUMENT_REGISTRY.md`, and `CHANGELOG.md`.

## Non-final status

This package is not final rulebook content. It is DRAFT interaction material for paper playtest and balance screening.