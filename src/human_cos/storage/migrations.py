"""Minimal deterministic SQL migration runner for S1."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from psycopg import Connection

_MIGRATION_ROOT = Path(__file__).resolve().parents[3] / "migrations"
_FORWARD = _MIGRATION_ROOT / "0001_s1_case_evidence.sql"
_ROLLBACK = _MIGRATION_ROOT / "0001_s1_case_evidence.rollback.sql"


def apply_s1_migration(connection: Connection[Any]) -> None:
    connection.execute(_FORWARD.read_text(encoding="utf-8"))
    connection.commit()


def rollback_s1_migration(connection: Connection[Any]) -> None:
    connection.execute(_ROLLBACK.read_text(encoding="utf-8"))
    connection.commit()
