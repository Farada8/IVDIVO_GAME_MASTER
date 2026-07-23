"""
Движок правил "Порталы Звёзд" для баланс-симулятора.

ЧЕСТНЫЕ УПРОЩЕНИЯ v1 (см. REPORT.md для полного списка):
- Карты Действий (18 шт) НЕ разыгрываются автоигроками в v1 — они социальные
  и требуют модели взаимодействия, не только сольной оптимизации.
- Тайные цели (24 шт) НЕ проверяются как индивидуальные условия — победа
  определяется по очкам Света с порталов. Полная система целей — v2.
- Спец-эффекты порталов peek_top_deck, free_exchange_on_open,
  free_action_card_on_open, final_synthesis — флейвор без числового эффекта
  в v1 (кроме permanent discount_earth/water/fire, которые реализованы).
- Наблюдатель и Летописец в v1 не имеют измеримого эффекта на бота
  (их сила — информационная/стратегическая, не арифметическая) — это
  ЗАФИКСИРОВАНО как открытый риск для баланса, не скрыто.
"""
import csv
import random
import yaml
from pathlib import Path

BASE = Path(__file__).parent
DATA = BASE.parent.parent / "data"

ELEMENTS = ["earth", "water", "fire", "star"]


def load_portals():
    portals = []
    with open(DATA / "portal_cards.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            portals.append({
                "id": row["id"],
                "name": row["name"],
                "element": row["element"],
                "tier": int(row["tier"]),
                "cost": {
                    "earth": int(row["cost_earth"]),
                    "water": int(row["cost_water"]),
                    "fire": int(row["cost_fire"]),
                    "star": int(row["cost_star"]),
                    "synth": int(row["cost_synth"]),
                },
                "vp": int(row["vp"]),
                "effect": row["effect"].strip(),
            })
    return portals


def load_characters():
    chars = []
    with open(DATA / "characters.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            chars.append(row)
    return chars


class Player:
    def __init__(self, pid, character, strategy):
        self.pid = pid
        self.character = character  # dict from characters.csv
        self.strategy = strategy
        self.sparks = {"earth": 0, "water": 0, "fire": 0, "star": 0, "synth": 0}
        self.discount = {"earth": 0, "water": 0, "fire": 0, "star": 0}
        self.vp = 0
        self.portals_owned = []
        self.trap_shield_used = False  # Хранитель Пути
        self.bag_bonus_pending = False  # Кладоискатель flag, resolved in bag draw

    def effective_cost(self, portal):
        cost = dict(portal["cost"])
        for el in ["earth", "water", "fire"]:
            if cost[el] > 0:
                reduction = self.discount[el]
                cost[el] = max(0, cost[el] - reduction)
        return cost

    def can_afford(self, portal):
        cost = self.effective_cost(portal)
        # Проводник: снять 1 с любого цвета, где стоимость >=1, при недостатке ровно на 1
        deficit = {}
        for el, amt in cost.items():
            have = self.sparks.get(el, 0)
            if have < amt:
                deficit[el] = amt - have
        if not deficit:
            return True, cost
        if self.character["ability_code"] == "discount_1" and sum(deficit.values()) == 1:
            # снимаем 1 с единственного недостающего цвета
            el = next(iter(deficit))
            cost2 = dict(cost)
            cost2[el] -= 1
            return True, cost2
        return False, cost

    def pay(self, cost):
        for el, amt in cost.items():
            self.sparks[el] -= amt

    def apply_portal_effect(self, portal):
        eff = portal["effect"]
        if eff.startswith("discount_earth"):
            self.discount["earth"] += 1
        elif eff.startswith("discount_water"):
            self.discount["water"] += 1
        elif eff.startswith("discount_fire"):
            self.discount["fire"] += 1
        # остальные эффекты — флейвор в v1, см. докстринг модуля

    def total_sparks(self):
        return sum(self.sparks.values())


class Bag:
    def __init__(self, cfg):
        self.counts = dict(cfg["bag_base"])
        self.escalation_add = cfg["bag_escalation_trap_add"]
        self.tier2_escalated = False
        self.tier3_escalated = False

    def escalate(self, tier_opened):
        if tier_opened == 2 and not self.tier2_escalated:
            self.counts["trap"] += self.escalation_add
            self.tier2_escalated = True
        if tier_opened == 3 and not self.tier3_escalated:
            self.counts["trap"] += self.escalation_add
            self.tier3_escalated = True

    def draw(self, rng):
        total = sum(self.counts.values())
        if total == 0:
            return None
        pick = rng.randint(1, total)
        cum = 0
        for key, cnt in self.counts.items():
            cum += cnt
            if pick <= cum:
                self.counts[key] -= 1
                return key
        return None  # не должно происходить


class Game:
    def __init__(self, cfg, players_setup, rng_seed=None):
        self.cfg = cfg
        self.rng = random.Random(rng_seed)
        self.n = len(players_setup)
        self.bank = dict(cfg["bank_by_players"][self.n])
        self.deck = load_portals()
        self.rng.shuffle(self.deck)
        self.market = [self.deck.pop() for _ in range(min(cfg["market_size"], len(self.deck)))]
        self.bag = Bag(cfg)
        self.players = [Player(i, ch, st) for i, (ch, st) in enumerate(players_setup)]
        self.portals_opened_total = 0
        self.turn_count = 0
        self.log = []
        self.leader_at_checkpoint = None
        self.checkpoint_turn = self.n * 3

    def refill_market(self):
        while len(self.market) < self.cfg["market_size"] and self.deck:
            self.market.append(self.deck.pop())

    def take_from_bank(self, colors):
        """colors: list of 1-2 element keys (не synth, synth не берётся сбором)."""
        for c in colors:
            if self.bank.get(c, 0) <= 0:
                return False
        for c in colors:
            self.bank[c] -= 1
        return True

    def can_collect_two_same(self, color):
        return self.bank.get(color, 0) >= self.cfg["same_color_requires_bank_min"]

    def game_over(self):
        if self.portals_opened_total >= self.cfg["end_trigger_portals_by_players"][self.n]:
            return True
        if any(p.vp >= self.cfg["end_trigger_vp"] for p in self.players):
            return True
        return False

    def resolve_winner(self):
        # v1: победа по очкам Света, тай-брейк — число открытых порталов
        ranked = sorted(
            self.players,
            key=lambda p: (p.vp, len(p.portals_owned), p.total_sparks()),
            reverse=True,
        )
        return ranked[0]

    def record_checkpoint_if_due(self):
        if self.leader_at_checkpoint is None and self.turn_count >= self.checkpoint_turn:
            best = max(self.players, key=lambda p: p.vp)
            self.leader_at_checkpoint = best.pid
