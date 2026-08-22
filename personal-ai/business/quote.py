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

from business.models import Job, Quote
from business.store import BusinessStore

_CURRENCY_RE = re.compile(r"^[A-Z]{3}$")
_MONEY = Decimal("0.01")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _decimal(value: Any, field: str) -> Decimal | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        raise ValueError(f"{field} must be a decimal-compatible value")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{field} must be a decimal-compatible value") from exc
    if not result.is_finite() or result < 0:
        raise ValueError(f"{field} must be a finite non-negative value")
    return result


def _money(value: Decimal) -> str:
    return format(value.quantize(_MONEY, rounding=ROUND_HALF_UP), "f")


@dataclass(frozen=True)
class AmountState:
    status: str
    amount: str | None
    currency: str
    reason: str | None = None

    @classmethod
    def known(cls, value: Decimal, currency: str) -> "AmountState":
        return cls("KNOWN", _money(value), currency, None)

    @classmethod
    def tbd(cls, currency: str, reason: str) -> "AmountState":
        return cls("TBD", None, currency, reason)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "amount": self.amount,
            "currency": self.currency,
            "reason": self.reason,
        }

    def decimal(self) -> Decimal | None:
        return Decimal(self.amount) if self.status == "KNOWN" and self.amount is not None else None


class BusinessQuoteService:
    """Fail-closed CLIENT REQUEST -> JOB -> COSTS -> MARGIN -> QUOTE -> SAVE workflow."""

    def __init__(self, home: Path) -> None:
        self.home = Path(home)
        self.projects = ProjectStateManager(self.home)
        self.memory = MemoryStore(self.home / "runtime" / "state.db")
        self.store = BusinessStore(self.home)

    @staticmethod
    def _currency(payload: dict[str, Any]) -> str:
        currency = str(payload.get("currency", "EUR")).strip().upper()
        if not _CURRENCY_RE.fullmatch(currency):
            raise ValueError("currency must be a three-letter ISO-style code")
        return currency

    @staticmethod
    def _labour(payload: dict[str, Any], currency: str, unknowns: list[str]) -> AmountState:
        hours = _decimal(payload.get("hours"), "hours")
        rate = _decimal(payload.get("labour_rate"), "labour_rate")
        if hours is None:
            unknowns.append("LABOUR_HOURS_TBD")
        if rate is None:
            unknowns.append("LABOUR_RATE_TBD")
        if hours is None or rate is None:
            return AmountState.tbd(currency, "hours and labour_rate must both be explicitly supplied")
        return AmountState.known(hours * rate, currency)

    @staticmethod
    def _materials(
        payload: dict[str, Any],
        currency: str,
        unknowns: list[str],
    ) -> tuple[AmountState, list[dict[str, Any]]]:
        raw_lines = payload.get("materials")
        not_required = payload.get("materials_not_required", False)
        if not isinstance(not_required, bool):
            raise ValueError("materials_not_required must be boolean")
        if not_required:
            if raw_lines not in (None, []):
                raise ValueError("materials cannot be supplied when materials_not_required=true")
            return AmountState.known(Decimal("0"), currency), []

        if raw_lines is None or raw_lines == []:
            unknowns.append("MATERIALS_TBD")
            return AmountState.tbd(
                currency,
                "materials are missing; set materials_not_required=true only when explicitly applicable",
            ), []
        if not isinstance(raw_lines, list):
            raise ValueError("materials must be a list")

        lines: list[dict[str, Any]] = []
        total = Decimal("0")
        complete = True
        for index, raw in enumerate(raw_lines, start=1):
            if not isinstance(raw, dict):
                raise ValueError(f"materials[{index}] must be an object")
            description = str(raw.get("description", "")).strip()
            if not description:
                raise ValueError(f"materials[{index}].description is required")
            quantity = _decimal(raw.get("quantity"), f"materials[{index}].quantity")
            unit_price = _decimal(raw.get("unit_price"), f"materials[{index}].unit_price")
            reasons: list[str] = []
            if quantity is None:
                reasons.append("QUANTITY_TBD")
            if unit_price is None:
                reasons.append("UNIT_PRICE_TBD")

            line_total: Decimal | None = None
            if not reasons:
                assert quantity is not None and unit_price is not None
                line_total = quantity * unit_price
                total += line_total
            else:
                complete = False
                unknowns.extend(f"MATERIAL_{index}_{reason}" for reason in reasons)

            lines.append(
                {
                    "description": description,
                    "quantity": format(quantity, "f") if quantity is not None else None,
                    "unit": str(raw.get("unit", "")).strip() or None,
                    "unit_price": _money(unit_price) if unit_price is not None else None,
                    "price_source": str(raw.get("price_source", "")).strip() or None,
                    "line_total": _money(line_total) if line_total is not None else None,
                    "status": "KNOWN" if not reasons else "TBD",
                    "reasons": reasons,
                }
            )

        if not complete:
            return AmountState.tbd(currency, "one or more material quantities/prices are TBD"), lines
        return AmountState.known(total, currency), lines

    @staticmethod
    def _combine(
        labour: AmountState,
        materials: AmountState,
        currency: str,
        unknowns: list[str],
    ) -> AmountState:
        labour_value = labour.decimal()
        material_value = materials.decimal()
        if labour_value is None or material_value is None:
            unknowns.append("SUBTOTAL_TBD")
            return AmountState.tbd(currency, "labour and material totals must both be KNOWN")
        return AmountState.known(labour_value + material_value, currency)

    @staticmethod
    def _margin_and_total(
        subtotal: AmountState,
        payload: dict[str, Any],
        currency: str,
        unknowns: list[str],
    ) -> tuple[str | None, AmountState, AmountState]:
        margin_percent = _decimal(payload.get("margin_percent"), "margin_percent")
        subtotal_value = subtotal.decimal()
        if margin_percent is None:
            unknowns.append("MARGIN_PERCENT_TBD")
        if subtotal_value is None or margin_percent is None:
            margin = AmountState.tbd(currency, "known subtotal and explicit margin_percent are required")
            total = AmountState.tbd(currency, "subtotal or margin is TBD")
            unknowns.append("QUOTE_TOTAL_TBD")
            return None if margin_percent is None else format(margin_percent, "f"), margin, total
        margin_value = subtotal_value * margin_percent / Decimal("100")
        return (
            format(margin_percent, "f"),
            AmountState.known(margin_value, currency),
            AmountState.known(subtotal_value + margin_value, currency),
        )

    @staticmethod
    def _markdown(document: dict[str, Any]) -> str:
        estimate = document["estimate"]

        def show(state: dict[str, Any]) -> str:
            if state["status"] == "KNOWN":
                return f'{state["currency"]} {state["amount"]}'
            return f'TBD — {state["reason"]}'

        rows = [
            ("Labour", show(estimate["labour"])),
            ("Materials", show(estimate["materials"]["total"])),
            ("Subtotal", show(estimate["subtotal"])),
            (
                "Margin",
                (f'{estimate["margin_percent"]}% / ' if estimate["margin_percent"] is not None else "TBD % / ")
                + show(estimate["margin"]),
            ),
            ("Quote total", show(estimate["total"])),
        ]
        lines = [
            f'# Quote {document["quote_id"]}',
            "",
            f'**Status:** {document["status"]}',
            f'**Project:** {document["project_id"]}',
            f'**Job:** {document["job"]["job_type"]} — {document["job"]["description"]}',
            "",
            "| Component | Value |",
            "|---|---:|",
        ]
        lines.extend(f"| {label} | {value} |" for label, value in rows)
        if document["unknowns"]:
            lines.extend(["", "## TBD / unknown inputs"])
            lines.extend(f"- {item}" for item in document["unknowns"])
        lines.extend(
            [
                "",
                "No missing price, rate, quantity or margin is converted to zero.",
                "Area/quantity is descriptive unless an explicit price input is supplied.",
                "",
            ]
        )
        return "\n".join(lines)

    def create_quote(self, project_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise ValueError("quote request must be a JSON object")
        project = self.projects.load_project(project_id)
        client_request = str(payload.get("client_request", "")).strip()
        job_type = str(payload.get("job_type", "")).strip()
        if not client_request:
            raise ValueError("client_request is required")
        if not job_type:
            raise ValueError("job_type is required")

        currency = self._currency(payload)
        description = str(payload.get("description", "")).strip() or client_request
        area = payload.get("area_quantity")
        if area is not None and not isinstance(area, dict):
            raise ValueError("area_quantity must be an object when supplied")

        quote_id = str(payload.get("quote_id") or f"quote-{uuid.uuid4().hex}").strip()
        job_id = str(payload.get("job_id") or f"job-{uuid.uuid4().hex}").strip()
        customer_id = str(payload.get("customer_id", "")).strip() or None
        created_at = _utc_now()

        unknowns: list[str] = []
        labour = self._labour(payload, currency, unknowns)
        materials_total, material_lines = self._materials(payload, currency, unknowns)
        subtotal = self._combine(labour, materials_total, currency, unknowns)
        margin_percent, margin, total = self._margin_and_total(
            subtotal, payload, currency, unknowns
        )
        unknowns = list(dict.fromkeys(unknowns))
        status = "READY" if total.status == "KNOWN" else "TBD"

        area_quantity = None
        if area is not None:
            value = str(area.get("value", "")).strip()
            unit = str(area.get("unit", "")).strip()
            if not value or not unit:
                raise ValueError("area_quantity requires value and unit")
            area_quantity = {"value": value, "unit": unit}

        job = Job(
            id=job_id,
            customer_id=customer_id,
            job_type=job_type,
            description=description,
            area_quantity=area_quantity,
            status="ESTIMATED" if status == "READY" else "ESTIMATE_TBD",
        )
        quote_entity = Quote(
            id=quote_id,
            project_id=project_id,
            job_id=job_id,
            status=status,
            currency=currency,
            total=total.to_dict(),
            unknowns=tuple(unknowns),
        )

        document: dict[str, Any] = {
            "schema": "ivdivo.personal_ai.business_quote/0.1",
            "quote_id": quote_id,
            "project_id": project_id,
            "created_at": created_at,
            "status": status,
            "price_policy": "NO_INVENTED_PRICES",
            "request": {
                "client_request": client_request,
                "currency": currency,
                "hours": payload.get("hours"),
                "labour_rate": payload.get("labour_rate"),
                "margin_percent": payload.get("margin_percent"),
                "materials_not_required": payload.get("materials_not_required", False),
                "area_quantity": area_quantity,
            },
            "job": job.to_dict(),
            "estimate": {
                "labour": labour.to_dict(),
                "materials": {"total": materials_total.to_dict(), "lines": material_lines},
                "subtotal": subtotal.to_dict(),
                "margin_percent": margin_percent,
                "margin": margin.to_dict(),
                "total": total.to_dict(),
            },
            "unknowns": unknowns,
        }
        markdown = self._markdown(document)
        json_path, md_path = self.store.save_quote_artifacts(
            Path(project["root"]), quote_id, document, markdown
        )
        self.store.save_entity("job", job_id, job.to_dict())
        self.store.save_entity("quote", quote_id, quote_entity.to_dict())

        memory_record = self.memory.store(
            json.dumps(document, sort_keys=True),
            kind="OUTPUT",
            source="PL-06 Business Core",
            project_id=project_id,
            metadata={
                "quote_id": quote_id,
                "job_id": job_id,
                "status": status,
                "json_path": str(json_path),
                "markdown_path": str(md_path),
            },
        )
        result = dict(document)
        result["artifacts"] = {
            "json": str(json_path),
            "markdown": str(md_path),
            "output_memory_id": memory_record["id"],
        }
        return result
