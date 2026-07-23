"""
4 стратегии автоигроков + разыгрывание одного хода.
Способности персонажей: discount_1, bag_bonus, flex_2to1, trap_shield_1
реализованы численно. peek_deck и objective_choice — флейвор в v1 (см. engine.py).
"""
from engine import ELEMENTS

STRATEGIES = ["random", "greedy", "risk_taker", "engine_builder"]


def affordable_portals(game, player):
    result = []
    for portal in game.market:
        ok, cost = player.can_afford(portal)
        if ok:
            result.append((portal, cost))
    return result


def try_druid_flex(player, portal):
    """Друид: если не хватает ровно 1 в одном цвете, конвертирует 2 избыточные Искры."""
    if player.character["ability_code"] != "flex_2to1":
        return False
    cost = player.effective_cost(portal)
    deficit_color = None
    deficit_amt = 0
    for el, amt in cost.items():
        have = player.sparks.get(el, 0)
        if have < amt:
            if deficit_color is not None:
                return False  # не хватает больше чем в одном цвете — Друид не поможет
            deficit_color = el
            deficit_amt = amt - have
    if deficit_color is None or deficit_amt != 1:
        return False
    spare = sum(v for k, v in player.sparks.items() if k != deficit_color)
    if spare < 2:
        return False
    remaining = 2
    for k in list(player.sparks.keys()):
        if k == deficit_color:
            continue
        while remaining > 0 and player.sparks[k] > 0:
            player.sparks[k] -= 1
            remaining -= 1
        if remaining == 0:
            break
    player.sparks[deficit_color] += 1
    return True


def buy_portal(game, player, portal, cost):
    player.pay(cost)
    player.vp += portal["vp"]
    player.portals_owned.append(portal["id"])
    player.apply_portal_effect(portal)
    game.market.remove(portal)
    game.portals_opened_total += 1
    game.bag.escalate(portal["tier"])
    game.refill_market()


def do_collect(game, player, rng, prefer_colors=None):
    prefer_colors = prefer_colors or []
    candidates = [c for c in prefer_colors if game.bank.get(c, 0) > 0]
    while len(candidates) < 2:
        pool = [c for c in ELEMENTS if game.bank.get(c, 0) > 0 and c not in candidates]
        if not pool:
            break
        candidates.append(rng.choice(pool))
    if len(candidates) == 2 and candidates[0] == candidates[1]:
        if not game.can_collect_two_same(candidates[0]):
            pool = [c for c in ELEMENTS if c != candidates[0] and game.bank.get(c, 0) > 0]
            if pool:
                candidates[1] = rng.choice(pool)
    take = candidates[:2]
    if game.take_from_bank(take):
        for c in take:
            player.sparks[c] += 1
        return True
    for c in take:
        if game.bank.get(c, 0) > 0:
            game.bank[c] -= 1
            player.sparks[c] += 1
    return True


def resolve_bag_draw(game, player, rng):
    result = game.bag.draw(rng)
    if result is None:
        return "empty"
    if result == "trap":
        if player.character["ability_code"] == "trap_shield_1" and not player.trap_shield_used:
            player.trap_shield_used = True
            return "trap_shielded"
        return "trap"
    gain = 1
    if player.character["ability_code"] == "bag_bonus":
        gain = 2
    player.sparks[result] += gain
    return result


def scarcest_color(player):
    return min(ELEMENTS, key=lambda e: player.sparks.get(e, 0))


def cheapest_market_target_colors(game):
    if not game.market:
        return []
    cheapest = min(game.market, key=lambda p: sum(p["cost"][e] for e in ELEMENTS))
    return [e for e in ELEMENTS if cheapest["cost"][e] > 0]


def take_turn(game, player, rng):
    strategy = player.strategy
    afford = affordable_portals(game, player)

    if not afford:
        for portal in game.market:
            if try_druid_flex(player, portal):
                ok, cost = player.can_afford(portal)
                if ok:
                    afford = [(portal, cost)]
                    break

    if strategy == "random":
        choice = rng.choice(["collect", "adventure_safe", "adventure_risky", "buy"])
        if choice == "buy" and afford:
            portal, cost = rng.choice(afford)
            buy_portal(game, player, portal, cost)
            return "buy"
        if choice == "adventure_safe":
            target = scarcest_color(player)
            player.sparks[target] += 1
            return "adventure_safe"
        if choice == "adventure_risky":
            resolve_bag_draw(game, player, rng)
            return "adventure_risky"
        do_collect(game, player, rng)
        return "collect"

    if strategy == "greedy":
        if afford:
            portal, cost = max(afford, key=lambda pc: pc[0]["vp"] - sum(pc[1].values()))
            buy_portal(game, player, portal, cost)
            return "buy"
        target = scarcest_color(player)
        player.sparks[target] += 1
        return "adventure_safe"

    if strategy == "risk_taker":
        if afford:
            portal, cost = min(afford, key=lambda pc: sum(pc[1].values()))
            buy_portal(game, player, portal, cost)
            return "buy"
        outcome = resolve_bag_draw(game, player, rng)
        draws = 1
        while outcome not in ("trap", "empty") and draws < 2:
            outcome = resolve_bag_draw(game, player, rng)
            draws += 1
        return "adventure_risky"

    if strategy == "engine_builder":
        engine_afford = [pc for pc in afford if pc[0]["effect"].startswith("discount_")]
        if engine_afford:
            portal, cost = min(engine_afford, key=lambda pc: sum(pc[1].values()))
            buy_portal(game, player, portal, cost)
            return "buy"
        if afford:
            portal, cost = min(afford, key=lambda pc: sum(pc[1].values()))
            buy_portal(game, player, portal, cost)
            return "buy"
        targets = cheapest_market_target_colors(game) or [scarcest_color(player)]
        do_collect(game, player, rng, prefer_colors=targets)
        return "collect"

    do_collect(game, player, rng)
    return "collect"
