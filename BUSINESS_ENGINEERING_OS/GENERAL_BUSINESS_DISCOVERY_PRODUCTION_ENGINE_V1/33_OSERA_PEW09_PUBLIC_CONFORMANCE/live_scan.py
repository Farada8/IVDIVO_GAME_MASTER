#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from pathlib import Path

ORG = "finos-osera"
RELEASE_RE = re.compile(r"^v(?P<base>.+)\+backpatch\.(?P<n>\d{3})$")
BASELINE_RE = re.compile(r"^v(?P<base>.+)\+backpatch\.baseline$")


def ls_remote(repo: str) -> set[str]:
    url = f"https://github.com/{ORG}/{repo}.git"
    cp = subprocess.run(
        ["git", "ls-remote", "--heads", "--tags", url],
        text=True,
        capture_output=True,
        timeout=60,
    )
    if cp.returncode != 0:
        raise RuntimeError(f"git ls-remote failed for {repo}: {cp.stderr.strip()}")
    refs = set()
    for line in cp.stdout.splitlines():
        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue
        ref = parts[1]
        if ref.endswith("^{}"):
            ref = ref[:-3]
        refs.add(ref)
    return refs


def tag_ref(tag: str) -> str:
    return f"refs/tags/{tag}"


def base_from_baseline(tag: str) -> str | None:
    m = BASELINE_RE.match(tag)
    return m.group("base") if m else None


def release_parts(tag: str):
    m = RELEASE_RE.match(tag)
    if not m:
        return None
    return m.group("base"), int(m.group("n"))


def scan_one(item: dict) -> dict:
    repo = item["repo"]
    refs = ls_remote(repo)
    heads = sorted(r for r in refs if r.startswith("refs/heads/"))
    tags = sorted(r[len("refs/tags/"):] for r in refs if r.startswith("refs/tags/"))

    baseline_tag = item["baseline_tag"]
    expected_release_tags = item["release_tags"]
    baseline_exists = tag_ref(baseline_tag) in refs
    missing_expected_releases = [t for t in expected_release_tags if tag_ref(t) not in refs]
    release_exists = len(missing_expected_releases) == 0
    backpatch_heads = [h for h in heads if h.startswith("refs/heads/backpatch/")]

    baseline_base = base_from_baseline(baseline_tag)
    expected_release_parts = [release_parts(t) for t in expected_release_tags]
    valid_release_syntax = all(x is not None for x in expected_release_parts)
    bases = [x[0] for x in expected_release_parts if x is not None]
    ordinals = [x[1] for x in expected_release_parts if x is not None]
    lineage_ok = bool(baseline_base) and valid_release_syntax and all(b == baseline_base for b in bases)
    ordinals_ok = (
        valid_release_syntax
        and all(n > 0 for n in ordinals)
        and ordinals == sorted(set(ordinals))
        and all(re.search(r"\+backpatch\.\d{3}$", t) for t in expected_release_tags)
    )

    controls = {
        "FORK_001_repository_name": repo.startswith("backpatch-"),
        "FORK_002_current_backpatch_branch_visible": bool(backpatch_heads),
        "FORK_003_expected_baseline_tag_resolves": baseline_exists,
        "REL_003A_expected_release_tags_resolve": release_exists,
        "REL_003B_baseline_release_base_lineage": lineage_ok,
        "REL_003C_release_ordinal_metadata": ordinals_ok,
    }

    gap_classes = []
    # Count this only when a real baseline + published release exist, so an empty
    # or pre-release repository cannot masquerade as a branch/release mismatch.
    if baseline_exists and release_exists and not backpatch_heads:
        gap_classes.append("CURRENT_BACKPATCH_BRANCH_CONVENTION_GAP")
    if not baseline_exists:
        gap_classes.append("BASELINE_TAG_GAP")
    if not release_exists:
        gap_classes.append("RELEASE_TAG_GAP")
    if not lineage_ok or not ordinals_ok:
        gap_classes.append("VERSION_LINEAGE_GAP")

    return {
        "repo": repo,
        "baseline_tag": baseline_tag,
        "expected_release_tags": expected_release_tags,
        "backpatch_heads": backpatch_heads,
        "missing_expected_release_tags": missing_expected_releases,
        "controls": controls,
        "gap_classes": sorted(set(gap_classes)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    sample = json.loads(Path(args.sample).read_text(encoding="utf-8"))
    rows = [scan_one(x) for x in sample["repositories"]]

    gap_repos = {}
    for row in rows:
        for gap in row["gap_classes"]:
            gap_repos.setdefault(gap, []).append(row["repo"])

    independent_gap_classes = sorted(gap_repos)
    route = (
        "PASS_TECHNICAL_WEDGE_SURVIVES_M1_ONLY"
        if len(independent_gap_classes) >= 2
        else "KILL_AS_CURRENT_NEW_WIP_WATCH_STANDARD_EVOLUTION"
    )

    result = {
        "schema": "ivdivo.general_business.osera_pew09_result/1.0",
        "sample_size": len(rows),
        "controls_per_repo": 6,
        "rows": rows,
        "gap_classes": {k: sorted(v) for k, v in sorted(gap_repos.items())},
        "independent_frozen_public_gap_class_count": len(independent_gap_classes),
        "technical_route": route,
        "standards_level_observation_not_counted_as_release_defect": {
            "REL_002_AUTOMATED_ACCEPTANCE_CHECK_NOT_YET_DEFINED": True,
            "reason": "OSERA draft itself calls for a future automated publish-time bytecode comparison; no published artifact mismatch was measured by this gate."
        },
        "buyer_demand": "UNPROVEN",
        "wtp": "UNKNOWN",
        "price": None,
        "transactions": 0,
        "profitability": "UNPROVEN",
        "wip_promotion": False,
        "external_action_authorized": False,
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
