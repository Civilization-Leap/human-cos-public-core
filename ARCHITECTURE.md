# Architecture

High-level runtime architecture (V0.1 scope; S0 implements only the protocol
contract layer).

```text
┌─────────────────────────────────────────────────────────────────┐
│ Human Expert  (formal system subject — review & adjudication)    │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│ Deterministic Orchestrator  ← process authority (code + registry) │
│  state_machine · context_builder · permissions · provenance       │
└───────────────┬───────────────────────────────┬─────────────────┘
                │                               │
┌───────────────▼─────────────┐   ┌─────────────▼───────────────────┐
│ Qualified Domain Model/Tool │   │ Meta-Controller (global cognition)│
│ (Task-Capability gated)     │   │ cannot edit evidence / skip states │
└───────────────┬─────────────┘   └─────────────┬───────────────────┘
                │                               │
┌───────────────▼───────────────────────────────▼─────────────────┐
│ Separation of concerns: Solver ≠ Judge. Evaluator / Challenger  │
│ / Blind Judge are distinct identities.                          │
└─────────────────────────────────────────────────────────────────┘
```

## Layers (S0 implemented = bold)

- **Protocol contract layer** — registry loader, version/change control, JSON Schema validation. ✅ S0
- **Case/Evidence data boundary** — frozen-contract application models, T0 filtering, actor/role ACL. ✅ S1
- **Evidence revision storage** — PostgreSQL append-only revisions + database mutation guard. ✅ S1
- **Context Manifest builder** — admitted Evidence IDs, stable hash, explicit forbidden scopes. ✅ S1
- State machine + mode transitions + guards — S3
- Model registry + adapters + qualification — S2
- Run/manifest immutable storage — S3

## Core rules

1. Frozen evidence/raw output are append-only; no in-place UPDATE (I-02).
2. External evidence never modifies System Prompt / Tool Policy / Protocol (I-11).
3. Semantic protocol change ⇒ RFC + version bump (I-19).
4. Runtime (not GitHub) is the source of truth for approval state (I-20).
