#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"
source scripts/validation/ensure_nested_docker.sh
mkdir -p artifacts/qa

cleanup() {
  docker compose logs --no-color > artifacts/qa/compose.log 2>&1 || true
  docker compose down -v --remove-orphans >/dev/null 2>&1 || true
}
trap cleanup EXIT

docker compose down -v --remove-orphans >/dev/null 2>&1 || true
docker compose --profile test build
docker compose up -d --wait postgres redis api web
docker compose ps | tee artifacts/qa/compose-ps.txt
docker compose --profile test run --rm integration-tests \
  | tee artifacts/qa/integration-tests.txt
docker compose --profile test run --rm browser-tests \
  | tee artifacts/qa/browser-tests.txt
echo "STACK VERIFICATION PASSED"
