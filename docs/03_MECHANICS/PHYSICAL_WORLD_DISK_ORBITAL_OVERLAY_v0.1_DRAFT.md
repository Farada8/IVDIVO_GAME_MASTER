# PHYSICAL_WORLD_DISK_ORBITAL_OVERLAY_v0.1_DRAFT

Status: GAME-MECHANIC DRAFT / TO-PLAYTEST
Date: 2026-07-22
Project: IVDIVO Card Game / Metagalactic Synthesis
Section: docs/03_MECHANICS

## 1. Purpose

This document develops the founder's request:

```text
World cells / move cells on a circular world disk should work like a Monopoly-style track.
Worlds and orbitals rotate and overlay each other.
Orbital cells can overlay world cells.
Orbitals can also overlay each other.
Start with the Physical World.
```

## 2. Core board idea

The Physical World is represented as a circular disk / track.

```text
Physical World Disk = 64 cells arranged as a circular movement track.
```

The player moves through the Physical World by stepping from cell to cell around the disk, similar to a Monopoly board, but each cell is not only a place. Each cell is a rule-bearing field with slots for:

```text
- terrain / material condition;
- resource generation;
- building / Form slot;
- Root or biological state;
- Distortion or Scar;
- Portal mark;
- orbital influence;
- event trigger;
- law interaction.
```

## 3. Difference between world cells and orbitals

A world cell is a fixed position on the main disk.

An orbital is a separate parallel ring / world that rotates relative to the main disk.

```text
World cell = fixed position inside a world disk.
Orbital cell = position on a rotating parallel ring.
Overlay = moment when a rotating orbital cell stands above a world cell.
```

This means:

```text
A player can stand on Physical Cell 12.
At the beginning of the round, the Fey orbital rotates.
Fey Cell 04 may now overlay Physical Cell 12.
The physical cell keeps its base property, but now receives Fey influence.
```

## 4. Physical World disk: 64-cell base structure

The first working model divides the Physical World into 8 macro-sectors of 8 cells each.

```text
8 sectors x 8 cells = 64 Physical World cells.
```

### Sector A: Body / Entry / Birth

```text
Cells 01-08
Function: character entry, body, food, fatigue, first material action.
Typical resources: Food, Energy, Matter.
Typical risks: Fatigue, biological inertia, weak body threshold.
```

### Sector B: Road / Labour / Movement

```text
Cells 09-16
Function: movement, work, material route, cost of action.
Typical resources: Tools, Energy, People.
Typical risks: blocked road, heavy matter, material debt.
```

### Sector C: Resource / Territory / Economy

```text
Cells 17-24
Function: gathering, territory, economy, exchange.
Typical resources: Matter, Food, Energy, Territory.
Typical risks: resource exhaustion, ownership conflict, debt.
```

### Sector D: Building / Form / Craft

```text
Cells 25-32
Function: creating Forms, repairing structures, placing instruments.
Typical resources: Matter, Tools, Buildings.
Typical risks: damaged Form, unstable construction, wrong material.
```

### Sector E: Root / Life / Biosphere

```text
Cells 33-40
Function: Roots, living connections, recovery, biological/ecological state.
Typical resources: Vitika, Food, Connection, living Matter.
Typical risks: wounded Root, contamination, loss of life-force.
```

### Sector F: Ecopolis / Organization / Society

```text
Cells 41-48
Function: Ecopolis buildings, collective institutions, team engine.
Typical resources: People, Connection, Building, Law.
Typical risks: bureaucracy, social conflict, building damage.
```

### Sector G: Scar / Rupture / Lower Trace

```text
Cells 49-56
Function: consequences, Scars, lower-world pressure, rupture cost.
Typical resources: Ash, Warning, Fire after transformation.
Typical risks: Distortion, lower debt, rupture, blocked route.
```

### Sector H: Threshold / Portal / Edge of World

```text
Cells 57-64
Function: portals, transitions, edge routes, orbital contact.
Typical resources: Key, Permission, Impulse, Clarity.
Typical risks: wrong portal, return to start, unstable transfer.
```

## 5. Cell anatomy

Each Physical World cell should have a standard structure.

```text
Cell ID: PHYS-01 to PHYS-64
Base type: Road / Resource / Building / Root / Scar / Portal / Ecopolis / Body
Base effect: what happens without orbitals
Slot 1: resource token
Slot 2: Form / building / Root marker
Slot 3: Distortion / Scar marker
Slot 4: current orbital overlay
Event rule: how the cell reacts when an orbital overlays it
```

Example:

```text
PHYS-33 — Root Field
Base: gain 1 Food or restore 1 Fatigue.
If damaged: pay 1 Matter to enter.
If Fey overlay: hidden resource appears.
If Lower World overlay: Root gains contamination.
If Paradise overlay: restore Root or remove one Scar.
```

## 6. How orbitals rotate over the Physical World

Each orbital has its own number of cells and its own rotation speed.

```text
Physical disk: 64 cells, fixed.
Paradise orbital: 16 cells, rotates +1 per round.
Fey/Leprechaun orbital: 16 cells, rotates +2 per round.
Lower World orbital: 16 cells, rotates -1 per round or reacts to Scars.
Arcana orbital: 22 cells, special high overlay, not always active.
```

