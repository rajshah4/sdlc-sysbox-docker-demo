# SDLC Automation Demo for GitHub

This repository is a GitHub-native version of the SDLC Automation Demo. It shows how OpenHands can turn sparse GitHub issues and PR signals into controlled SDLC work cells while humans keep final authority through GitHub issues, labels, comments, reviews, checks, and merge decisions.

The demo uses a small Petstore application so the automation output is concrete:

- `openhands-build`: issue label -> clarified spec -> implementation branch -> PR
- `openhands-review`: PR label -> code review comment
- `openhands-qa`: PR label -> generated QA/test evidence, including UI checks when relevant
- `openhands-incident`: incident issue label -> GCP log analysis -> report or small fix PR

## Why This Repo Exists

The Azure DevOps demo remains preserved in its original repository. This repo is intentionally GitHub-first: GitHub issues, PRs, labels, comments, and OpenHands event automations are the demo boundary.

## Fast Local Validation

```bash
python3 -m pytest -q
python3 scripts/preflight_github_demo.py --offline
python3 scripts/simulate_github_event.py --fixture tests/fixtures/github_issue_labeled_build.json
```

## Repo Map

| Folder | Purpose |
| --- | --- |
| `app/` | Small Petstore app, static UI, Cloud Run surface, and app tests. |
| `automations/` | Four OpenHands prompt-preset automations registered in Rajistics. |
| `skills/` | Four repo-local OpenHands skills with scripts and references. |
| `scripts/` | Deterministic setup, registration, preflight, QA, and SRE helpers. |
| `docs/` | Customer-facing setup, walkthrough, and validation notes. |
| `.github/` | Issue/PR templates and label definitions; the live demo uses OpenHands labels, not GitHub Actions. |

## Register OpenHands Automations

OpenHands Automations should be registered with the prompt preset API. The checked-in package specs live under `automations/github/`.

Dry-run the registration payloads:

```bash
python3 scripts/register_github_automations.py --dry-run
```

Apply registration when `OPENHANDS_HOST_GITHUB`, `OPENHANDS_API_KEY_GITHUB`, `GITHUB_DEMO_REPOSITORY`, and `GITHUB_DEMO_REPO_URL` are set:

```bash
python3 scripts/register_github_automations.py --apply
```

No secrets belong in this repo. Store OpenHands, GitHub, Slack, and GCP credentials in the OpenHands secret store or a local `.env` excluded by `.gitignore`.

## Demo Docs

- [GitHub demo walkthrough](docs/github-demo-walkthrough.md)
- [Setup checklist](docs/setup-checklist.md)
- [Work log](docs/work-log.md)
- [Tested flow and validation notes](docs/tested-demo-flow.md)
