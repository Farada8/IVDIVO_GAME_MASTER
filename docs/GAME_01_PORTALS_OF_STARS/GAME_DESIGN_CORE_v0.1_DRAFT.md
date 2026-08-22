# PORTALS_OF_STARS_GAME_DESIGN_CORE_v0.1_DRAFT

Status: DRAFT / GAME_01 / MONTH PROTOTYPE  
Project: IVDIVO — игра №1 «Порталы Звёзд»

## 1. Positioning

«Порталы Звёзд» — первая малая семейная настольная игра IVDIVO на 2–5 игроков, 30–40 минут, целевой вес 1.8–2.0.

Это не большая энциклопедическая игра IVDIVO, а быстрый коммерческий вход: яркая, азартная, понятная игра про сбор Искр, открытие порталов, тайные маршруты и восстановление уже существующей целостности мира.

References:
- Ticket to Ride — тайные маршруты, сеть, мягкая конкуренция.
- Splendor — простая экономика ресурсов, открытый рынок, темп накопления.
- Century: Spice Road — превращение ресурсов и планирование комбинаций.
- Quacks of Quedlinburg — жадность и мешок риска.
- Cascadia — условия подсчёта и разные scoring-стратегии.
- Sky Team — напряжение, но без тяжёлого кооператива.
- Everdell / Root — асимметрия персонажей через одно простое нарушение правила.

## 2. Core loop

Игроки собирают Искры, выбирают маршрут по круговой карте, открывают порталы между местами, выполняют тайные пути и получают Свет за восстановление уже существующих связей быстрее и точнее соперников.

Short rules version:

> Возьми Искры → пройди по карте → активируй место → открой или используй портал → продвинь тайный путь → получи Свет.

Main question each turn:

> Мне сейчас выгоднее собрать нужные Искры, занять важный портал раньше других или рискнуть ради тайного пути и большего Света?

## 3. Story frame: ascent as remembering wholeness

Ascent means not gaining power, but remembering already existing wholeness. Players do not become magically stronger; they rediscover the links between places and restore the network that was always there.

### A. Порталы Памяти

Ancient portals did not disappear — people forgot how they were connected. Players restore routes of memory by collecting Sparks and opening the existing network again.

### B. Острова, которые уже были одним миром

Worlds look like separate islands, but they are fragments of one ancient picture. Players reconnect them until the islands remember that they always belonged together.

### C. Звёздные Врата под обычным миром

Under ordinary hills, villages, stone circles, and cliffs lies an ancient star network. Players find the right keys so places remember their true connections.

v0.1 decision: use A as the rules frame and C as the visual hook.

## 4. Spark economy

The game uses 4 basic Spark types + 1 joker:

1. Earth — green.
2. Water — blue.
3. Fire — red.
4. Air — white-blue.
5. Star — gold joker.

### Bank

| Element | v0.1 value | Reasoning |
|---|---:|---|
| Basic Spark types | 4 | Lower cognitive load than 5–6 colors; fits 1.8–2.0 weight. |
| Joker type | 1 | Similar to gold in Splendor: flexible but limited. |
| Basic Spark bank | 4 × 18 = 72 | Enough for 2–5 players without constant depletion. |
| Star bank | 10 | Joker should be rare, about 12% of the bank. |
| Total Spark bank | 82 tokens | Supports 30–40 minutes and 12–16 opened portals. |
| Player Spark limit | 8 | Like Splendor’s chip limit, prevents hoarding. |
| Player Star limit | 2 | Joker must not replace color strategy. |

### Spark income

| Source | Income rate | Reasoning |
|---|---:|---|
| Basic action | Take 2 different basic Sparks or 1 Star if available | Splendor gives 3 different / 2 same, but this game has fewer types and lower target weight. |
| Spark space | Take 1 Spark of the shown type | Movement gives small rewards. |
| Chest | 1 Spark + Treasure card, or 2 Sparks with bag risk | Quacks-style greed choice. |
| Helper | 1 discount/conversion per round | Century-style economy improvement without heavy engine. |
| Portal income | When another player uses your portal, gain 1 basic Spark or 1 Light | Soft competition and positive interaction. |

### Portal costs by tier

