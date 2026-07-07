# Agent Canvas SDLC Automation Recipe

This folder contains the Agent Canvas SDLC automation recipe. It is
structured as a reusable software-factory recipe: one parent conversation acts
as the orchestrator, and delegated child conversations perform bounded SDLC
workcells.

The Canvas-specific prompts and executable helpers live together under this
folder so the recipe can be reviewed, copied, or adapted as a unit. The matching
root-level `scripts/` entries are compatibility wrappers for existing commands.

The existing GitHub automation demo is event-driven: a human adds GitHub labels,
and each label creates a separate OpenHands automation run. This Canvas version
does not use labels as the trigger mechanism. It uses one visible parent
conversation as the workflow spine. The parent conversation delegates each
lifecycle cell to child Agent Canvas conversations, then gathers their outputs
into one lifecycle report.

For the full customer-facing walkthrough, reproduction steps, and adaptation
points, see `../docs/agent-canvas-dark-factory-demo.md`.

## Conversation Topology

```mermaid
flowchart TD
    A["Parent conversation: factory supervisor"] --> B["Child: story to PR"]
    B --> C["Child: code review"]
    C --> D["Child: QA"]
    B --> A
    C --> A
    D --> A
```

## Files

| Path | Purpose |
| --- | --- |
| `prompts/supervisor.md` | Initial prompt for the one parent conversation. |
| `prompts/workcells/*.md` | Self-contained prompts for delegated child conversations. |
| `scripts/start_agent_canvas_factory.py` | Starts the parent conversation. |
| `scripts/run_agent_canvas_factory.py` | Deterministic parent-side orchestrator that starts and monitors child conversations. |
| `scripts/agent_canvas_delegate.py` | Creates, waits for, and inspects child conversations through the local Agent Canvas API. |
| `scripts/run_petstore_playwright_qa.py` | Runs the Petstore Playwright evidence flow on an available local port. |
| `../docs/agent-canvas-dark-factory-demo.md` | Customer-facing walkthrough, reproduction recipe, and adaptation guide. |

## Quick Start

Start local Agent Canvas first. The helper defaults to `http://localhost:8000`
and also checks common backend ports.

From the repository root:

```bash
python3 agent-canvas/scripts/start_agent_canvas_factory.py \
  --repo . \
  --repo-slug rajshah4/sdlc-automation-github-demo \
  --issue-number 88
```

Use a repository path that the local Agent Canvas runtime can read. On macOS,
review the dedicated note below before running from `Documents`, `Desktop`,
`Downloads`, or a cloud-synced folder.

To use a different Agent Canvas profile for the code-review child only:

```bash
python3 agent-canvas/scripts/start_agent_canvas_factory.py \
  --repo . \
  --repo-slug rajshah4/sdlc-automation-github-demo \
  --issue-number 88 \
  --code-review-profile Minimax
```

To require Playwright UI evidence from the QA workcell:

```bash
python3 agent-canvas/scripts/start_agent_canvas_factory.py \
  --repo . \
  --repo-slug rajshah4/sdlc-automation-github-demo \
  --issue-number 88 \
  --require-playwright-qa \
  --playwright-node-path /path/to/node_modules
```

The command creates one parent conversation and prints its UI URL. Open that
parent conversation. The supervisor will run `agent-canvas/scripts/run_agent_canvas_factory.py`,
which uses `agent-canvas/scripts/agent_canvas_delegate.py` inside the repo to create the
child conversations and write run artifacts under:

```text
factory_runs/<run-id>/
```

The launcher also writes `factory_runs/<run-id>/parent.conversation.json` so the
parent conversation ID and URL are explicit in the run artifacts.

For this local recipe, the external trigger is the operator or demo harness that
runs `agent-canvas/scripts/start_agent_canvas_factory.py`. In a deployed version, that same
script can be called by an automation or webhook adapter, such as a GitHub issue
event, Jira transition, ServiceNow request, or scheduled polling job. The trigger
passes story metadata into the launcher; the parent Agent Canvas conversation
remains the lifecycle orchestrator.

For a dry preview of the parent prompt:

```bash
python3 agent-canvas/scripts/start_agent_canvas_factory.py --render-only
```

## Reproducing Or Extending This Demo

