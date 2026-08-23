"""Frozen-contract verification — the outer immutability gate for V0.1.

Human-COS's "unchangeable semantics" are only trustworthy if CI can prove the
frozen artifacts did not change byte-for-byte.  This module implements the
S0 review recommendation (P0-3):

- ``BASELINE_CONTRACT_HASHES.yaml`` lists the SHA-256 of the 10 signed files
  (the Protocol Registry + all 9 core JSON Schemas).
- ``assert_frozen_contracts_intact`` recomputes every hash and fails the build
  on ANY byte change, deletion, or addition to those files.

Rule is deliberately simple and non-heuristic: a frozen contract is immutable.
Real semantic change requires an RFC + regression impact review + a NEW
baseline version, which updates this manifest in the same reviewed change.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, cast

import yaml

_MODULE_DIR = Path(__file__).resolve().parent
# src/human_cos/protocols -> 2 up from the module dir = repository root
_REPO_ROOT = _MODULE_DIR.parents[2]

DEFAULT_MANIFEST_NAME = "BASELINE_CONTRACT_HASHES.yaml"


class ContractHashMismatchError(ValueError):
    """Raised when a signed frozen-contract file is missing or differs from its
    recorded SHA-256."""


@dataclass
class ContractCheck:
    path: str
    expected_sha256: str
    actual_sha256: str
    ok: bool
    note: str = ""


@dataclass
class ContractReport:
    items: list[ContractCheck] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(item.ok for item in self.items)

    @property
    def failures(self) -> list[ContractCheck]:
        return [item for item in self.items if not item.ok]

    def summary(self) -> str:
        return (
            "; ".join(f"{i.path}: {i.note}" for i in self.failures)
            or "all 10 frozen contracts intact"
        )


def repo_root() -> Path:
    return _REPO_ROOT


def default_manifest_path() -> Path:
    return _REPO_ROOT / DEFAULT_MANIFEST_NAME


def _load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ContractHashMismatchError(
            f"frozen contract manifest not found: {path} (file: {DEFAULT_MANIFEST_NAME})"
        )
    with path.open("r", encoding="utf-8") as fh:
        manifest = yaml.safe_load(fh) or {}
    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        raise ContractHashMismatchError("frozen contract manifest has no 'files' list")
    if manifest.get("version") != "V0.1":
        raise ContractHashMismatchError(
            f"frozen contract manifest version {manifest.get('version')!r} != V0.1"
        )
    return cast("dict[str, Any]", manifest)


def compute_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_frozen_contracts(
    root: Path | None = None, manifest_path: Path | None = None
) -> ContractReport:
    """Recompute the SHA-256 of every signed file and compare to the manifest.

    Never raises for a mismatch — it returns a :class:`ContractReport` so the
    caller can decide how to surface failures.
    """
    root = Path(root or _REPO_ROOT)
    manifest_path = Path(manifest_path or root / DEFAULT_MANIFEST_NAME)
    manifest = _load_manifest(manifest_path)

    report = ContractReport()
    for entry in manifest["files"]:
        rel = str(entry["path"])
        expected = str(entry["sha256"]).lower()
        candidate = root / rel
        if not candidate.exists():
            report.items.append(
                ContractCheck(rel, expected, "", ok=False, note="missing signed file")
            )
            continue
        actual = compute_sha256(candidate)
        ok = actual == expected
        report.items.append(
            ContractCheck(
                rel,
                expected,
                actual,
                ok=ok,
                note="intact"
                if ok
                else f"hash mismatch (expected {expected[:12]}… got {actual[:12]}…)",
            )
        )

    # Missing signed files are already reported above (ok=False).  Whether the
    # repository carries *extra* contract-shaped files beyond the signed set is
    # asserted by the unit tests (test_signed_set_is_exactly_the_10_expected_files).
    return report


def assert_frozen_contracts_intact(
    root: Path | None = None, manifest_path: Path | None = None
) -> ContractReport:
    """Verify the frozen contracts; raise :class:`ContractHashMismatchError`
    if any signed file is missing, changed, or inconsistent.  Merge-blocking."""
    report = verify_frozen_contracts(root=root, manifest_path=manifest_path)
    if not report.ok:
        raise ContractHashMismatchError("FROZEN CONTRACT VIOLATION — " + report.summary())
    return report
