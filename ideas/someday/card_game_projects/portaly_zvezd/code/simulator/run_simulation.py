import csv
import random
import statistics
import sys
import yaml
from pathlib import Path

from engine import Game, load_characters
from players import take_turn, STRATEGIES

BASE = Path(__file__).parent

TRIALS_PER_PLAYER_COUNT = 2500
PLAYER_COUNTS = [2, 3, 4, 5]


def run_one_game(cfg, characters, n_players, game_index, seed):
    # ВАЖНО: персонаж и стратегия ротируются НЕЗАВИСИМО (через отдельный shuffle),
    # а не одной формулой (i+game_index) для обоих — иначе индексы коррелируют
    # и каждый персонаж систематически недополучает часть стратегий (баг v1.0,
    # исправлен здесь; см. REPORT.md, "методологическая правка").
    setup_rng = random.Random(seed)
    char_order = [characters[(i + game_index) % len(characters)] for i in range(n_players)]
    strat_pool = list(STRATEGIES)
    setup_rng.shuffle(strat_pool)
    strat_order = [strat_pool[i % len(strat_pool)] for i in range(n_players)]
    setup = list(zip(char_order, strat_order))
    game = Game(cfg, setup, rng_seed=seed)
    rng = random.Random(seed + 1)

    while not game.game_over() and game.turn_count < cfg["max_turns_safety"]:
        for p in game.players:
            if game.game_over():
                break
            take_turn(game, p, rng)
            game.turn_count += 1
            game.record_checkpoint_if_due()

    winner = game.resolve_winner()
    scores = [p.vp for p in game.players]
    trap_draws = sum(1 for _ in [])  # placeholder, recomputed below via bag deltas

    return {
        "n_players": n_players,
        "turns": game.turn_count,
        "winner_character": winner.character["name"],
        "winner_strategy": winner.strategy,
        "winner_pid": winner.pid,
        "leader_at_checkpoint": game.leader_at_checkpoint,
        "leader_won": int(game.leader_at_checkpoint == winner.pid) if game.leader_at_checkpoint is not None else None,
        "score_spread": statistics.pstdev(scores) if len(scores) > 1 else 0,
        "top_score": max(scores),
        "portals_opened_total": game.portals_opened_total,
        "characters": [p.character["name"] for p in game.players],
        "strategies": [p.strategy for p in game.players],
        "scores": scores,
    }


def main():
    cfg = yaml.safe_load(open(BASE / "config.yaml", encoding="utf-8"))
    characters = load_characters()

    rows = []
    seed = 12345
    for n in PLAYER_COUNTS:
        for gi in range(TRIALS_PER_PLAYER_COUNT):
            seed += 1
            rows.append(run_one_game(cfg, characters, n, gi, seed))

    out_csv = BASE / "results.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["n_players", "turns", "winner_character", "winner_strategy",
                    "leader_won", "score_spread", "top_score", "portals_opened_total"])
        for r in rows:
            w.writerow([r["n_players"], r["turns"], r["winner_character"], r["winner_strategy"],
                        r["leader_won"], round(r["score_spread"], 2), r["top_score"],
                        r["portals_opened_total"]])

    print(f"Прогнано партий: {len(rows)}")
    print(f"Сохранено: {out_csv}")

    # --- агрегированная сводка в консоль ---
    char_wins = {}
    char_games = {}
    for r in rows:
        for ch in r["characters"]:
            char_games[ch] = char_games.get(ch, 0) + 1
        char_wins[r["winner_character"]] = char_wins.get(r["winner_character"], 0) + 1

    print("\n=== Винрейт по персонажам (ожидание при честном балансе: 1/6 = 16.7%) ===")
    for ch, wins in sorted(char_wins.items(), key=lambda x: -x[1]):
        games = char_games.get(ch, 1)
        print(f"{ch:20s}  побед: {wins:5d}  партий-участий: {games:6d}  винрейт от партий-участий: {wins/games*100:5.1f}%")

    strat_wins = {}
    strat_games = {}
    for r in rows:
        for st in r["strategies"]:
            strat_games[st] = strat_games.get(st, 0) + 1
        strat_wins[r["winner_strategy"]] = strat_wins.get(r["winner_strategy"], 0) + 1

    print("\n=== Винрейт по стратегиям (ожидание: 1/4 = 25%) ===")
    for st, wins in sorted(strat_wins.items(), key=lambda x: -x[1]):
        games = strat_games.get(st, 1)
        print(f"{st:15s}  побед: {wins:5d}  партий-участий: {games:6d}  винрейт от партий-участий: {wins/games*100:5.1f}%")

    leader_data = [r["leader_won"] for r in rows if r["leader_won"] is not None]
    if leader_data:
        pct = sum(leader_data) / len(leader_data) * 100
        print(f"\n=== Runaway-leader риск ===")
        print(f"Лидер по очкам после {rows[0]['n_players']*3}-x ходов на игрока побеждает в {pct:.1f}% партий (n={len(leader_data)})")

    print("\n=== Длительность партии (ходов всего на игру) ===")
    for n in PLAYER_COUNTS:
        turns = [r["turns"] for r in rows if r["n_players"] == n]
        print(f"{n} игрока(ов): среднее {statistics.mean(turns):.1f} ходов, "
              f"медиана {statistics.median(turns):.0f}, разброс {min(turns)}-{max(turns)}")

    print("\n=== Разброс итогового счёта (score_spread, чем ниже — тем ровнее партия) ===")
    for n in PLAYER_COUNTS:
        spreads = [r["score_spread"] for r in rows if r["n_players"] == n]
        print(f"{n} игрока(ов): среднее std {statistics.mean(spreads):.2f}")


if __name__ == "__main__":
    main()
