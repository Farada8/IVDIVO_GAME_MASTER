from __future__ import annotations

import json
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Any

from memory.store import MemoryStore
from projects.manager import ProjectStateManager

DOCUMENT_TYPES = {"estimate", "quote"}
_CURRENCY_RE = re.compile(r"^[A-Z]{3}$")
_MONEY = Decimal("0.01")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _decimal(value: Any, field: str, *, minimum: Decimal | None = None) -> Decimal:
    if isinstance(value, bool) or value is None:
        raise ValueError(f"{field} must be a decimal-compatible value")
    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{field} must be a decimal-compatible value") from exc
    if not parsed.is_finite():
        raise ValueError(f"{field} must be finite")
    if minimum is not None and parsed < minimum:
        raise ValueError(f"{field} must be >= {minimum}")
    return parsed


def _money(value: Decimal) -> str:
    return format(value.quantize(_MONEY, rounding=ROUND_HALF_UP), "f")


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


@dataclass(frozen=True)
class EvidenceReference:
    label: str | None
    memory_id: str | None
    memory_kind: str | None
    memory_hash: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "memory_id": self.memory_id,
            "memory_kind": self.memory_kind,
            "memory_hash": self.memory_hash,
        }


class BusinessCore:
    def __init__(self, home: Path) -> None:
        self.home = Path(home)
        self.projects = ProjectStateManager(self.home)
        self.memory = MemoryStore(self.home / "runtime" / "state.db")

    def _evidence(
        self,
        *,
        label: Any,
        memory_id: Any,
        field: str,
    ) -> EvidenceReference | None:
        clean_label = str(label).strip() if label is not None else ""
        clean_id = str(memory_id).strip() if memory_id is not None else ""
        if not clean_label and not clean_id:
            return None
        if clean_id:
            try:
                record = self.memory.get(clean_id)
            except KeyError as exc:
                raise ValueError(f"{field}_id does not resolve to persisted memory: {clean_id}") from exc
            if record.get("status") != "ACTIVE":
                raise ValueError(f"{field}_id is not ACTIVE: {clean_id}")
            return EvidenceReference(
                label=clean_label or record.get("source") or None,
                memory_id=clean_id,
                memory_kind=record.get("kind"),
                memory_hash=record.get("content_hash"),
            )
        return EvidenceReference(
            label=clean_label,
            memory_id=None,
            memory_kind=None,
            memory_hash=None,
        )

    def create_document(
        self,
        project_id: str,
        request: dict[str, Any],
        *,
        document_type: str,
    ) -> dict[str, Any]:
        if document_type not in DOCUMENT_TYPES:
            raise ValueError(f"document_type must be one of {sorted(DOCUMENT_TYPES)}")
        if not isinstance(request, dict):
            raise ValueError("business request must be a JSON object")

        project = self.projects.load_project(project_id)
        client = str(request.get("client", "")).strip()
        if not client:
            raise ValueError("client cannot be empty")
        currency = str(request.get("currency", "")).strip().upper()
        if not _CURRENCY_RE.fullmatch(currency):
            raise ValueError("currency must be a three-letter ISO-style code")
        raw_items = request.get("items")
        if not isinstance(raw_items, list) or not raw_items:
            raise ValueError("items must contain at least one line")

        document_id = f"business-{document_type}-{uuid.uuid4().hex}"
        created_at = _utc_now()
        missing_price_evidence: list[dict[str, Any]] = []
        items: list[dict[str, Any]] = []
        priced_subtotal = Decimal("0")

        for index, raw in enumerate(raw_items, start=1):
            if not isinstance(raw, dict):
                raise ValueError(f"items[{index}] must be a JSON object")
            item_id = str(raw.get("id") or f"item-{index:03d}").strip()
            description = str(raw.get("description", "")).strip()
            unit = str(raw.get("unit", "")).strip()
            if not item_id or not description or not unit:
                raise ValueError(f"items[{index}] requires id/description/unit")
            quantity = _decimal(raw.get("quantity"), f"items[{index}].quantity", minimum=Decimal("0"))
            if quantity == 0:
                raise ValueError(f"items[{index}].quantity must be > 0")

            unit_price_raw = raw.get("unit_price")
            unit_price = None
            if unit_price_raw is not None:
                unit_price = _decimal(
                    unit_price_raw,
                    f"items[{index}].unit_price",
                    minimum=Decimal("0"),
                )
            price_evidence = self._evidence(
                label=raw.get("price_source"),
                memory_id=raw.get("price_source_id"),
                field=f"items[{index}].price_source",
            )

            reasons: list[str] = []
            if unit_price is None:
                reasons.append("MISSING_UNIT_PRICE")
            if price_evidence is None:
                reasons.append("MISSING_PRICE_SOURCE")

            line_total: Decimal | None = None
            if not reasons and unit_price is not None:
                line_total = quantity * unit_price
                priced_subtotal += line_total
            else:
                missing_price_evidence.append({"item_id": item_id, "reasons": reasons})

            items.append(
                {
                    "id": item_id,
                    "description": description,
                    "quantity": format(quantity, "f"),
                    "unit": unit,
                    "unit_price": _money(unit_price) if unit_price is not None else None,
                    "price_evidence": price_evidence.to_dict() if price_evidence else None,
                    "line_total": _money(line_total) if line_total is not None else None,
                }
            )

        tax_rate_raw = request.get("tax_rate")
        tax_evidence = self._evidence(
            label=request.get("tax_source"),
            memory_id=request.get("tax_source_id"),
            field="tax_source",
        )
        tax_status = "NOT_SPECIFIED"
        tax_rate: Decimal | None = None
        tax_missing: list[str] = []
        if tax_rate_raw is not None:
            tax_rate = _decimal(tax_rate_raw, "tax_rate", minimum=Decimal("0"))
            if tax_rate > Decimal("1"):
                raise ValueError("tax_rate must be between 0 and 1")
            if tax_evidence is None:
                tax_status = "NEEDS_TAX_EVIDENCE"
                tax_missing.append("MISSING_TAX_SOURCE")
            else:
                tax_status = "SPECIFIED_WITH_SOURCE"
        elif tax_evidence is not None:
            tax_status = "NEEDS_TAX_EVIDENCE"
            tax_missing.append("MISSING_TAX_RATE")

        if missing_price_evidence:
            status = "NEEDS_PRICE_EVIDENCE"
        elif tax_missing:
            status = "NEEDS_TAX_EVIDENCE"
        else:
            status = "READY"

        subtotal_ex_tax = priced_subtotal if not missing_price_evidence else None
        tax_amount: Decimal | None = None
        total_inc_tax: Decimal | None = None
        if status == "READY" and subtotal_ex_tax is not None and tax_rate is not None:
            tax_amount = subtotal_ex_tax * tax_rate
            total_inc_tax = subtotal_ex_tax + tax_amount

        artifact_path = (
            Path(project["root"])
            / "artifacts"
            / "business"
            / f"{document_id}.json"
        )
        document: dict[str, Any] = {
            "schema": "ivdivo.personal_ai.business_document/0.1",
            "document_id": document_id,
            "document_type": document_type,
            "project_id": project_id,
            "client": client,
            "currency": currency,
            "status": status,
            "created_at": created_at,
            "items": items,
            "missing_price_evidence": missing_price_evidence,
            "priced_subtotal": _money(priced_subtotal),
            "subtotal_ex_tax": _money(subtotal_ex_tax) if subtotal_ex_tax is not None else None,
            "tax": {
                "status": tax_status,
                "rate": format(tax_rate, "f") if tax_rate is not None else None,
                "evidence": tax_evidence.to_dict() if tax_evidence else None,
                "missing_evidence": tax_missing,
                "amount": _money(tax_amount) if tax_amount is not None else None,
            },
            "total_inc_tax": _money(total_inc_tax) if total_inc_tax is not None else None,
            "assumptions": [],
            "price_policy": "NO_INVENTED_PRICES",
            "artifact_path": str(artifact_path),
        }
        _atomic_json(artifact_path, document)

        memory_record = self.memory.store(
            json.dumps(document, sort_keys=True),
            kind="OUTPUT",
            source="PL-06 Business Core",
            project_id=project_id,
            metadata={
                "document_id": document_id,
                "document_type": document_type,
                "status": status,
                "currency": currency,
                "artifact_path": str(artifact_path),
            },
        )
        document["output_memory_id"] = memory_record["id"]
        _atomic_json(artifact_path, document)
        return document
