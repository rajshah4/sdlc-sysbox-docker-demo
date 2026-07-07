#!/usr/bin/env python3
"""List recent OpenHands automation runs without printing secrets."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen


def load_env_file(path: Path) -> None:
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key or not key.replace("_", "").isalnum():
            continue
        os.environ.setdefault(key, value.strip().strip("'").strip('"'))


def get_runs(host: str, api_key: str, automation_id: str, limit: int) -> dict[str, Any]:
    endpoint = host.rstrip("/") + f"/api/automation/v1/{automation_id}/runs?limit={limit}"
    request = Request(
        endpoint,
        headers={"Authorization": f"Bearer {api_key}"},
        method="GET",
    )
    with urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def summarize(payload: dict[str, Any]) -> list[dict[str, Any]]:
    runs = payload.get("runs") or payload.get("data") or payload.get("items") or []
    summary = []
    for run in runs:
        summary.append(
            {
                "id": run.get("id") or run.get("run_id"),
                "status": run.get("status"),
                "created_at": run.get("created_at"),
                "started_at": run.get("started_at"),
                "completed_at": run.get("completed_at"),
            }
        )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", type=Path, help="load KEY=value entries without printing values")
    parser.add_argument("--automation-id", required=True)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    if args.env_file:
        load_env_file(args.env_file)

    host = (
        os.getenv("OPENHANDS_HOST_GITHUB")
        or os.getenv("OPENHANDS_HOST_RAJISTICS")
        or os.getenv("OPENHANDS_HOST")
        or "https://app.replicated.rajistics.com"
    )
    api_key = (
        os.getenv("OPENHANDS_API_KEY_ORG")
        or os.getenv("OPENHANDS_API_KEY_GITHUB")
        or os.getenv("OPENHANDS_API_KEY_RAJISTICS")
        or os.getenv("OPENHANDS_API_KEY")
    )
    if not api_key:
        raise SystemExit("OPENHANDS_API_KEY_ORG, OPENHANDS_API_KEY_GITHUB, OPENHANDS_API_KEY_RAJISTICS, or OPENHANDS_API_KEY is required")

    print(json.dumps(summarize(get_runs(host, api_key, args.automation_id, args.limit)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
