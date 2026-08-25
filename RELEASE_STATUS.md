# Human-COS Public Core — Release Status

Initial public engineering baseline: **S0/S1 Public Core**

## Canonical release record

Private source anchor:

`Civilization-Leap/human-cos-runtime@da2c62e21871e911ab26b877928676bc81056e09`

Public repository:

`Civilization-Leap/human-cos-public-core`

Initial protected-main release commit:

`b7fd3b42eef257f3c9c8fe5942e09f6606e3756d`

Initial release tree:

`f1c1491af69c422f89dd60172d0c0ed1d5ba3649`

Hardened deterministic clean snapshot SHA-256:

`7186c60e002f70b1e1f487d1f3d2e5c048e51c3361c17896185b69425420f87f`

Initial `PUBLIC_CORE_MANIFEST.json` SHA-256:

`f1c8fb42063f38420417433e1229b198e294b42dc8976148339fe9515190c5a2`

Frozen `uv.lock` SHA-256:

`37267c6369be88608eecce1cf251dab0df2ea615131b5efbed1eb89425fb05a5`

The snapshot and manifest hashes above belong to the **initial protected-main release commit**. Later documentation-only closure metadata does not redefine that frozen initial-release snapshot and must not be used to recalculate or replace those hashes.

## Included capability

- Frozen Protocol Registry + 9 Frozen Schemas;
- Frozen Contract hash enforcement;
- declared JSON Schema `date-time` format enforcement;
- strict Frozen Registry guard including registry-level metadata changes;
- Case/Evidence application models;
- T0/time-boundary enforcement;
- actor/role ACL visibility;
- append-only Case/Evidence revisions;
- Context admission sidecar and provenance binding;
- PostgreSQL S1 storage/migrations;
- protocol, contract, unit and integration tests.

## Not included / not authorized

This release does not include or authorize S2 or later Runtime capability, model registry/adapters, qualification, full state-machine orchestration, Responsibility Map, No Silent Crossing execution guard, cross-platform federation, or real-world execution.

Wheel/PyPI/non-editable installation support is not claimed by this initial source-reproducibility release and remains separately tracked in Issue #4.

## Publication gates — final closure

- G0 Public Scope: **PASS**
- G1 Source provenance: **PASS**
- G2 License/copyright: **PASS**
- G3 Security reporting / PVR: **PASS**
- G4 Public documentation and participation routing: **PASS**
- G5 Reproducibility and Frozen Contract verification: **PASS**
- G6 Protected-main governance and required checks: **PASS**
- G7 Publication safety scan: **PASS** — findings `[]`
- G8 Hardened release validation: **PASS** — manifest 72/72, final tree 74/74, Frozen Contract drift 0/10, public Python 3.10/3.12 required checks passed
- G9 Formal protected-main publication: **PASS** — initial Public Core source release merged at `b7fd3b42eef257f3c9c8fe5942e09f6606e3756d`

## Post-publication metadata boundary

This document may be updated after publication to record closure evidence. Such metadata-only updates are **not** a new Runtime release, do not modify the initial frozen snapshot, do not alter the Frozen Contract, do not close Issue #4, and do not authorize S2.

The public repository is a reproducibility surface, not an authority over independent professional judgment or real-world decisions.
