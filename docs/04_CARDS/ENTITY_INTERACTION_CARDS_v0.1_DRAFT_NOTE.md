# ENTITY_INTERACTION_CARDS_v0.1_DRAFT — note

Status: DRAFT / TO-PLAYTEST / FULL-DATA-MIRRORED-AS-CSV-PARTS
Date: 2026-07-22
Section: docs/04_CARDS

## Purpose

This note records the generated entity-interaction card package requested by the founder:

- 50 World Inhabitant cards;
- 36 Ally cards;
- 24 Mediator cards;
- 110 total cards.

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

## Google Drive storage

The full package has been imported into Google Drive as a native Google Sheet and moved to `04_КАРТЫ_И_КОМПОНЕНТЫ`:

```text
ENTITY_INTERACTION_CARDS_v0.1_DRAFT
https://docs.google.com/spreadsheets/d/1Y14rkCOPWCcVUNeiCkMyMAqACFXGHyhJF-qMRzTPOtk/edit
```

A previous Drive note also exists:

```text
ENTITY_INTERACTION_CARDS_v0.1_DRAFT__DRIVE_NOTE
https://docs.google.com/document/d/1rcUex-4LzjZHO4ZJW877Pvz1l7VrTZe4zuE6qYKOBpE/edit
```

## GitHub raw-data mirror

The full raw card data is mirrored in this PR as CSV parts under `docs/04_CARDS/data/`:

```text
docs/04_CARDS/data/ENTITY_INTERACTION_CARDS_v0.1_DRAFT_part01_inhabitants_001_030.csv
docs/04_CARDS/data/ENTITY_INTERACTION_CARDS_v0.1_DRAFT_part02_inhabitants_031_050_allies_001_010.csv
docs/04_CARDS/data/ENTITY_INTERACTION_CARDS_v0.1_DRAFT_part03_allies_011_036.csv
docs/04_CARDS/data/ENTITY_INTERACTION_CARDS_v0.1_DRAFT_part04_mediators_001_024.csv
```

Why split: the connector accepts UTF-8 text writes reliably; binary XLSX and large single-file local uploads are not available through the current GitHub connector. The four CSV parts together contain all 110 cards and preserve the required columns.

## Next integration tasks

1. Optionally concatenate the four CSV parts into one raw CSV when a direct file-upload path is available.
2. Link the package from `CARD_TABLES_IMPORT_INDEX_v0.1.md`, `DOCUMENT_REGISTRY.md`, and `CHANGELOG.md` in the next cards-index PR.
3. Run paper playtest and mark weak/overpowered cards.

## Non-final status

This package is not final rulebook content. It is DRAFT interaction material for paper playtest and balance screening.
