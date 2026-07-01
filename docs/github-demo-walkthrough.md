# GitHub Demo Walkthrough

This is the live flow for the GitHub-native SDLC Automation Demo.

## 0. Optional Context Scout

For the memory-and-cost version of the demo, create or reuse a sparse GitHub issue and add `openhands-context` before `openhands-build`.

This triggers the OpenHands automation through the GitHub `issues.labeled` event. It runs only on issues, skips items already marked `openhands:done`, and posts a context reuse comment before any coding work begins.

OpenHands should produce a context reuse report that shows:

- `AGENTS.md` durable repo memory
- selected repo-local skills
- existing logs and QA reports
- targeted GitHub repo search results
- previous OpenHands conversations or run records
- recommended lower-cost scout and stronger coding/review model routing

Use this as the setup for the rest of the live demo: the expensive model should start after the scout has narrowed context.

If you need to run the scout again on the same issue, remove the status label that would cause the filter to skip the item, then remove and reapply `openhands-context`.

## 1. Create A Bug Issue

Create a GitHub issue with a sparse, business-language bug title such as:

```text
Customers are seeing pets that are not available
```

Use a short body, for example:

```text
Support says Nova is showing up in the available pets list even though she should not be adoptable.
Logs mention PENDING_PET_VISIBLE.
```

Add the label `openhands-build`.

OpenHands should clarify the bug inside the conversation, use repo-local docs and log evidence, find the Petstore catalog code, create a fix branch, run focused tests, and open a draft PR. The PR should document assumptions, acceptance criteria, evidence, and human review notes.

## 2. Show The Evidence Stops

In the OpenHands conversation, pause on the named waypoints:

- `Stop 1 - Ticket`: the sparse business-language bug report.
- `Stop 2 - Wiki/Docs`: the catalog availability rule, usually `docs/wiki/petstore-catalog-availability.md`.
- `Stop 3 - Logs`: the log clue, usually `docs/logs/pending-pet-visible.ndjson` with `PENDING_PET_VISIBLE`.
- `Stop 4 - Repo/Files`: the Petstore files the agent identified for the fix.
- `Stop 5 - Tests/PR`: the regression test, validation result, and draft PR link.

## 3. Automation Creates OpenSpec-Style Artifacts And PR

Show the generated OpenSpec-style change folder, usually:

```text
openspec/changes/github-issue-<number>-<slug>/
```

Call out how the sparse bug became:

- `proposal.md`
- `design.md`
- `tasks.md`
- `specs/<capability>/spec.md`
- assumptions
- non-goals
- requirements and scenarios
- human gates
- validation plan

Lineage note: this demo follows the Fission-AI/OpenSpec change-folder model. The live automation writes the artifacts directly instead of installing or invoking the OpenSpec CLI during the timed label-triggered run, which keeps the customer demo deterministic.

Then show the generated PR, including the regression test that proves pending pets stay out of the default available-pets experience.

Call out the human controls:

- PR is draft or reviewable, not auto-merged.
- Reviewers decide whether the implementation is acceptable.
- CI and branch protections still apply.
- Humans choose whether to merge.

## 4. Trigger Code Review

On the PR, add the label `openhands-review`.

OpenHands should inspect the diff, apply the repo-local `sdlc-code-review` skill, classify risk, check Petstore contracts, and post a structured code review comment. It should not claim tests passed unless it ran them or verified evidence.

## 5. Trigger QA And Test Generation

On the PR, add the label `openhands-qa`.

OpenHands should run or add focused tests, exercise the changed behavior, map results back to the OpenSpec-style change artifacts, and include UI evidence when the static web app changed.

For a concrete browser-evidence example, show:

- `docs/ui-playwright-example.md`
- PR #6, `Add adoption fee filter to Petstore UI`
- the PR QA comment with an inline GIF
- PR-branch artifact links for the screenshot, video, and report

If the remote runtime lacks Playwright or BrowserToolSet, the automation should say that and fall back to deterministic checks rather than claiming browser coverage.

## 6. Human Review And Merge

Show the normal GitHub review path:

- humans inspect OpenHands comments and code diffs
- humans resolve findings or ask follow-up questions
- humans approve and merge only when ready

## Skills To Show

- `skills/sdlc-story`: issue to OpenSpec-style change artifacts to PR.
- `skills/sdlc-qa`: automated test suite and UI evidence.
- `skills/sdlc-code-review`: OpenHands `/codereview` plus Petstore-specific risk checks.
- `skills/sdlc-context-sidekick` and `skills/sdlc-sidekick-launcher`: optional visible multi-conversation context search for Jira demos.
