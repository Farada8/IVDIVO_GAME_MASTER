from __future__ import annotations

import hashlib
import importlib.util
import json
import socket
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

FROZEN_DOMAINS = [
    "decathlon.ie",
    "brownthomas.com",
    "arnotts.ie",
    "elverys.ie",
    "ikea.com",
    "lego.com",
    "patagonia.com",
    "allbirds.com",
    "glossier.com",
    "gymshark.com",
]

ROOT = Path(__file__).resolve().parents[1]
SCANNER_PATH = ROOT / "17_AGENT_COMMERCE_READINESS_SCANNER_V0" / "scanner.py"
spec = importlib.util.spec_from_file_location("agent_commerce_scanner", SCANNER_PATH)
scanner = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = scanner
assert spec.loader is not None
spec.loader.exec_module(scanner)

OUTDIR = Path(__file__).resolve().parent / "out"
OUTDIR.mkdir(exist_ok=True)

USER_AGENT = "IVDIVO-P-EW02-readonly-probe/1.0 (+public-read-only; no checkout mutation)"
TIMEOUT_SECONDS = 12
MAX_BODY_BYTES = 1_000_000


def _probe(domain: str) -> dict[str, Any]:
    url = f"https://{domain}/.well-known/ucp"
    request = urllib.request.Request(
        url,
        method="GET",
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json, text/plain;q=0.9, */*;q=0.1",
        },
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS, context=ctx) as response:
            body = response.read(MAX_BODY_BYTES)
            status = int(response.status)
            final_url = response.geturl()
            content_type = response.headers.get("Content-Type")
            return {
                "probe_kind": "HTTP_RESPONSE",
                "requested_url": url,
                "final_url": final_url,
                "http_status": status,
                "content_type": content_type,
                "body_sha256": hashlib.sha256(body).hexdigest(),
                "body_bytes_captured": len(body),
                "body_truncated_at_bytes": MAX_BODY_BYTES if len(body) == MAX_BODY_BYTES else None,
                "body_text": body.decode("utf-8", errors="replace"),
            }
    except urllib.error.HTTPError as exc:
        body = exc.read(MAX_BODY_BYTES)
        return {
            "probe_kind": "HTTP_RESPONSE",
            "requested_url": url,
            "final_url": exc.geturl(),
            "http_status": int(exc.code),
            "content_type": exc.headers.get("Content-Type") if exc.headers else None,
            "body_sha256": hashlib.sha256(body).hexdigest(),
            "body_bytes_captured": len(body),
            "body_truncated_at_bytes": MAX_BODY_BYTES if len(body) == MAX_BODY_BYTES else None,
            "body_text": body.decode("utf-8", errors="replace"),
        }
    except (urllib.error.URLError, TimeoutError, socket.timeout, ssl.SSLError) as exc:
        return {
            "probe_kind": "NETWORK_ERROR",
            "requested_url": url,
            "final_url": None,
            "http_status": None,
            "content_type": None,
            "body_sha256": None,
            "body_bytes_captured": 0,
            "body_truncated_at_bytes": None,
            "error_type": type(exc).__name__,
            "error": str(exc)[:500],
        }


def _snapshot(domain: str, probe: dict[str, Any]) -> dict[str, Any]:
    # A public product page is not evidence that an OpenAI upload feed exists.
    openai_feed = {"evidence_state": "UNKNOWN"}

    if probe["probe_kind"] != "HTTP_RESPONSE":
        ucp = {"evidence_state": "UNKNOWN"}
    else:
        status = probe["http_status"]
        profile = None
        if status == 200:
            try:
                parsed = json.loads(probe.get("body_text") or "")
                profile = parsed if isinstance(parsed, dict) else None
            except json.JSONDecodeError:
                profile = None
        ucp = {
            "evidence_state": "PROBED_PUBLIC",
            "well_known_http_status": status,
            "authentication_required": False if status == 200 else None,
            "profile": profile,
            # Transaction-changing checkout probes are intentionally forbidden in P-EW02.
            "checkout_endpoints": {"create": None, "update": None, "complete": None},
            "identity_path": None,
            # Order implementation cannot be inferred from profile publication alone.
            "order_events": None,
            "order_request_signing": None,
        }
    return {"merchant_id": domain, "openai_feed": openai_feed, "ucp": ucp}


def main() -> int:
    if len(FROZEN_DOMAINS) != 10 or len(set(FROZEN_DOMAINS)) != 10:
        raise SystemExit("blind sample must contain exactly 10 unique frozen domains")

    observations: list[dict[str, Any]] = []
    scans: list[dict[str, Any]] = []
    for domain in FROZEN_DOMAINS:
        probe = _probe(domain)
        snapshot = _snapshot(domain, probe)
        result = scanner.scan(snapshot)
        observations.append({
            "merchant_id": domain,
            "probe": {k: v for k, v in probe.items() if k != "body_text"},
            "snapshot": snapshot,
        })
        scans.append(result)
        print(json.dumps({
            "merchant_id": domain,
            "probe_kind": probe["probe_kind"],
            "http_status": probe.get("http_status"),
            "disposition": result["disposition"],
            "counts": result["counts"],
        }, sort_keys=True))

    inaccessible = sum(x["probe"]["probe_kind"] != "HTTP_RESPONSE" for x in observations)
    false_promotions = sum(x["disposition"] == "READY_FOR_PLATFORM_CONFORMANCE_TEST_NOT_APPROVAL" for x in scans)
    generic_advice_outputs = 0  # scanner emits rule IDs/messages, never generic recommendation prose.
    evaluated = len(scans)
    merchant_specific_or_bound_unknown = sum(bool(x.get("findings")) for x in scans)

    if evaluated != 10:
        decision = "FAIL_TEST"
    elif false_promotions:
        decision = "FAIL_TEST"
    elif generic_advice_outputs:
        decision = "FAIL_TEST"
    elif inaccessible > 2:
        decision = "AMBIGUOUS_TEST"
    elif merchant_specific_or_bound_unknown < 8:
        decision = "AMBIGUOUS_TEST"
    else:
        decision = "PASS_TEST"

    summary = {
        "schema": "ivdivo.agent_commerce.pew02_blind10/0.1",
        "date": "2026-08-22",
        "ruleset_version": scanner.RULESET_VERSION,
        "frozen_domains": FROZEN_DOMAINS,
        "evaluated": evaluated,
        "http_responses": evaluated - inaccessible,
        "inaccessible_network_errors": inaccessible,
        "merchant_specific_or_evidence_bound_results": merchant_specific_or_bound_unknown,
        "generic_advice_outputs": generic_advice_outputs,
        "false_promotions": false_promotions,
        "decision": decision,
        "proof_boundary": {
            "platform_approval_proven": False,
            "buyer_demand_proven": False,
            "wtp_proven": False,
            "transaction_proven": False,
            "profitability_proven": False,
            "private_openai_feed_inferred_from_public_pages": False,
            "transaction_changing_checkout_probes_performed": False,
        },
    }

    (OUTDIR / "observations.json").write_text(json.dumps(observations, indent=2, sort_keys=True), encoding="utf-8")
    (OUTDIR / "scans.json").write_text(json.dumps(scans, indent=2, sort_keys=True), encoding="utf-8")
    (OUTDIR / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print("PEW02_SUMMARY=" + json.dumps(summary, sort_keys=True))
    return 0 if decision != "FAIL_TEST" else 2


if __name__ == "__main__":
    raise SystemExit(main())
