"""Constraint-failure tests: duplicate ids, missing versions, unknown status,
and illegal change control must all fail validation (S0 exit criteria)."""

import pytest

from human_cos.protocols.registry import (
    ProtocolConstraintError,
    ProtocolRegistryError,
    load_protocol_registry,
)


def _build_yaml(  # noqa: E501 - signature readability
    protocols_yaml: str,
    *,
    reg_status: str = "FROZEN",
    change_control: str = "RFC + regression impact review",
) -> str:
    return (
        f'registry_version: "0.1"\n'
        f"status: {reg_status}\n"
        f'change_control: "{change_control}"\n'
        f"protocols:\n{protocols_yaml}"
    )


def _entry(pid: str, version: str = "0.1", status: str = "FROZEN") -> str:
    return (
        f"  - id: {pid}\n"
        f'    version: "{version}"\n'
        f"    status: {status}\n"
        f"    purpose: purpose of {pid}\n"
        f"    merge_blocking_tests: [AT-X]\n"
    )


def test_duplicate_protocol_id_fails() -> None:
    yaml_text = _build_yaml(_entry("P") + _entry("P"))
    with pytest.raises(ProtocolConstraintError, match="duplicate protocol id"):
        load_protocol_registry(yaml_text)


def test_missing_version_fails() -> None:
    # A missing 'version' is a structural/schema violation.
    entry = "  - id: P\n    status: FROZEN\n    purpose: demo\n    merge_blocking_tests: [AT-X]\n"
    with pytest.raises(ProtocolRegistryError, match="version"):
        load_protocol_registry(_build_yaml(entry))


def test_unknown_status_fails() -> None:
    # An unknown status is rejected by the JSON Schema enum.
    entry = _entry("P", status="WHATEVER")
    with pytest.raises(ProtocolRegistryError, match="status"):
        load_protocol_registry(_build_yaml(entry))


def test_bare_rfc_change_control_is_rejected() -> None:
    """A bare 'RFC' is NOT enough for the V0.1 frozen registry (S0 review P0-3)."""
    entry = _entry("P")
    with pytest.raises(ProtocolConstraintError, match="change_control"):
        load_protocol_registry(_build_yaml(entry, change_control="RFC"))


def test_invalid_change_control_fails() -> None:
    entry = _entry("P")
    with pytest.raises(ProtocolConstraintError, match="change_control"):
        load_protocol_registry(_build_yaml(entry, change_control="just fix it silently"))


def test_empty_change_control_fails() -> None:
    entry = _entry("P")
    with pytest.raises(ProtocolConstraintError, match="change_control"):
        load_protocol_registry(_build_yaml(entry, change_control=""))


def test_missing_status_key_flagged() -> None:
    # A missing 'status' key is a structural/schema violation.
    entry = '  - id: P\n    version: "0.1"\n    purpose: demo\n    merge_blocking_tests: [AT-X]\n'
    with pytest.raises(ProtocolRegistryError, match="status"):
        load_protocol_registry(_build_yaml(entry))


def test_schema_violation_raises_schema_error() -> None:
    """A registry missing the mandatory 'protocols' list must fail JSON Schema."""
    from human_cos.protocols.registry import ProtocolSchemaError

    yaml_text = (
        'registry_version: "0.1"\n'
        "status: FROZEN\n"
        'change_control: "RFC + regression impact review"\n'
        # protocols key intentionally absent
    )
    with pytest.raises(ProtocolSchemaError):
        load_protocol_registry(yaml_text)
