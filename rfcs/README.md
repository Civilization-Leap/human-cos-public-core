# RFCs

This directory holds RFC proposals that would change the *semantics* of the
Human-COS protocol, state machine, permissions, admission, validation,
publication, or safety rules (invariants I-19, and `../01_ABSOLUTE_INVARIANTS.md`).

Rules (per `../00_MASTER_HANDOFF_PROMPT.md` and S0):

- RFC_REQUIRED changes are **reported, never self-approved**.
- Adding an RFC does **not** alter the frozen protocol; it only opens a
  proposal for human/governance review.
- An accepted semantic change requires: RFC + regression impact review +
  a **new baseline version**.
- One file per proposal, named `<NNNN>-<slug>.md`.

No RFCs have been opened during S0.

## Frozen contract

The V0.1 frozen contract — `../protocols/protocol_registry_v0.1.yaml` and the 9
JSON Schemas in `../schemas/` — is byte-locked by `../BASELINE_CONTRACT_HASHES.yaml`
and enforced by the merge-blocking test `../tests/protocol/test_frozen_contract.py`.
Those 10 files must never be touched by an ordinary change; only the
RFC + regression impact review + new-baseline flow may update them (together
with the manifest).
