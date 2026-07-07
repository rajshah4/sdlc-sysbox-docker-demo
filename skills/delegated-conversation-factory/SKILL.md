---
name: delegated-conversation-factory
description: Build or adapt parent-child delegated conversation workflows for OpenHands Replicated, Agent Canvas, SDLC automation, reusable software-factory patterns, supervisor conversations, child work cells, lifecycle reports, and prompt/blueprint scaffolding. Use when replacing label-by-label automations with one orchestrating conversation that delegates bounded child conversations, or when creating a reusable delegated workflow for another repo or team.
---

# Delegated Conversation Factory

## Overview

Use this skill to turn a sequential automation demo into a delegated
conversation workflow for OpenHands Replicated or Agent Canvas:

- one supervisor conversation acts as the visible control plane
- child conversations perform bounded work cells
- every child gets a self-contained prompt
- artifacts, final responses, gates, and links are written to a run directory
- humans keep authority over scope, review, merge, deployment, secrets, and
  production changes

## Workflow

1. Identify the work cells and gates. Keep each child narrow enough that its
   final response can be judged by the supervisor.
2. Read `references/blueprint.md` before creating or changing the parent
   prompt, orchestration script, or work-cell list.
3. Read `references/work-cell-contract.md` before creating child prompts.
4. For OpenHands Enterprise/Cloud or Replicated, start from the runnable
   Replicated template in this repo: copy/adapt
   `automations/replicated-jira-delegated-factory/`,
   `scripts/run_replicated_factory.py`,
   `scripts/openhands_v1_delegate.py`, and
   `scripts/register_replicated_factory_automation.py`.
5. For Agent Canvas, start from `agent-canvas/prompts/` and
   `agent-canvas/scripts/`.
6. Prefer the repo helpers for child creation:
   `scripts/openhands_v1_delegate.py` for OpenHands Replicated and
   `agent-canvas/scripts/agent_canvas_delegate.py` for Agent Canvas. Do not
   hand-roll settings payloads, print encrypted settings, or store API keys in
   files.
7. When bootstrapping a new repo, run
   `scripts/scaffold_delegated_factory.py --runtime replicated --target <repo> --name <factory-name>`
   from this skill folder for OpenHands Enterprise/Cloud, or pass
   `--runtime agent-canvas` for Agent Canvas. Then customize the generated
   prompts and orchestrator defaults.
6. Preserve the legacy automation path unless the user explicitly wants it
   removed. The delegated workflow can reference GitHub labels as context, but
   labels should not control sequencing.

## Design Rules

- The parent conversation orchestrates; it should not silently do all child
  work itself.
- Child prompts must include all inputs they need. Do not rely on hidden parent
  context.
- Each child must write a durable artifact and return a small machine-readable
  final response contract.
- In OpenHands Replicated, child conversations run in separate sandboxes. The
  parent can always capture final response text, but child-written files are
  only visible to the parent if the child commits or pushes them. Put gate
  evidence in the final response and treat `<cell>.final.md` as the parent-side
  artifact.
- The supervisor advances only when the previous child returns an acceptable
  status and artifact.
- Use deterministic scripts and repo-local skills before broad exploration.
- Stop or mark `needs-human` for missing credentials, unsafe production access,
  unresolved product scope, security risk, or failed validation.
- Expect to adapt the orchestrator for the app and source system: event payload
  parsing, Jira/GitHub/Linear comment posting, repo slug defaults, work-cell
  order, and any demo-specific story hints live outside the prompts.

## Resources

- `references/blueprint.md`: parent conversation, run directory, sequencing,
  artifacts, and gate model.
- `references/work-cell-contract.md`: required sections and final response
  contract for child prompts.
- `assets/factory-blueprint.json`: editable starting point for another team's
  delegated workflow.
- `scripts/scaffold_delegated_factory.py`: creates a Replicated or Agent Canvas
  skeleton in a target repo.
