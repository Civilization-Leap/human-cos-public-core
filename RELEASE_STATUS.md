# Human-COS Public Core — Release Status

Initial public engineering baseline: **S0/S1 Public Core**

Private source anchor:

`Civilization-Leap/human-cos-runtime@da2c62e21871e911ab26b877928676bc81056e09`

Public repository:

`Civilization-Leap/human-cos-public-core`

## Included capability

- Frozen Protocol Registry + 9 Frozen Schemas;
- Frozen Contract hash enforcement;
- declared JSON Schema `date-time` format enforcement;
- strict Frozen Registry guard including registry-level metadata changes;
- Case/Evidence application models;
- T0/time-boundary enforcement;
- actor/role ACL visibility;
- append-only Case/Evidence revisions;
- Context admission sidecar and provenance binding;
- PostgreSQL S1 storage/migrations;
- protocol, contract, unit and integration tests.

## Not included / not authorized

This release does not include or authorize S2 or later Runtime capability, model registry/adapters, qualification, full state-machine orchestration, Responsibility Map, No Silent Crossing execution guard, cross-platform federation, or real-world execution.

Wheel/PyPI/non-editable installation support is not claimed by this initial source-reproducibility release and remains separately tracked in Issue #4.

## Publication gates

- G0 Public Scope: PASS
- G1 Source provenance: PASS — refreshed to the hardened private source anchor above
- G2 License/copyright: PASS
- G3 Security reporting: PASS
- G4–G8: REVALIDATION IN PROGRESS for the hardened snapshot; final PASS requires the regenerated manifest, safety scan, snapshot artifact and public dual-version CI.
- G9: NOT AUTHORIZED until G4–G8 revalidation closes.

The public repository is a reproducibility surface, not an authority over independent professional judgment or real-world decisions.
