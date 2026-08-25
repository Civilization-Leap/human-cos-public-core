# ADR-0001: Repository structure & default execution mode

- Status: Accepted
- Date: 2026-08-18
- Related Sprints: S0

## Context

The V0.1 baseline defines a deterministic-orchestration runtime whose protocol
semantics must not drift during implementation. We need a repo layout and
working discipline that make the "unchangeable semantics" a *verifiable
engineering contract* rather than prose.

## Decision

1. **Layout**: adopt the `src/human_cos/...` package layout defined in
   `02_REPO_INITIALIZATION.md`, with top-level `schemas/`, `protocols/`,
   `migrations/`, `tests/{unit,contract,integration,protocol,regression}/`,
   `docs/adr/`, `rfcs/`, and `.github/workflows/`.
2. **Default execution mode = CONTROLLED**: a single Sprint per run; tests,
   static checks, change-list, and fixed return format must complete and **stop**
   before the next Sprint is authorized. No cross-Sprint overreach.
3. **Protocol Registry as code + data**: the frozen registry lives in
   `protocols/protocol_registry_v0.1.yaml` and is loaded/validated by
   `src/human_cos/protocols`. Semantic changes require a version bump guarded by
   `assert_no_silent_mutation`.
4. **JSON Schemas as source of truth**: the 9 data-contract schemas are copied
   verbatim from the handoff package and are the only accepted definition of
   those shapes; all validation delegates to them.

## Consequences

- Protocol/schema drift is now detectable by CI, not by review.
- Future Sprints add business logic on top without weakening the S0 contract.
- The registry's `change_control` value at schema level must be one of a small
  allowed set; anything else fails load.
