# Human-COS Public Core

Human-COS Public Core is a curated open-source reproducibility surface for the current Human-COS Runtime S0/S1 engineering baseline.

It exists so independent researchers and engineering teams can inspect, reproduce, criticize, falsify, fork or replace implementation choices without joining a central organization or accepting the project's conclusions.

> **This is NOT a "main agent + free workers" orchestration product.**
> Process authority belongs to the **Deterministic Orchestrator + Protocol Registry**; cognitive authority belongs to qualified models/experts. Evidence and frozen records are data, not authority.

## Current engineering scope

**Sprint S1** — Case/Evidence persistence, T0 data-layer isolation, actor/role visibility, append-only Evidence revisions, and Context Manifest ACL.

Not implemented in this Public Core:

- model registry/adapters or qualification;
- full state-machine orchestration;
- UI;
- Responsibility Map / Decision Record Runtime contract;
- R1–R7 Runtime enums;
- No Silent Crossing execution guard;
- Stakeholder-visible enum;
- L0–L3 automated thresholds;
- Spark/Nebula Application Profile;
- cross-platform federation / attestation / SEGI machine interface;
- any real-world destructive or sovereign execution capability.

## Publication provenance

Initial Public Core source anchor:

`Civilization-Leap/human-cos-runtime@c48b630d98339a6a7a0ddec68926071420e699c5`

Public repository:

`Civilization-Leap/human-cos-public-core`

The Public Core starts from a **curated clean snapshot with new public Git history**. The complete private engineering history is intentionally excluded. See `PUBLIC_PROVENANCE.md` and `PUBLIC_CORE_MANIFEST.json`.

## License and attribution

- Copyright holder: **ZhongXinWang**
- Chinese name: **王忠新**
- Pen name: **子君赋**
- License: **Apache License 2.0**

See `LICENSE` and `NOTICE`.

## Security reporting

Do **not** open a public Issue for an untriaged security vulnerability.

Use the repository's GitHub **Security → Advisories → Report a vulnerability** private reporting flow. See `SECURITY.md`.

## What's here

- `src/human_cos/protocols/` — registry loader, version validator, no-silent-mutation guard, frozen-contract verifier, schema loader.
- `protocols/protocol_registry_v0.1.yaml` + `schemas/*.schema.json` — Frozen Contract: Protocol Registry + 9 Schemas.
- `BASELINE_CONTRACT_HASHES.yaml` — byte-locks those 10 files.
- `src/human_cos/core/` + `src/human_cos/storage/` — S1 data boundary and PostgreSQL layer.
- `migrations/` — S1 forward/rollback SQL.
- `tests/` — protocol, contract, ACL, unit and PostgreSQL integration tests.
- `docs/adr/` — implementation architecture decisions.
- `rfcs/` — semantic-change process.
- `.github/workflows/ci.yml` — tests, lint/format, type check, CLI, Frozen Contract gate, secret scan and Docker build.

## Quick start

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
pytest -q
human-cos-protocols load protocols/protocol_registry_v0.1.yaml
```

Or via Docker:

```bash
docker build -t human-cos-runtime:s1 .
docker run --rm human-cos-runtime:s1 pytest -q
```

PostgreSQL-backed integration tests require `HUMAN_COS_TEST_DATABASE_URL`; the GitHub Actions workflow supplies a disposable PostgreSQL 16 service.

## Frozen Contract

`BASELINE_CONTRACT_HASHES.yaml` records the SHA-256 of the 10 signed V0.1 contract files. CI recomputes and compares them on every run; **any unauthorized byte change fails the gate**.

A real semantic change requires an RFC, regression-impact review and a **new baseline version**, with the hash manifest updated in the same reviewed change.

## Key invariants

See `01_ABSOLUTE_INVARIANTS.md` and `SECURITY.md`. In particular:

- **I-01** process authority ≠ cognitive authority;
- **I-02 / AT-03** frozen data uses append-only revisions;
- **I-11** external evidence is data, never authority;
- **I-17** no real-world destructive execution;
- **I-19** semantic protocol change ⇒ RFC + version bump;
- **I-20** GitHub never replaces Runtime Approval State.

## Independent implementation

Public Core is a reference implementation and reproducibility surface, not a unique implementation center. Independent teams may reproduce, critique, fork or replace implementation choices. Agreement is not required; reproducible convergence and preserved disagreement are both useful evidence.

## Contribution mode

The initial release does **not** merge external code contributions. No DCO or CLA is active yet.

External participation is still welcome through:

- independent reproduction reports;
- issues and falsification findings;
- RFC proposals;
- private security reports;
- independent implementations and comparative results.

See `CONTRIBUTING.md` and `GOVERNANCE.md`.
