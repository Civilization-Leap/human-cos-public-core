"""Protocol Registry — the machine-readable contract that fixes the semantics
Human-COS will never let a model silently change.

Design intent (see ``01_ABSOLUTE_INVARIANTS.md``):
- Process authority lives in code + versioned protocols (I-01).
- Semantic protocol changes require an RFC + regression impact review (I-19).
- This module *loads*, *validates*, and *guards* the registry in a deterministic
  way so an agent cannot drift the contract during implementation.

S0 scope only: structure loading, schema validation, version/change control
guards, and no-silent-mutation checks.  No state machine, no orchestration,
no model adapters.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .version import InvalidVersionError, ProtocolVersion, parse_version

# --- Registry-level constants -------------------------------------------------

# Change-control discipline for the frozen registry.  A semantic change must go
# through an RFC + regression impact review; moving to a NEW development
# baseline additionally requires a new baseline version.  A bare "RFC" is NOT
# sufficient for V0.1 and must be rejected (see S0 review P0-3).
_ALLOWED_CHANGE_CONTROL: tuple[str, ...] = (
    "RFC + regression impact review",
    "RFC + regression impact review + new baseline version",
)

_REGISTRY_STATI = frozenset({"DRAFT", "FROZEN", "SUPERSEDED"})
_PROTOCOL_STATI = frozenset({"DRAFT", "FROZEN", "SUPERSEDED"})

# Registry keys whose *presence* is mandatory and never optional.
_REQUIRED_PROTOCOL_KEYS = ("id", "version", "status", "purpose", "merge_blocking_tests")


class ProtocolRegistryError(ValueError):
    """Base error for registry loading / validation problems."""


class ProtocolSchemaError(ProtocolRegistryError):
    """The registry document violates its own JSON Schema."""


class ProtocolConstraintError(ProtocolRegistryError):
    """The registry is structurally valid but violates Human-COS constraints:
    duplicate ids, missing versions, unknown status, illegal change control, etc.
    """


class ProtocolSilentChangeError(ProtocolConstraintError):
    """A FROZEN protocol changed semantic content without a version bump."""


@dataclass(frozen=True)
class ProtocolEntry:
    """A single protocol as declared in the registry."""

    id: str
    version: str
    status: str
    purpose: str
    merge_blocking_tests: tuple[str, ...]

    @property
    def parsed_version(self) -> ProtocolVersion:
        return parse_version(self.version)

    @property
    def semantic_signature(self) -> tuple[str, str, tuple[str, ...]]:
        """Everything about a protocol that, if changed without a version bump,
        constitutes a silent mutation."""
        return (self.status, self.purpose, self.merge_blocking_tests)


@dataclass(frozen=True)
class Registry:
    """Parsed, validated protocol registry."""

    version: str
    status: str
    change_control: str
    protocols: tuple[ProtocolEntry, ...]

    def by_id(self) -> dict[str, ProtocolEntry]:
        return {p.id: p for p in self.protocols}


@dataclass
class RegistryChange:
    """Outcome of diffing two registries, used for no-silent-mutation checks."""

    version_bumps: list[str] = field(default_factory=list)
    version_downgrades: list[str] = field(default_factory=list)
    added: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    silent_mutations: list[str] = field(default_factory=list)

    @property
    def is_clean(self) -> bool:
        return not self.silent_mutations

    @property
    def is_empty(self) -> bool:
        return not (
            self.version_bumps
            or self.version_downgrades
            or self.added
            or self.removed
            or self.silent_mutations
        )


# --- Loading ------------------------------------------------------------------


def _load_yaml(text_or_path: str | Path) -> dict[str, Any]:
    """Load YAML from a path or an inline YAML string, returning a dict."""
    candidate = str(text_or_path)
    if isinstance(text_or_path, Path):
        with text_or_path.open("r", encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    # A short string may be a relative file path; probe defensively.
    try:
        probe = Path(candidate)
        if probe.is_file():
            with probe.open("r", encoding="utf-8") as fh:
                return yaml.safe_load(fh) or {}
    except OSError:
        # Not a usable path (e.g. inline YAML too long for a filename).
        pass
    data = yaml.safe_load(candidate)
    return data if isinstance(data, dict) else ({} if data is None else data)


def load_protocol_registry(source: str | Path) -> Registry:
    """Load and fully validate a protocol registry from a YAML file or string.

    Validation pipeline (deterministic, all blocks on any failure):
    1. Parse YAML -> dict.
    2. Check against ``schemas/protocol-registry.schema.json`` (structural
       conformance: required keys, types, enums).
    3. Enforce Human-COS semantic constraints (unique ids, valid versions,
       legal change control).
    """
    registry = _load_yaml(source)
    if not isinstance(registry, dict):
        raise ProtocolConstraintError("protocol registry must be a YAML mapping")

    # Schema conformance first: missing keys, wrong types, and bad enums are
    # structural problems, reported as schema violations.
    _validate_schema(registry)

    return _build_registry(registry)


def _build_registry(registry: dict[str, Any]) -> Registry:
    constraints: list[str] = []

    version = str(registry["registry_version"])
    try:
        parse_version(version)
    except InvalidVersionError:
        constraints.append(f"registry version {version!r} is not a valid protocol version")

    status = registry["status"]
    if status not in _REGISTRY_STATI:
        constraints.append(f"registry status {status!r} not in {sorted(_REGISTRY_STATI)}")

    change_control = str(registry["change_control"]).strip()
    if not change_control:
        constraints.append("change_control must be non-empty")
    elif change_control not in _ALLOWED_CHANGE_CONTROL:
        constraints.append(
            f"change_control {change_control!r} is not an allowed control; "
            f"expected one of {_ALLOWED_CHANGE_CONTROL}"
        )

    seen_ids: set[str] = set()
    entries: list[ProtocolEntry] = []
    for item in registry["protocols"]:
        for key in _REQUIRED_PROTOCOL_KEYS:
            if key not in item:
                constraints.append(f"protocol entry missing key {key!r}")

        pid = str(item.get("id", "")).strip()
        if not pid:
            constraints.append("protocol id must be non-empty")
        elif pid in seen_ids:
            constraints.append(f"duplicate protocol id {pid!r}")
        seen_ids.add(pid)

        pver = item.get("version", "")
        try:
            parse_version(pver)
        except InvalidVersionError:
            constraints.append(f"protocol {pid!r} version {pver!r} is invalid")

        pstatus = item.get("status", "")
        if pstatus not in _PROTOCOL_STATI:
            constraints.append(
                f"protocol {pid!r} status {pstatus!r} not in {sorted(_PROTOCOL_STATI)}"
            )

        tests = tuple(item.get("merge_blocking_tests") or [])
        entries.append(
            ProtocolEntry(
                id=pid or "<missing>",
                version=pver or "<missing>",
                status=pstatus or "<missing>",
                purpose=str(item.get("purpose", "")),
                merge_blocking_tests=tests,
            )
        )

    if constraints:
        raise ProtocolConstraintError(
            "protocol registry constraint violations:\n  - " + "\n  - ".join(constraints)
        )

    return Registry(
        version=version,
        status=status,
        change_control=change_control,
        protocols=tuple(entries),
    )


def _validate_schema(registry: dict[str, Any]) -> None:
    """Validate the registry against the bundled protocol-registry schema."""
    from .schema_loader import validate_instance  # local import to avoid cycle

    errors = validate_instance(registry, "protocol-registry.schema.json")
    if errors:
        raise ProtocolSchemaError(
            "registry violates protocol-registry schema: " + "; ".join(errors[:10])
        )


# --- Change control: no silent mutation ---------------------------------------


def snapshot(registry: Registry) -> dict[str, ProtocolEntry]:
    """Return a stable id->entry map usable as a baseline snapshot."""
    return registry.by_id()


def detect_change(previous: dict[str, ProtocolEntry], current: Registry) -> RegistryChange:
    """Diff a previous snapshot against a newer registry.

    Raises nothing by itself; the caller decides whether the change is allowed.
    Semantic fields (status/purpose/merge_blocking_tests) changing while the
    *version stays identical* are flagged as ``silent_mutations`` because under
    I-19 a semantic change requires a version bump + RFC.
    """
    change = RegistryChange()
    current_map = current.by_id()

    for pid in sorted(current_map.keys() - previous.keys()):
        change.added.append(pid)
    for pid in sorted(previous.keys() - current_map.keys()):
        change.removed.append(pid)

    for pid in sorted(previous.keys() & current_map.keys()):
        old = previous[pid]
        new = current_map[pid]
        if new.parsed_version > old.parsed_version:
            change.version_bumps.append(f"{pid}: {old.version} -> {new.version}")
        elif new.parsed_version < old.parsed_version:
            change.version_downgrades.append(f"{pid}: {old.version} -> {new.version}")
        elif new.semantic_signature != old.semantic_signature:
            change.silent_mutations.append(pid)

    return change


def assert_no_silent_mutation(
    previous: dict[str, ProtocolEntry], current: Registry
) -> RegistryChange:
    """Raise if any FROZEN protocol mutated without authorization.

    Rejects (all are semantic-change hazards under I-19):
    - a *silent* semantic change without a version bump;
    - a version *downgrade* (never benign for a FROZEN protocol);
    - *removal* of a protocol that existed in the previous snapshot.

    A version *bump* or *addition* is reported but not rejected here (they
    cannot silently alter existing frozen semantics); the frozen-contract hash
    gate blocks them from the signed files.  Returns the change record otherwise.
    """
    change = detect_change(previous, current)
    faults: list[str] = []
    if change.silent_mutations:
        faults.append(
            "silent semantic change without version bump: " + ", ".join(change.silent_mutations)
        )
    if change.version_downgrades:
        faults.append("version downgrade: " + ", ".join(change.version_downgrades))
    if change.removed:
        faults.append("protocol removal: " + ", ".join(change.removed))
    if faults:
        raise ProtocolSilentChangeError("; ".join(faults))
    return change


def assert_no_unblessed_change(
    previous: dict[str, ProtocolEntry], current: Registry
) -> RegistryChange:
    """Strict gate for a FROZEN contract: raise unless the registry matches the
    previous snapshot exactly.

    Any addition, removal, version bump, version downgrade, or silent semantic
    change is rejected.  Encodes the S0 review rule that deleting, downgrading,
    modifying, or adding frozen protocols must never be silently accepted by an
    ordinary PR; real change requires RFC + regression impact review + a NEW
    baseline version (a new snapshot).
    """
    change = detect_change(previous, current)
    if change.is_empty:
        return change
    parts: list[str] = []
    if change.added:
        parts.append("added " + ", ".join(change.added))
    if change.removed:
        parts.append("removed " + ", ".join(change.removed))
    if change.version_bumps:
        parts.append("version bumps " + ", ".join(change.version_bumps))
    if change.version_downgrades:
        parts.append("version downgrades " + ", ".join(change.version_downgrades))
    if change.silent_mutations:
        parts.append("silent mutations " + ", ".join(change.silent_mutations))
    raise ProtocolSilentChangeError(
        (
            "unblessed change to frozen contract "
            "(RFC + regression impact review + new baseline version required): "
        )
        + "; ".join(parts)
    )


# --- Convenience iterators ----------------------------------------------------


def frozen_protocols(registry: Registry) -> Iterator[ProtocolEntry]:
    """Yield only FROZEN protocols — the ones that must never change silently."""
    for entry in registry.protocols:
        if entry.status == "FROZEN":
            yield entry
