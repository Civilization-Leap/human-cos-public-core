# Human-COS Public Core — Provenance

Status: **INITIAL PUBLIC CORE RELEASE LINEAGE FROZEN; PACKAGING MAINTENANCE LINEAGE RECORDED**

## Private source anchors

Initial release source:

- Private engineering repository: `Civilization-Leap/human-cos-runtime`
- Source branch: `main`
- Initial source commit: `da2c62e21871e911ab26b877928676bc81056e09`
- Initial source state: Sprint S1 merged plus pre-publication S0/S1 hardening from private PR #4.

Subsequent packaging maintenance source:

- Canonical maintenance commit: `4098a69817d220634b156fab12ee3d664d504e8e`
- Parent: `da2c62e21871e911ab26b877928676bc81056e09`
- Canonical private PR: `#5` — `S1 packaging hardening: installed resource-safe wheel support`
- Scope: S0/S1 distribution hardening only; S2 remains unauthorized.

The initial hardening makes already-declared JSON Schema `date-time` formats enforceable and closes a strict Frozen Registry guard gap for registry-level metadata. The later packaging hardening adds byte-identical distribution transport resources, installed-resource-safe loading, and clean-wheel validation. Neither change modifies the Protocol Registry YAML, any of the 9 Frozen Schemas, or `BASELINE_CONTRACT_HASHES.yaml`; packaging hardening also leaves `uv.lock` unchanged.

## Initial public release record — frozen identity

- Public repository: `Civilization-Leap/human-cos-public-core`
- Initial protected-main release PR: `#2`
- Initial protected-main release commit: `b7fd3b42eef257f3c9c8fe5942e09f6606e3756d`
- Initial release tree: `f1c1491af69c422f89dd60172d0c0ed1d5ba3649`
- Hardened deterministic clean snapshot SHA-256: `7186c60e002f70b1e1f487d1f3d2e5c048e51c3361c17896185b69425420f87f`
- Initial `PUBLIC_CORE_MANIFEST.json` SHA-256: `f1c8fb42063f38420417433e1229b198e294b42dc8976148339fe9515190c5a2`
- Frozen `uv.lock` SHA-256: `37267c6369be88608eecce1cf251dab0df2ea615131b5efbed1eb89425fb05a5`
- Publication safety: PASS / findings `[]`
- Manifest verification: 72/72
- Exact initial release tree: 74/74
- Frozen Contract drift: 0/10
- Protected-main required checks: `test (3.10)` PASS / `test (3.12)` PASS
- Publication gate state: G0–G9 PASS

These hashes identify the **initial protected-main source release only**. The initial manifest is not regenerated for later maintenance and does not claim to enumerate the later maintenance tree.

## Packaging-hardening public maintenance lineage

The current maintenance projection is derived from canonical private `human-cos-runtime@4098a69817d220634b156fab12ee3d664d504e8e` and preserves the Public Core publication overlay:

- Apache License 2.0 remains the public license;
- ZhongXinWang / 王忠新 / 子君赋 attribution remains public metadata;
- private Git history and private-only control files remain excluded;
- root Frozen Contract artifacts remain the canonical signed originals;
- package-internal `_resources` copies are transport artifacts only and must remain byte-identical to those originals;
- `PUBLIC_CORE_MANIFEST.json` and its recorded SHA remain the frozen initial-release manifest, not a mutable current-tree manifest.

The protected-main commit that lands this maintenance state is intentionally recorded after merge as closure evidence; it is not guessed or predeclared in this branch. Public Issue #4 remains open until that commit, the required public checks and installed-distribution evidence are confirmed.

## Public legal and installation state

- Legal copyright holder: **ZhongXinWang** (王忠新; pen name: 子君赋)
- License: **Apache License 2.0**
- Security reporting: GitHub Private Vulnerability Reporting, enabled and externally verified before Runtime source upload.
- Initial release installation contract: source checkout + editable install + source-tree/Docker reproduction.
- Packaging maintenance installation contract: source checkout plus locally built normal wheel/non-editable installation, with contract and migration resources included.
- PyPI publication: **not claimed**.

## Engineering lineage

The private source repository contains the recovered S0/PATCH-1 engineering baseline, merged S1 implementation, pre-publication hardening, and the subsequent packaging-hardening maintenance commit identified above. Public Core does **not** reproduce the full private Git history or private-only handoff/freeze-control records.

The public lineage remains verifiable through:

- the exact private source anchors above;
- the exact protected-main initial release commit and tree above;
- the later protected-main maintenance commit once recorded after merge;
- `BASELINE_CONTRACT_HASHES.yaml`;
- Frozen Protocol Registry + 9 Frozen Schemas;
- package-resource byte-identity tests;
- public-safe invariants, ADRs, Acceptance Tests and CI configuration;
- `LICENSE` and `NOTICE`;
- the frozen initial-release `PUBLIC_CORE_MANIFEST.json` and deterministic snapshot hashes.

## Clean-history rule

The Public Core repository begins from a **curated clean snapshot with new public history**. No statement should imply that Public Core contains or audits every historical private blob.

## Explicit exclusions from lineage transfer

The Public Core does not transfer:

- private Git history;
- `00_MASTER_HANDOFF_PROMPT.md`;
- `11_BASELINE_FREEZE.yaml`;
- private review history;
- private publication-gate control records;
- unpublished cases, evidence, prompts, participant data or research packs.

## Frozen Contract relationship

Public packaging maintenance does not silently revise the Frozen Protocol or Frozen Schemas. Any semantic change follows the Runtime RFC + regression-impact + new-baseline rule. A fork may independently modify its own implementation, but it must not claim byte-equivalence with the frozen Human-COS baseline unless the contract hashes actually match.

## Authority boundary

This provenance proves engineering lineage. It does **not** make this repository the sole legitimate Human-COS implementation and does not transfer Human-COS decision authority to GitHub, repository maintainers or code owners.
