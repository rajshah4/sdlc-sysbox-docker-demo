# Design

## Context

The Petstore catalog keeps adoption fees as integer cents and default search behavior returns available pets only.

## Decision

- Add a keyword-only `max_adoption_fee_cents` argument to catalog search.
- Validate that the maximum fee is not negative.
- Filter available pets after existing query/species/status/tag checks.

## Risks

- Money logic can become inconsistent if floats are introduced; keep integer cents.
- Search defaults could accidentally expose pending pets; preserve the available-only default.

## Validation Plan

- Run focused catalog tests for matching, exclusion, and negative validation.
- Run the full pytest suite before opening the PR.
