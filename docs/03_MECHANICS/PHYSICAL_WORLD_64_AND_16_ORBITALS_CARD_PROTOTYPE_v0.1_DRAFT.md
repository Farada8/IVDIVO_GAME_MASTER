# PHYSICAL_WORLD_64_AND_16_ORBITALS_CARD_PROTOTYPE_v0.1_DRAFT

Status: GAME-MECHANIC DRAFT / CARD-PROTOTYPE / TO-PLAYTEST
Date: 2026-07-22
Project: IVDIVO Card Game / Metagalactic Synthesis
Section: docs/03_MECHANICS

## 1. Founder direction

The founder confirmed the last visual logic as correct and requested a playable card-game prototype:

```text
Physical World: 64 movement cells.
Orbitals / parallel worlds: 16 cells each.
Orbitals overlap the Physical World and can overlap each other.
Orbital movement happens by day.
Example movement:
- orbital 1 moves 3 cells per day;
- orbital 2 moves 2 cells per day;
- orbital 3 moves 1 cell per day.
Also create card decks for world cells, orbital cells, and levels.
```

## 2. Core physical prototype

The first playable table prototype should use:

```text
1 main Physical World disk = 64 movement cells.
3 active physical orbitals = 16 cells each.
1 player track / round-day marker.
4 main decks:
- Physical World Cell Deck, 64 cards.
- Paradise Orbital Deck, 16 cards.
- Fey / Leprechaun Orbital Deck, 16 cards.
- Unified Lower World Deck, 16 cards.
1 Overlay / Level Deck, 12 cards.
```

This is the minimum physical-card prototype for testing whether the orbital overlay mechanic is fun and understandable.

## 3. Board geometry

### 3.1 Physical World disk

```text
Physical World = 64 cells arranged around a circular movement track.
```

The cells may be physically printed:

```text
- around the outer edge, like Monopoly;
- across the whole disk, as radial/concentric cells;
- or as a hybrid: outer movement track plus inner special zones.
```

For the first prototype, use the simplest version:

```text
64 cells on the rim.
```

The inner disk can show terrain, sectors, major zones, and lore art, but movement uses the 64 edge cells.

### 3.2 Eight sectors of eight cells

```text
Sector 1: PHYS-01 to PHYS-08 — Mountains / Body / Entry
Sector 2: PHYS-09 to PHYS-16 — Forests / Life / Roots
Sector 3: PHYS-17 to PHYS-24 — Rivers / Movement / Flows
Sector 4: PHYS-25 to PHYS-32 — Plains / Labour / Settlements
Sector 5: PHYS-33 to PHYS-40 — Deserts / Trial / Scar
Sector 6: PHYS-41 to PHYS-48 — Caverns / Hidden Matter / Lower trace
Sector 7: PHYS-49 to PHYS-56 — Sanctuary / Ecopolis / Organization
Sector 8: PHYS-57 to PHYS-64 — Ruins / Rift / Portal / Ancient memory
```

These names are draft names and can be changed after playtest.

## 4. Orbital circles

Each orbital is a separate 16-cell circular track.

```text
Paradise Orbital = 16 cells.
Fey / Leprechaun Orbital = 16 cells.
Unified Lower World Orbital = 16 cells.
```

Each orbital can be represented as:

```text
- a transparent physical ring laid partly over the Physical World disk;
- a separate round wheel with a pointer;
- a side ring on the table with connection lines;
- a digital ring in a computer prototype.
```

The important rule is not physical shape but current alignment.

```text
Alignment = which Physical World cells are currently touched by an orbital cell.
```

## 5. Orbital movement by day

At the start of each day, before player turns:

```text
Paradise Orbital moves +3 cells clockwise.
Fey / Leprechaun Orbital moves +2 cells clockwise.
Unified Lower World Orbital moves +1 cell clockwise.
```

Alternative direction rules for testing:

```text
Paradise: +3 clockwise.
Fey / Leprechaun: +2 clockwise.
Unified Lower World: +1 counterclockwise.
```

