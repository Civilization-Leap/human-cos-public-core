from __future__ import annotations

import pytest
from pydantic import ValidationError

from human_cos.core.models import ContractValidationError, parse_case, parse_evidence


def test_case_application_model_round_trips_frozen_contract(case_document) -> None:
    case = parse_case(case_document)
    assert case.case_id == "HC-S1-CASE-001"
    assert case.phase_profile.civilization_stage == "STARTUP"
    assert case.actors == ("actor-a", "actor-b")
    assert case.to_document()["actors"] == ["actor-a", "actor-b"]


def test_evidence_keeps_source_quality_separate_from_fact_confidence(evidence_factory) -> None:
    doc = evidence_factory("e-quality")
    doc["source_quality"] = 0.25
    doc["fact_confidence"] = 0.9
    evidence = parse_evidence(doc)
    assert evidence.source_quality == 0.25
    assert evidence.fact_confidence == 0.9


def test_evidence_rejects_unknown_contract_fields(evidence_factory) -> None:
    doc = evidence_factory("e-extra")
    doc["authority_override"] = "SYSTEM"
    with pytest.raises(ContractValidationError):
        parse_evidence(doc)


def test_nested_visibility_is_deeply_immutable(evidence_factory) -> None:
    evidence = parse_evidence(evidence_factory("e-frozen", actor_ids=["actor-a"]))
    assert evidence.visibility.actor_ids == ("actor-a",)
    with pytest.raises(ValidationError):
        evidence.visibility.actor_ids += ("actor-b",)


def test_temporal_contract_rejects_naive_datetime(evidence_factory) -> None:
    doc = evidence_factory("e-naive")
    doc["available_from"] = "2025-12-01T00:00:00"
    with pytest.raises(ContractValidationError, match="date-time"):
        parse_evidence(doc)
