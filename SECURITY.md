# Security Policy — Human-COS Public Core

## Reporting a vulnerability

Do **not** open a public Issue for an untriaged security vulnerability.

Use the repository's GitHub private vulnerability reporting flow:

**Security → Advisories → Report a vulnerability**

GitHub Private Vulnerability Reporting was enabled and externally verified on the public `Civilization-Leap/human-cos-public-core` repository before Runtime source publication.

## What to include

Include enough information to reproduce and triage the finding without exposing unnecessary sensitive data:

- affected commit/release;
- affected file or component;
- reproduction steps or minimal proof;
- expected vs observed behavior;
- security impact;
- whether the issue can affect Frozen Contract enforcement, T0/ACL boundaries, immutable storage, evidence/authority separation, secrets, or publication controls.

Do not submit live credentials or unnecessary private third-party data.

## Scope & invariants

Human-COS separates *process authority* from *cognitive authority*. Security includes protecting the Runtime against:

- **Evidence/authority confusion** (I-11): external pages, emails, files or model output must never gain power to modify System Prompt, Tool Policy or Protocol. Evidence is data, never authority.
- **Immutable storage** (I-02, AT-03): frozen Evidence, Raw Output and Expert Submission must not be updated in place; changes use newer revisions where the protocol permits.
- **T0 / visibility bypass**: data not admissible at the relevant time or for the relevant actor/role must not enter Context through a permissive source.
- **Secrets handling**: API keys, tokens and credentials must not be committed. Secrets come from environment/secret-store mechanisms.
- **Frozen-contract drift**: unauthorized byte or semantic changes to the Frozen Contract must fail the defined gates.
- **No real-world destructive capabilities** (I-17): the current Runtime performs research, evaluation and recording only; it does not provide automatic military, financial-trading or critical-infrastructure actions.

## Publication boundary

Public Core is a curated clean snapshot with new public history. The complete private engineering Git history is excluded because current-file scanning does not prove every historical private blob safe for publication.

Every published snapshot must be scanned immediately before release and must carry file-level provenance and SHA-256 hashes in `PUBLIC_CORE_MANIFEST.json`.

## Disclosure expectations

No bounty, response-time SLA or safe-harbor promise exists unless separately published by the responsible maintainer. Reporters should avoid public disclosure before triage when doing so would increase avoidable risk.
