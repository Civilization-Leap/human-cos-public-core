# Human-COS Public Core — Release Status

Initial public engineering baseline: **S0/S1 Public Core**

## Canonical initial release record

Initial private source anchor:

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

The snapshot and manifest hashes above belong exclusively to the **initial protected-main release commit**. They are historical frozen identities and must not be recalculated or replaced because of later maintenance work.

## Subsequent packaging-hardening maintenance state

Canonical private maintenance source anchor:

`Civilization-Leap/human-cos-runtime@4098a69817d220634b156fab12ee3d664d504e8e`

Canonical private PR: `human-cos-runtime#5` — S1 packaging hardening: installed resource-safe wheel support.

This maintenance state adds distribution transport and verification only:

- package-internal byte-identical copies of the Frozen Contract manifest, Registry, 9 Schemas and S1 migrations;
- installed-resource-safe loading via Python package resources;
- bundled-registry CLI fallback when no repository path is supplied;
- packaged-resource byte-identity regression gates;
- normal wheel build and clean non-editable installation validation outside the repository;
- installed-distribution verification of Registry loading, JSON Schema `date-time` enforcement, Frozen Contract 10/10, and PostgreSQL S1 forward/rollback migrations.

It does **not** change the Frozen Contract, `BASELINE_CONTRACT_HASHES.yaml`, `uv.lock`, the S0/S1 Runtime semantic baseline, or S2 authorization state.

The protected-main public maintenance commit is recorded as post-merge closure evidence rather than guessed in advance. The initial release commit/tree/snapshot/manifest remain unchanged regardless of that later commit.

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
- protocol, contract, unit and integration tests;
- source-checkout/editable reproduction;
- locally built wheel / non-editable installation with bundled contract and migration resources.

## Not included / not authorized

This maintenance state does not include or authorize S2 or later Runtime capability, model registry/adapters, qualification, full state-machine orchestration, Responsibility Map, No Silent Crossing execution guard, cross-platform federation, or real-world execution.

PyPI publication is not claimed. A local wheel built from this source tree is the supported non-editable installation contract for this maintenance state.

Public Issue #4 remains the closure/evidence tracker until the protected-main maintenance commit, public required checks, installed-distribution verification and final provenance record are all confirmed.

## Initial publication gates — frozen record

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

## Maintenance boundary

Subsequent maintenance may improve reproducibility, packaging, tests or documentation without redefining the initial release identity or the Frozen Contract. Any semantic protocol change still requires the separate RFC + regression-impact + new-baseline process.

The public repository is a reproducibility surface, not an authority over independent professional judgment or real-world decisions.
