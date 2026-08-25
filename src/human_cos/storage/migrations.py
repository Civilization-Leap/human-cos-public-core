"""Minimal deterministic SQL migration runner for S1."""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from psycopg import Connection

from human_cos.resources import read_runtime_resource_text

_MIGRATION_ROOT = Path(__file__).resolve().parents[3] / "migrations"
_FORWARD_NAME = "0001_s1_case_evidence.sql"
_ROLLBACK_NAME = "0001_s1_case_evidence.rollback.sql"


def _migration_sql(name: str) -> str:
    source = _MIGRATION_ROOT / name
    if source.is_file():
        return source.read_text(encoding="utf-8")
    return cast(str, read_runtime_resource_text(f"migrations/{name}", prefer_source=False))


def apply_s1_migration(connection: Connection[Any]) -> None:
    connection.execute(_migration_sql(_FORWARD_NAME))
    connection.commit()


def rollback_s1_migration(connection: Connection[Any]) -> None:
    connection.execute(_migration_sql(_ROLLBACK_NAME))
    connection.commit()
