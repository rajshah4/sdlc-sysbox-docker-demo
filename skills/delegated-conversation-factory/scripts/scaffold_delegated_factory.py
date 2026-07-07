#!/usr/bin/env python3
"""Scaffold a delegated conversation workflow in a target repository."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_ROOT.parents[1]


def write_if_missing(path: Path, text: str, *, force: bool) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def canvas_supervisor_prompt(name: str) -> str:
    return f"""# {name} Supervisor

You are the parent Agent Canvas conversation for this delegated workflow.

The human starts only this parent conversation. Orchestrate child conversations,
collect their artifacts, apply gate logic, and write one lifecycle report. Do
not perform the full lifecycle silently inside the parent conversation.

## Inputs

- Run id: `{{{{run_id}}}}`
- Repository: `{{{{repo_slug}}}}`
- Local repository path: `{{{{repo_path}}}}`
- Request title: `{{{{request_title}}}}`
- Request body: `{{{{request_body}}}}`

## Operating Rules

1. Keep humans in control of scope, credentials, review, merge, deployment, and
   production changes.
2. Give each child a self-contained prompt.
3. Record every child id, UI URL, final response, and artifact under
   `factory_runs/{{{{run_id}}}}/`.
4. Stop or mark `needs-human` when a child reports unsafe scope, missing
   credentials, failed validation, or unresolved product/security questions.

## Final Report

Write `factory_runs/{{{{run_id}}}}/lifecycle-report.md` with the child table,
artifact links, gate decisions, and exact next human action.
"""


def canvas_workcell_prompt(name: str) -> str:
    title = name.replace("-", " ").title()
    return f"""# {title} Work Cell

You are a delegated Agent Canvas child conversation.

## Inputs

- Run id: `{{{{run_id}}}}`
- Repository: `{{{{repo_slug}}}}`
- Local repository path: `{{{{repo_path}}}}`
- Request title: `{{{{request_title}}}}`
- Request body: `{{{{request_body}}}}`

## What You Do

Use `{{{{repo_path}}}}` as the only working tree. Do the bounded work for this
cell, prefer deterministic scripts and repo-local skills, and write a durable
artifact for the supervisor.

## Human Control

Do not merge, approve your own work, bypass branch protection, mutate
production, or reveal secrets.

## Output Contract

Write `factory_runs/{{{{run_id}}}}/{name}.md`.

Final response format:

```text
status: done | needs-human | failed
artifact: factory_runs/{{{{run_id}}}}/{name}.md
summary: <five or fewer bullets>
next_gate: <next-cell-or-stop>
```
"""


def replicated_supervisor_prompt(name: str) -> str:
    return f"""# {name} Replicated Supervisor

You are the parent OpenHands conversation for this delegated workflow.

The event-triggered automation starts only this parent conversation. Stay alive,
run the Replicated orchestrator, create bounded child conversations, wait for
their final responses, apply gate logic, and write one lifecycle report. Do not
do the whole lifecycle silently inside the parent.

## Inputs To Adapt

- Event source and ticket parser
- Repository slug and Git ref
- Work-cell order
- Source-system comment or report destination

## Operating Rules

1. Keep humans in control of scope, credentials, review, merge, deployment, and
   production changes.
2. Give each child a self-contained prompt.
3. Record every child id, UI URL, final response, and gate decision under
   `factory_runs/<run-id>/`.
4. Stop or mark `needs-human` when a child reports unsafe scope, missing
   credentials, failed validation, or unresolved product/security questions.

Run the orchestrator from the repository root after replacing the placeholders:

```bash
python3 scripts/run_replicated_factory.py \\
  --base-url <OPENHANDS_BASE_URL> \\
  --repo-slug <owner/repo> \\
  --branch <git-ref> \\
  --issue-key <ticket-key> \\
  --cell-timeout-seconds 1200
```
"""


def replicated_workcell_prompt(name: str) -> str:
    title = name.replace("-", " ").title()
    return f"""# {title} Work Cell

You are a delegated OpenHands child conversation.

## Inputs

- Run id: `{{{{run_id}}}}`
- Repository: `{{{{repo_slug}}}}`
- Ticket or request: `{{{{issue_key}}}}`
- Request title: `{{{{request_title}}}}`
- Request body: `{{{{request_body}}}}`
- Parent artifact directory: `{{{{parent_artifact_dir}}}}`
- Prior child summary:

```text
{{{{prior_summary}}}}
```

## What You Do

Use the selected repository workspace for this bounded work cell. Prefer
repo-local skills and deterministic scripts before broad exploration.

## Human Control

Do not merge, approve your own work, bypass branch protection, mutate
production, or reveal secrets.

## Output Contract

Child conversations run in separate sandboxes. The parent captures your final
response as `{{{{parent_final_artifact}}}}`. You may also write
`{{{{artifact_path}}}}` inside your child workspace, but that file is only
visible to the parent if you commit or push it. Put the required evidence in
your final response.

Final response format:

