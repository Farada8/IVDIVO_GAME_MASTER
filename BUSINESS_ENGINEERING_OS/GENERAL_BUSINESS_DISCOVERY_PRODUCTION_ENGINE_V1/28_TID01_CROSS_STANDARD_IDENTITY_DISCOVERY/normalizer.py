#!/usr/bin/env python3
"""T-ID01 loss-aware normalization canary.

This intentionally normalizes only the documentation-derived fixture subset used by
T-ID01. It is not a full implementation of DNS-AID, ANS, A2A or MCP.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def _base(source_family: str, source_version: str | None) -> Dict[str, Any]:
    return {
        "source_family": source_family,
        "source_version": source_version,
        "identity": {
            "canonical_id": None,
            "display_name": None,
            "host": None,
            "provider": None,
            "agent_version": None,
            "protocol_version": None,
            "identity_anchor_kind": None,
        },
        "discovery_locations": [],
        "endpoints": [],
        "capability_evidence": {
            "source_type": None,
            "freshness": "UNKNOWN",
            "static_items": [],
            "live_introspection_required": False,
        },
        "trust_evidence": {
            "domain_control": "UNKNOWN",
            "card_signature": "UNKNOWN",
            "transparency_receipt": "UNKNOWN",
            "certificate_binding": "UNKNOWN",
            "integrity_digest": "UNKNOWN",
        },
    }


def _host(url: str | None) -> str | None:
    if not url or "://" not in url:
        return None
    return url.split("://", 1)[1].split("/", 1)[0]


def normalize_a2a(card: Dict[str, Any], source_version: str, discovery_path: str) -> Dict[str, Any]:
    out = _base("A2A", source_version)
    out["identity"].update(
        {
            "display_name": card.get("name"),
            "host": _host(card.get("url")),
            "provider": (card.get("provider") or {}).get("organization"),
            "agent_version": card.get("version"),
            "protocol_version": card.get("protocolVersion"),
            "identity_anchor_kind": "PROVIDER_DECLARED_METADATA",
        }
    )
    out["discovery_locations"].append(discovery_path)
    if card.get("url"):
        out["endpoints"].append(
            {
                "url": card["url"],
                "transport": card.get("preferredTransport", "JSONRPC"),
                "role": "REMOTE_INTERACTION",
            }
        )
    for item in card.get("additionalInterfaces", []):
        out["endpoints"].append(
            {"url": item.get("url"), "transport": item.get("transport"), "role": "REMOTE_INTERACTION"}
        )
    out["capability_evidence"].update(
        {
            "source_type": "STATIC_AGENT_CARD_SKILLS",
            "freshness": "CARD_FETCH_TIME",
            "static_items": [x.get("id") or x.get("name") for x in card.get("skills", [])],
            "live_introspection_required": False,
        }
    )
    out["trust_evidence"]["card_signature"] = "PRESENT" if card.get("signatures") else "ABSENT_OR_OPTIONAL"
    return out


def normalize_ans(reg: Dict[str, Any]) -> Dict[str, Any]:
    out = _base("ANS", reg.get("spec_version"))
    agent = reg.get("agent") or {}
    out["identity"].update(
        {
            "canonical_id": reg.get("ansName"),
            "display_name": agent.get("name"),
            "host": reg.get("agentHost") or agent.get("host"),
            "agent_version": agent.get("version") or reg.get("version"),
            "identity_anchor_kind": "FQDN_PROOF_OF_CONTROL_PLUS_VERSIONED_ANS_NAME",
        }
    )
    if out["identity"]["host"]:
        out["discovery_locations"].append(f"dns://{out['identity']['host']}")
    out["capability_evidence"].update(
        {
            "source_type": "SEALED_REGISTRATION_METADATA_OR_HASH",
            "freshness": "SEALED_EVENT_TIME",
            "static_items": sorted((reg.get("metadataHashes") or {}).keys()),
            "live_introspection_required": True,
        }
    )
    out["trust_evidence"].update(
        {
            "domain_control": "PROVEN_BY_ANS_PROFILE" if reg.get("domainValidation") else "UNKNOWN",
            "card_signature": "NOT_APPLICABLE",
            "transparency_receipt": "PRESENT" if reg.get("receipt") else "UNKNOWN",
            "certificate_binding": "PRESENT" if reg.get("identityCerts") else "UNKNOWN",
            "integrity_digest": "PRESENT" if reg.get("metadataHashes") else "UNKNOWN",
        }
    )
    return out


def normalize_dns_aid(meta: Dict[str, Any]) -> Dict[str, Any]:
    out = _base("DNS_AID", meta.get("aid_version"))
    identity = meta.get("identity") or {}
    connection = meta.get("connection") or {}
    out["identity"].update(
        {
            "canonical_id": meta.get("fqdn"),
            "display_name": identity.get("name"),
            "host": meta.get("fqdn") or meta.get("endpoint_host"),
            "agent_version": identity.get("version"),
            "protocol_version": connection.get("protocol"),
            "identity_anchor_kind": "DNS_NAME",
        }
    )
    if meta.get("fqdn"):
        out["discovery_locations"].extend(
            [f"dns://{meta['fqdn']}", f"https://{meta['fqdn']}/.well-known/agent.json"]
        )
    if meta.get("endpoint_url"):
        out["endpoints"].append(
            {
                "url": meta["endpoint_url"],
                "transport": connection.get("transport"),
                "role": "REMOTE_INTERACTION",
            }
        )
    actions = ((meta.get("capabilities") or {}).get("actions") or [])
    out["capability_evidence"].update(
        {
            "source_type": meta.get("capability_source", "DNS_AID_SOURCE_PRIORITY_CHAIN"),
            "freshness": "SOURCE_DEPENDENT",
            "static_items": [x.get("name") for x in actions],
            "live_introspection_required": connection.get("protocol") == "mcp",
        }
    )
    out["trust_evidence"].update(
        {
            "domain_control": meta.get("domain_control", "UNKNOWN"),
            "card_signature": "UNKNOWN",
            "transparency_receipt": "NOT_NATIVE_CORE_ASSURANCE",
            "certificate_binding": "UNKNOWN",
            "integrity_digest": "PRESENT" if meta.get("cap_sha256") else "UNKNOWN",
        }
    )
    return out


def normalize_mcp_registry(server: Dict[str, Any]) -> Dict[str, Any]:
    out = _base("MCP_REGISTRY", server.get("$schema"))
    name = server.get("name")
    out["identity"].update(
        {
            "canonical_id": name,
            "display_name": server.get("title") or name,
            "agent_version": server.get("version"),
            "identity_anchor_kind": "REGISTRY_NAMESPACE",
        }
    )
    for remote in server.get("remotes", []):
        out["endpoints"].append(
            {"url": remote.get("url"), "transport": remote.get("type"), "role": "REMOTE_MCP"}
        )
    for package in server.get("packages", []):
        out["endpoints"].append(
            {
                "url": package.get("identifier"),
                "transport": (package.get("transport") or {}).get("type"),
                "role": "INSTALLABLE_PACKAGE",
            }
        )
    out["capability_evidence"].update(
        {
            "source_type": "STATIC_SERVER_JSON_METADATA",
            "freshness": "REGISTRY_PUBLICATION_TIME",
            "static_items": [],
            "live_introspection_required": True,
        }
    )
    out["trust_evidence"].update(
        {
            "domain_control": "NAMESPACE_DEPENDENT",
            "card_signature": "NOT_APPLICABLE",
            "transparency_receipt": "NOT_APPLICABLE",
            "certificate_binding": "UNKNOWN",
            "integrity_digest": "PRESENT"
            if any(x.get("fileSha256") for x in server.get("packages", []))
            else "UNKNOWN",
        }
    )
    return out


def detect_findings(manifest: Dict[str, Any], normalized: Dict[str, Dict[str, Any]]) -> List[Dict[str, str]]:
    findings: List[Dict[str, str]] = []
    paths = manifest["a2a_paths"]
    if paths.get("0.2.6") != paths.get("0.3.0"):
        findings.append(
            {
                "id": "F001",
                "type": "WELL_KNOWN_PATH_DRIFT",
                "severity": "REAL_COMPATIBILITY_BREAK",
                "detail": f"A2A discovery path changed {paths.get('0.2.6')} -> {paths.get('0.3.0')}.",
            }
        )

    findings.append(
        {
            "id": "F002",
            "type": "VERSION_SEMANTICS_COLLISION",
            "severity": "LOSSY_IF_FLATTENED",
            "detail": "ANS identity version, A2A protocolVersion/agent version, DNS-AID identity/protocol and MCP server/schema version are distinct semantics.",
        }
    )
    findings.append(
        {
            "id": "F003",
            "type": "TRUST_ASSURANCE_NON_EQUIVALENCE",
            "severity": "UNSAFE_BOOLEAN_COLLAPSE",
            "detail": "A2A JWS card integrity, ANS domain/certificate/transparency proof, DNS integrity/domain evidence and MCP namespace/package evidence are separate assurance dimensions.",
        }
    )

    if normalized["mcp_registry"]["capability_evidence"]["live_introspection_required"]:
        findings.append(
            {
                "id": "F004",
                "type": "CAPABILITY_FRESHNESS_MISMATCH",
                "severity": "STATIC_METADATA_CANNOT_PROVE_RUNTIME_TOOLS",
                "detail": "MCP Registry server.json is static discovery/install metadata; live MCP tools are runtime protocol data, unlike a static A2A skills list.",
            }
        )

    if any(x["role"] == "INSTALLABLE_PACKAGE" for x in normalized["mcp_registry"]["endpoints"]):
        findings.append(
            {
                "id": "F005",
                "type": "ENDPOINT_ROLE_COLLISION",
                "severity": "REMOTE_URL_CANNOT_REPRESENT_INSTALLABLE_PACKAGE",
                "detail": "MCP package/stdio targets are installation artifacts, not remote interaction endpoints.",
            }
        )

    if normalized["a2a_0_3"]["identity"]["canonical_id"] is None and normalized["ans"]["identity"]["canonical_id"]:
        findings.append(
            {
                "id": "F006",
                "type": "GLOBAL_IDENTITY_SCOPE_MISMATCH",
                "severity": "IDENTIFIER_SYNTHESIS_WOULD_BE_INVENTED_DATA",
                "detail": "ANS exposes a versioned canonical ANSName; the minimal A2A AgentCard has no equivalent globally verified identifier. A normalizer must not invent one from display name or URL.",
            }
        )
    return findings


def run(manifest: Dict[str, Any]) -> Dict[str, Any]:
    fx = manifest["fixtures"]
    normalized = {
        "a2a_0_3": normalize_a2a(fx["a2a_0_3"]["data"], "0.3.0", manifest["a2a_paths"]["0.3.0"]),
        "ans": normalize_ans(fx["ans"]["data"]),
        "dns_aid": normalize_dns_aid(fx["dns_aid"]["data"]),
        "mcp_registry": normalize_mcp_registry(fx["mcp_registry"]["data"]),
    }
    findings = detect_findings(manifest, normalized)
    return {
        "schema": "ivdivo.general_business.tid01_result/1.0",
        "normalized": normalized,
        "findings": findings,
        "finding_count": len(findings),
        "semantic_gap_found": bool(findings),
        "proof_boundary": {
            "buyer_demand": "UNPROVEN",
            "wtp": "UNKNOWN",
            "market_winner": None,
            "external_action_authorized": False,
        },
    }


def main() -> None:
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "01_PUBLIC_FIXTURE_MANIFEST.json").read_text(encoding="utf-8"))
    print(json.dumps(run(manifest), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
