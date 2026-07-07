# Build a Parent-Child Automation Factory

Use this guide when you want one event to run an entire SDLC workflow through a
visible supervisor conversation.

The pattern is:

```text
event
  -> OpenHands automation or Agent Canvas launcher
    -> parent supervisor conversation
      -> child conversation: story-to-PR
      -> child conversation: code-review
      -> child conversation: QA
    -> lifecycle report
    -> Jira, GitHub, or demo summary
```

## When To Use This

Use the parent-child pattern when the team wants the whole lifecycle to run from
one request. Use the step-by-step label approach when humans need to approve or
inspect every gate before the next one starts.

The parent-child pattern still keeps human authority over scope, review, merge,
deployment, production credentials, and unsafe remediation.

## Files To Copy

| Runtime | Start here | Copy/adapt |
| --- | --- | --- |
| **Agent Canvas** | [`agent-canvas/README.md`](../agent-canvas/README.md) | `agent-canvas/prompts/supervisor.md`, `agent-canvas/prompts/workcells/*.md`, `agent-canvas/scripts/run_agent_canvas_factory.py`, `agent-canvas/scripts/agent_canvas_delegate.py` |
| **OpenHands Enterprise/Cloud** | [PR #86](https://github.com/rajshah4/sdlc-automation-github-demo/pull/86) | prompt-preset automation, parent orchestrator, child prompts, app-conversation API helper, delegated-factory skill |

The Agent Canvas version is already on `main`. The OpenHands Enterprise/Cloud
version was live-tested on the Rajistics Replicated instance and currently lives
on the PR #86 branch.

## Build Checklist

Keep the existing step-by-step demo intact. Its automations should stay as
short orchestrators that call repo-local skills; do not copy detailed skill
behavior into automation prompts just to build a delegated factory.

1. **Choose the event.**
   Examples: Jira Task created, GitHub issue label, GitHub PR label, or a
   scheduled OpenHands automation.

2. **Write the parent supervisor prompt.**
   The parent owns orchestration. It should know the source request, the child
   workcells to run, the repo-local skills each child should use, the human
   gates, and where to post the final summary.

3. **Write one child prompt per workcell.**
   Each child prompt should be self-contained. It should name the input, output
   artifact, status contract, and expected final response.

4. **Use a helper to start and wait for children.**
   Agent Canvas uses `agent_canvas_delegate.py`. OpenHands Enterprise/Cloud uses
   the app-conversation API helper from PR #86.

5. **Record a lifecycle report.**
   Save child IDs, conversation links, statuses, artifacts, and human next
   steps. This is the thing you can show customers to prove the workflow was
   orchestrated rather than hidden.

6. **Post back to the system of record.**
   Jira, GitHub, or another ticket system should receive the summary. The
   parent should not silently finish without leaving evidence where the team
   works.

## Parent Prompt Shape

```md
You are the parent supervisor for this SDLC workflow.

Input:
- source request: {{issue_or_ticket}}
- repository: {{repo}}
- branch/ref: {{branch}}

Run these child workcells:
1. story-to-PR
2. code-review
3. QA

For each child:
- start a new child conversation
- wait for its final response
- record status, conversation link, and artifact path
- stop if the child reports needs-human or a blocking failure

Finish by writing a lifecycle report and posting a summary back to {{system_of_record}}.
```

## Child Prompt Contract

Each child should end with a small parseable contract:

```text
status: pass | findings | needs-human | fail
artifact: factory_runs/<run-id>/<workcell>.md
summary: <short human-readable result>
next: <human next step or none>
```

That contract lets the parent decide whether to continue, stop, or ask for
human input.

## Minimal Orchestrator Shape

```python
entries = []

for cell in ["story-to-pr", "code-review", "qa"]:
    child = start_child_conversation(cell)
    result = wait_for_final_response(child.id)
    entries.append(result)

    if result.status in {"needs-human", "fail"}:
        break

write_lifecycle_report(entries)
post_summary(entries)
```

The real implementation adds event parsing, repository setup, Jira/GitHub API
calls, timeouts, and artifact writing, but this is the core loop.

## What Customers Replace

| Replace | Examples |
| --- | --- |
| Source event | Jira Task, Linear issue, GitHub label, cron schedule |
| Workcells | implementation, review, QA, security, docs, release notes |
| Context sources | business wiki, code repos, logs, dashboards, prior run reports |
| System of record | Jira, GitHub, GitLab, Linear, ServiceNow |
| Human gates | review approval, merge, deploy, production secret access |

Keep the control rule stable: one parent conversation coordinates bounded child
conversations, child prompts call skills for domain behavior, and humans keep
authority over irreversible decisions.
