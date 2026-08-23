"""Registry loader tests against the bundled protocol_registry_v0.1.yaml
(S0 / T-002, T-003 part)."""

import pytest

from human_cos.protocols.registry import (
    ProtocolRegistryError,
    frozen_protocols,
    load_protocol_registry,
    snapshot,
)
from human_cos.protocols.schema_loader import SchemaNotFoundError

REGISTRY_PATH = "protocols/protocol_registry_v0.1.yaml"


def test_loads_bundled_registry() -> None:
    registry = load_protocol_registry(REGISTRY_PATH)
    assert registry.version == "0.1"
    assert registry.status == "FROZEN"
    assert "RFC" in registry.change_control
    assert len(registry.protocols) >= 9


def test_bundled_registry_has_no_duplicate_ids() -> None:
    registry = load_protocol_registry(REGISTRY_PATH)
    ids = [p.id for p in registry.protocols]
    assert len(ids) == len(set(ids))


def test_bundled_registry_expected_protocols_present() -> None:
    registry = load_protocol_registry(REGISTRY_PATH)
    ids = {p.id for p in registry.protocols}
    expected = {
        "T0_FREEZE",
        "CONTAMINATION",
        "INDEPENDENCE",
        "BASELINE_PARITY",
        "DISSENT",
        "FALSIFICATION",
        "QUALIFICATION",
        "SAFETY",
        "PUBLICATION",
    }
    assert expected <= ids


def test_all_bundled_protocols_are_frozen() -> None:
    registry = load_protocol_registry(REGISTRY_PATH)
    frozen = list(frozen_protocols(registry))
    assert len(frozen) == len(registry.protocols)
    for entry in registry.protocols:
        assert entry.status == "FROZEN"


def test_every_protocol_has_merge_blocking_tests() -> None:
    registry = load_protocol_registry(REGISTRY_PATH)
    for entry in registry.protocols:
        assert entry.merge_blocking_tests, f"protocol {entry.id} has no merge-blocking tests"


def test_snapshot_is_stable_key_set() -> None:
    registry = load_protocol_registry(REGISTRY_PATH)
    snap = snapshot(registry)
    assert set(snap) == {p.id for p in registry.protocols}


def test_load_inline_yaml_works() -> None:
    yaml_text = """
registry_version: "0.1"
status: DRAFT
change_control: "RFC + regression impact review"
protocols:
  - id: P_DEMO
    version: "0.1"
    status: DRAFT
    purpose: demo
    merge_blocking_tests: [AT-DEMO]
"""
    registry = load_protocol_registry(yaml_text)
    assert registry.by_id()["P_DEMO"].purpose == "demo"


def test_load_non_mapping_raises() -> None:
    with pytest.raises(ProtocolRegistryError):
        load_protocol_registry("- just\n- a\n- list")


def test_missing_schema_raises_schema_error() -> None:
    with pytest.raises(SchemaNotFoundError):
        from human_cos.protocols.schema_loader import load_json_schema

        load_json_schema("no-such-file.schema.json")
