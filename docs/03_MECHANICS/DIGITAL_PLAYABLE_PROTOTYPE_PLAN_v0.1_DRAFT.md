# DIGITAL_PLAYABLE_PROTOTYPE_PLAN_v0.1_DRAFT

Status: DIGITAL-PROTOTYPE DRAFT / TO-BUILD
Date: 2026-07-22
Project: IVDIVO Card Game / Metagalactic Synthesis
Section: docs/03_MECHANICS

## 1. Purpose

This document answers the founder's question:

```text
Can the disk/orbital system be made playable on a computer, not only drawn as a 3D image?
```

Answer:

```text
Yes. It requires a playable digital prototype, not only a visual concept.
```

The prototype must include game state, movement, rotating orbitals, overlay calculation, event resolution, resources, players, and a turn log.

## 2. Recommended first playable version

The fastest playable prototype should be:

```text
Browser-based 2.5D prototype first.
Then 3D visualization.
```

Reason:

```text
A full 3D game is slower to build and harder to debug.
A 2.5D web prototype can prove the rules first:
- 64-cell world disk;
- rotating orbital rings;
- player movement;
- overlay events;
- resources;
- turn log.
```

After the system works, it can be ported or visualized in:

```text
- Unity;
- Unreal Engine;
- Godot;
- Three.js / WebGL;
- Blender for visual assets.
```

## 3. Minimum playable prototype

The first digital prototype must include:

```text
1. One Physical World disk with 64 cells.
2. Three active physical orbitals:
   - Paradise;
   - Fey / Leprechaun;
   - Unified Lower World.
3. Optional Arcana orbital with 22 cells.
4. One player token.
5. Dice or controlled movement.
6. Orbital rotation at the start of each round.
7. Overlay detection.
8. Base cell effects.
9. Overlay effects.
10. Resource counters.
11. Event log.
12. End-turn button.
```

## 4. Data model

### 4.1 World disk

```json
{
  "worldId": "PHYSICAL",
  "cellCount": 64,
  "cells": [
    {
      "id": "PHYS-01",
      "sector": "Body / Entry / Birth",
      "name": "Body Gate",
      "baseType": "Body",
      "baseEffect": "Gain 1 Energy or remove 1 Fatigue.",
      "resourceSlot": "Energy",
      "riskSlot": "Fatigue",
      "portalSlot": null
    }
  ]
}
```

### 4.2 Orbital

```json
{
  "orbitalId": "PARADISE",
  "name": "Paradise Orbital",
  "cellCount": 16,
  "offset": 0,
  "rotationPerRound": 1,
  "cells": [
    {
      "id": "PAR-01",
      "name": "Blessing Field",
      "effect": "Remove 1 Fatigue or restore 1 Root."
    }
  ]
}
```

### 4.3 Player

```json
{
  "playerId": "P1",
  "name": "Founder Test Player",
  "world": "PHYSICAL",
  "position": 0,
  "resources": {
    "Energy": 3,
    "Matter": 2,
    "Food": 1,
    "Clarity": 0,
    "Fire": 0,
    "Synthesis": 0
  },
  "states": {
    "Fatigue": 0,
    "Debt": 0,
    "Scar": 0
  }
}
```

## 5. Overlay calculation

Each world cell is fixed.
Each orbital rotates by changing its offset.

Pseudo-code:

```ts
function rotateOrbitals(game) {
  for (const orbital of game.orbitals) {
    orbital.offset = (orbital.offset + orbital.rotationPerRound) % orbital.cellCount;
  }
}
```

For each physical world cell, calculate which orbital cell overlays it:

```ts
function getOrbitalCellForWorldCell(worldCellIndex, orbital) {
  const ratio = worldCellIndex / 64;
  const approximateOrbitalIndex = Math.floor(ratio * orbital.cellCount);
  return (approximateOrbitalIndex - orbital.offset + orbital.cellCount) % orbital.cellCount;
}
```

Alternative simple prototype rule:

```text
A 16-cell orbital maps to the 64-cell Physical disk by groups of 4.
Orbital cell 1 overlays Physical cells 1-4.
Orbital cell 2 overlays Physical cells 5-8.
...
Orbital cell 16 overlays Physical cells 61-64.
```

This is easier for first playtest.

## 6. Player turn loop

```text
1. Start round.
2. Rotate active orbitals.
3. Show highlighted overlay zones.
4. Player rolls die or chooses movement.
5. Move token along Physical World disk.
6. Resolve base cell effect.
7. Resolve current orbital overlay effect.
8. Check if two orbitals overlay the same world cell.
9. Apply World Law if active.
10. Allow player action: use Instrument / Form / Portal / Ecopolis building.
11. Update resources and states.
12. Write result to log.
13. End turn.
```

## 7. First playable interaction

The first version should have buttons:

```text
- Roll / Move
- Rotate Orbitals
- Resolve Cell
- Use Portal
- End Turn
- Reset Prototype
```

