# Fix the concurrent adoption race and prove it with nested Docker

Work on the GitHub issue supplied with this prompt. You own the change through
a reviewable draft pull request; do not merge it.

Required workflow:

1. Read `AGENTS.md` and `docs/sysbox-demo-runbook.md`.
2. Run `scripts/validation/sysbox_preflight.sh`. Record that nested Docker is
   usable and that the host Docker socket is not mounted.
3. Run `scripts/validation/reproduce_adoption_race.sh` before editing. Preserve
   the command result in the working tree as pre-fix evidence.
4. Inspect the API and database schema. Fix the concurrency bug at the database
   transaction boundary. Add a durable database invariant so correctness does
   not depend only on application timing.
5. Keep API behavior explicit: one request succeeds with HTTP 201 and the
   concurrent loser receives HTTP 409.
6. Run `scripts/validation/verify_stack.sh`. This must build images, start the
   Compose topology, pass the concurrent integration tests, and pass the
   Playwright browser flow.
7. Create a focused branch, commit the code and maintainable tests, push it,
   and open a draft PR linked to the issue. Do not commit generated QA logs or
   secrets.

The PR body must include:

- root cause and transaction strategy;
- database invariant added;
- nested Docker and no-host-socket evidence;
- Compose services started;
- integration and browser results;
- remaining risks and the human merge gate.

Do not substitute unit tests for the required containerized verification. Do
not mount `/var/run/docker.sock`.