First prototype recommendation:

```text
Use all clockwise movement first.
It is easier to teach and calculate.
After playtest, test counter-rotation for conflict/tension.
```

## 6. Alignment calculation

Each orbital has an offset.

```text
Day 0 offsets:
Paradise = 0
Fey / Leprechaun = 0
Unified Lower World = 0
```

At each day start:

```text
Paradise offset = Paradise offset + 3 mod 16.
Fey offset = Fey offset + 2 mod 16.
Lower offset = Lower offset + 1 mod 16.
```

Because the Physical World has 64 cells and each orbital has 16 cells:

```text
1 orbital cell corresponds to a 4-cell physical arc.
64 / 16 = 4.
```

Therefore one orbital cell can influence either:

```text
A. one exact physical anchor cell;
B. a four-cell physical zone;
C. one anchor cell strongly and adjacent cells weakly.
```

First prototype recommendation:

```text
Use anchor-cell alignment for simplicity.
Orbital Cell 1 anchors to PHYS-01, PHYS-17, PHYS-33, PHYS-49 depending on ring geometry or quadrant.
```

Second prototype recommendation:

```text
Use 4-cell influence zones.
Orbital Cell 1 influences PHYS-01 to PHYS-04.
Orbital Cell 2 influences PHYS-05 to PHYS-08.
...
Orbital Cell 16 influences PHYS-61 to PHYS-64.
```

The second model is easier for physical play because every Physical cell can be under an orbital zone.

## 7. Recommended overlay model for first playtest

Use the zone model:

```text
Physical cells 01-04 = Orbital Zone 01.
Physical cells 05-08 = Orbital Zone 02.
Physical cells 09-12 = Orbital Zone 03.
Physical cells 13-16 = Orbital Zone 04.
Physical cells 17-20 = Orbital Zone 05.
Physical cells 21-24 = Orbital Zone 06.
Physical cells 25-28 = Orbital Zone 07.
Physical cells 29-32 = Orbital Zone 08.
Physical cells 33-36 = Orbital Zone 09.
Physical cells 37-40 = Orbital Zone 10.
Physical cells 41-44 = Orbital Zone 11.
Physical cells 45-48 = Orbital Zone 12.
Physical cells 49-52 = Orbital Zone 13.
Physical cells 53-56 = Orbital Zone 14.
Physical cells 57-60 = Orbital Zone 15.
Physical cells 61-64 = Orbital Zone 16.
```

When an orbital's current cell matches the zone of the player's Physical cell, that orbital overlays the player.

## 8. Types of overlay

### 8.1 World + one orbital

```text
Physical World cell + one orbital cell = minor overlay.
```

Example:

```text
PHYS-10 Forest Resource + Paradise Orbital Cell 03 = recover and gain Essence.
PHYS-10 Forest Resource + Fey Orbital Cell 03 = find hidden resource, but accept a bargain.
PHYS-10 Forest Resource + Lower World Cell 03 = resource is corrupted or costs extra.
```

### 8.2 World + two orbitals

```text
Physical World cell + two orbital overlays = strong overlay.
```

Draw from the Overlay / Level Deck.

### 8.3 World + three orbitals

```text
Physical World cell + all three orbitals = rare convergence.
```

Draw Level III or Great Conjunction.

### 8.4 Orbital + orbital without player

If two orbital cells overlap each other away from the player, place a temporary marker.

```text
Paradise + Fey = Joy Path / lucky blessing.
Fey + Lower World = Trick Debt / dangerous bargain.
Paradise + Lower World = Redemption Test / healing through danger.
Paradise + Fey + Lower World = Great Conjunction / campaign event.
```

## 9. Day and turn structure

A day is one global rotation cycle.

```text
Start of Day:
1. Move all active orbitals.
2. Mark all current orbital overlaps.
3. Resolve any automatic orbital-to-orbital events.
4. Start player turns.
```

Player turn:

