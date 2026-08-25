"""JSON Schema validation tests for every bundled schema (S0 / T-003 part 1).

Each schema must:
- be valid JSON,
- target Draft 2020-12,
- accept a representative valid instance,
- reject a representative invalid instance,
- not silently permit extra unknown properties (unless allowed).
"""

import re

import pytest

from human_cos.protocols.schema_loader import (
    list_schema_files,
    load_json_schema,
    validate_instance,
)

# A representative *valid* instance per schema.
_VALID: dict[str, dict] = {
    "audit-event.schema.json": {
        "event_id": "evt-1",
        "timestamp": "2026-01-01T00:00:00+00:00",
        "actor_type": "SYSTEM",
        "actor_id": "orchestrator",
        "event_type": "CASE_FROZEN",
        "object_ref": "case/c1",
    },
    "case.schema.json": {
        "case_id": "c1",
        "revision": 1,
        "case_mode": "HISTORICAL_BLIND_EVAL",
        "question": "Evaluate the decision.",
        "protocol_version": "0.1",
        "phase_profile": {"civilization_stage": "STABLE", "case_phase": "DISCOVERY"},
        "time_boundary": {"T0": "2026-01-01T00:00:00+00:00", "timezone": "UTC"},
        "publication_policy": "RESTRICTED",
    },
    "context-manifest.schema.json": {
        "context_manifest_id": "cm-1",
        "case_id": "c1",
        "run_id": "r1",
        "stage": "DOMAIN_INDEPENDENT_RUN",
        "role_id": "worker",
        "evidence_ids": ["e1"],
        "prior_run_ids": [],
        "tool_permissions": ["retrieve"],
        "protocol_version": "0.1",
        "model_id": "m1",
        "prompt_version": "p1",
        "forbidden_scopes": ["post_t0"],
    },
    "evidence.schema.json": {
        "evidence_id": "e1",
        "case_id": "c1",
        "source_type": "web",
        "source_timestamp": "2025-12-31T00:00:00+00:00",
        "ingested_at": "2026-01-01T00:00:00+00:00",
        "available_from": "2026-01-01T00:00:00+00:00",
        "visibility": {"public": False, "actor_ids": [], "role_ids": ["worker"]},
        "temporal_class": "PRE_T0",
        "fact_status": "OBSERVED",
        "source_quality": 0.8,
        "fact_confidence": 0.9,
        "snapshot_hash": "a" * 64,
    },
    "model-profile.schema.json": {
        "model_id": "m1",
        "model_family": "family-a",
        "provider": "provider-a",
        "status": "QUALIFIED",
        "role_eligibility": {"meta_controller": True, "domain_worker": ["mechanism_analysis"]},
    },
    "phase-profile.schema.json": {
        "civilization_stage": "TRANSITION",
        "case_phase": "ESCALATION",
    },
    "protocol-registry.schema.json": {
        "registry_version": "0.1",
        "status": "FROZEN",
        "change_control": "RFC",
        "protocols": [
            {
                "id": "P1",
                "version": "0.1",
                "status": "FROZEN",
                "purpose": "demo",
                "merge_blocking_tests": ["AT-1"],
            }
        ],
    },
    "run-manifest.schema.json": {
        "run_id": "r1",
        "case_id": "c1",
        "stage": "DOMAIN_INDEPENDENT_RUN",
        "role_type": "domain_worker",
        "model_id": "m1",
        "model_family": "family-a",
        "provider": "provider-a",
        "protocol_version": "0.1",
        "context_manifest_hash": "b" * 64,
        "status": "RUNNING",
        "independence": {
            "context": True,
            "prompt": True,
            "model_family": False,
            "provider": True,
            "evidence_path": True,
        },
    },
    "visibility.schema.json": {
        "public": False,
        "actor_ids": ["a1"],
        "role_ids": ["worker"],
    },
}

