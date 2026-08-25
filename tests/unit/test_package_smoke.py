"""Package import smoke test — verifies the S0 package is importable and
declares the expected metadata."""

import importlib.metadata

import human_cos  # noqa: F401
from human_cos.protocols import cli, registry, schema_loader, version


def test_package_importable() -> None:
    assert human_cos is not None


def test_module_surface_present() -> None:
    for mod in (cli, registry, schema_loader, version):
        assert mod.__name__.startswith("human_cos.protocols")


def test_distribution_metadata() -> None:
    dist = importlib.metadata.version("human-cos-runtime")
    assert dist
