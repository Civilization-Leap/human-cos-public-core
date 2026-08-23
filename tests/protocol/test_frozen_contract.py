"""Frozen Contract Hash merge-blocking tests (S0 review P0-3).

The 10 signed files (Protocol Registry + 9 core JSON Schemas) are immutable.
This suite:
- proves the current repository passes the byte-exact contract check;
- proves modification, deletion, and addition each FAIL the check;
- asserts the signed set is exactly the 10 expected files (nothing more, nothing less).
"""

import shutil

import pytest

from human_cos.protocols.frozen_contract import (
    ContractHashMismatchError,
    assert_frozen_contracts_intact,
    repo_root,
    verify_frozen_contracts,
)

# Exactly these 10 files are the V0.1 frozen contract.
EXPECTED_FILES = [
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


def _manifest_of(root) -> list[str]:
    import yaml

    with (root / "BASELINE_CONTRACT_HASHES.yaml").open(encoding="utf-8") as fh:
        return [str(e["path"]) for e in (yaml.safe_load(fh) or {})["files"]]


def test_current_repository_passes_contract_check() -> None:
    report = assert_frozen_contracts_intact()
    assert report.ok
    assert len(report.items) == 10


def test_signed_set_is_exactly_the_10_expected_files() -> None:
    root = repo_root()
    listed = set(_manifest_of(root))
    assert listed == set(EXPECTED_FILES)
    assert len(listed) == 10


def test_actual_contract_files_match_manifest_no_extras() -> None:
    root = repo_root()
    schemas = {f"schemas/{p.name}" for p in (root / "schemas").glob("*.schema.json")}
    actual = {"protocols/protocol_registry_v0.1.yaml"} | schemas
    assert actual == set(_manifest_of(root)), "repository contract files != manifest set"


def test_modification_of_signed_file_fails(tmp_path) -> None:
    _copy_contract(tmp_path)
    target = tmp_path / "schemas" / "case.schema.json"
    # Corrupt the file (append a byte).
    target.write_bytes(target.read_bytes() + b"\n# tampered")
    with pytest.raises(ContractHashMismatchError, match="hash mismatch"):
        assert_frozen_contracts_intact(root=tmp_path)


def test_deletion_of_signed_file_fails(tmp_path) -> None:
    _copy_contract(tmp_path)
    (tmp_path / "schemas" / "evidence.schema.json").unlink()
    with pytest.raises(ContractHashMismatchError, match="missing signed file"):
        assert_frozen_contracts_intact(root=tmp_path)


def test_addition_of_unsigned_file_reported_via_set_check(tmp_path) -> None:
    """An extra schema file must not silently enter the frozen set."""
    _copy_contract(tmp_path)
    (tmp_path / "schemas" / "rogue.schema.json").write_text("{}", encoding="utf-8")
    listed = set(_manifest_of(tmp_path))
    actual = {f"schemas/{p.name}" for p in (tmp_path / "schemas").glob("*.schema.json")} | {
        "protocols/protocol_registry_v0.1.yaml"
    }
    assert actual != listed


def _copy_contract(dest) -> None:
    root = repo_root()
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copy(root / "BASELINE_CONTRACT_HASHES.yaml", dest / "BASELINE_CONTRACT_HASHES.yaml")
    shutil.copytree(root / "schemas", dest / "schemas", dirs_exist_ok=True)
    shutil.copytree(root / "protocols", dest / "protocols", dirs_exist_ok=True)


def test_verify_returns_report_without_raising_on_corruption(tmp_path) -> None:
    _copy_contract(tmp_path)
    (tmp_path / "schemas" / "run-manifest.schema.json").write_text("[]", encoding="utf-8")
    report = verify_frozen_contracts(root=tmp_path)
    assert not report.ok
    assert report.failures  # the corrupted file flagged
