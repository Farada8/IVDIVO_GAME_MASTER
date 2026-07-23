# REPOSITORY_STRUCTURE_v0.1_DRAFT — GAME_01_PORTALS_OF_STARS

Status: DRAFT / REPOSITORY ORGANIZATION  
Date: 2026-07-23  
Game: Portals of Stars  
Master repo: `Farada8/IVDIVO_GAME_MASTER`

## 1. Repository decision

At the current stage, **Portals of Stars should live inside the master IVDIVO repository**, not in a separate standalone GitHub repo.

Reason:

- the game is still being shaped as part of the wider IVDIVO tabletop/IP universe;
- design documents, world logic, mechanics, Kickstarter planning, and franchise thinking are shared;
- a monorepo keeps AI and human collaborators aligned;
- a separate repo can be created later when the prototype becomes a clean standalone product.

## 2. Current canonical GitHub location

```text
Farada8/IVDIVO_GAME_MASTER
└── docs/20_GAMES/GAME_01_PORTALS_OF_STARS/
```

This is the dedicated product workspace for the Portals of Stars game.

## 3. Future optional standalone repo

If the game becomes a separate product line, recommended standalone repository name:

```text
Farada8/portals-of-stars
```

Alternative public-facing names:

```text
Farada8/portals-game
Farada8/portals-of-stars-board-game
Farada8/sparks-and-portals
```

Preferred: `portals-of-stars`.

## 4. Folder structure

```text
docs/20_GAMES/GAME_01_PORTALS_OF_STARS/
  README.md

  00_INDEX/
    REPOSITORY_STRUCTURE_v0.1_DRAFT.md
    MASTER_INDEX_v0.1_DRAFT.md
    DECISIONS_v0.1_DRAFT.md
    CHANGELOG_v0.1_DRAFT.md

  01_CORE_RULES/
    PORTALS_QUICK_RULES_v0.1_DRAFT.md
    PORTALS_TURN_STRUCTURE_v0.1_DRAFT.md
    PORTALS_VICTORY_MODES_v0.1_DRAFT.md

  02_BOARD/
    PORTALS_LIVING_BOARD_SPEC_v0.1_DRAFT.md
    PORTALS_BOARD_SPACE_TYPES_v0.1_DRAFT.md
    PORTALS_BOARD_ART_PROMPT_v0.1_DRAFT.md

  03_CARDS/
    CARD_DECKS_INDEX_v0.1_DRAFT.md
    PORTAL_CARDS_v0.1_DRAFT.md
    HERO_CARDS_v0.1_DRAFT.md
    MISSION_CARDS_v0.1_DRAFT.md
    TREASURE_ARTIFACT_CARDS_v0.1_DRAFT.md
    CATASTROPHE_CARDS_v0.1_DRAFT.md

  04_RESOURCES_AND_ECONOMY/
    SPARK_ECONOMY_v0.1_DRAFT.md
    BAG_SYSTEM_v0.1_DRAFT.md
    BALANCE_TARGETS_v0.1_DRAFT.md

  05_PLAYTESTS/
    PLAYTEST_PROTOCOL_v0.1_DRAFT.md
    PLAYTEST_REPORT_TEMPLATE_v0.1_DRAFT.md
    PLAYTEST_LOG.md

  06_ART_AND_COMPONENTS/
    COMPONENT_LIST_v0.1_DRAFT.md
    ICON_LANGUAGE_v0.1_DRAFT.md
    PLAYER_BOARD_SPEC_v0.1_DRAFT.md

  07_KICKSTARTER_AND_PROMOTION/
    SELL_SHEET_v0.1_DRAFT.md
    LANDING_PAGE_COPY_v0.1_DRAFT.md
    PROMOTION_KIT_v0.1_DRAFT.md

  08_LORE_LIGHT/
    LORE_ONE_PAGE_v0.1_DRAFT.md
    PUBLIC_WORLD_LANGUAGE_v0.1_DRAFT.md

  99_ARCHIVE/
```

## 5. What belongs here

Put here only materials directly related to the first small-family-game product:

- quick rules;
- board layout;
- card lists;
- Spark economy;
- bag/risk system;
- player boards;
- playtest reports;
- product pitch;
- Kickstarter/sell sheet copy;
- light public-facing lore.

Do not put here heavy IVDIVO metaphysics unless simplified for the product.

## 6. What stays in the master project folders

Use global project folders for:

- deep canon;
- world architecture;
- full franchise model;
- general Kickstarter research;
- multi-game studio planning;
- AI collaboration protocols;
- archived conversations.

## 7. AI collaboration instruction

When working on Portals of Stars, AI assistants must treat this folder as the game-specific source of truth, while still checking the master project context and active decisions when needed.

Priority order:

1. Founder instruction in current chat.
2. This game folder's README and index.
3. Active Portals rules/economy/playtest docs.
4. Master `PROJECT_CORE_CONTEXT_2026`.
5. Global mechanics/canon/Kickstarter documents.
6. Older drafts and archives.

## 8. Current next files to create

1. `00_INDEX/MASTER_INDEX_v0.1_DRAFT.md`
2. `01_CORE_RULES/PORTALS_QUICK_RULES_v0.1_DRAFT.md`
3. `02_BOARD/PORTALS_LIVING_BOARD_SPEC_v0.1_DRAFT.md`
4. `03_CARDS/CARD_DECKS_INDEX_v0.1_DRAFT.md`
5. `04_RESOURCES_AND_ECONOMY/SPARK_ECONOMY_v0.1_DRAFT.md`
6. `05_PLAYTESTS/PLAYTEST_REPORT_TEMPLATE_v0.1_DRAFT.md`

## 9. Status

This structure is DRAFT. It does not create final game canon. It creates a clean workspace for fast prototype development.
