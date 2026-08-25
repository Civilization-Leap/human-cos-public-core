"""Pre-publication hardening regressions for S0/S1 Public Core review findings."""

import pytest

from human_cos.protocols.registry import (
    ProtocolSilentChangeError,
    assert_no_unblessed_change,
    detect_change,
    load_protocol_registry,
    snapshot,
)
from human_cos.protocols.schema_loader import validate_instance

BASE_REGISTRY = """
registry_version: "0.1"
status: FROZEN
change_control: "RFC + regression impact review"
protocols:
  - id: T0_FREEZE
    version: "0.1"
    status: FROZEN
    purpose: "time boundary isolation"
    merge_blocking_tests: [AT-01, AT-03]
"""


def test_declared_datetime_format_is_enforced() -> None:
    instance = {
        "event_id": "evt-1",
        "timestamp": "not-a-date",
        "actor_type": "SYSTEM",
        "actor_id": "orchestrator",
        "event_type": "CASE_FROZEN",
        "object_ref": "case/c1",
    }

    errors = validate_instance(instance, "audit-event.schema.json")

    assert errors
    assert any("date-time" in error for error in errors)


@pytest.mark.parametrize(
    ("old", "new", "field_name"),
    [
        ('registry_version: "0.1"', 'registry_version: "0.2"', "registry_version"),
        ("status: FROZEN", "status: SUPERSEDED", "status"),
        (
            'change_control: "RFC + regression impact review"',
            'change_control: "RFC + regression impact review + new baseline version"',
            "change_control",
        ),
    ],
)
def test_strict_snapshot_rejects_registry_level_metadata_change(
    old: str, new: str, field_name: str
) -> None:
    previous = snapshot(load_protocol_registry(BASE_REGISTRY))
    current = load_protocol_registry(BASE_REGISTRY.replace(old, new, 1))

    # snapshot() remains dict-compatible for existing callers while retaining
    # metadata required by the strict frozen-registry gate.
    assert isinstance(previous, dict)
    assert "T0_FREEZE" in previous

    change = detect_change(previous, current)
    assert change.registry_metadata_changes
    assert any(field_name in item for item in change.registry_metadata_changes)
    assert not change.is_empty

    with pytest.raises(ProtocolSilentChangeError, match="registry metadata"):
        assert_no_unblessed_change(previous, current)
