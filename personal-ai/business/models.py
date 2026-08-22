from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


class _Serializable:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Lead(_Serializable):
    id: str
    name: str
    contact: str | None = None
    status: str = "NEW"


@dataclass(frozen=True)
class Customer(_Serializable):
    id: str
    name: str
    contact: str | None = None


@dataclass(frozen=True)
class Job(_Serializable):
    id: str
    customer_id: str | None
    job_type: str
    description: str
    area_quantity: dict[str, str] | None = None
    status: str = "NEW"


@dataclass(frozen=True)
class Quote(_Serializable):
    id: str
    project_id: str
    job_id: str
    status: str
    currency: str
    total: dict[str, Any]
    unknowns: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Invoice(_Serializable):
    id: str
    quote_id: str
    total: str | None = None
    status: str = "DRAFT"


@dataclass(frozen=True)
class Supplier(_Serializable):
    id: str
    name: str
    contact: str | None = None


@dataclass(frozen=True)
class Expense(_Serializable):
    id: str
    job_id: str
    description: str
    amount: str | None = None
    status: str = "RECORDED"


@dataclass(frozen=True)
class Payment(_Serializable):
    id: str
    reference_id: str
    amount: str | None = None
    status: str = "PENDING"


@dataclass(frozen=True)
class FollowUp(_Serializable):
    id: str
    job_id: str
    note: str
    due_at: str | None = None
    status: str = "OPEN"
