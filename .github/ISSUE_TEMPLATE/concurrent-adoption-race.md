---
name: Concurrent adoption race
about: Demo issue for Sysbox-backed containerized verification
title: "Adoption requests can exceed inventory under concurrency"
labels: "type:bug,openhands-build"
assignees: ""
---

## Problem

Two customers can occasionally adopt the last available pet at the same time.
The UI looks correct during normal use, and unit tests pass, but production-like
concurrent requests can both be accepted.

## Expected behavior

- Exactly one request is accepted.
- The other request receives a conflict response.
- Only one adoption is stored for the pet.
- The fix is verified against PostgreSQL in the Docker Compose stack.
- The normal browser adoption flow still passes.

## Human gate

OpenHands may create a branch and draft PR with containerized QA evidence. A
human must review and merge.