| Tier | Cost | Light | Timing | Reasoning |
|---|---|---:|---|---|
| I. Small portal | 2 same Sparks or 2 location-matched Sparks | 2 | turns 2–4 | Early cheap build like Splendor low-tier cards. |
| II. Medium portal | 3 Sparks: 2 of one type + 1 any | 4 | turns 4–7 | Requires planning, does not stall play. |
| III. Complex portal | 4 Sparks: 3 different + 1 any | 6 | turns 7–10 | Medium purchase requiring several turns. |
| IV. Star portal | 5 Sparks: 4 different + 1 Star | 9 | turns 10–14 | Big mid-late moment, should be rare. |
| V. Spiral portal | 6 Sparks: 4 different + 2 any, max 1 Star | 12 | finale | Final scoring object, not the only victory path. |

### Pace

| Parameter | v0.1 value | Reasoning |
|---|---:|---|
| Players | 2–5 | Family range. |
| Duration | 30–40 min | First-product goal. |
| Turns per player | 10–12 | Enough for 2–3 portals and 1–2 secret goals. |
| Total turns at 4p | 40–48 | Good tempo, low downtime. |
| Opened portals | 12–16 | Creates network on a 24-location board without filling everything. |
| End trigger | 14 opened portals or one player reaches 35 Light; finish round | Clear family-game ending. |
| Target winner score | 32–45 Light | Combines routes, portals, bonuses. |

## 5. Bag instead of universal dice

The bag is used only on risk spaces: Chest, Shipwreck, Ruins, Trap, Star Shard.

| Bag token | Count | Effect |
|---|---:|---|
| Luck | 6 | Gain +1 Spark or +1 Light. |
| Treasure | 5 | Draw Treasure card. |
| Path | 4 | Move 1 space or use adjacent portal free. |
| Hero | 3 | Gain temporary helper until end of round. |
| Vortex | 4 | Lose 1 Spark or place Fog on adjacent space. |
| Trap | 3 | Stop; may pay 1 Spark to cancel. |
| Star | 1 | Gain joker or activate portal with -1 discount. |

Anti-randomness rules:
- player chooses whether to draw;
- draw 1 safe token or up to 3 with risk;
- after first bad token, player may stop and keep current gains;
- Heroes can preview, return, or soften tokens;
- traps slow but rarely remove scored points;
- no effect targets the trailing player more harshly.

## 6. 24 secret goals

| # | Name | Condition | Points | Provoked strategy | Duplication risk |
|---:|---|---|---:|---|---|
| 1 | Три тихих места | Connect 3 locations without danger icons. | 4 | Safe network. | Low |
| 2 | Первая дуга | Open 2 neighboring portals in one ring. | 4 | Early local control. | Medium |
| 3 | Две стихии | Connect any 2 elemental locations. | 5 | Two-color tempo. | Medium |
| 4 | Малый обход | Visit 4 different space types without opening a portal. | 5 | Mobility and events. | Low |
| 5 | Один чужой путь | Use another player’s portal and complete a 2-location route. | 5 | Use shared network. | Low |
| 6 | Сундук у моря | Activate a Chest and a Shipwreck in one game. | 6 | Bag risk/reward. | Low |
| 7 | Три круга | Connect locations in 3 different rings. | 7 | Expansion. | Medium |
| 8 | Путь воды и ветра | Connect Water and Air through any portal. | 7 | Fast paths. | Medium |
| 9 | Кладоискатель | Gain 3 Treasure cards and open at least 1 portal. | 7 | Economy alternative. | Low |
| 10 | Друидская цепь | Connect 2 Ruins and 1 Shrine. | 8 | Relics + route. | Low |
| 11 | Обход соперника | Complete a route with at least 1 segment through another player’s portal. | 8 | Positive interaction. | Medium |
| 12 | Четыре Искры | Spend 4 different basic Sparks on one or two portals. | 8 | Diverse resource plan. | Medium |
| 13 | Узел торговли | Gain income from other players using your portal twice. | 8 | Build useful portals. | Low |
| 14 | Портал на руинах | Open a portal on Ruins, then take a Relic. | 9 | Location combo. | Low |
| 15 | Серединный путь | Connect outer ring to central portal. | 9 | Center control. | Medium |
| 16 | Без джокера | Complete a goal without spending a Star. | 9 | Pure color planning. | Low |
| 17 | Большая дуга | Build a chain of 5 linked portals. | 10 | Long network. | High |
| 18 | Четыре стихии | Connect Earth, Water, Fire, and Air in one network. | 10 | Balanced colors. | Medium |
| 19 | Звёздный мост | Open a Star portal and use it in a route. | 10 | High-tier build. | Low |
| 20 | Сокровища и путь | Gain 2 Treasures and complete a 3-location route. | 10 | Economy + movement. | Medium |
| 21 | Пять мест памяти | Visit 5 space types and open 2 portals. | 11 | Hybrid strategy. | Low |
| 22 | Спиральное соединение | Connect 2 outer locations through central portal. | 11 | Center route. | Medium |
| 23 | Путь без остановки | In one turn, travel through portal and activate destination. | 11 | Timing movement cards. | Low |
| 24 | Врата целостности | Open/use 3 portals of different owners/colors in one route. | 12 | Network interaction. | Low; test needed |

