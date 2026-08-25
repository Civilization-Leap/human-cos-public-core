# Human-COS Public Core — Provenance

Status: **INITIAL PUBLIC CORE RELEASE LINEAGE FROZEN**

## Private source anchor

- Private engineering repository: `Civilization-Leap/human-cos-runtime`
- Source branch: `main`
- Source commit: `da2c62e21871e911ab26b877928676bc81056e09`
- Source state: Sprint S1 merged plus pre-publication S0/S1 hardening from private PR #4; later Runtime sprints are neither included nor authorized by this publication work.

The hardening commit makes already-declared JSON Schema `date-time` formats enforceable and closes a strict Frozen Registry guard gap for registry-level metadata. It does **not** change the Protocol Registry YAML, any of the 9 Frozen Schemas, or `BASELINE_CONTRACT_HASHES.yaml`.

## Public release record

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

The snapshot and manifest hashes above identify the **initial protected-main source release**. Documentation-only post-publication closure metadata is intentionally outside that frozen snapshot and does not redefine, invalidate, or replace those hashes.

## Public release target and legal state

- Legal copyright holder: **ZhongXinWang** (王忠新; pen name: 子君赋)
- License: **Apache License 2.0**
- Security reporting: GitHub Private Vulnerability Reporting, enabled and externally verified before Runtime source upload.
- Wheel/PyPI/non-editable installation support: not claimed by the initial release; separately tracked in public Issue #4.

## Engineering lineage

The private source repository contains the recovered S0/PATCH-1 engineering baseline, merged S1 implementation and the publication-hardening merge identified above. Public Core does **not** reproduce the full private Git history or private-only handoff/freeze-control records.

The public release preserves verifiable lineage through:

- the exact private source commit above;
- the exact protected-main public release commit and tree above;
- `BASELINE_CONTRACT_HASHES.yaml`;
- Frozen Protocol Registry + 9 Frozen Schemas;
- public-safe invariants, ADRs, Acceptance Tests and CI configuration;
- `LICENSE` and `NOTICE`;
- the initial-release `PUBLIC_CORE_MANIFEST.json` and deterministic clean snapshot hashes recorded above.

## Clean-history rule

The Public Core repository begins from a **curated clean snapshot with new public history**. The initial public snapshot records:

1. exact private source commit;
2. exact staging publication-layer source lineage;
3. list and SHA-256 of published files;
4. excluded private-history/internal-control scope;
5. active Apache-2.0 license and NOTICE state;
6. verified PVR security-reporting state;
7. final protected-main publication commit and tree.

No statement should imply that Public Core contains or audits every historical private blob.

## Explicit exclusions from lineage transfer

The initial Public Core does not transfer:

- private Git history;
- `00_MASTER_HANDOFF_PROMPT.md`;
- `11_BASELINE_FREEZE.yaml`;
- private review history;
- private publication-gate control records;
- unpublished cases, evidence, prompts, participant data or research packs.

## Frozen Contract relationship

Public publication does not silently revise the Frozen Protocol or Frozen Schemas. Any semantic change follows the Runtime RFC + regression-impact + new-baseline rule. A fork may independently modify its own implementation, but it must not claim byte-equivalence with the frozen Human-COS baseline unless the contract hashes actually match.

## Post-publication closure metadata

Post-publication updates to this provenance record are administrative evidence only. They do not create a new Runtime baseline, alter the initial release snapshot, change the Frozen Contract, close Issue #4, or authorize S2.

## Authority boundary

This provenance proves engineering lineage. It does **not** make this repository the sole legitimate Human-COS implementation and does not transfer Human-COS decision authority to GitHub, repository maintainers or code owners.
