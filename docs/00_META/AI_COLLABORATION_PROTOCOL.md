# AI_COLLABORATION_PROTOCOL

Status: MANDATORY / FOUNDER-DIRECTIVE
Date: 2026-07-22
Scope: IVDIVO / CARD GAME / ALL AI AGENTS

## 1. Core law

For this project, any AI agent working on the IVDIVO card game must treat GitHub as the primary machine-readable source of truth for cross-AI collaboration.

```text
If GPT creates, changes, rejects, renames, balances, or systematizes anything meaningful for the game, it must be written to GitHub or to another resource that Claude and other AI agents can open.
```

Google Drive may remain a comfortable human editing layer, especially for spreadsheets, but it is not enough by itself. Every important Google Drive artifact must have a GitHub mirror, index, raw data export, or handoff note.

## 2. Why this protocol exists

The founder works in parallel with GPT, Claude, Codex, Gemini, NotebookLM, and other AI systems.

Therefore, no AI may assume that a local chat answer is sufficient project memory. A useful answer must become project-readable material.

## 3. Required behavior for future AI sessions

When a new substantial development is produced:

1. Create or update the relevant GitHub file.
2. Use clear paths under `docs/` and `docs/04_CARDS/data/`.
3. Mark the status: `FOUNDER-CONFIRMED`, `GAME-DRAFT`, `SOURCE-CANDIDATE`, `TO-PLAYTEST`, `SUPERSEDED`, or `REJECTED`.
4. Add enough context so another AI can continue without reading the original chat.
5. When Drive files are created, add their Drive URL to GitHub.
6. When tables are created, store raw CSV in GitHub whenever possible.
7. When a term is replaced, explicitly mark the old term as superseded.

## 4. Current active branch and PR

```text
Repository: Farada8/IVDIVO_GAME_MASTER
Branch: cards/2026-07-22-card-tables
Pull Request: https://github.com/Farada8/IVDIVO_GAME_MASTER/pull/26
Base branch: worlds/2026-07-22-orbitals-revision
```

## 5. Current active decision

```text
Shelter / Убежище is superseded.
The active model is: Экополис IVDIVO = 32 buildings / organizations / public-institution modules.
```

Do not continue the game using a bunker/shelter frame unless the founder explicitly asks for a rejected/alternate version.

## 6. Current active card packages

The following packages must be visible to Claude and other AI systems:

```text
IVDIVO_144_starter_cards_v0_1_DRAFT
IVDIVO_90_deckbuilding_development_cards_v0_1_DRAFT
IVDIVO_100_instrument_cards_v0_1_DRAFT
IVDIVO_50_form_cards_v0_1_DRAFT
IVDIVO_32_ecopolis_organization_buildings_v0_1_DRAFT
IVDIVO_36_world_law_cards_v0_1_DRAFT
IVDIVO_WORLD_LAWS_MASTER_POOL_v0.2_SOURCE_MERGE
IVDIVO_36_portal_cards_12_vortex_modes_v0_1_DRAFT
```

## 7. Current law-bank direction

World Laws are no longer a single 36-card list. They are becoming a master bank with layers:

```text
- 36 gameplay law cards created for board-game mechanics.
- 36 source-law cards from the PHY/SUB/MET/FIR/SYN/ORB set.
- 36 source-law cards from the PH/SB/MG/FR/SY/OR set.
- 72 expanded high-mode laws from the P/S/M/F/SN/ORB package.
- Founder-confirmed M-27 / Law of 8 Evolutions as a high-mode / FA victory law.
- Further law development from IVDIVO, Theosophy, Blavatsky, Bailey, Mahatmism, Cosmism, Hindu systems, Egyptian/Hermetic lines, and adjacent esoteric/mythic systems.
```

## 8. Handoff rule for Claude

Claude should start from:

```text
docs/00_META/AI_COLLABORATION_PROTOCOL.md
docs/04_CARDS/CARD_TABLES_IMPORT_INDEX_v0.1.md
docs/04_CARDS/PORTALS_AND_VORTEX_MODES_v0.1_DRAFT.md
docs/04_CARDS/data/
```

Then Claude should continue by opening the linked Drive spreadsheets only when it needs human-facing table formatting.

## 9. Non-final status

All card data produced in this stage is draft material for paper playtest and balance work. It is not a final rulebook and must not be treated as final public canon.
