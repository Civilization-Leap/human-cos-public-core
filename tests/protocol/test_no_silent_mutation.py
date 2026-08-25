"""No-silent-mutation change control (S0 / T-002, invariant I-19)."""

import pytest

from human_cos.protocols.registry import (
    ProtocolSilentChangeError,
    assert_no_silent_mutation,
    assert_no_unblessed_change,
    detect_change,
    load_protocol_registry,
    snapshot,
)

BASE = """
registry_version: "0.1"
status: FROZEN
change_control: "RFC + regression impact review"
protocols:
  - id: T0_FREEZE
    version: "0.1"
    status: FROZEN
    purpose: "time boundary isolation"
    merge_blocking_tests: [AT-01, AT-03]
  - id: DISSENT
    version: "0.1"
    status: FROZEN
    purpose: "minority opinion preservation"
    merge_blocking_tests: [AT-07]
"""


@pytest.fixture()
def baseline() -> dict:
    return snapshot(load_protocol_registry(BASE))


def _registry_with(*overrides_yaml: str) -> str:
    block = "".join(overrides_yaml)
    head = (
        'registry_version: "0.1"\n'
        "status: FROZEN\n"
        'change_control: "RFC + regression impact review"\n'
        "protocols:\n"
    )
    return head + block


def _as_yaml(pid: str, version: str, purpose: str, tests: str = "[AT-07]") -> str:
    return (
        f"  - id: {pid}\n"
        f'    version: "{version}"\n'
        f"    status: FROZEN\n"
        f'    purpose: "{purpose}"\n'
        f"    merge_blocking_tests: {tests}\n"
    )


def test_identical_registry_is_clean(baseline: dict) -> None:
    current = load_protocol_registry(BASE)
    change = assert_no_silent_mutation(baseline, current)
    assert change.is_clean
    assert not change.added and not change.removed and not change.version_bumps


def test_version_bump_is_allowed(baseline: dict) -> None:
    modified = _registry_with(
        _as_yaml("T0_FREEZE", "0.1", "time boundary isolation", tests="[AT-01, AT-03]"),
        _as_yaml("DISSENT", "0.2", "minority opinion preservation"),
    )
    current = load_protocol_registry(modified)
    change = assert_no_silent_mutation(baseline, current)
    assert change.is_clean
    assert "DISSENT" in {b.split(":")[0] for b in change.version_bumps}


def test_frozen_semantic_change_without_version_bump_fails(baseline: dict) -> None:
    # Same version 0.1 but purpose changed -> silent mutation.
    modified = _registry_with(_as_yaml("DISSENT", "0.1", "now lets models delete dissent"))
    current = load_protocol_registry(modified)
    with pytest.raises(ProtocolSilentChangeError, match="DISSENT"):
        assert_no_silent_mutation(baseline, current)


def test_detect_change_reports_silent_mutation(baseline: dict) -> None:
    modified = _registry_with(_as_yaml("DISSENT", "0.1", "changed purpose same version"))
    current = load_protocol_registry(modified)
    change = detect_change(baseline, current)
    assert change.silent_mutations == ["DISSENT"]
    assert not change.is_clean


def test_added_and_removed_are_reported_but_not_silent(baseline: dict) -> None:
    modified = _registry_with(
        _as_yaml("DISSENT", "0.1", "minority opinion preservation"),
        _as_yaml("NEW_PROTO", "0.1", "brand new"),
    )
    current = load_protocol_registry(modified)
    change = detect_change(baseline, current)
    assert change.added == ["NEW_PROTO"]
    assert change.is_clean


def test_version_downgrade_fails(baseline: dict) -> None:
    # Registry-level downgrade of a FROZEN protocol must be rejected.
    prev_yaml = _registry_with(_as_yaml("DISSENT", "0.2", "minority opinion preservation"))
    cur_yaml = _registry_with(_as_yaml("DISSENT", "0.1", "minority opinion preservation"))
    prev = snapshot(load_protocol_registry(prev_yaml))
    current = load_protocol_registry(cur_yaml)
    with pytest.raises(ProtocolSilentChangeError, match="downgrade"):
        assert_no_silent_mutation(prev, current)


def test_removal_of_frozen_protocol_fails(baseline: dict) -> None:
    # Dropping DISSENT from the registry must be rejected.
    current = load_protocol_registry(
        _registry_with(_as_yaml("T0_FREEZE", "0.1", "time boundary isolation"))
    )
    with pytest.raises(ProtocolSilentChangeError, match="removal"):
        assert_no_silent_mutation(baseline, current)


def test_no_unblessed_change_accepts_identical(baseline: dict) -> None:
    current = load_protocol_registry(BASE)
    change = assert_no_unblessed_change(baseline, current)
    assert change.is_empty


def test_no_unblessed_change_rejects_bump(baseline: dict) -> None:
    current = load_protocol_registry(
        _registry_with(_as_yaml("DISSENT", "0.2", "minority opinion preservation"))
    )
    with pytest.raises(ProtocolSilentChangeError, match="unblessed"):
        assert_no_unblessed_change(baseline, current)


def test_no_unblessed_change_rejects_addition(baseline: dict) -> None:
    current = load_protocol_registry(
        _registry_with(
            _as_yaml("DISSENT", "0.1", "minority opinion preservation"),
            _as_yaml("EXTRA", "0.1", "should not sneak in"),
        )
    )
    with pytest.raises(ProtocolSilentChangeError, match="unblessed"):
        assert_no_unblessed_change(baseline, current)
