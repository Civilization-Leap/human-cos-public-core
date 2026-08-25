"""PostgreSQL repositories for S1 Case/Evidence data boundaries."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from typing import Any

from psycopg import Connection, errors
from psycopg.types.json import Jsonb

from human_cos.core.context import AdmittedEvidence, ContextAdmissionRecord
from human_cos.core.models import Case, Evidence, parse_case, parse_evidence
from human_cos.core.visibility import temporal_allows, visibility_basis


class RepositoryError(RuntimeError):
    """Base storage error."""


class DuplicateRevisionError(RepositoryError):
    """A revision already exists."""


class MissingRecordError(RepositoryError):
    """Requested record does not exist."""


class InvalidRevisionError(RepositoryError):
    """A requested revision does not continue the immutable lineage."""


class PostgresRepository:
    def __init__(self, connection: Connection[Any]) -> None:
        self.connection = connection

    def create_case(self, document: dict[str, Any]) -> Case:
        case = parse_case(document)
        if case.revision != 1:
            raise InvalidRevisionError("initial Case revision must be 1")
        try:
            self.connection.execute(
                """
                INSERT INTO human_cos_case_revision (case_id, revision, payload)
                VALUES (%s, %s, %s)
                """,
                (case.case_id, case.revision, Jsonb(case.to_document())),
            )
            self.connection.commit()
        except errors.UniqueViolation as exc:
            self.connection.rollback()
            raise DuplicateRevisionError(
                f"case revision exists: {case.case_id}@{case.revision}"
            ) from exc
        return case

    def revise_case(self, document: dict[str, Any]) -> Case:
        case = parse_case(document)
        with self.connection.transaction():
            self.connection.execute("SELECT pg_advisory_xact_lock(hashtext(%s))", (case.case_id,))
            row = self.connection.execute(
                """
                SELECT revision
                FROM human_cos_case_revision
                WHERE case_id = %s
                ORDER BY revision DESC
                LIMIT 1
                """,
                (case.case_id,),
            ).fetchone()
            if row is None:
                raise MissingRecordError(f"case not found: {case.case_id}")
            expected = int(row[0]) + 1
            if case.revision != expected:
                raise InvalidRevisionError(
                    f"Case revision must continue lineage: expected {expected}, got {case.revision}"
                )
            self.connection.execute(
                """
                INSERT INTO human_cos_case_revision (case_id, revision, payload)
                VALUES (%s, %s, %s)
                """,
                (case.case_id, case.revision, Jsonb(case.to_document())),
            )
        return case

    def get_case(self, case_id: str, revision: int | None = None) -> Case:
        if revision is None:
            row = self.connection.execute(
                """
                SELECT payload
                FROM human_cos_case_revision
                WHERE case_id = %s
                ORDER BY revision DESC
                LIMIT 1
                """,
                (case_id,),
            ).fetchone()
        else:
            row = self.connection.execute(
                """
                SELECT payload
                FROM human_cos_case_revision
                WHERE case_id = %s AND revision = %s
                """,
                (case_id, revision),
            ).fetchone()
        if row is None:
            raise MissingRecordError(f"case not found: {case_id}@{revision or 'latest'}")
        return parse_case(dict(row[0]))

    def create_evidence(self, document: dict[str, Any]) -> Evidence:
        evidence = parse_evidence(document)
        self.get_case(evidence.case_id)
        self._insert_evidence(evidence, revision=1, parent_revision=None)
        return evidence

    def revise_evidence(self, document: dict[str, Any]) -> tuple[Evidence, int]:
        """Append a new immutable revision; never UPDATE the prior row."""
        evidence = parse_evidence(document)
        with self.connection.transaction():
            self.connection.execute(
                "SELECT pg_advisory_xact_lock(hashtext(%s))", (evidence.evidence_id,)
            )
            row = self.connection.execute(
                """
                SELECT revision, case_id
                FROM human_cos_evidence_revision
                WHERE evidence_id = %s
                ORDER BY revision DESC
                LIMIT 1
                """,
                (evidence.evidence_id,),
            ).fetchone()
            if row is None:
                raise MissingRecordError(f"evidence not found: {evidence.evidence_id}")
            parent_revision, case_id = int(row[0]), str(row[1])
            if evidence.case_id != case_id:
                raise InvalidRevisionError("evidence revision cannot change case_id")
            revision = parent_revision + 1
            self.connection.execute(
                """
                INSERT INTO human_cos_evidence_revision
                    (evidence_id, revision, case_id, parent_revision, payload, snapshot_hash)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    evidence.evidence_id,
                    revision,
                    evidence.case_id,
                    parent_revision,
                    Jsonb(evidence.to_document()),
                    evidence.snapshot_hash,
                ),
            )
        return evidence, revision

    def _insert_evidence(
        self,
        evidence: Evidence,
        *,
        revision: int,
        parent_revision: int | None,
    ) -> None:
        try:
            self.connection.execute(
                """
                INSERT INTO human_cos_evidence_revision
                    (evidence_id, revision, case_id, parent_revision, payload, snapshot_hash)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    evidence.evidence_id,
                    revision,
                    evidence.case_id,
                    parent_revision,
                    Jsonb(evidence.to_document()),
                    evidence.snapshot_hash,
                ),
            )
            self.connection.commit()
        except errors.UniqueViolation as exc:
            self.connection.rollback()
            raise DuplicateRevisionError(
                f"evidence revision exists: {evidence.evidence_id}@{revision}"
            ) from exc

    def get_evidence(self, evidence_id: str, revision: int | None = None) -> tuple[Evidence, int]:
        if revision is None:
            row = self.connection.execute(
                """
                SELECT payload, revision
                FROM human_cos_evidence_revision
                WHERE evidence_id = %s
                ORDER BY revision DESC
                LIMIT 1
                """,
                (evidence_id,),
            ).fetchone()
        else:
            row = self.connection.execute(
                """
                SELECT payload, revision
                FROM human_cos_evidence_revision
                WHERE evidence_id = %s AND revision = %s
                """,
                (evidence_id, revision),
            ).fetchone()
        if row is None:
            raise MissingRecordError(f"evidence not found: {evidence_id}@{revision or 'latest'}")
        return parse_evidence(dict(row[0])), int(row[1])

    def list_latest_evidence(self, case_id: str) -> list[Evidence]:
        rows = self.connection.execute(
            """
            SELECT DISTINCT ON (evidence_id) payload
            FROM human_cos_evidence_revision
            WHERE case_id = %s
            ORDER BY evidence_id, revision DESC
            """,
            (case_id,),
        ).fetchall()
        return [parse_evidence(dict(row[0])) for row in rows]

    def list_context_evidence(
        self,
        case: Case,
        *,
        actor_id: str | None,
        role_id: str | None,
        as_of: datetime,
    ) -> Sequence[AdmittedEvidence]:
        """Select latest temporally admissible revision, then enforce ACL.

        ACL is evaluated only on the selected revision; the code never falls
        back to an older revision merely because a newer admissible revision is
        more restrictive.
        """
        rows = self.connection.execute(
            """
            SELECT evidence_id, revision, payload
            FROM human_cos_evidence_revision
            WHERE case_id = %s
            ORDER BY evidence_id, revision DESC
            """,
            (case.case_id,),
        ).fetchall()

        selected: dict[str, tuple[Evidence, int]] = {}
        exhausted: set[str] = set()
        for evidence_id_raw, revision_raw, payload in rows:
            evidence_id = str(evidence_id_raw)
            if evidence_id in exhausted:
                continue
            evidence = parse_evidence(dict(payload))
            if temporal_allows(case, evidence, as_of=as_of):
                selected[evidence_id] = (evidence, int(revision_raw))
                exhausted.add(evidence_id)

        admitted: list[AdmittedEvidence] = []
        for evidence_id in sorted(selected):
            evidence, revision = selected[evidence_id]
            basis = visibility_basis(evidence.visibility, actor_id=actor_id, role_id=role_id)
            if basis is not None:
                admitted.append(
                    AdmittedEvidence(evidence=evidence, revision=revision, visibility_basis=basis)
                )
        return admitted

    def store_context_admission(self, record: ContextAdmissionRecord) -> None:
        try:
            self.connection.execute(
                """
                INSERT INTO human_cos_context_admission
                    (context_manifest_id, manifest_hash, record_hash, payload)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    record.context_manifest_id,
                    record.manifest_hash,
                    record.record_hash,
                    Jsonb(record.to_document()),
                ),
            )
            self.connection.commit()
        except errors.UniqueViolation as exc:
            self.connection.rollback()
            raise DuplicateRevisionError(
                f"context admission exists: {record.context_manifest_id}"
            ) from exc

    def get_context_admission(self, context_manifest_id: str) -> ContextAdmissionRecord:
        row = self.connection.execute(
            """
            SELECT payload
            FROM human_cos_context_admission
            WHERE context_manifest_id = %s
            """,
            (context_manifest_id,),
        ).fetchone()
        if row is None:
            raise MissingRecordError(f"context admission not found: {context_manifest_id}")
        return ContextAdmissionRecord.model_validate(dict(row[0]))
