# Human-COS Public Core — Provenance

Status: **INITIAL PUBLIC CORE RELEASE LINEAGE FROZEN**

## Private source anchor

- Private engineering repository: `Civilization-Leap/human-cos-runtime`
- Source branch: `main`
- Source commit: `c48b630d98339a6a7a0ddec68926071420e699c5`
- Source state: Sprint S1 merged; later Runtime sprints are neither included nor authorized by this publication work.

## Public release target

- Public repository: `Civilization-Leap/human-cos-public-core`
- Legal copyright holder: **ZhongXinWang** (王忠新; pen name: 子君赋)
- License: **Apache License 2.0**
- Security reporting: GitHub Private Vulnerability Reporting, enabled and externally verified before Runtime source upload.

## Engineering lineage

The private source repository contains the recovered S0/PATCH-1 engineering baseline and merged S1 implementation. Public Core does **not** reproduce the full private Git history or private-only handoff/freeze-control records.

The public release preserves verifiable lineage through:

- the exact source commit above;
- `BASELINE_CONTRACT_HASHES.yaml`;
- Frozen Protocol Registry + 9 Frozen Schemas;
- public-safe invariants, ADRs, Acceptance Tests and CI configuration;
- `LICENSE` and `NOTICE`;
- `PUBLIC_CORE_MANIFEST.json`, containing the published file set and SHA-256 hashes.

## Clean-history rule

The Public Core repository begins from a **curated clean snapshot with new public history**. The initial public snapshot records:

1. exact private source commit;
2. exact staging publication-layer source commit;
3. list and SHA-256 of published files;
4. excluded private-history/internal-control scope;
5. active Apache-2.0 license and NOTICE state;
6. verified PVR security-reporting state.

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

## Authority boundary

This provenance proves engineering lineage. It does **not** make this repository the sole legitimate Human-COS implementation and does not transfer Human-COS decision authority to GitHub, repository maintainers or code owners.