This recipe was built from two parts: the repo-local SDLC demo assets and the
Agent Canvas delegation pattern. The useful pattern is that the parent
conversation stays small and supervisory, while each child conversation receives
a complete prompt, one working tree, a clear output contract, and the specific
validation it owns.

To reproduce the recipe in another repository:

1. Copy `agent-canvas/` into the target repo. Copy the root-level compatibility
   wrappers from `scripts/` only if you want old commands such as
   `python3 scripts/start_agent_canvas_factory.py` to keep working.
2. Update `prompts/supervisor.md` with the workcell order, story metadata, and
   the exact orchestrator command for the target repo.
3. Update each prompt under `prompts/workcells/` so it is self-contained. A
   delegated conversation does not inherit hidden context from the parent
   conversation.
4. Adapt `agent-canvas/scripts/run_agent_canvas_factory.py` for the workcells
   you want. The default sequence is `story-to-pr`, `code-review`, and `qa`.
5. Adapt the QA command and evidence expectations for the target application.
   For UI-visible changes, require browser evidence such as Playwright reports,
   screenshots, traces, videos, or an equivalent artifact.
6. Point the launcher at the target repo, issue source, and GitHub repo slug.
   The current demo starts from a GitHub issue, but the launcher can receive
   equivalent story metadata from Jira, ServiceNow, a webhook, or a scheduled
   polling automation.
7. Run a dry prompt preview with `--render-only`, then run one full workflow and
   inspect `factory_runs/<run-id>/`, the child conversation links, and the PR
   body before presenting the recipe.

We used an Agent Canvas environment skill as the implementation guide for local
delegation. The important mechanics from that skill are:

- Create delegated conversations through the local Agent Canvas API instead of
  browser-clicking the UI.
- Fetch Agent Canvas settings with encrypted secrets and send them back with
  `secrets_encrypted: true`; do not print API keys or write settings files.
- Include the terminal, file editor, browser, task tracker, and Canvas UI tools
  when the child needs to work inside the repo.
- Use a self-contained prompt for every child conversation.
- Attach the repo as a `LocalWorkspace` and use `worktree: false` when the repo
  checkout is already isolated.

Hints that made this demo more reliable:

- Keep labels as optional metadata only. The Canvas parent conversation is the
  workflow control plane.
- Treat the external trigger as an adapter. It should pass story inputs into
  `agent-canvas/scripts/start_agent_canvas_factory.py`; it should not become the
  lifecycle orchestrator.
- Snapshot prompts and helper scripts into `factory_runs/<run-id>/` before
  creating child conversations. This keeps downstream gates working even when
  the story branch changes the checked-out tree.
- Let downstream gates update only their own PR sections. That keeps the PR
  useful for reviewers without turning it into a scripted demo transcript.
- Use a separate Agent Canvas profile for review when you want model diversity
  without changing the story or QA delegates.
- Make Playwright evidence explicit for UI stress tests. If browser execution is
  unavailable, the QA delegate should report `needs-human` instead of silently
  substituting weaker evidence.

## For Mac Users

macOS can block local Agent Canvas conversations from reading repositories in
privacy-protected folders. If the parent reports `Operation not permitted`, use
a checkout outside `Documents`, `Desktop`, `Downloads`, and cloud-synced folders,
or grant Full Disk Access to the terminal or IDE process that launches Agent
Canvas and restart that app before rerunning.

## Safety Boundaries

- The supervisor starts the lifecycle; children do the bounded work.
- Child prompts are self-contained because delegated conversations do not
  inherit hidden parent context.
- GitHub labels may be referenced as historical context from the old demo, but
  they are not used to start, gate, or sequence this Canvas run.
- The default live lifecycle is `story-to-pr`, `code-review`, then `qa`.
- `--require-playwright-qa` makes Playwright evidence mandatory for the QA child.
- The helper forwards encrypted Agent Canvas settings and sets
  `secrets_encrypted: true`; it does not print API keys or LLM secrets.
- The prompts preserve human gates for scope, PR review, merge, deployment,
  production remediation, and secret access.
- The existing GitHub-label automation packages remain intact.

## What This Does Not Change

This folder is additive. It does not modify or replace the existing
`automations/github/` label-triggered demo, and it does not add
environment-specific Jira automation. Trigger adapters can be added separately
after the Canvas recipe is stable.
