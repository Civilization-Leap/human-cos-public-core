from __future__ import annotations

from datetime import datetime, timezone

from human_cos.core.models import parse_case, parse_evidence
from human_cos.core.visibility import context_allows, temporal_allows, visibility_allows

T0 = datetime(2026, 1, 1, tzinfo=timezone.utc)


def test_public_visibility(case_document, evidence_factory) -> None:
    case = parse_case(case_document)
    evidence = parse_evidence(evidence_factory("e-public", public=True))
    assert context_allows(case, evidence, actor_id=None, role_id=None, as_of=T0)


def test_actor_visibility_is_specific(case_document, evidence_factory) -> None:
    case = parse_case(case_document)
    evidence = parse_evidence(evidence_factory("e-actor", actor_ids=["actor-a"]))
    assert context_allows(case, evidence, actor_id="actor-a", role_id=None, as_of=T0)
    assert not context_allows(case, evidence, actor_id="actor-b", role_id=None, as_of=T0)


def test_role_visibility_is_specific(case_document, evidence_factory) -> None:
    case = parse_case(case_document)
    evidence = parse_evidence(evidence_factory("e-role", role_ids=["analyst"]))
    assert context_allows(case, evidence, actor_id=None, role_id="analyst", as_of=T0)
    assert not context_allows(case, evidence, actor_id=None, role_id="observer", as_of=T0)


def test_visibility_denies_by_default(evidence_factory) -> None:
    evidence = parse_evidence(evidence_factory("e-deny"))
    assert not visibility_allows(evidence.visibility, actor_id=None, role_id=None)


def test_t0_and_visibility_are_both_required(case_document, evidence_factory) -> None:
    case = parse_case(case_document)
    evidence = parse_evidence(
        evidence_factory(
            "e-future-authorized",
            temporal_class="POST_T0",
            source_timestamp="2026-02-01T00:00:00+00:00",
            available_from="2026-02-01T00:00:00+00:00",
            actor_ids=["actor-a"],
        )
    )
    assert not context_allows(case, evidence, actor_id="actor-a", role_id=None, as_of=T0)


def test_later_verification_never_enters_historical_clean_world(
    case_document, evidence_factory
) -> None:
    case = parse_case(case_document)
    evidence = parse_evidence(
        evidence_factory("e-later-verify", temporal_class="LATER_VERIFICATION_OF_PRE_T0_FACT")
    )
    assert not temporal_allows(case, evidence, as_of=T0)


def test_live_future_and_expired_availability_are_enforced(case_document, evidence_factory) -> None:
    live_doc = dict(case_document)
    live_doc["case_mode"] = "LIVE_FORESIGHT"
    case = parse_case(live_doc)
    reference = datetime(2026, 2, 1, tzinfo=timezone.utc)
    future = parse_evidence(
        evidence_factory(
            "e-live-future",
            temporal_class="POST_T0",
            source_timestamp="2026-01-20T00:00:00+00:00",
            ingested_at="2026-01-20T00:00:00+00:00",
            available_from="2026-02-02T00:00:00+00:00",
            public=True,
        )
    )
    expired = parse_evidence(
        evidence_factory(
            "e-live-expired",
            temporal_class="POST_T0",
            source_timestamp="2026-01-01T00:00:00+00:00",
            ingested_at="2026-01-01T00:00:00+00:00",
            available_from="2026-01-01T00:00:00+00:00",
            available_until="2026-01-31T23:59:59+00:00",
            public=True,
        )
    )
    assert not temporal_allows(case, future, as_of=reference)
    assert not temporal_allows(case, expired, as_of=reference)
