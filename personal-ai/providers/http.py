from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from providers.base import ProviderHTTPError


@dataclass(frozen=True)
class JsonHTTPResponse:
    status: int
    headers: Mapping[str, str]
    data: dict[str, Any]


class JsonTransport(Protocol):
    def post_json(
        self,
        *,
        provider: str,
        url: str,
        headers: Mapping[str, str],
        payload: Mapping[str, Any],
        timeout: float,
    ) -> JsonHTTPResponse: ...


class UrllibJsonTransport:
    """Small stdlib JSON transport. Request headers are never echoed in errors."""

    def post_json(
        self,
        *,
        provider: str,
        url: str,
        headers: Mapping[str, str],
        payload: Mapping[str, Any],
        timeout: float,
    ) -> JsonHTTPResponse:
        request_headers = {"Content-Type": "application/json", **dict(headers)}
        body = json.dumps(dict(payload)).encode("utf-8")
        request = urllib.request.Request(url, data=body, headers=request_headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw = response.read().decode("utf-8")
                data = json.loads(raw) if raw else {}
                if not isinstance(data, dict):
                    raise ProviderHTTPError(provider, response.status, "non-object JSON response")
                return JsonHTTPResponse(
                    status=response.status,
                    headers=dict(response.headers.items()),
                    data=data,
                )
        except urllib.error.HTTPError as exc:
            message = "provider request failed"
            try:
                raw = exc.read().decode("utf-8")
                parsed = json.loads(raw)
                if isinstance(parsed, dict):
                    error = parsed.get("error")
                    if isinstance(error, dict) and isinstance(error.get("message"), str):
                        message = error["message"][:500]
                    elif isinstance(error, str):
                        message = error[:500]
            except Exception:
                pass
            raise ProviderHTTPError(provider, exc.code, message) from exc
        except urllib.error.URLError as exc:
            raise ProviderHTTPError(provider, 0, "network connection failed") from exc
        except json.JSONDecodeError as exc:
            raise ProviderHTTPError(provider, 0, "invalid JSON response") from exc