# A representative *invalid* instance per schema (must be rejected).
_INVALID: dict[str, dict] = {
    "audit-event.schema.json": {"event_id": "evt-1"},  # missing required fields
    "case.schema.json": {
        "case_id": "c1",
        "revision": 1,
        "case_mode": "NOT_A_MODE",  # bad enum
        "question": "x",
        "protocol_version": "0.1",
        "phase_profile": {"civilization_stage": "STABLE", "case_phase": "DISCOVERY"},
        "time_boundary": {"T0": "2026-01-01T00:00:00+00:00"},
        "publication_policy": "RESTRICTED",
    },
    "context-manifest.schema.json": {
        "context_manifest_id": "cm-1",
        "case_id": "c1",
        "run_id": "r1",
        "stage": "DOMAIN_INDEPENDENT_RUN",
        "role_id": "worker",
        # missing evidence_ids / protocol_version / ...
        "model_id": "m1",
        "prompt_version": "p1",
        "forbidden_scopes": [],
    },
    "evidence.schema.json": {
        "evidence_id": "e1",
        "case_id": "c1",
        "source_type": "web",
        "source_timestamp": "2025-12-31T00:00:00+00:00",
        "ingested_at": "2026-01-01T00:00:00+00:00",
        "available_from": "2026-01-01T00:00:00+00:00",
        "visibility": {"public": False, "actor_ids": [], "role_ids": ["worker"]},
        "temporal_class": "POST_T0_AND_LATER",  # bad enum
        "fact_status": "OBSERVED",
        "source_quality": 0.8,
        "fact_confidence": 1.5,  # > max 1
        "snapshot_hash": "not-a-hash",
    },
    "model-profile.schema.json": {
        "model_id": "m1",
        "model_family": "family-a",
        "provider": "provider-a",
        "status": "QUALIFIED",
        # missing role_eligibility
    },
    "phase-profile.schema.json": {"civilization_stage": "STABLE"},  # missing case_phase
    "protocol-registry.schema.json": {
        "registry_version": "0.1",
        "status": "FROZEN",
    },  # missing protocols
    "run-manifest.schema.json": {
        "run_id": "r1",
        "case_id": "c1",
        "stage": "DOMAIN_INDEPENDENT_RUN",
        "role_type": "domain_worker",
        "model_id": "m1",
        "model_family": "family-a",
        "provider": "provider-a",
        "protocol_version": "0.1",
        "context_manifest_hash": "bad",
        "status": "RUNNING",
        # missing independence
    },
    "visibility.schema.json": {"public": True},  # missing actor_ids / role_ids
}


@pytest.mark.parametrize("filename", list_schema_files())
def test_schema_is_valid_json(filename) -> None:
    doc = load_json_schema(filename.name)
    assert isinstance(doc, dict)
    assert doc.get("type") == "object"
    assert doc.get("$schema", "").startswith("https://json-schema.org/draft/2020-12")


@pytest.mark.parametrize("filename", list_schema_files())
def test_valid_instance_passes(filename) -> None:
    key = filename.name
    assert key in _VALID, f"no valid sample provided for {key}"
    errors = validate_instance(_VALID[key], key)
    assert not errors, f"{key} valid sample failed: {errors}"


@pytest.mark.parametrize("filename", list_schema_files())
def test_invalid_instance_fails(filename) -> None:
    key = filename.name
    assert key in _INVALID, f"no invalid sample provided for {key}"
    errors = validate_instance(_INVALID[key], key)
    assert errors, f"{key} invalid sample unexpectedly passed"


def test_additional_properties_disallowed_where_expected() -> None:
    """Case and Evidence must reject unknown keys (data-lineage hygiene)."""
    case = dict(_VALID["case.schema.json"])
    case["unknown_field"] = True
    assert validate_instance(case, "case.schema.json")

    ev = dict(_VALID["evidence.schema.json"])
    ev["rogue"] = 1
    assert validate_instance(ev, "evidence.schema.json")


def test_all_schemas_share_draft_and_object_shape() -> None:
    for path in list_schema_files():
        doc = load_json_schema(path.name)
        assert re.match(r"https://json-schema\.org/draft/2020-12/schema$", doc["$schema"])
        assert "required" in doc
