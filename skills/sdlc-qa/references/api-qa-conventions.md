# API And Behavior QA Conventions

Use this reference when a PR changes Python behavior or Petstore API behavior.

## Test Shape

Prefer a three-part pytest shape:

1. Arrange only the data or runtime state needed for the behavior.
2. Act once through the public function or HTTP boundary being tested.
3. Assert status, body/return value, and important side effects.

Keep tests readable enough that a reviewer can map them back to the OpenSpec-style requirements and scenarios.

## Petstore Coverage Matrix

| Change area | Test file | Must cover |
| --- | --- | --- |
| Catalog filters | `app/tests/test_pet_catalog.py` | matching, exclusion, invalid values, default status behavior |
| Adoption validation | `app/tests/test_adoptions.py` | available pet succeeds, pending/adopted/unknown pet fails |

## Strong Assertions

- Assert IDs or names when order matters.
- Assert error messages only when they are user/operator visible.
- Assert integer cents for fee behavior.
- Assert pending pets are absent from default available-pet paths.

## Avoid

- Broad snapshots that obscure behavior.
- Mocking local Petstore functions when direct calls are cheap.
- Adding dependencies just to test simple Python code.
- Only running lint or type checks and calling that QA.

## Report Wording

Use plain evidence:

```markdown
QA Status: pass | fail | partial

Changed behavior tested:
- ...

Commands run:
- ...

Tests added:
- ...

Acceptance criteria:
- [x] ...
- [ ] ...

Remaining risk:
- ...
```
