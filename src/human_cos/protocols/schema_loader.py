"""Loader for the JSON Schemas bundled with Human-COS.

Schema files live in ``schemas/`` at the repository root and are the single
source of truth for the data contracts (Case, Evidence, Visibility, ...).

Because schemas cross-reference each other via relative ``$ref`` (e.g.
``case.schema.json`` references ``phase-profile.schema.json``), this module
builds a resolver scoped to the ``schemas/`` directory so references resolve
without network access.
"""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path
from typing import Any, cast

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

_SCHEMA_ROOT = Path(__file__).resolve().parents[3] / "schemas"


class SchemaNotFoundError(FileNotFoundError):
    """Raised when a requested schema file does not exist in ``schemas/``."""


@cache
def load_json_schema(name: str) -> dict[str, Any]:
    """Load and parse a bundled JSON Schema by filename (resolved under schemas/)."""
    path = Path(name)
    if not path.is_absolute():
        path = _SCHEMA_ROOT / path
    if not path.exists():
        raise SchemaNotFoundError(f"schema {name!r} not found under {_SCHEMA_ROOT}")
    with path.open("r", encoding="utf-8") as fh:
        return cast("dict[str, Any]", json.load(fh))


def list_schema_files() -> list[Path]:
    """Return all bundled schema files, sorted."""
    return sorted(_SCHEMA_ROOT.glob("*.schema.json"))


@cache
def _registry() -> Registry:
    """Build a ``referencing`` registry mapping each schema's file URI and bare
    filename to its parsed resource, so relative ``$ref`` (e.g. case ->
    phase-profile) resolves locally without network access."""
    resources: dict[str, Resource] = {}
    for path in list_schema_files():
        resource = Resource.from_contents(load_json_schema(path.name))
        resources[path.name] = resource
        resources[path.resolve().as_uri()] = resource
    return Registry().with_resources(resources.items())


def validator_for(name: str) -> Draft202012Validator:
    """Return a Draft-2020-12 validator for the named schema, resolving
    relative ``$ref`` against the bundled schemas directory."""
    schema = load_json_schema(name)
    return Draft202012Validator(schema, registry=_registry())


def validate_instance(instance: dict[str, Any], name: str) -> list[str]:
    """Validate ``instance`` against ``name``; return a list of error messages
    (empty means valid)."""
    errors = sorted(validator_for(name).iter_errors(instance), key=lambda e: list(e.absolute_path))
    return [f"{'/'.join(map(str, e.absolute_path)) or '.'}: {e.message}" for e in errors]