And visible panels:

```text
- central world disk;
- orbital ring display;
- player resources;
- active overlays;
- current cell card;
- event log;
- active World Law;
- debug panel with offsets.
```

## 8. Visual layers

### 8.1 MVP view

```text
Top-down board view:
- 64 cells arranged in a circle;
- player token on one cell;
- colored overlay highlights;
- orbitals shown as rotating rings or small external tracks.
```

### 8.2 3D view

```text
- main Physical World disk as a circular board;
- translucent orbital rings above it;
- glowing overlay columns where cells align;
- player token as a miniature/avatar;
- event panel on the right;
- resource panel at the bottom.
```

3D is valuable for presentation, but the rules must work first in 2D/2.5D.

## 9. Playable MVP scope

First version should not include the full game.
It should prove only the core engine:

```text
Physical World disk + orbitals + overlays + movement + event log.
```

Included:

```text
- 64 Physical cells;
- 3 orbitals;
- 1 player;
- 6 resources;
- 3 states: Fatigue, Debt, Scar;
- 12 sample events;
- 6 sample portals;
- 3 sample World Laws.
```

Excluded for MVP:

```text
- full deckbuilding market;
- all 144 starter cards;
- all 100 instruments;
- all 50 forms;
- all 32 Ecopolis buildings;
- campaign progression;
- multiplayer networking;
- account system;
- monetization;
- final art.
```

## 10. Development route

### Stage 1: Rules engine

```text
Plain JavaScript / TypeScript.
No 3D yet.
Goal: movement and overlays work correctly.
```

### Stage 2: Browser visual prototype

```text
HTML/CSS/SVG or Canvas.
Goal: visible 64-cell circular board and rotating overlays.
```

### Stage 3: 2.5D playable prototype

```text
Add animation, cards, resources, event log.
Goal: one full playable test loop.
```

### Stage 4: 3D prototype

```text
Three.js / Unity / Godot.
Goal: visual presentation with translucent orbitals and glowing overlays.
```

### Stage 5: Real game prototype

```text
Add multiple worlds, decks, roles, campaign state, save/load.
```

## 11. Best implementation options

### Fastest AI-buildable option

```text
Browser app: TypeScript + SVG/Canvas + simple state machine.
```

Good for:

```text
- Claude;
- Codex;
- GPT;
- quick iteration;
- sharing by link;
- debugging rules.
```

### Best 3D game option

```text
Unity.
```

Good for:

```text
- real 3D board;
- miniatures;
- animation;
- future Steam/mobile prototype.
```

### Best open-source 3D option

```text
Godot.
```

Good for:

```text
- free engine;
- smaller prototype;
- clean scripting.
```

### Best visual concept option

```text
Blender + rendered mockups.
```

Good for:

```text
- Kickstarter visuals;
- pitch deck;
- 3D board renders;
- not for first rules testing.
```

## 12. Immediate next build prompt for Claude/Codex

```text
Build a browser-based playable prototype for the IVDIVO Physical World disk.

Requirements:
- Use HTML/CSS/JavaScript or TypeScript.
- Render a circular board with 64 cells.
- Divide the board into 8 sectors of 8 cells.
- Add one player token.
- Add three orbitals: Paradise, Fey, Lower World.
- Each orbital has 16 cells and an offset.
- Paradise rotates +1 per round.
- Fey rotates +2 per round.
- Lower World rotates -1 per round.
- Highlight cells affected by each orbital.
- When a player lands on a cell, show:
  - base cell effect;
  - Paradise overlay effect if present;
  - Fey overlay effect if present;
  - Lower World overlay effect if present;
  - combined overlay if 2+ orbitals affect the cell.
- Add resources: Energy, Matter, Food, Clarity, Fire, Synthesis.
- Add states: Fatigue, Debt, Scar.
- Add event log.
- Add buttons: Roll, Rotate Orbitals, Resolve Cell, End Turn, Reset.
- Keep code modular: gameState, cells, orbitals, renderBoard, rotateOrbitals, resolveCell.
- No networking, no backend, no final art.
```

## 13. Success criteria

The prototype is playable when a tester can:

```text
1. Start a game.
2. Move a token around the 64-cell disk.
3. See orbitals rotate.
4. Land on a cell.
5. See the base effect and overlay effect.
6. Gain/lose resources or states.
7. Read the event log.
8. Play at least 10 turns and observe changing cell behavior.
```

## 14. Next project task

Before coding, create:

```text
PHYSICAL_WORLD_64_CELLS_v0.1.csv
```

Required columns:

```text
ID, sector, cell name, base type, base effect, resource slot, building/form/root slot, risk slot, portal slot, Paradise overlay effect, Fey overlay effect, Lower World overlay effect, Strong overlay effect, Great conjunction effect, test note
```

This table becomes the data source for the first playable digital prototype.
