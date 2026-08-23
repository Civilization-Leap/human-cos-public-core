# Human-COS Public Core — Public Scope

Status: **FROZEN FOR INITIAL PUBLIC CORE RELEASE**

Source anchor: `main@c48b630d98339a6a7a0ddec68926071420e699c5`

Public Core exists to make the current S0/S1 engineering claims independently inspectable and reproducible. It is not the complete private engineering repository and it is not the authority that defines Human-COS theory.

## Included in the initial Public Core

- `README.md`, `ARCHITECTURE.md`, `GOVERNANCE.md`, `CONTRIBUTING.md`, `SECURITY.md`;
- `PUBLIC_SCOPE.md`, `PUBLIC_PROVENANCE.md`, `PUBLIC_CORE_MANIFEST.json`;
- `LICENSE`, `NOTICE`;
- `01_ABSOLUTE_INVARIANTS.md`;
- `07_BRANCH_PR_DISCIPLINE.md`;
- `09_ACCEPTANCE_TESTS.yaml`;
- `BASELINE_CONTRACT_HASHES.yaml`;
- Frozen Protocol Registry + 9 Frozen Schemas;
- protocol loader, schema validation and Frozen Contract verification;
- S1 Case/Evidence application models, T0/time boundaries, actor/role ACL, Context admission logic and append-only PostgreSQL storage;
- S1 forward/rollback migrations;
- protocol, contract, unit and integration tests needed to reproduce S0/S1 claims;
- ADRs that explain included implementation choices;
- RFC process documentation;
- public CI workflow, deterministic lockfile and build metadata;
- non-sensitive development examples required for reproducibility.

## Excluded from the initial Public Core

The following are not part of this release unless separately reviewed and explicitly added in a later version:

- full private Git history;
- private branches, review conversations and internal issue history;
- `00_MASTER_HANDOFF_PROMPT.md` and Programming-AI execution handoff/control prompts;
- `11_BASELINE_FREEZE.yaml`, which records private engineering governance/source material not needed for public reproduction;
- `.github/CODEOWNERS.example`, because placeholder ownership must not be published as governance fact;
- private publication-staging control records such as `PUBLICATION_DECISIONS.md`, `LICENSE_DECISION.md` and `SECURITY_PUBLICATION_GATE.md`;
- private operational instructions not required to reproduce public S0/S1 claims;
- credentials, tokens, secrets, private endpoints, private account identifiers or unpublished contact information;
- retained case data, private evidence, model outputs, expert submissions or participant information;
- unpublished research packs and evaluation datasets;
- later-sprint implementation not already merged into the fixed source anchor;
- Responsibility Map / Decision Record Runtime contract;
- R1–R7 Runtime enums;
- Stakeholder-visible enum or No Silent Crossing execution guard;
- L0–L3 thresholds;
- Spark/Nebula Application Profile;
- cross-platform federation / attestation / SEGI machine interface;
- real-world military, trading, infrastructure or other destructive execution capability.

## Scope discipline

Public Core is a **curated reproducibility surface**. Exclusion does not mean a concept is rejected; inclusion does not grant the included code or maintainer superior authority over independent Human-COS implementations.

Independent platforms may adopt, reject, fork or replace implementation choices. Frozen Contract changes still require the defined semantic-change process; implementation diversity remains allowed.