No goal should win by itself. Max 12 points should be about 25–30% of the winning score.

## 7. Six asymmetrical characters

One character breaks exactly one rule with one ability line.

| Character | Ability | Play style | Counter-strategy | Balance check |
|---|---|---|---|---|
| Лира, Проводница Спирали | Once per turn, use any open portal as adjacent by paying 1 Spark. | Mobility, route completion. | Do not leave easy chains to center. | If she completes goals 2+ turns faster, reduce to once per round. |
| Бран, Искатель Кладов | When activating Chest or Shipwreck, draw 2 bag tokens and choose 1. | Risk/reward. | Occupy chest spaces first. | If +30% resources, forbid choosing Star with this effect. |
| Нив, Друид Узоров | Once per turn, exchange any 2 basic Sparks for 1 basic Spark. | Flexible economy. | Take precise-color portals. | If she never stalls, allow exchange only before portal opening. |
| Финн, Морской Следопыт | Shipwreck and Water spaces do not stop your movement. | Movement tempo. | Route through land/fire portals. | If movement goals dominate, limit to once per turn. |
| Эйлин, Хранительница Света | First time each round you draw Trap or Vortex, cancel the effect. | Safe play. | Race for high-point routes. | If too stable, require paying 1 Spark to cancel. |
| Роуэн, Малый Дракон | When opening Fire or Complex portal, replace 1 any Spark with Fire. | Midgame expensive portals. | Occupy fire/star nodes early. | If tier IV too early, restrict to tier II–III. |

Quarterback risk: Лира. Her mobility may let her see efficient routes and steer the table. Narrowing rule: her ability affects only her own pawn and cannot move or optimize other players; in family mode, secret goals remain private.

## 8. 12 mechanical twists

No evil PvP. Do not punish the trailing player.

| # | Twist | Trigger | Effect | Emotion | Family-risk control |
|---:|---|---|---|---|---|
| 1 | Комета открыла короткий путь | Event card | Temporary portal usable by everyone until end of round. | Race | Public access. |
| 2 | Туман меняет тропу | Draw Vortex | Close one unoccupied route for 1 round. | Tension | Cannot close only route of trailing player. |
| 3 | Звёздный дождь | End of every 3rd round | Everyone gains random basic Spark; trailing player chooses color. | Shared lift | Catch-up. |
| 4 | Дремлющий портал проснулся | 5th portal opened | Cheapest unopened portal gets -1 cost this round. | Opportunity | Public. |
| 5 | Фейри перепутали подарки | Fairy space | Everyone may exchange 1 Spark; active player exchanges 2. | Funny chaos | No stealing. |
| 6 | Башня Света зажглась | Portal to Tower opened | Nearby traps become Chests until end of round. | Positive surprise | Helps all nearby. |
| 7 | Корабль выбросило на берег | Event card | Treasure appears on nearest sea node. First to arrive takes it. | Race | Does not remove existing rewards. |
| 8 | Портал отразился | Player uses another player’s portal | Owner gains income, user gains +1 movement. | Win-win | Positive interaction. |
| 9 | Руины вспомнили путь | Player gains Relic | Reveal one public secret route worth 5 Light. | Shared discovery | Optional race. |
| 10 | Перегрузка Искр | Player ends with 8 Sparks | Must open portal or discard 1 Spark for 1 Light. | Pressure | Compensation. |
| 11 | Механизм времени щёлкнул | Draw Star from bag | Repeat last action, but cannot score same points twice. | Wow | No double scoring. |
| 12 | Спираль зовёт всех | 12th portal opened | Everyone gets +1 action in final round. | Finale | Helps all players. |

## 9. Prototype v0.1 fixed decisions

- 4 basic Sparks + 1 joker.
- 82 Spark tokens.
- 120 cards minimum version.
- 24 secret goals.
- 6 characters, each with one line of asymmetry.
- Bag risk system instead of universal dice.
- 12 mechanical twists.
- Victory by Light.
- Soft competition, no evil PvP.
