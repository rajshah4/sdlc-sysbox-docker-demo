#!/usr/bin/env bash
set -euo pipefail

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: Docker CLI is not installed in this sandbox." >&2
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "Docker daemon is not running; starting an inner daemon in the sandbox."
  if ! command -v sudo >/dev/null 2>&1; then
    echo "ERROR: sudo is required to start the nested Docker daemon." >&2
    exit 1
  fi
  # `sudo -b` detaches the daemon from the agent's individual terminal action.
  # A plain trailing `&` can be reaped when that action exits or times out.
  sudo -b dockerd > /tmp/petstore-dockerd.log 2>&1
  for _ in $(seq 1 60); do
    docker info >/dev/null 2>&1 && break
    sleep 1
  done
fi

if ! docker info >/dev/null 2>&1; then
  echo "ERROR: nested Docker daemon did not become ready." >&2
  tail -50 /tmp/petstore-dockerd.log >&2 || true
  exit 1
fi

docker compose version >/dev/null
