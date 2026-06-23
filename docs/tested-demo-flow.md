# Tested Demo Flow

Last updated: 2026-06-23 UTC.

## Local Validation

The intended validation sequence is:

```bash
python3 -m pytest -q
python3 scripts/preflight_github_demo.py --offline
python3 scripts/simulate_github_event.py --fixture fixtures/github_issue_comment_build.json
python3 skills/sdlc-story/scripts/validate_open_spec.py <path-to-open-spec.md>
```

## Safe GitHub Validation

Use a disposable private GitHub repo for the first live test:

1. Push this repo.
2. Install only the self-hosted Rajistics OpenHands GitHub App.
3. Create labels with `python3 scripts/create_github_labels.py --repo OWNER/REPO --apply`.
4. Register automations with `python3 scripts/register_github_automations.py --apply`.
5. Create a fresh issue and comment `openhands-build`.
6. Confirm an OpenHands conversation appears and a result comment or PR is posted.

Cloud-mutating incident remediation is not required for the safe test. Use dry-run or report-only mode unless `scripts/petstore_gcp_observe.py` reports `diagnosis.safe_to_remediate=true`.

## Latest Safe Test

Repository:

- `https://github.com/rajshah4/sdlc-automation-github-demo`

Issue:

- `https://github.com/rajshah4/sdlc-automation-github-demo/issues/1`

Validated:

- Labels were created from `config/github-labels.json`.
- Issue #1 was labeled with `type:story`, `openhands-build`, and `openhands:ready`.
- The deterministic GitHub Actions workflow ran successfully for work-cell label events.
- The test exposed a duplicate-trigger risk from status labels; filters were tightened so status labels no longer trigger work cells.
- After the guard fix, an `issue_comment` retest using `openhands-build` produced one successful deterministic workflow run.
- After OpenHands automation registration, a second `openhands-build` issue comment produced another successful GitHub Actions run, but the OpenHands build automation still showed no runs after the event.

Evidence:

- Successful run `27996217965`: `https://github.com/rajshah4/sdlc-automation-github-demo/actions/runs/27996217965`
- Successful run `27996217942`: `https://github.com/rajshah4/sdlc-automation-github-demo/actions/runs/27996217942`
- Successful comment-trigger retest run `27996297265`: `https://github.com/rajshah4/sdlc-automation-github-demo/actions/runs/27996297265`
- Comment-trigger acknowledgement: `https://github.com/rajshah4/sdlc-automation-github-demo/issues/1#issuecomment-4774842490`
- Post-registration GitHub trigger run `27996464141`: `https://github.com/rajshah4/sdlc-automation-github-demo/actions/runs/27996464141`
- Post-richer-skill registration GitHub trigger run `27997482066`: `https://github.com/rajshah4/sdlc-automation-github-demo/actions/runs/27997482066`
- Post-richer-skill trigger comment: `https://github.com/rajshah4/sdlc-automation-github-demo/issues/1#issuecomment-4774994463`
- Post-richer-skill GitHub Actions acknowledgement: `https://github.com/rajshah4/sdlc-automation-github-demo/issues/1#issuecomment-4774995085`
- Rajistics-key trigger comment: `https://github.com/rajshah4/sdlc-automation-github-demo/issues/1#issuecomment-4775032297`
- Rajistics-key GitHub Actions run `27997770664`: `https://github.com/rajshah4/sdlc-automation-github-demo/actions/runs/27997770664`
- Rajistics OpenHands automation run `f84671ac-33b7-43d8-a0e4-3532fb180263`: completed at `2026-06-23T02:29:45Z`
- OpenHands result comment: `https://github.com/rajshah4/sdlc-automation-github-demo/issues/1#issuecomment-4775062401`
- Created PR #2: `https://github.com/rajshah4/sdlc-automation-github-demo/pull/2`
- A skipped non-matching event confirmed the workflow boundary also skips events outside the trigger guard.

Not tested live:

- GCP incident remediation was not run; cloud mutation remains report-only unless the safe-remediation script reports `safe_to_remediate=true`.
- SRE, QA, and review automations were registered but not live-triggered in this pass.

## Registered OpenHands Automations

Prompt-preset automations were registered through `scripts/register_github_automations.py --apply` using the configured OpenHands API credentials:

| Work cell | Automation ID |
| --- | --- |
| `openhands-build` | `0ce7add1-fbba-40ef-bc0d-bef77f1bd108` |
| `openhands-incident` | `31c15181-2c7a-446e-8156-232808e6d1fc` |
| `openhands-qa` | `d6f6e6f9-202c-45cc-afcc-69cf5379fb16` |
| `openhands-review` | `a8605df3-d80a-487c-bf11-1932f81a2c0c` |

Run-list check:

```bash
python3 scripts/list_openhands_automation_runs.py \
  --env-file /path/to/local/.env \
  --automation-id 0ce7add1-fbba-40ef-bc0d-bef77f1bd108 \
  --limit 5
```

Result after the post-registration issue comment: `[]`.

Result after the post-richer-skill registration issue comment on 2026-06-23 with the generic API key path: `[]`.

Result after re-registering with the Rajistics Replicated API key and posting a fresh issue comment: build run `f84671ac-33b7-43d8-a0e4-3532fb180263` completed and opened PR #2.

The earlier registrations that referenced the hidden skill path were disabled after the skills moved to the first-class `skills/` directory. The second set of lightweight prompt registrations was disabled after the richer four-skill prompts were added. The third set used the generic API key path and was disabled after confirming the UI expectation was the Rajistics Replicated automations page.

## Skill Baseline Validation

The current repo-local skills are designed to be inspected in GitHub:

- `skills/sdlc-story` includes the open specification template, acceptance extraction, event classification, and OpenSpec validation.
- `skills/sdlc-qa` includes API/UI QA references, static UI smoke checks, and a local server harness.
- `skills/sdlc-incident` includes Cloud Run incident runbook guidance plus observation-report helpers.
- `skills/sdlc-code-review` includes risk and supply-chain review references plus a deterministic Petstore checklist.

The four OpenHands automations were re-registered with the Rajistics Replicated API key, and the Rajistics API returned all four as enabled. A safe `openhands-build` issue comment validated event delivery end to end.
