# Sysbox Docker-in-Docker SDLC Demo Runbook

## Demo outcome

Show that an OpenHands Enterprise agent can recreate a realistic application
topology, diagnose behavior across services, and verify its own fix while its
Docker daemon remains isolated inside the agent sandbox.

## Operator setup

- The OpenHands Enterprise runtime must use the `sysbox-runc` runtime class.
- The GitHub integration must have access to this repository.
- The sandbox image must include Docker CLI, Docker Compose, and permission to
  start the inner daemon.
- Allow up to 30 minutes for the first run because base images may need to be
  pulled into a fresh inner Docker cache.

For a newly created repository, add it to the OpenHands GitHub App installation
before using a repo-backed conversation. An unbound conversation can still
clone the public repository and use the stored `GITHUB_TOKEN`, which is useful
for initial validation but is not the final event-triggered setup.

## Live sequence

1. Open the race-condition GitHub issue.
2. Start a repo-backed OpenHands conversation using
   `prompts/fix-adoption-race.md` and include the issue URL.
3. In the conversation, call out the preflight lines:
   `host_socket_mounted=no` and `nested_container=passed`.
4. Show the baseline result: two HTTP 201 responses and two stored adoptions.
5. Let the agent implement the database transaction and invariant.
6. Show the rebuilt Compose stack and the passing integration result:
   one HTTP 201, one HTTP 409, one stored adoption.
7. Show the Playwright result and adoption screenshot.
8. Finish on the draft PR. The human still owns review and merge.

## Evidence checklist

- `artifacts/qa/sysbox-preflight.txt`
- `artifacts/qa/race-reproduction.txt`
- `artifacts/qa/compose-ps.txt`
- `artifacts/qa/integration-tests.txt`
- `artifacts/qa/browser-tests.txt`
- `artifacts/qa/adoption-success.png`
- draft PR link and OpenHands conversation link

Generated evidence stays out of Git. Summarize it in the PR body or attach it
through the demo environment.

## Troubleshooting

- If `docker info` fails, inspect `/tmp/petstore-dockerd.log` inside the
  sandbox. Do not work around this by mounting the host socket.
- Give the preflight terminal action at least 600 seconds on a cold sandbox;
  the nested `hello-world` pull is platform verification, not agent reasoning.
- If the first build is slow, distinguish image pull time from agent reasoning
  time. Subsequent warm-sandbox runs should be faster.
- If PostgreSQL has stale state, rerun with `docker compose down -v`.
- If browser verification is the only failure, inspect Compose health and the
  Playwright trace under `artifacts/qa/playwright/`.