The numbers are working values, not final canon.

Overlay is calculated by the current orbital offset.

```text
World cell number + orbital offset = current overlay position.
```

In a physical tabletop prototype, this can be represented by:

```text
- transparent rotating rings;
- separate orbital wheels placed around/over the main disk;
- tokens showing which physical cells are currently under orbital influence;
- cards that list current orbital alignment.
```

## 7. Basic overlay rule

When a player lands on a Physical World cell, check the overlay state.

```text
Event = Physical cell base type + active orbital cell + player action + current World Law.
```

Example:

```text
Player lands on PHYS-42: Ecopolis cell.
Fey orbital overlays this cell.
Current World Law: Law of Material Debt.
Result: player may find a hidden construction resource, but if it is used without payment, it becomes material debt.
```

## 8. Three levels of overlay intensity

### Minor overlay

```text
One orbital overlays a physical cell.
Effect: small modifier or choice.
```

Example:

```text
Fey overlay on Resource cell -> gain hidden resource, but owe a promise.
```

### Strong overlay

```text
Two orbitals overlay the same physical cell.
Effect: event card, risk, or special portal opens.
```

Example:

```text
Paradise + Fey overlay on Root cell -> rare recovery event.
Lower World + Fey overlay on Resource cell -> trick/debt event.
```

### Great conjunction

```text
A rare orbital alignment matches a key Physical World cell, a Portal, and a World Law.
Effect: campaign-level event.
```

Example:

```text
Arcana orbital position 22 overlays Physical Portal cell 64 while Law of Rare Coincidence is active.
Result: 22nd Arcana Gate opens; old route can be reset or a new path begins.
```

## 9. Orbitals currently connected to Physical World

### Paradise orbital

```text
Theme: recovery, harmony, blessing, restoration, safe growth.
Typical overlay effects:
- remove Fatigue;
- heal Root;
- restore Form;
- reduce Scar;
- open Paradise Arc / recovery portal.
Risk:
- passive dependence;
- avoiding necessary transformation.
```

### Fey / Leprechaun orbital

```text
Theme: hidden resource, trick, bargain, luck, side path.
Typical overlay effects:
- hidden resource appears;
- movement shortcut;
- strange exchange;
- promise/debt token;
- fey path to bypass obstacle.
Risk:
- trick cost;
- illusion;
- promise must be fulfilled.
```

### Unified Lower World orbital

```text
Theme: Hell + Demonic + Omaric lower pressure.
Typical overlay effects:
- lower debt;
- contamination;
- rupture pressure;
- fear or temptation event;
- risky access to strong resource.
Risk:
- Distortion grows;
- Root contamination;
- route blockage;
- debt enters campaign memory.
```

## 10. Orbitals overlaying each other

Orbitals can align not only with the Physical World, but also with each other.

```text
Orbital-to-world overlay = orbital cell affects a physical cell.
Orbital-to-orbital overlay = two orbitals affect each other before or while touching the world.
```

Example:

```text
Fey Cell 07 aligns with Paradise Cell 03.
This creates a temporary Joy Path.
If the Joy Path also touches a Physical Resource cell, it produces a blessed hidden resource.
```

Example:

```text
Lower World Cell 12 aligns with Fey Cell 05.
This creates a Trick Debt.
If the Trick Debt touches a Physical Ecopolis cell, an organization receives social conflict unless stabilized.
```

## 11. Physical gameplay loop

A simple turn inside the Physical World:

```text
1. Rotate active orbitals.
2. Reveal current overlays.
3. Player rolls/moves/chooses movement according to rules.
4. Player lands on a Physical cell.
5. Resolve base cell effect.
6. Resolve orbital overlay.
7. Check if another orbital also overlays the same cell.
8. Apply World Law.
9. Player may use Instrument, Form, Portal, or Ecopolis building.
10. Place consequences: resource, Scar, debt, Root state, building damage, or portal mark.
```

## 12. Why this matters mechanically

This system makes the same Physical World cell change over time.

```text
Cell 33 is not always the same event.
Cell 33 + no orbital = Root recovery.
Cell 33 + Paradise = healing / blessing.
Cell 33 + Fey = hidden living resource / bargain.
Cell 33 + Lower World = Root contamination.
Cell 33 + Paradise + Fey = rare living gift.
Cell 33 + Fey + Lower World = trick debt in the Root.
```

Therefore the board is not static. It becomes a rotating world machine.

## 13. First physical prototype requirement

For the first paper prototype, create:

```text
- 1 main Physical World disk with 64 cells;
- 3 Physical orbitals with 16 cells each: Paradise, Fey, Lower World;
- 1 optional Arcana test orbital with 22 cells;
- 64 physical cell cards or printed cell labels;
- overlay tokens for Minor / Strong / Great Conjunction;
- a turn tracker for orbital rotation.
```

## 14. Immediate next design task

The next task is to create the actual `PHYS-01 to PHYS-64` cell table.

Required columns:

```text
ID
sector
cell name
base type
base effect
resource slot
building/form/root slot
risk slot
portal slot
Paradise overlay effect
Fey overlay effect
Lower World overlay effect
Strong overlay effect
Great conjunction effect
test note
```

This table should become the first playable Physical World board map.
