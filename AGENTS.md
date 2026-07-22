# Agent Instructions

This is the Sysbox Docker-in-Docker SDLC Automation Demo. Customer-facing
language should say "SDLC Automation Demo" and should not use "software
factory."

## Demo Objective

This repository proves that an OpenHands agent running in an isolated Sysbox
sandbox can launch and test a realistic containerized application topology.
Docker must run inside the sandbox. Never mount or request the host Docker
socket (`/var/run/docker.sock`).

Before changing code:

1. Run `scripts/validation/sysbox_preflight.sh`.
2. Run `scripts/validation/reproduce_adoption_race.sh` to reproduce the bug.
3. Preserve the pre-fix evidence under `artifacts/qa/` in the working tree.

Before opening a PR:

1. Run `scripts/validation/verify_stack.sh`.
2. Include the Docker engine security options, Compose service health, the
   concurrent integration result, and browser result in the PR body.
3. Do not claim success from unit tests alone.

## Repository Shape

- Petstore API: `app/petstore_app/`
- Backend tests: `app/tests/`
- Containerized web UI: `app/web/`
- PostgreSQL schema: `app/db/`
- Concurrent integration tests: `tests/integration/`
- Docker/Sysbox validation: `scripts/validation/`
- GitHub automations: `automations/github/`
- Setup and registration scripts: `scripts/`
- Demo docs: `docs/`

## Automation Rules

- Humans approve scope, reviews, PRs, merges, deployments, and production changes.
- OpenHands may create branches, tests, comments, reports, and draft PRs when the relevant GitHub label or comment asks it to.
- Do not push directly to `main`.
- Do not print or commit secrets.
- Do not mount the host Docker socket.
- Prefer deterministic scripts and preflight checks before spending LLM calls.
- Read `docs/sysbox-demo-runbook.md` before broad exploration.
- Use event-driven GitHub triggers instead of polling.
- Avoid dependency installation in automation helper scripts unless a prompt explicitly authorizes it.

## Petstore Product Rules

- Default pet search returns only available pets.
- Pending pets can be shown only when explicitly requested and cannot be adopted.
- Money is represented as integer cents.
- UI-visible changes need UI evidence, not only unit tests.
- A pet can have at most one accepted adoption, even when requests arrive
  concurrently.
