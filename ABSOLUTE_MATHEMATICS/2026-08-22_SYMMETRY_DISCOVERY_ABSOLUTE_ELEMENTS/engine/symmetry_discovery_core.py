from __future__ import annotations
import itertools, math, random


def all_perms(n):
    return list(itertools.permutations(range(n)))


def apply_perm(x, p):
    return [x[p[i]] for i in range(len(p))]


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def identity(n):
    return tuple(range(n))


def closure(generators, n):
    G = {identity(n)}
    changed = True
    while changed:
        changed = False
        current = list(G)
        for a in current:
            for b in generators + current:
                for c in (compose(a, b), compose(b, a)):
                    if c not in G:
                        G.add(c)
                        changed = True
    return sorted(G)


def discover_candidate_symmetry(task, n=4, trials=400, seed=0, tol=1e-9):
    rng = random.Random(seed)
    samples = [[rng.uniform(-1.3, 1.3) for _ in range(n)] for _ in range(trials)]
    good = []
    violations = {}
    for p in all_perms(n):
        worst = max(abs(task(x) - task(apply_perm(x, p))) for x in samples)
        violations[p] = worst
        if worst <= tol:
            good.append(p)
    return {"group": good, "size": len(good), "violations": violations,
            "status": "EMPIRICAL_CANDIDATE_UNLESS_EXACTLY_PROVED"}


def nonempty_subsets(n):
    return [s for k in range(1, n + 1) for s in itertools.combinations(range(n), k)]


def subset_action(S, p):
    return tuple(sorted(p[i] for i in S))


def subset_orbits(n, G):
    unseen = set(nonempty_subsets(n))
    orbits = []
    while unseen:
        S = min(unseen)
        orbit = {subset_action(S, p) for p in G}
        orbits.append(sorted(orbit))
        unseen -= orbit
    return sorted(orbits, key=lambda O: (len(O[0]), O[0]))


def burnside_subset_orbit_count(n, G):
    fixed_sum = 0
    for p in G:
        fixed_sum += sum(1 for S in nonempty_subsets(n) if subset_action(S, p) == S)
    return fixed_sum // len(G)


def orbit_sum_features(x, G):
    out = []
    for orbit in subset_orbits(len(x), G):
        out.append(sum(math.prod(x[i] for i in S) for S in orbit))
    return out


def relation_type_count(n, G):
    return len(subset_orbits(n, G))


def formal_relation_count(n):
    return 2 ** n - 1


def squarefree_tier_intrinsic_rank(n):
    # The tier includes the n singleton coordinates themselves, hence its
    # Jacobian contains I_n and has rank n everywhere.
    return n


def absolute_element_certificate(n, G, promotion_mode, selected_features,
                                 hidden_residual, tasks=None, interventions=None):
    return {
        "source_peer_count": n,
        "formal_relation_count": formal_relation_count(n),
        "symmetry_group_size": len(G),
        "relation_type_count": relation_type_count(n, G),
        "promotion_mode": promotion_mode,
        "candidate_absolute_elements": selected_features,
        "tasks": tasks or [],
        "interventions": interventions or [],
        "hidden_residual": hidden_residual,
        "intrinsic_dimension_hint": n,
        "claim_ceiling": "REPRESENTATION/ENGINEERING RESULT; NOT A NEW PHYSICAL DIMENSION"
    }
