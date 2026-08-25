"""Distribution-resource regression gates for S0/S1 packaging hardening."""

from pathlib import Path

import pytest

from human_cos.protocols.frozen_contract import assert_bundled_frozen_contracts_intact
from human_cos.resources import read_runtime_resource_bytes, repository_root

ROOT = repository_root()
FROZEN_TRANSPORT_PATHS = [
    "BASELINE_CONTRACT_HASHES.yaml",
    "protocols/protocol_registry_v0.1.yaml",
    "schemas/audit-event.schema.json",
    "schemas/case.schema.json",
    "schemas/context-manifest.schema.json",
    "schemas/evidence.schema.json",
    "schemas/model-profile.schema.json",
    "schemas/phase-profile.schema.json",
    "schemas/protocol-registry.schema.json",
    "schemas/run-manifest.schema.json",
    "schemas/visibility.schema.json",
]
MIGRATION_PATHS = [
    "migrations/0001_s1_case_evidence.sql",
    "migrations/0001_s1_case_evidence.rollback.sql",
]


@pytest.mark.parametrize("relative_path", FROZEN_TRANSPORT_PATHS + MIGRATION_PATHS)
def test_packaged_transport_copy_is_byte_identical(relative_path: str) -> None:
    canonical = (ROOT / Path(relative_path)).read_bytes()
    packaged = read_runtime_resource_bytes(relative_path, prefer_source=False)
    assert packaged == canonical, f"packaged transport drift: {relative_path}"


def test_packaged_frozen_contract_verifies_10_of_10() -> None:
    report = assert_bundled_frozen_contracts_intact()
    assert report.ok
    assert len(report.items) == 10
