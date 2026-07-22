#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"
source scripts/validation/ensure_nested_docker.sh

cleanup() {
  docker compose down -v --remove-orphans >/dev/null 2>&1 || true
}
trap cleanup EXIT

docker compose down -v --remove-orphans >/dev/null 2>&1 || true
docker compose up -d --build --wait postgres redis api web
docker compose --profile test build integration-tests
docker compose --profile test run --rm integration-tests python tests/integration/reproduce_race.py \
  | tee artifacts/qa/race-reproduction.txt
docker compose ps | tee artifacts/qa/compose-ps.txt
