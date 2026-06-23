# Work Log

## 2026-06-22

- Created a fresh GitHub-native SDLC Automation Demo repo instead of modifying the Azure DevOps demo in place.
- Copied safe Petstore app, tests, GitHub provider adapter, GCP helper scripts, and integration docs from the existing demo.
- Did not copy `.env`, `.git`, Azure automation tarballs, or secret-bearing material.
- Renamed runtime service references from the old internal service name to `sdlc-automation-petstore`.
- Added GitHub labels, issue templates, prompt-preset automation packages, setup docs, and deterministic preflight scripts.
- Added repo-local OpenHands skills under `.agents/skills/` so automation behavior is version controlled and visible in the OpenHands UI.
- Created and pushed the private GitHub repo `rajshah4/sdlc-automation-github-demo` for safe GitHub-native validation.
- Created labels from `config/github-labels.json` and opened safe test issue #1.
- Validated the GitHub label path with the deterministic `OpenHands Label Demo` workflow. Two work-cell/status label events initially ran, which exposed an important retrigger risk before OpenHands automation registration.
- Fixed the GitHub Actions and OpenHands preset filters so only the four work-cell labels (`openhands-build`, `openhands-review`, `openhands-qa`, `openhands-incident`) trigger work. Status labels such as `openhands:ready` no longer retrigger automations.
- Re-tested the issue-comment path after the guard fix; run `27996297265` completed successfully and posted a single acknowledgement comment.
- Registered the four GitHub prompt-preset OpenHands automations against the configured OpenHands instance:
  - build: `e1fdf4a7-8735-4b58-bc76-eb1ff937aa6e`
  - incident: `91134259-a0f4-41bb-adf9-b1484bd013e7`
  - QA: `33fada53-9c8f-4151-bf61-83486a947121`
  - review: `64bb781d-81f7-415e-b7f6-fa7134b477ec`
- Posted a post-registration `openhands-build` comment on issue #1. GitHub Actions run `27996464141` passed, but the OpenHands build automation run list remained empty. Next required setup is to install or refresh the self-hosted OpenHands GitHub App for this new private repo.
