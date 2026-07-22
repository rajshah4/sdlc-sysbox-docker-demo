# Tested Environment

Live validation date: 2026-07-22

## OpenHands Enterprise deployment

- App: `https://app.replicated.rajistics.com`
- Enterprise server image: `cloud-1.46.2`
- Kubernetes runtime class: `sysbox-runc`
- Runtime API setting: `RUNTIME_CLASS=sysbox-runc`
- Sandbox memory limit: 2048 MiB
- Sandbox dead time: 86400 seconds

## Nested runtime observed in the agent sandbox

- Docker server: `29.6.1`
- Docker Compose: `5.3.1`
- Storage driver: `overlayfs`
- Cgroup driver: `cgroupfs`
- Host Docker socket mounted: `no`
- Nested `hello-world` container: passed

## Live demo result

- Baseline concurrency result: HTTP statuses `[201, 201]`, two stored adoptions
- Fixed concurrency suite: 2 tests passed
- Browser suite: 1 Playwright test passed
- Draft PR: `https://github.com/rajshah4/sdlc-sysbox-docker-demo/pull/2`
- OpenHands conversation:
  `https://app.replicated.rajistics.com/conversations/48c0298788c54c488feb53fa9d8c8421`

## Guidance revisions

- Official `openhands-extensions` revision reviewed: `ce324178a5a1b0eccf054fa37d1c9dd030644f03`
- Previously recorded local revision: `9b2dd52e1fbe416536618e8f965d9b75a14be72c`

The official Docker skill recommends starting `dockerd` in the background. In
the Enterprise agent terminal, the tested script uses `sudo -b dockerd` so the
daemon is detached from a single tool action and survives action completion or
timeout. Cold image pulls receive a 600-second terminal window.

## Known setup gap

The new repository was not yet included in the OpenHands GitHub App
installation during the first repo-backed start attempt. Live validation used
an unbound Sysbox conversation that cloned the public repo and used the stored
`GITHUB_TOKEN` for its branch and draft PR. Add this repo to the GitHub App
installation before registering the event-triggered automation packages.
