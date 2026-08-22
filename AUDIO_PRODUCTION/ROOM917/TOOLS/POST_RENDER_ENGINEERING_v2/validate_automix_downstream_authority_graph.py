#!/usr/bin/env python3
"""Fail-closed validator for ROOM917 E01 AutoMix downstream authority graph."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

PASS = "PASS_AUTOMIX_DOWNSTREAM_AUTHORITY_GRAPH"
HOLD = "HOLD_AUTOMIX_DOWNSTREAM_AUTHORITY_GRAPH"


def _edges(value: Any) -> List[Tuple[str, str]]:
    out: List[Tuple[str, str]] = []
    if not isinstance(value, list):
        return out
    for row in value:
        if isinstance(row, list) and len(row) == 2 and all(isinstance(x, str) and x for x in row):
            out.append((row[0], row[1]))
    return out


def _reachable(start: str, adjacency: Dict[str, Set[str]]) -> Set[str]:
    seen = {start}
    q = deque([start])
    while q:
        node = q.popleft()
        for nxt in adjacency.get(node, set()):
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
    return seen


def _has_cycle(nodes: Set[str], edges: List[Tuple[str, str]]) -> bool:
    indegree = {n: 0 for n in nodes}
    adjacency: Dict[str, Set[str]] = defaultdict(set)
    for a, b in edges:
        if b not in adjacency[a]:
            adjacency[a].add(b)
            indegree[b] = indegree.get(b, 0) + 1
    q = deque(sorted(n for n, deg in indegree.items() if deg == 0))
    visited = 0
    while q:
        node = q.popleft()
        visited += 1
        for nxt in sorted(adjacency.get(node, set())):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                q.append(nxt)
    return visited != len(nodes)


def evaluate(graph: Dict[str, Any]) -> Dict[str, Any]:
    reasons: List[str] = []
    if graph.get("schema_version") != "ivdivo.room917_automix_downstream_authority_graph/1.0":
        reasons.append("graph_schema_invalid")
    if graph.get("pipeline") != "AUTOMIX_V1":
        reasons.append("pipeline_not_automix_v1")
    if graph.get("release_authority") != "HUMAN_ONLY_AFTER_P003B":
        reasons.append("release_authority_boundary_invalid")

    nodes_raw = graph.get("nodes")
    if not isinstance(nodes_raw, list) or not nodes_raw or any(not isinstance(x, str) or not x for x in nodes_raw):
        reasons.append("nodes_invalid")
        nodes: Set[str] = set()
    else:
        nodes = set(nodes_raw)
        if len(nodes) != len(nodes_raw):
            reasons.append("duplicate_nodes")

    entry = graph.get("entry")
    terminal = graph.get("terminal")
    if entry not in nodes:
        reasons.append("entry_missing_from_nodes")
    if terminal not in nodes:
        reasons.append("terminal_missing_from_nodes")

    required_edges = _edges(graph.get("required_edges"))
    forbidden_edges = set(_edges(graph.get("forbidden_edges")))
    if len(required_edges) != len(graph.get("required_edges", [])):
        reasons.append("required_edges_invalid")
    if len(forbidden_edges) != len(graph.get("forbidden_edges", [])):
        reasons.append("forbidden_edges_invalid_or_duplicate")

    for a, b in required_edges:
        if a not in nodes or b not in nodes:
            reasons.append(f"required_edge_unknown_node:{a}->{b}")
        if (a, b) in forbidden_edges:
            reasons.append(f"required_edge_is_forbidden:{a}->{b}")

    if _has_cycle(nodes, required_edges):
        reasons.append("required_graph_has_cycle")

    adjacency: Dict[str, Set[str]] = defaultdict(set)
    for a, b in required_edges:
        adjacency[a].add(b)
    reachable = _reachable(entry, adjacency) if entry in nodes else set()
    if terminal in nodes and terminal not in reachable:
        reasons.append("terminal_not_reachable_from_entry")

    # Every node after entry must be reachable in the authoritative required chain.
    missing_reach = sorted(nodes - reachable)
    if missing_reach:
        reasons.append("unreachable_nodes:" + ",".join(missing_reach))

    # No-bypass invariants.
    eligibility = "P003B_AUTOMIX_ELIGIBILITY"
    package = "P003B_PACKAGE"
    listener = "P003B_LISTENER_QC"
    release = "RELEASE_DECISION"
    if eligibility not in nodes or package not in nodes:
        reasons.append("eligibility_or_package_node_missing")
    else:
        incoming_package = {a for a, b in required_edges if b == package}
        if incoming_package != {eligibility}:
            reasons.append("p003b_package_must_have_only_eligibility_as_authoritative_predecessor")

    if listener not in nodes or release not in nodes:
        reasons.append("listener_or_release_node_missing")
    else:
        incoming_release = {a for a, b in required_edges if b == release}
        if incoming_release != {listener}:
            reasons.append("release_must_have_only_listener_qc_as_authoritative_predecessor")

    machine_nodes = {
        "AUTOMIX_PREFLIGHT",
        "AUTOMATION_PLAN",
        "RENDER_MANIFEST",
        "REAL_RENDER_BYTES",
        "RENDER_MACHINE_QC",
        "P003B_RENDER_QC_HANDOFF",
        "P003B_AUTOMIX_ELIGIBILITY",
        "P003B_PACKAGE",
        "PASS_A_FREEZE",
    }
    for src in machine_nodes:
        if (src, release) in required_edges:
            reasons.append(f"machine_release_edge_forbidden:{src}")

    legacy = graph.get("legacy_paths")
    if not isinstance(legacy, dict) or "p003b_listener_package_builder.py" not in legacy:
        reasons.append("legacy_builder_authority_boundary_missing")
    else:
        note = str(legacy["p003b_listener_package_builder.py"])
        if "NOT_SUFFICIENT_AUTHORITY_FOR_AUTOMIX_V1" not in note:
            reasons.append("legacy_builder_not_explicitly_non_authoritative_for_automix")

    reasons = list(dict.fromkeys(reasons))
    return {
        "schema_version": "ivdivo.room917_automix_downstream_authority_graph_result/1.0",
        "project": graph.get("project", "ROOM917"),
        "episode": graph.get("episode", "E01"),
        "status": PASS if not reasons else HOLD,
        "release_authority": False,
        "entry": entry,
        "terminal": terminal,
        "reachable_node_count": len(reachable),
        "node_count": len(nodes),
        "reasons": reasons,
        "next": (
            "DOWNSTREAM_GRAPH_LOCKED__ADVANCE_NONSTOP_QUEUE"
            if not reasons
            else "REPAIR_GRAPH_OR_AUTHORITY_BOUNDARY__DO_NOT_TREAT_DOWNSTREAM_AS_SAFE"
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    graph = json.loads(args.graph.read_text(encoding="utf-8"))
    result = evaluate(graph)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(result["status"])
    for reason in result["reasons"]:
        print(f"- {reason}")
    return 0 if result["status"] == PASS else 4


if __name__ == "__main__":
    raise SystemExit(main())
