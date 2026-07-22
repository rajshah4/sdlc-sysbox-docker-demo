# OpenHands Sysbox SDLC Demo

**A sparse concurrency bug becomes a transaction-safe fix, proven against a
containerized application stack running inside an isolated OpenHands sandbox.**

This repository is a customer-facing SDLC Automation Demo for OpenHands
Enterprise. It makes Docker-in-Docker visible and useful: the agent launches
the same multi-service topology an engineer or CI job would use, without
mounting the host Docker socket.

## The Story

Two customers try to adopt the last available pet at the same time. The
baseline API performs its availability check and write in separate database
transactions, so both requests can succeed.

The OpenHands agent must:

1. Start an inner Docker daemon in its Sysbox sandbox.
2. Build and launch the Petstore topology with Docker Compose.
3. Reproduce the race against PostgreSQL.
4. Implement a transaction-safe fix and database invariant.
5. Rebuild the image and run concurrent integration tests.
6. Run the Playwright adoption flow through the web container.
7. Open a PR with the commands and evidence.

## What Runs Inside the Agent Sandbox

```text
OpenHands runtime pod (Sysbox)
└── inner Docker daemon
    ├── petstore API
    ├── PostgreSQL
    ├── Redis
    ├── nginx web UI
    ├── concurrent integration test (ephemeral)
    └── Playwright browser test (ephemeral)
```

The architectural proof is in `scripts/validation/sysbox_preflight.sh`: Docker
must be usable, a nested `hello-world` container must run, and
`/var/run/docker.sock` must **not** be mounted from the host.

## Demo Commands

Run these commands from an OpenHands Enterprise Sysbox sandbox:

```bash
scripts/validation/sysbox_preflight.sh
scripts/validation/reproduce_adoption_race.sh
scripts/validation/verify_stack.sh
```

On the intentionally vulnerable baseline:

- `reproduce_adoption_race.sh` succeeds and records two accepted adoptions.
- `verify_stack.sh` fails the concurrency invariant.

After the issue is fixed, the expected result reverses:

- the reproduction no longer observes two accepted requests;
- the full verification passes integration and browser checks.

QA evidence is written to `artifacts/qa/` and is excluded from commits except
for the directory placeholder.

## Audience-Friendly Before and After

| Without nested Docker verification | With OpenHands Enterprise + Sysbox |
| --- | --- |
| Unit tests pass | API image is rebuilt |
| PostgreSQL race is not exercised | PostgreSQL and Redis are launched |
| Browser flow is unavailable | Playwright verifies the web flow |
| Confidence is incomplete | Concurrency invariant is proven |

The narration line is:

> The coding agent is already isolated in an OpenHands sandbox. Sysbox lets it
> create another containerized application environment inside that sandbox,
> without giving it control of the host Docker daemon.

## Repository Map

| Path | Purpose |
| --- | --- |
| `compose.yaml` | API, PostgreSQL, Redis, web, integration, and browser services |
| `Dockerfile` | Petstore API image |
| `app/petstore_app/api.py` | Intentionally vulnerable baseline API |
| `app/db/001_schema.sql` | Baseline database schema and seed data |
| `tests/integration/` | Black-box concurrent adoption verification |
| `app/web/tests/` | Containerized Playwright test |
| `scripts/validation/` | Sysbox preflight, reproduction, and full QA path |
| `prompts/fix-adoption-race.md` | Prompt for the live OpenHands run |
| `docs/sysbox-demo-runbook.md` | Operator walkthrough and evidence checklist |

## Human Control

OpenHands may create a branch, tests, evidence, comments, and a draft PR. A
human approves scope, reviews the solution, merges, and controls deployment.
Secrets remain in the OpenHands secret store and never belong in this repo.
