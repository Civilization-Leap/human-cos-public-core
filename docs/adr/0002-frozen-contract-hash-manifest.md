# ADR-0002: Frozen Contract Hash Manifest

- Status: Accepted
- Date: 2026-08-18
- Related: S0-PATCH-1 / P0-3, ADR-0001

## Context

S0 review found that the frozen Protocol Registry and Schemas were "correct" but
not actually *pinned*: tests validated shape and sample behavior, not the
byte-exactness of the signed artifacts. A future edit to a frozen protocol could
pass CI as long as it still satisfied the Schema and existing sample tests.
Additionally, the registry change-control logic tolerated a bare `"RFC"` change
control and did not reject version downgrades or removals of frozen protocols.

## Decision

Introduce `BASELINE_CONTRACT_HASHES.yaml`: a SHA-256 manifest over the **10
signed V0.1 files** (the Protocol Registry + all 9 core JSON Schemas). A
merge-blocking test (`tests/protocol/test_frozen_contract.py`) recomputes every
hash on each CI run and fails on **any** byte change, deletion, or addition.

Supporting tightening (non-protocol, but part of the freeze gate):

- Registry change-control now **rejects** a bare `"RFC"` (only
  `RFC + regression impact review` and its `+ new baseline version` form are
  valid), since a bare RFC is weaker than the frozen contract.
- `assert_no_silent_mutation` now also rejects **version downgrades** and
  **protocol removals** of the previous snapshot.
- New `assert_no_unblessed_change` rejects **any** alteration (add/remove/bump/
  downgrade/silent) to a frozen snapshot.

## Consequences

- Deleting, downgrading, modifying, or adding any frozen protocol/schema now
  fails CI, not just review.
- Legitimate semantic change requires the RFC + regression impact review +
  new-baseline flow, which updates the manifest in the same reviewed change.
- The rule is deliberately simple and non-heuristic, avoiding "smart" judgment
  about which changes matter.
