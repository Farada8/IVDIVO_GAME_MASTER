"""Compatibility import for the runtime ProviderSnapshotContract."""
from runtime.provider_snapshot_contract import (  # noqa: F401
    AUTH_STATES,
    FORBIDDEN_KEY_TOKENS,
    SCHEMA_VERSION,
    canonical_hash,
    seal_snapshot,
    secret_field_hits,
    snapshot_content_hash,
    validate_provider_snapshot,
)

__all__ = [
    "AUTH_STATES",
    "FORBIDDEN_KEY_TOKENS",
    "SCHEMA_VERSION",
    "canonical_hash",
    "seal_snapshot",
    "secret_field_hits",
    "snapshot_content_hash",
    "validate_provider_snapshot",
]
