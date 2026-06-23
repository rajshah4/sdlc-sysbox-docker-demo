# Petstore Catalog Spec Delta

## ADDED Requirements

### Requirement: Search by maximum adoption fee

Catalog search MUST accept an optional maximum adoption fee expressed in integer cents.

#### Scenario: Matching pets at or below the maximum fee

- Given available pets with adoption fees
- When a maximum adoption fee is supplied
- Then pets at or below that fee are included

#### Scenario: Excluding pets above the maximum fee

- Given available pets with adoption fees
- When a maximum adoption fee is supplied
- Then pets above that fee are excluded

#### Scenario: Rejecting negative maximum fees

- Given a negative maximum adoption fee
- When catalog search is called
- Then the search is rejected with a validation error
