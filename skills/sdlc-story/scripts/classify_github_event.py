#!/usr/bin/env python3
"""Classify a label-only GitHub webhook fixture for the demo."""

from __future__ import annotations

import json
import sys
from pathlib import Path


AUTOMATION_LABELS = {
    "openhands-build",
    "openhands-review",
    "openhands-qa",
}


def summarize(payload: dict) -> dict:
    event_name = payload.get("_event_name")
    label = (payload.get("label") or {}).get("name", "")
    repo = payload.get("repository") or {}
    if event_name == "issues":
        issue = payload.get("issue") or {}
        return {
            "event_type": f"issues.{payload.get('action', 'unknown')}",
            "repository": repo.get("full_name"),
            "trigger": label if label in AUTOMATION_LABELS else "unknown",
            "issue_number": issue.get("number"),
            "issue_title": issue.get("title"),
        }
    if event_name == "pull_request":
        pr = payload.get("pull_request") or {}
        return {
            "event_type": f"pull_request.{payload.get('action', 'unknown')}",
            "repository": repo.get("full_name"),
            "trigger": label if label in AUTOMATION_LABELS else "unknown",
            "pull_request_number": pr.get("number"),
            "pull_request_title": pr.get("title"),
        }
    raise SystemExit(f"Unsupported _event_name: {event_name}")


def main() -> int:
    payload = json.load(sys.stdin)
    print(json.dumps(summarize(payload), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
