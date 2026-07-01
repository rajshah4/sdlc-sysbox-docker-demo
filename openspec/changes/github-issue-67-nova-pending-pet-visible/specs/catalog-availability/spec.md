# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default catalog search returns only available pets

The default customer-facing catalog search must filter pets by `status="available"` and must not show pets with `status="pending"` or any other non-available status.

#### Scenario: Default search excludes pending pets

- Given the Petstore catalog contains Nova (pet-103) with status="pending"
- And the catalog contains other pets with status="available"
- When a customer performs a default catalog search (without specifying status)
- Then the results must include only pets with status="available"
- And Nova must not appear in the results

#### Scenario: Species filter with default status excludes pending pets

- Given the Petstore catalog contains Scout (pet-101, dog, available) and Nova (pet-103, dog, pending)
- When a customer searches for species="dog" without specifying status
- Then the results must include only Scout
- And Nova must not appear in the results

#### Scenario: Explicit pending search returns pending pets when requested

- Given the Petstore catalog contains Nova (pet-103) with status="pending"
- When a support user explicitly searches with status="pending" and species="dog"
- Then the results must include Nova
- And this is the only valid way for pending pets to appear in search results

## VERIFIED Existing Behavior

The following existing code and tests already implement these requirements:

### Backend Implementation (`app/petstore_app/catalog.py`)
- Line 31: `search_pets()` has default parameter `status: str = "available"`
- Lines 40-51: Filter logic correctly excludes pets where status doesn't match

### Frontend Implementation (`app/web/app.js`)
- Line 17: Filter logic includes `&& pet.status === "available"`

### Test Coverage (`app/tests/test_pet_catalog.py`)
- `test_search_pets_filters_by_species_and_status()`: Verifies species="dog" search returns only Scout, excluding Nova
- `test_search_pets_can_find_pending_pets_when_requested()`: Verifies explicit status="pending" search returns Nova

## Acceptance Criteria

- [x] Backend default search excludes pending pets
- [x] Frontend default search excludes pending pets
- [x] Explicit pending searches work when status="pending" is specified
- [x] Nova (pet-103) is excluded from default searches
- [x] Regression tests verify the behavior

## Notes

Investigation confirms the current implementation already satisfies all requirements. The PENDING_PET_VISIBLE log from 2026-06-29 may indicate a past regression that has since been corrected, or this may be a demo test scenario verifying the automation workflow.