```text
1. Roll movement die or choose movement card.
2. Move on Physical World 64-cell track.
3. Resolve Physical World cell.
4. Check orbital overlays by current zone.
5. Draw and resolve relevant orbital card if overlay exists.
6. If 2+ orbitals overlay, draw Overlay / Level card.
7. Player may use Instrument, Form, Portal, or Ecopolis building.
8. End turn.
```

End of day:

```text
After all players acted, advance Day marker and repeat.
```

## 10. Physical World Cell Deck — 64 cards

Purpose:

```text
The Physical World Cell Deck defines what each of the 64 cells does.
```

Recommended distribution:

```text
8 Terrain cards.
8 Resource cards.
8 Body / Fatigue / Food cards.
8 Root / Life cards.
8 Labour / Movement cards.
8 Ecopolis / Building cards.
8 Rift / Scar cards.
8 Portal / Ruin / Ancient memory cards.
```

Each card format:

```text
ID
Cell name
Sector
Base type
Base effect
Resource generated
Risk
Portal possibility
Paradise overlay modifier
Fey overlay modifier
Lower World overlay modifier
Level modifier
Test note
```

Examples:

```text
PHYS-01 — Mountain Pass
Type: Terrain
Base: Movement through this cell costs +1.
Paradise: remove the extra cost once.
Fey: take a hidden shortcut but draw a Trick.
Lower: lose 1 Energy or gain Scar.
```

```text
PHYS-10 — Forest Resource
Type: Resource / Life
Base: Gain 1 Matter or 1 Food.
Paradise: gain +1 Essence.
Fey: gain hidden resource and receive Promise token.
Lower: resource is contaminated; purify or take Debt.
```

```text
PHYS-49 — Ecopolis Gate
Type: Ecopolis / Organization
Base: Activate one Ecopolis building.
Paradise: repair one building damage.
Fey: discount one action but owe a favour.
Lower: social conflict appears in one building.
```

```text
PHYS-64 — Ancient Portal
Type: Portal / Ruin
Base: Draw Portal card.
Paradise: safe portal.
Fey: hidden route.
Lower: dangerous portal with strong reward.
```

## 11. Paradise Orbital Deck — 16 cards

Theme:

```text
Restoration, harmony, protection, blessing, safe growth.
```

Recommended card types:

```text
4 Blessing cards.
4 Healing / repair cards.
4 Harmony / cooperation cards.
4 Light Path / safe movement cards.
```

Example cards:

```text
PAR-01 — Blessing of Return
Effect: Remove 1 Fatigue or 1 Scar.
If on Root cell: restore Root instead.
```

```text
PAR-04 — Harmony Field
Effect: If another player is in your sector, both gain 1 Influence.
```

```text
PAR-09 — Light Path
Effect: Your next movement ignores terrain penalty.
```

```text
PAR-16 — Garden of Renewal
Effect: Repair one Form or Ecopolis building by 1 step.
```

## 12. Fey / Leprechaun Orbital Deck — 16 cards

Theme:

```text
Luck, trick, hidden routes, bargain, strange exchange.
```

Recommended card types:

```text
4 Luck cards.
4 Trick cards.
4 Hidden Path cards.
4 Bargain / Promise cards.
```

Example cards:

```text
FEY-01 — Lucky Coin
Effect: Reroll one die.
Cost: take Promise token.
```

```text
FEY-05 — Hidden Path
Effect: Move to any cell in the same sector.
Risk: if Lower World also overlays, draw Trick Debt.
```

```text
FEY-09 — Laughing Exchange
Effect: Swap one resource with the market or another willing player.
```

```text
FEY-16 — Green Door
Effect: Open a temporary one-turn Fey portal.
```

## 13. Unified Lower World Deck — 16 cards

Theme:

```text
Shadow, debt, temptation, fear, dangerous gift, rupture pressure.
```

Recommended card types:

```text
4 Shadow cards.
4 Debt cards.
4 Fear / blockage cards.
4 Dangerous Gift cards.
```

Example cards:

```text
LOW-01 — Shadow Toll
Effect: Lose 1 Influence or place 1 Shadow marker.
```

