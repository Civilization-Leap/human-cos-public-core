from __future__ import annotations

import copy
from collections.abc import Callable
from typing import Any

import pytest


@pytest.fixture()
def case_document() -> dict[str, Any]:
    return {
        "case_id": "HC-S1-CASE-001",
        "revision": 1,
        "case_mode": "HISTORICAL_BLIND_EVAL",
        "question": "What could be known at T0?",
        "protocol_version": "0.1",
        "phase_profile": {"civilization_stage": "STARTUP", "case_phase": "DISCOVERY"},
        "time_boundary": {"T0": "2026-01-01T00:00:00+00:00", "timezone": "UTC"},
        "actors": ["actor-a", "actor-b"],
        "domains": ["test"],
        "publication_policy": "RESTRICTED",
        "state": "CREATED",
        "owner": "test-owner",
    }


@pytest.fixture()
def evidence_factory() -> Callable[..., dict[str, Any]]:
    def make(
        evidence_id: str,
        *,
        temporal_class: str = "PRE_T0",
        source_timestamp: str = "2025-12-01T00:00:00+00:00",
        ingested_at: str = "2025-12-02T00:00:00+00:00",
        available_from: str = "2025-12-01T00:00:00+00:00",
        available_until: str | None = None,
        public: bool = False,
        actor_ids: list[str] | None = None,
        role_ids: list[str] | None = None,
        content: str = "ordinary evidence",
        snapshot_char: str = "a",
    ) -> dict[str, Any]:
        document: dict[str, Any] = {
            "evidence_id": evidence_id,
            "case_id": "HC-S1-CASE-001",
            "content": content,
            "source_type": "test",
            "source_uri_or_ref": f"test://{evidence_id}",
            "source_timestamp": source_timestamp,
            "ingested_at": ingested_at,
            "available_from": available_from,
            "visibility": {
                "public": public,
                "actor_ids": actor_ids or [],
                "role_ids": role_ids or [],
            },
            "temporal_class": temporal_class,
            "fact_status": "OBSERVED",
            "source_quality": 0.8,
            "fact_confidence": 0.7,
            "snapshot_hash": snapshot_char * 64,
            "supersedes": [],
            "tags": ["s1"],
            "evidence_conflict_ids": [],
        }
        if available_until is not None:
            document["available_until"] = available_until
        return document

    return make


@pytest.fixture()
def clone_document() -> Callable[[dict[str, Any]], dict[str, Any]]:
    return copy.deepcopy
