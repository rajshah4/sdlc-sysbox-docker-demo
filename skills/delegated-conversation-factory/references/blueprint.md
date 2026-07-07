# Delegated Conversation Blueprint

## Purpose

Use a delegated conversation workflow when one visible supervisor should
coordinate specialized OpenHands child conversations. The same pattern can run
in OpenHands Enterprise/Cloud, OpenHands Replicated, or Agent Canvas when a team
wants reusable orchestration instead of a chain of label-triggered runs.

## Required Pieces

| Piece | Responsibility |
| --- | --- |
| Supervisor prompt | Names inputs, rules, work-cell order, gate logic, and final report requirements. |
| Orchestrator | Runs inside the parent and owns deterministic sequencing, gate checks, report writing, and system-of-record comments. |
| Delegate helper | Creates child conversations and retrieves final responses. Keep it infrastructure-only. |
| Work-cell prompts | Give each child complete context and a bounded output contract. |
| Run directory | Stores manifest, child metadata, final responses, and lifecycle report. |
| Gate model | Decides whether to continue, stop, or ask for humans. |

## Supervisor Checklist

The supervisor prompt should:

- say the human starts only the parent conversation
- forbid doing the full lifecycle inside the parent
- name the local repository path and system of record
- call the orchestrator script rather than hand-rolling API requests
- require every child conversation id and UI URL to be written to the run
  directory
- define the exact work-cell order
- define stop conditions and human gates
- require one final lifecycle report

## Artifact Layout

Use a stable run directory so the operator and future agents can inspect the
same evidence:

```text
factory_runs/<run-id>/
  manifest.md
  children.json
  <work-cell>.conversation.json
  <work-cell>.wait.json
  <work-cell>.final.md
  lifecycle-report.md
```

For OpenHands Replicated, child conversations run in separate sandboxes. A child
may write `factory_runs/<run-id>/<work-cell>.md` inside its own workspace, but
the parent will not see that file unless the child commits or pushes it. The
parent-side durable artifact is the captured final response:
`factory_runs/<run-id>/<work-cell>.final.md`.

## Gate Statuses

Prefer a small status vocabulary:

- `done` or `pass`: continue when the artifact exists and evidence is enough
- `findings`: continue only when findings are non-blocking
- `needs-human`: stop before unsafe or under-specified work
- `failed`: stop and report the failure

## Adaptation Notes

To adapt the pattern for another team, change the cells and prompts first, then
adapt the orchestrator for the app and source system. Common orchestrator edits
include ticket parsing, repo/ref defaults, branch naming, status reporting,
comment posting, and cell order. Keep the delegate helper generic: settings
transport, conversation creation, waiting, and final-response retrieval are
infrastructure, not business logic.
