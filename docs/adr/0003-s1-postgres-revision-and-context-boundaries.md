# ADR-0003: S1 PostgreSQL revision storage and context boundaries

- Status: Accepted
- Date: 2026-08-19
- Updated: 2026-08-20 after pre-merge blocker review
- Related: Sprint S1 / T-003, T-004, T-005, T-006 (part 1)

## Context

S1 must make T0, actor/role/time visibility, Case/Evidence immutability, and
Context construction executable at the data layer without changing the frozen
V0.1 JSON Schemas. It must also keep Evidence as data rather than allowing
Evidence content or a permissive data source to influence protocol, tool, prompt,
or visibility authority.

## Decision

1. The five frozen S1-facing JSON Schemas remain the admission contracts. Internal
   Pydantic models use deeply immutable tuple-based representations, while JSON
   serialization continues to emit the arrays required by the frozen Schemas.
2. PostgreSQL stores Case and Evidence as append-only JSONB revisions. Evidence
   revisions use `(evidence_id, revision)` plus an internal `parent_revision`;
   Case revisions use `(case_id, revision)`. Existing revisions may not be
   updated or deleted.
3. Database triggers reject `UPDATE` and `DELETE` on Case revisions, Evidence
   revisions, and Context admission records. Case and Evidence changes are
   represented by new revisions, not mutation of old records.
4. Time is a data-layer boundary in every Case mode. Historical blind evaluation
   is fixed to Case T0. Non-historical Context construction requires an explicit,
   timezone-aware reference time. `available_from`, `available_until`, and live
   ingestion time are enforced against that reference time.
5. Historical Evidence revision selection is time-aware: for each `evidence_id`,
   the repository selects the latest revision admissible at the target time,
   rather than selecting the global latest revision and filtering afterward.
6. Actor/role visibility is enforced only after the target-time revision is
   selected. The system does not fall back to an older revision merely because a
   newer temporally admissible revision is more restrictive.
7. Context construction applies temporal and actor/role gates twice by design:
   the repository narrows candidates, and the Context Builder independently
   re-applies the deterministic gates. A data source is not trusted as authority.
8. The frozen Context Manifest schema remains unchanged. An implementation-side
   immutable Context admission sidecar binds the Manifest hash to the exact
   Evidence revision/snapshot, actor scope, role, reference time, visibility
   basis, and its own verified record hash. This preserves reconstruction without
   silently extending the frozen Manifest contract.
9. Evidence prose is never parsed to derive `tool_permissions`,
   `protocol_version`, `prompt_version`, `forbidden_scopes`, T0, or ACL decisions.
10. No new S1 dependency is introduced; existing `psycopg`, Pydantic, JSON Schema,
    PostgreSQL, pytest, and Docker dependencies are reused.

## Migration / rollback

- Forward: `migrations/0001_s1_case_evidence.sql` creates Case/Evidence revision
  tables, Context admission storage, indexes, and immutable-record triggers.
- Rollback: `migrations/0001_s1_case_evidence.rollback.sql` removes all three S1
  storage tables and the immutable-record function. Rollback is destructive and
  is intended only before retained S1 data becomes authoritative.
- Compatibility: all S0 protocol/schema files remain byte-identical; S1 adds
  storage and application-layer behavior around them.

## Pre-merge review closure

The 2026-08-19 pre-merge review identified five blockers: deep immutability,
live reference-time enforcement, time-aware revision selection, reconstructable
Context admission lineage, and Case/T0 database immutability. They are resolved
entirely at the implementation/storage layer. No Frozen Schema or Protocol
semantic change was required; therefore no RFC is opened by this correction.

## Non-decisions / explicit exclusions

This ADR does not add Responsibility Map, Application Profile, L0-L3 thresholds,
Stakeholder-visible enums, No Silent Crossing execution guards, model
qualification, state-machine orchestration, or any real-world execution ability.
Those remain outside S1.
