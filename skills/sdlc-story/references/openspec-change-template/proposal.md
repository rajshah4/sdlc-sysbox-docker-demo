# Change: Filter pets by max adoption fee

## Why

Adopters need a quick way to find pets whose adoption fees fit their budget.

## Source

- GitHub issue: https://github.com/example-org/sdlc-automation-github-demo/issues/123
- Trigger label: `openhands-build`
- Automation: `sdlc-story`

## Assumptions

- Adoption fees are represented as integer cents in the Petstore domain model.
- The request is limited to catalog search behavior.

## Non-Goals

- Payment processing, billing, discounts, and persistence changes are out of scope.

## What Changes

- Catalog search accepts an optional maximum adoption fee.
- Pets with fees above the maximum are excluded.
- Negative maximum fees are rejected.

## Impact

- App behavior: adopters can narrow search results by budget.
- Tests: catalog tests cover matching, exclusion, and validation.
- Humans: reviewers approve the product scope and merge decision.

## Human Gates

- Scope approval: GitHub issue and PR review.
- Review approval: GitHub PR review.
- Merge approval: repository maintainers.
- Deployment approval: outside this automation.
