#!/usr/bin/env python3
import argparse
import json
import re
import urllib.request
from pathlib import Path

API = "https://api.github.com/repos/OpenSecureAIAlliance/RFCs"
UA = {"User-Agent": "ivdivo-business-engine-pew10"}


def get_json(url: str):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def get_text(url: str):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    repo = get_json(API)
    branch = repo.get("default_branch", "main")
    tree = get_json(f"{API}/git/trees/{branch}?recursive=1")
    rfc = get_text(f"https://raw.githubusercontent.com/OpenSecureAIAlliance/RFCs/{branch}/rfc-safe-proposal.md")
    issue5 = get_json(f"{API}/issues/5")

    paths = sorted(x.get("path", "") for x in tree.get("tree", []) if x.get("type") == "blob")
    schema_patterns = [
        re.compile(r"\.schema\.json$", re.I),
        re.compile(r"(^|/)(schema|schemas)/.*\.(json|ya?ml)$", re.I),
        re.compile(r"\.(proto|avsc|xsd|thrift|capnp)$", re.I),
    ]
    schema_artifacts = [p for p in paths if any(rx.search(p) for rx in schema_patterns)]

    lower_rfc = rfc.lower()
    machine_readable_mentions = lower_rfc.count("machine-readable")
    explicit_format_terms = {
        "opentelemetry": "opentelemetry" in lower_rfc,
        "ocsf": "ocsf" in lower_rfc,
        "stix": bool(re.search(r"\bstix\b", lower_rfc)),
        "json_schema": "json schema" in lower_rfc,
        "protobuf": "protobuf" in lower_rfc,
    }
    explicit_canonical_format_adopted = any(explicit_format_terms.values())

    issue_body = issue5.get("body") or ""
    issue5_open = issue5.get("state") == "open"
    issue5_says_no_format = "None of these name a format".lower() in issue_body.lower()

    rfc_exists = "Shared AI Findings Exchange (SAFE)" in rfc
    has_machine_readable_requirement = machine_readable_mentions > 0
    contract_ready = bool(schema_artifacts) or explicit_canonical_format_adopted

    route = "PROOF_ELIGIBLE_M1_ONLY" if contract_ready else "WATCH_SCHEMA_NOT_STABLE_ENOUGH_FOR_CONFORMANCE_PROOF"

    result = {
        "schema": "ivdivo.general_business.safe_pew10_contract_maturity/1.0",
        "upstream_repo": "OpenSecureAIAlliance/RFCs",
        "upstream_default_branch": branch,
        "upstream_head": tree.get("sha"),
        "rfc_exists": rfc_exists,
        "machine_readable_mentions": machine_readable_mentions,
        "has_machine_readable_requirement": has_machine_readable_requirement,
        "repository_blob_paths": paths,
        "normative_looking_schema_artifacts": schema_artifacts,
        "explicit_format_terms_in_rfc": explicit_format_terms,
        "explicit_canonical_format_adopted": explicit_canonical_format_adopted,
        "issue_5": {
            "state": issue5.get("state"),
            "open": issue5_open,
            "title": issue5.get("title"),
            "says_requirements_name_no_format": issue5_says_no_format,
            "url": issue5.get("html_url"),
        },
        "contract_ready_for_independent_conformance_proof": contract_ready,
        "technical_route": route,
        "generic_agent_observability_wedge": "KILL_SUBSTITUTED",
        "future_possible_wedge": "SAFE_SPECIFIC_EXCHANGE_COMPATIBILITY_COMPLETENESS_OR_REGRESSION_ONLY_IF_CANONICAL_CONTRACT_EMERGES",
        "buyer_demand": "UNPROVEN",
        "wtp": "UNKNOWN",
        "price": None,
        "transactions": 0,
        "profitability": "UNPROVEN",
        "wip_promotion": False,
        "external_action_authorized": False,
    }

    assert rfc_exists, "SAFE RFC disappeared; investigate upstream change"
    assert has_machine_readable_requirement, "machine-readable requirement disappeared; candidate changed materially"

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
