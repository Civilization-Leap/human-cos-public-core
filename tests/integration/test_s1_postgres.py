from __future__ import annotations

import os
from datetime import datetime, timezone

import psycopg
import pytest

from human_cos.core.context import ContextBuildRequest, build_context
from human_cos.storage.migrations import apply_s1_migration, rollback_s1_migration
from human_cos.storage.repository import PostgresRepository

DATABASE_URL = os.getenv("HUMAN_COS_TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(not DATABASE_URL, reason="HUMAN_COS_TEST_DATABASE_URL not set")


@pytest.fixture()
def db_connection():
    assert DATABASE_URL is not None
    connection = psycopg.connect(DATABASE_URL)
    try:
        rollback_s1_migration(connection)
        apply_s1_migration(connection)
        yield connection
    finally:
        try:
            rollback_s1_migration(connection)
        finally:
            connection.close()


def test_at03_evidence_is_append_only_and_revisioned(
    db_connection, case_document, evidence_factory, clone_document
) -> None:
    repo = PostgresRepository(db_connection)
    repo.create_case(case_document)
    original_doc = evidence_factory("e-revision", public=True, snapshot_char="a")
    repo.create_evidence(original_doc)

    with pytest.raises(psycopg.errors.RaiseException, match="immutable record"):
        db_connection.execute(
            "UPDATE human_cos_evidence_revision SET snapshot_hash = %s WHERE evidence_id = %s",
            ("b" * 64, "e-revision"),
        )
    db_connection.rollback()

    revised = clone_document(original_doc)
    revised["content"] = "new observation; old revision retained"
    revised["snapshot_hash"] = "c" * 64
    _, revision = repo.revise_evidence(revised)
    assert revision == 2
    old, old_revision = repo.get_evidence("e-revision", revision=1)
    latest, latest_revision = repo.get_evidence("e-revision")
    assert old_revision == 1 and old.snapshot_hash == "a" * 64
    assert latest_revision == 2 and latest.snapshot_hash == "c" * 64


def test_case_t0_is_immutable_and_case_changes_use_new_revision(
    db_connection, case_document, clone_document
) -> None:
    repo = PostgresRepository(db_connection)
    repo.create_case(case_document)

    with pytest.raises(psycopg.errors.RaiseException, match="immutable record"):
        db_connection.execute(
            """
            UPDATE human_cos_case_revision
            SET payload = jsonb_set(payload, '{time_boundary,T0}', '"2030-01-01T00:00:00+00:00"')
            WHERE case_id = %s AND revision = 1
            """,
            (case_document["case_id"],),
        )
    db_connection.rollback()
    original = repo.get_case(case_document["case_id"], revision=1)
    assert original.time_boundary.T0 == datetime(2026, 1, 1, tzinfo=timezone.utc)

    revised = clone_document(case_document)
    revised["revision"] = 2
    revised["state"] = "REVISED"
    repo.revise_case(revised)
    assert repo.get_case(case_document["case_id"], revision=1).state == "CREATED"
    assert repo.get_case(case_document["case_id"], revision=2).state == "REVISED"


def test_at01_and_actor_visibility_enforced_before_context(
    db_connection, case_document, evidence_factory
) -> None:
    repo = PostgresRepository(db_connection)
    case = repo.create_case(case_document)
    repo.create_evidence(evidence_factory("e-public", public=True, snapshot_char="a"))
    repo.create_evidence(evidence_factory("e-actor", actor_ids=["actor-a"], snapshot_char="b"))
    repo.create_evidence(evidence_factory("e-role", role_ids=["analyst"], snapshot_char="c"))
    repo.create_evidence(
        evidence_factory(
            "e-future",
            temporal_class="POST_T0",
            source_timestamp="2026-02-01T00:00:00+00:00",
            available_from="2026-02-01T00:00:00+00:00",
            public=True,
            snapshot_char="d",
        )
    )
    repo.create_evidence(evidence_factory("e-denied", snapshot_char="e"))

    visible = repo.list_context_evidence(
        case,
        actor_id="actor-a",
        role_id="analyst",
        as_of=case.time_boundary.T0,
    )
    assert {item.evidence.evidence_id for item in visible} == {"e-public", "e-actor", "e-role"}

    result = build_context(
        repo,
        case,
        ContextBuildRequest(
            context_manifest_id="cm-integration",
            run_id="run-integration",
            stage="DOMAIN_INDEPENDENT_RUN",
            role_id="analyst",
            actor_id="actor-a",
            model_id="model-1",
            prompt_version="p1",
            forbidden_scopes=("POST_T0",),
        ),
    )
    assert result.manifest.evidence_ids == ("e-actor", "e-public", "e-role")
    repo.store_context_admission(result.admission)
    stored = repo.get_context_admission("cm-integration")
    assert stored.manifest_hash == result.manifest.hash_sha256
    assert stored.actor_id == "actor-a"
    assert {item.evidence_id for item in stored.evidence} == {"e-actor", "e-public", "e-role"}

    with pytest.raises(psycopg.errors.RaiseException, match="immutable record"):
        db_connection.execute(
            "UPDATE human_cos_context_admission "
            "SET manifest_hash = %s WHERE context_manifest_id = %s",
            ("f" * 64, "cm-integration"),
        )
    db_connection.rollback()


def test_historical_context_uses_latest_temporally_admissible_revision(
    db_connection, case_document, evidence_factory, clone_document
) -> None:
    repo = PostgresRepository(db_connection)
    case = repo.create_case(case_document)
    first = evidence_factory("e-time-travel", public=True, snapshot_char="a")
    repo.create_evidence(first)

    later = clone_document(first)
    later["content"] = "later correction"
    later["snapshot_hash"] = "b" * 64
    later["temporal_class"] = "POST_T0"
    later["source_timestamp"] = "2026-02-01T00:00:00+00:00"
    later["ingested_at"] = "2026-02-01T00:00:00+00:00"
    later["available_from"] = "2026-02-01T00:00:00+00:00"
    repo.revise_evidence(later)

    admitted = repo.list_context_evidence(
        case,
        actor_id=None,
        role_id=None,
        as_of=case.time_boundary.T0,
    )
    assert len(admitted) == 1
    assert admitted[0].evidence.evidence_id == "e-time-travel"
    assert admitted[0].revision == 1
    assert admitted[0].evidence.snapshot_hash == "a" * 64


def test_live_reference_time_filters_future_and_expired_evidence(
    db_connection, case_document, evidence_factory, clone_document
) -> None:
    live_doc = clone_document(case_document)
    live_doc["case_mode"] = "LIVE_FORESIGHT"
    repo = PostgresRepository(db_connection)
    case = repo.create_case(live_doc)
    repo.create_evidence(
        evidence_factory(
            "e-live-ok",
            temporal_class="POST_T0",
            source_timestamp="2026-01-20T00:00:00+00:00",
            ingested_at="2026-01-20T00:00:00+00:00",
            available_from="2026-01-20T00:00:00+00:00",
            public=True,
            snapshot_char="a",
        )
    )
    repo.create_evidence(
        evidence_factory(
            "e-live-future",
            temporal_class="POST_T0",
            source_timestamp="2026-01-20T00:00:00+00:00",
            ingested_at="2026-01-20T00:00:00+00:00",
            available_from="2026-02-02T00:00:00+00:00",
            public=True,
            snapshot_char="b",
        )
    )
    repo.create_evidence(
        evidence_factory(
            "e-live-expired",
            temporal_class="POST_T0",
            source_timestamp="2026-01-01T00:00:00+00:00",
            ingested_at="2026-01-01T00:00:00+00:00",
            available_from="2026-01-01T00:00:00+00:00",
            available_until="2026-01-31T23:59:59+00:00",
            public=True,
            snapshot_char="c",
        )
    )
    reference = datetime(2026, 2, 1, tzinfo=timezone.utc)
    result = build_context(
        repo,
        case,
        ContextBuildRequest(
            context_manifest_id="cm-live",
            run_id="run-live",
            stage="DOMAIN_INDEPENDENT_RUN",
            role_id="analyst",
            actor_id=None,
            model_id="model-1",
            prompt_version="p1",
            reference_time=reference,
        ),
    )
    assert result.manifest.evidence_ids == ("e-live-ok",)
    assert result.manifest.time_boundary == reference


def test_migration_rollback_removes_s1_tables(db_connection) -> None:
    rollback_s1_migration(db_connection)
    row = db_connection.execute(
        """
        SELECT to_regclass('public.human_cos_context_admission'),
               to_regclass('public.human_cos_evidence_revision'),
               to_regclass('public.human_cos_case_revision')
        """
    ).fetchone()
    assert row == (None, None, None)
