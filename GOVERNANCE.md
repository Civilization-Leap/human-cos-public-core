# Governance

This document describes ownership and change authority for the Human-COS Public Core implementation. It does **not** grant repository maintainers authority over external professional judgment, independent Human-COS platforms or real-world decisions.

## Publication ownership

- Legal copyright holder: **ZhongXinWang**
- Chinese name: **王忠新**
- Pen name: **子君赋**
- License: **Apache License 2.0**

Copyright/licensing ownership does not create superior authority over independent Human-COS implementations, professional facts, public reality or real-world responsible actors.

## Authority model

- **Process authority**: Deterministic Orchestrator + Protocol Registry govern Runtime process boundaries.
- **Cognitive authority**: models/experts admitted through Qualification (Task Capability). No role-play substitutes for missing capability (I-09).
- **Human Expert**: formal system subject; results carry provenance, freeze, dissent and falsification. Being human does not equal truth (I-13).
- **Review separation**: Solver ≠ Judge; Evaluator/Challenger/Blind Judge are distinct from the Solver of the same run (I-12).

## Public Core does not create a central authority

Public Core is a reference implementation and reproducibility surface. It is not the sole legitimate Human-COS implementation.

Independent platforms may:

- reproduce the frozen baseline;
- maintain a compatible implementation;
- fork implementation choices;
- preserve a prior protocol version;
- propose a new semantic baseline through their own governance;
- disagree with this repository's judgments or architecture.

Compatibility claims must remain precise. An implementation that changes Frozen Contract semantics must not claim byte-equivalence with the frozen Human-COS baseline.

Protocol maintenance power is **not** civilization judgment power. Maintaining a registry, schema, test suite or repository does not give the maintainer superior authority over professional facts, public reality or real-world responsible actors.

## Change control

| Change type | Required gate |
|---|---|
| Pure implementation detail | ADR (`docs/adr/`) when materially architectural |
| Semantic protocol / state machine / permission / admission / validation / publication / safety change | RFC (`rfcs/`) + regression impact review + **new baseline version** (I-19) |
| Any byte change to the 10 Frozen Contract files (`protocol_registry_v0.1.yaml` + `schemas/*.schema.json`) | Blocked unless the RFC + regression-impact + **new baseline version** flow updates `BASELINE_CONTRACT_HASHES.yaml` in the same reviewed change |

## Repository & review discipline

- The private engineering source repository remains private; Public Core uses a clean public history.
- `main` should be protected from direct push and changes should enter through reviewed PRs once repository protection is configured.
- Merge-blocking protocol tests may not be deleted or downgraded to accommodate an implementation.
- GitHub Environments/reviewers are repository controls only; Runtime Approval State remains the system mechanism of record (I-20).
- Public Core publication does not authorize S2 or later sprints.

## Initial external contribution boundary

The initial Public Core release does not merge external code until a contribution-license mechanism is separately approved. No DCO or CLA is active at initial publication.

Independent reproduction, critique, issues, RFC proposals, private security reports and independent implementations remain valid participation paths.

## Publication provenance

The initial Public Core release identifies its private source anchor and clean-snapshot manifest. The complete private Git history is not part of public governance and is not required to establish public-source provenance.
