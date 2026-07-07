# Scripts

Scripts are grouped by the demo path they support. Top-level scripts with the
old names are compatibility wrappers, so existing docs and live automations can
keep calling commands such as `python3 scripts/register_github_automations.py`.

The existing step-by-step demo should continue to call repo-local skills from
its automation prompts. These folders organize helper scripts; they do not move
SDLC policy out of skills or change the automation boundaries.

| Folder | Use |
| --- | --- |
| `scripts/automations/` | Register, list, disable, and label OpenHands automations. |
| `scripts/context/` | Build deterministic context-reuse reports before expensive agent work. |
| `scripts/validation/` | Run local preflight checks and fixture simulations. |
| `scripts/openhands/` | Inspect or summarize OpenHands conversations. |
| `scripts/sidekick/` | Legacy sidekick launch helpers for the visible multi-conversation Jira demo. |
| `agent-canvas/scripts/` | Parent-child Agent Canvas factory launcher, orchestrator, delegate helper, and QA helpers. |

## Common Commands

Register step-by-step GitHub automations:

```bash
python3 scripts/register_github_automations.py --dry-run
python3 scripts/register_github_automations.py --apply
```

Register Jira automations:

```bash
python3 scripts/register_jira_automations.py --dry-run
python3 scripts/register_jira_automations.py --apply
```

Validate the local demo shape:

```bash
python3 scripts/preflight_github_demo.py --offline
python3 scripts/simulate_github_event.py --fixture tests/fixtures/github_issue_labeled_build.json
```

Run the Agent Canvas parent-child factory:

```bash
python3 agent-canvas/scripts/start_agent_canvas_factory.py --help
```

## Compatibility Policy

Prefer the foldered paths for new docs and examples. Keep the top-level wrapper
paths when updating existing prompts or live automation instructions, unless you
are deliberately migrating that automation.