```text
status: done | findings | needs-human | failed
artifact: {{{{parent_final_artifact}}}}
summary: <five or fewer bullets>
next_gate: <next-cell-or-stop>
```
"""


def build_blueprint(name: str, cells: list[str], runtime: str) -> dict[str, object]:
    if runtime == "replicated":
        package = name
        prompt_prefix = f"automations/{package}"
        artifact_suffix = ".final.md"
    else:
        prompt_prefix = "agent-canvas/prompts"
        artifact_suffix = ".md"
    return {
        "name": name,
        "runtime": runtime,
        "run_directory": "factory_runs/{{run_id}}",
        "supervisor": {
            "prompt": f"{prompt_prefix}/prompt.md" if runtime == "replicated" else "agent-canvas/prompts/supervisor.md",
            "report": "factory_runs/{{run_id}}/lifecycle-report.md",
        },
        "cells": [
            {
                "name": cell,
                "prompt": f"{prompt_prefix}/workcells/{cell}.md",
                "artifact": f"factory_runs/{{{{run_id}}}}/{cell}{artifact_suffix}",
                "continue_on": ["done"],
                "next": cells[index + 1 : index + 2],
            }
            for index, cell in enumerate(cells)
        ],
        "human_gates": ["scope", "credentials", "review", "merge", "deployment"],
    }


def automation_spec(name: str) -> str:
    spec = {
        "preset": "prompt",
        "name": name.replace("-", " ").title(),
        "prompt_file": "prompt.md",
        "trigger": {
            "type": "event",
            "source": "${WEBHOOK_SOURCE}",
            "on": "${WEBHOOK_EVENT}",
            "filter": "${WEBHOOK_FILTER}",
        },
        "repos": [
            {
                "url": "${GITHUB_DEMO_REPO_URL}",
                "provider": "github",
                "ref": "${GITHUB_DEMO_REF}",
            }
        ],
        "timeout": 3600,
        "model": "${OPENHANDS_LLM_PROFILE}",
    }
    return json.dumps(spec, indent=2) + "\n"


def copied_runtime_scripts(package: str) -> dict[Path, str]:
    files: dict[Path, str] = {}
    replacements = {
        "replicated-jira-delegated-factory": package,
        "SDLC Demo - Replicated Jira Delegated Factory": package.replace("-", " ").title(),
    }
    for script_name in (
        "run_replicated_factory.py",
        "openhands_v1_delegate.py",
        "register_replicated_factory_automation.py",
    ):
        source = REPO_ROOT / "scripts" / script_name
        if not source.exists():
            continue
        text = source.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        files[Path("scripts") / script_name] = text
    return files


def scaffold_replicated(args: argparse.Namespace, target: Path, cells: list[str]) -> dict[Path, str]:
    package = args.name
    files: dict[Path, str] = {
        Path("automations") / package / "automation.prompt-preset.json": automation_spec(package),
        Path("automations") / package / "prompt.md": replicated_supervisor_prompt(args.name),
        Path("automations") / package / "factory-blueprint.json": json.dumps(
            build_blueprint(package, cells, "replicated"), indent=2
        )
        + "\n",
    }
    for cell in cells:
        files[Path("automations") / package / "workcells" / f"{cell}.md"] = replicated_workcell_prompt(cell)
    files.update(copied_runtime_scripts(package))
    return {target / path: text for path, text in files.items()}


def scaffold_canvas(args: argparse.Namespace, target: Path, cells: list[str]) -> dict[Path, str]:
    files: dict[Path, str] = {
        target / "agent-canvas" / "factory-blueprint.json": json.dumps(
            build_blueprint(args.name, cells, "agent-canvas"), indent=2
        )
        + "\n",
        target / "agent-canvas" / "prompts" / "supervisor.md": canvas_supervisor_prompt(args.name),
    }
    for cell in cells:
        files[target / "agent-canvas" / "prompts" / "workcells" / f"{cell}.md"] = canvas_workcell_prompt(cell)
    return files


def scaffold(args: argparse.Namespace) -> int:
    target = args.target.resolve()
    cells = args.cells or ["plan", "build", "review", "qa"]
    created: list[str] = []
    skipped: list[str] = []

    if args.runtime == "replicated":
        files = scaffold_replicated(args, target, cells)
    else:
        files = scaffold_canvas(args, target, cells)

    for path, text in files.items():
        if write_if_missing(path, text, force=args.force):
            created.append(str(path))
        else:
            skipped.append(str(path))

    print(json.dumps({"created": created, "skipped": skipped}, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True, help="target repository")
    parser.add_argument("--name", default="delegated-sdlc-factory", help="workflow name")
    parser.add_argument(
        "--runtime",
        choices=("replicated", "agent-canvas"),
        default="replicated",
        help="workflow runtime to scaffold",
    )
    parser.add_argument("--cells", nargs="+", help="ordered work-cell names")
    parser.add_argument("--force", action="store_true", help="overwrite existing scaffold files")
    return parser


def main() -> int:
    return scaffold(build_parser().parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