```text
LOW-04 — Material Debt
Effect: Gain 2 Matter now; pay 3 Matter later or receive Scar.
```

```text
LOW-09 — Fear Gate
Effect: Your movement stops here unless you pay 1 Courage / Clarity.
```

```text
LOW-16 — Dangerous Gift
Effect: Gain one strong resource, but draw one Rift card.
```

## 14. Overlay / Level Deck — 12 cards

Purpose:

```text
This deck resolves stronger combinations when two or three overlays are active.
```

Recommended distribution:

```text
4 Level I — Minor combined effect.
4 Level II — Strong combined effect.
4 Level III — Great convergence / rare event.
```

Examples:

```text
OVR-01 — Level I: Soft Resonance
Effect: Choose one active overlay and apply it with +1 resource.
```

```text
OVR-05 — Level II: Crossed Paths
Effect: Two orbitals combine. Gain benefit from one and cost from the other.
```

```text
OVR-09 — Level III: Great Conjunction
Effect: Open a temporary portal and change the cell state permanently.
```

```text
OVR-12 — Level III: World Rewrites Itself
Effect: Replace the current Physical cell card with a transformed version.
```

## 15. Level system for cells and overlays

Each cell can have level:

```text
Level 0: normal cell.
Level I: activated / touched by one orbital.
Level II: transformed by two orbitals or repeated use.
Level III: campaign state / Great Conjunction.
```

Level changes can be represented with small tokens:

```text
I token = touched.
II token = changed.
III token = transformed.
```

Example:

```text
Forest Resource Level 0 = gain 1 resource.
Forest Resource + Paradise = Level I: gain resource and remove Fatigue.
Forest Resource + Paradise + Fey = Level II: gain hidden living resource and team blessing.
Forest Resource + Paradise + Fey + Lower = Level III: create Living Gate or corrupted miracle.
```

## 16. Components for paper prototype

Required components:

```text
1 circular Physical World board with 64 numbered cells.
3 orbital rings with 16 numbered cells each.
1 Day marker.
1 player pawn per player.
64 Physical World Cell cards.
16 Paradise cards.
16 Fey / Leprechaun cards.
16 Unified Lower World cards.
12 Overlay / Level cards.
Resource tokens.
Scar tokens.
Promise/Debt tokens.
Portal markers.
Level I/II/III markers.
```

Minimum card count:

```text
64 + 16 + 16 + 16 + 12 = 124 prototype cards.
```

## 17. Minimal first-session test

Test scenario:

```text
Players: 1-4.
Length: 30-45 minutes.
Goal: reach or transform one key cell before Day 8.
Board: Physical World only.
Orbitals: Paradise, Fey, Lower World.
Cards: simplified decks.
Win condition: build/stabilize one Ecopolis or open one stable Portal.
Lose/pressure condition: 5 Scars or 5 Debts accumulate.
```

## 18. First balancing questions

During playtest, record:

```text
1. Are 64 cells too many for first prototype?
2. Are 16-cell orbitals easy to understand?
3. Is movement 3/2/1 per day readable?
4. Do overlays create excitement or confusion?
5. How often do two-orbital overlaps occur?
6. Is the Overlay / Level Deck needed every time, or only on rare overlaps?
7. Are players making interesting choices, or only resolving automatic effects?
```

## 19. Immediate next production task

Create these tables:

```text
PHYSICAL_WORLD_64_CELLS_v0.1.csv
PARADISE_ORBITAL_16_CELLS_v0.1.csv
FEY_LEPRECHAUN_ORBITAL_16_CELLS_v0.1.csv
UNIFIED_LOWER_WORLD_ORBITAL_16_CELLS_v0.1.csv
OVERLAY_LEVEL_DECK_12_v0.1.csv
```

These tables will become the first playable card-and-board prototype.

## 20. Non-final status

This is not a final rulebook. It is the first physical/digital prototype definition for testing the 64-cell world disk plus 16-cell orbital system.
