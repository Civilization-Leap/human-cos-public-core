"""Version parsing unit tests (S0 / T-002)."""

import pytest

from human_cos.protocols.version import (
    InvalidVersionError,
    parse_version,
    version_ge,
    version_gt,
)


def test_parse_valid_versions() -> None:
    assert parse_version("0.1").segments == (0, 1)
    assert parse_version("2.4.1").segments == (2, 4, 1)
    assert parse_version("10.20").segments == (10, 20)


def test_parse_rejects_bad_versions() -> None:
    for bad in ("", None, 5, "0", "one.two", "-1.0", "0..1", "1.", "a.b", "0.1-rc1", "  "):
        with pytest.raises(InvalidVersionError):
            parse_version(bad)


def test_comparisons() -> None:
    assert version_ge("0.2", "0.1")
    assert version_ge("0.1", "0.1")
    assert not version_ge("0.1", "0.2")
    assert version_gt("1.0", "0.9")
    assert not version_gt("1.0", "1.0")
