#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"
source scripts/validation/ensure_nested_docker.sh

mkdir -p artifacts/qa
evidence="artifacts/qa/sysbox-preflight.txt"
{
  echo "nested_docker=ready"
  echo "host_socket_mounted=$(awk '$2 == "/var/run/docker.sock" {found=1} END {print found ? "yes" : "no"}' /proc/mounts)"
  docker version --format 'docker_server={{.Server.Version}}'
  docker compose version --short | sed 's/^/compose=/'
  docker info --format 'storage_driver={{.Driver}} cgroup_driver={{.CgroupDriver}}'
  docker run --rm hello-world >/dev/null
  echo "nested_container=passed"
} | tee "$evidence"

if grep -q 'host_socket_mounted=yes' "$evidence"; then
  echo "ERROR: host Docker socket is mounted; this is not the Sysbox isolation story." >&2
  exit 1
fi
