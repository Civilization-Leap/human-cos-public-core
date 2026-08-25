"""``human-cos-protocols`` CLI.

Small operational surface for the S0 deliverable:
- ``load <path>`` : load + validate a protocol registry, print summary.
- ``snapshot <path>`` : print a stable id->version snapshot (for change control).

No write path exists yet; S0 only fixes the contract.
"""

from __future__ import annotations

import argparse
import sys

from .registry import ProtocolRegistryError, load_protocol_registry


def _cmd_load(registry_path: str) -> int:
    try:
        registry = load_protocol_registry(registry_path)
    except ProtocolRegistryError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"registry_version={registry.version} status={registry.status}")
    print(f"change_control={registry.change_control}")
    for entry in registry.protocols:
        tests = ",".join(entry.merge_blocking_tests)
        print(f"  {entry.id}@{entry.version} [{entry.status}] AT{{{tests}}}")
    return 0


def _cmd_snapshot(registry_path: str) -> int:
    try:
        registry = load_protocol_registry(registry_path)
    except ProtocolRegistryError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    for entry in registry.protocols:
        print(f"{entry.id}@{entry.version}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="human-cos-protocols")
    sub = parser.add_subparsers(dest="command", required=True)
    p_load = sub.add_parser("load", help="load and validate a protocol registry")
    p_load.add_argument("path")
    p_snap = sub.add_parser("snapshot", help="print a stable id@version snapshot")
    p_snap.add_argument("path")
    args = parser.parse_args(argv)

    if args.command == "load":
        return _cmd_load(args.path)
    if args.command == "snapshot":
        return _cmd_snapshot(args.path)
    parser.error(f"unknown command {args.command}")  # pragma: no cover
    return 2  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
