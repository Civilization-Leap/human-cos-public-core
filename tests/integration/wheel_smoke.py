"""Smoke validation executed with an installed wheel from outside the repository."""

from __future__ import annotations

import os

import psycopg

from human_cos.protocols.frozen_contract import assert_bundled_frozen_contracts_intact
from human_cos.protocols.schema_loader import validate_instance
from human_cos.storage.migrations import apply_s1_migration, rollback_s1_migration


def main() -> None:
    report = assert_bundled_frozen_contracts_intact()
    assert report.ok and len(report.items) == 10

    invalid_event = {
        "event_id": "wheel-smoke",
        "timestamp": "not-a-date",
        "actor_type": "SYSTEM",
        "actor_id": "wheel-smoke",
        "event_type": "SMOKE",
        "object_ref": "distribution",
    }
    errors = validate_instance(invalid_event, "audit-event.schema.json")
    assert errors and any("date-time" in error for error in errors)

    database_url = os.environ["HUMAN_COS_TEST_DATABASE_URL"]
    connection = psycopg.connect(database_url)
    try:
        rollback_s1_migration(connection)
        apply_s1_migration(connection)
        row = connection.execute(
            """
            SELECT to_regclass('public.human_cos_context_admission'),
                   to_regclass('public.human_cos_evidence_revision'),
                   to_regclass('public.human_cos_case_revision')
            """
        ).fetchone()
        assert row is not None and all(item is not None for item in row)
        rollback_s1_migration(connection)
        row = connection.execute(
            """
            SELECT to_regclass('public.human_cos_context_admission'),
                   to_regclass('public.human_cos_evidence_revision'),
                   to_regclass('public.human_cos_case_revision')
            """
        ).fetchone()
        assert row == (None, None, None)
    finally:
        connection.close()

    print("installed wheel smoke: PASS")


if __name__ == "__main__":
    main()
