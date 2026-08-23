# Contributing

Human-COS Public Core is designed for independent verification, criticism and reproducibility. Participation does not require joining an organization or accepting the project's conclusions.

## Current contribution mode

**External code contributions are not accepted in the initial Public Core release.**

Reason: the initial release prioritizes independent reproduction and stable provenance before opening a contributor-licensing workflow. No DCO or CLA is active at this stage.

Preferred external participation paths are:

- reproduce S0/S1 claims and publish the result;
- report a failing test, invariant violation or irreproducible behavior;
- propose an RFC for a semantic issue;
- submit an architecture critique or independent implementation comparison;
- report security findings through GitHub Private Vulnerability Reporting;
- maintain an independent fork or implementation.

A public code PR may be used to show a proposed patch, but maintainers must not merge external code until a contribution-license policy is formally activated.

## Maintainer branch & PR discipline

For code maintained inside the authorized repository:

- work on short-lived branches off `main`;
- open a Pull Request for review;
- never force-push shared branches;
- follow `.github/PULL_REQUEST_TEMPLATE.md` and `07_BRANCH_PR_DISCIPLINE.md`;
- never lower or remove a merge-blocking protocol test simply to restore a green build.

## Before a maintainer PR

```bash
pip install -e ".[dev]"
ruff check src tests && ruff format --check src tests
mypy src/human_cos
pytest -q
pre-commit run --all-files
```

## Semantic vs implementation changes

- Semantic protocol / state-machine / permission / admission / validation / safety / publication changes ⇒ open an RFC first (`rfcs/`). Do **not** self-approve.
- Pure implementation detail ⇒ record the decision in an ADR (`docs/adr/`) when it materially affects architecture or reproducibility.

## Independent disagreement is valid participation

A reproduction that shows **no Human-COS incremental value**, an implementation that reaches a different result, or a critique that falsifies an assumption is not treated as a failed contribution. Public Core exists for independent verification, not consensus production.

## Definition of done

A Sprint or reviewed implementation change is done only when:

- exit conditions and applicable Acceptance Tests pass;
- Frozen Protocol/Schemas show no unauthorized semantic drift;
- changes are traceable;
- tests run from a clean environment;
- publication/security boundaries remain intact.
