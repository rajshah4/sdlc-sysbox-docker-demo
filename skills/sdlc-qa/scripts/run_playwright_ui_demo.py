#!/usr/bin/env python3
"""Run the checked-in Playwright UI demo when browser tooling is available."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Petstore Playwright UI demo.")
    parser.add_argument("--url", default="http://localhost:4173")
    parser.add_argument("--artifact-dir", default="/tmp/sdlc-petstore-playwright/catalog-search")
    parser.add_argument("--script", default="app/web/tests/catalog-search.playwright.mjs")
    parser.add_argument(
        "--node-modules",
        help="Optional node_modules directory to prepend to NODE_PATH when Playwright is installed outside this repo.",
    )
    args = parser.parse_args()

    if not shutil.which("node"):
        print("Node.js is required for Playwright UI evidence but was not found.", file=sys.stderr)
        return 2

    script_path = Path(args.script)
    if not script_path.exists():
        print(f"Playwright script not found: {script_path}", file=sys.stderr)
        return 2

    env = os.environ.copy()
    if args.node_modules:
        node_modules = str(Path(args.node_modules).expanduser().resolve())
        env["NODE_PATH"] = node_modules + os.pathsep + env.get("NODE_PATH", "")

    command = [
        "node",
        str(script_path),
        "--url",
        args.url,
        "--artifact-dir",
        args.artifact_dir,
    ]
    completed = subprocess.run(command, env=env, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
