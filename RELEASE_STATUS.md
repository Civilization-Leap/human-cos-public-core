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

## Packaging-hardening maintenance — protected-main record

Canonical private maintenance source anchor:

`Civilization-Leap/human-cos-runtime@4098a69817d220634b156fab12ee3d664d504e8e`

Canonical private PR:

`human-cos-runtime#5` — `S1 packaging hardening: installed resource-safe wheel support`

Audited Public Core projection PR:

`human-cos-public-core#6` — `Public Core packaging hardening — audited canonical projection`

Final reviewed public PR head:

`0c18ee535c594a4c48a2831bcf6842569f58c9c5`

Protected-main packaging maintenance commit:

`117d3e28bf633c4726f1a42c5a4575a0da9974a5`

Protected-main packaging maintenance tree:

`8bf6fdfbc9cc123010df6e760c7a40ae440598be`

Validation evidence:

- Public PR CI run `#25`: **SUCCESS**;
- protected-main push CI run `#26`: **SUCCESS**;
- required `test (3.10)`: **PASS**;
- required `test (3.12)`: **PASS**;
- unit / protocol / Frozen Contract tests: **PASS**;
- ruff / format / mypy: **PASS**;
- bundled Protocol Registry CLI: **PASS**;
- packaged-resource byte-identity gate: **PASS**;
- Frozen Contract packaged verification: **10/10 PASS**;
- wheel build: **PASS**;
- clean non-editable installed-distribution validation outside the repository: **PASS**;
- installed-distribution JSON Schema `date-time` enforcement: **PASS**;
- installed-distribution PostgreSQL S1 forward/rollback migrations: **PASS**;
- secret scan: **PASS**;
- Docker build: **PASS**.

Final base-to-head audit confirmed zero changes to the repository-root Protocol Registry, all 9 repository-root Frozen Schemas, `BASELINE_CONTRACT_HASHES.yaml`, `uv.lock`, `PUBLIC_CORE_MANIFEST.json`, and `PUBLIC_CORE_MANIFEST.sha256`. Package-internal `_resources` files are distribution transport copies only and do not establish a second semantic baseline.

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

## Installation contract

The packaging maintenance state supports a normal wheel built locally from this source tree and installed non-editably without retaining a repository checkout at runtime. CI verifies the installed distribution from outside the repository on Python 3.10 and 3.12.

**PyPI publication is not claimed.** No PyPI release is asserted by this repository.

## Not included / not authorized

This maintenance state does not include or authorize S2 or later Runtime capability, model registry/adapters, qualification, full state-machine orchestration, Responsibility Map, No Silent Crossing execution guard, cross-platform federation, or real-world execution.

## Public Issue #4 closure gate

The functional packaging-hardening closure conditions are now evidenced:

- canonical private implementation merged and green: **PASS**;
- clean-wheel/non-editable validation: **PASS**;
- audited Public Core canonical projection: **PASS**;
- Public Core protected-main required checks: **PASS**;
- installed-distribution verification on the public tree: **PASS**;
- public installation documentation accurately states local wheel/non-editable support and no PyPI claim: **PASS**.

Issue #4 remains open only until this post-merge metadata closure PR itself is merged through protected `main` and its real `main` CI completes successfully. Closing Issue #4 after that verification is administrative closure; it does not redefine the initial release identity, alter the Frozen Contract, or authorize S2.

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

## Maintenance and metadata boundary

Packaging maintenance improves distribution reproducibility without redefining the initial release identity or Frozen Contract. This closure metadata records verified evidence only. Any semantic protocol change still requires the separate RFC + regression-impact + new-baseline process.

The public repository is a reproducibility surface, not an authority over independent professional judgment or real-world decisions.
