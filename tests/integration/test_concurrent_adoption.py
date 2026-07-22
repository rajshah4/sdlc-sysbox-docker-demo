"""Black-box checks that require the complete Compose topology."""

from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor

import httpx


BASE_URL = os.getenv("PETSTORE_API_URL", "http://localhost:8000").rstrip("/")


def post(path: str, payload: dict[str, str] | None = None) -> httpx.Response:
    return httpx.post(f"{BASE_URL}{path}", json=payload, timeout=10)


def test_only_one_concurrent_adoption_is_accepted() -> None:
    reset = post("/api/demo/reset")
    assert reset.status_code == 200

    payloads = [
        {"pet_id": "pet-100", "adopter_email": "alex@example.com"},
        {"pet_id": "pet-100", "adopter_email": "blair@example.com"},
    ]
    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(lambda payload: post("/api/adoptions", payload), payloads))

    assert sorted(response.status_code for response in responses) == [201, 409]
    count = httpx.get(f"{BASE_URL}/api/demo/adoptions/pet-100", timeout=10).json()["count"]
    assert count == 1


def test_health_proves_postgres_and_redis_are_reachable() -> None:
    health = httpx.get(f"{BASE_URL}/health", timeout=10)
    assert health.status_code == 200
    assert health.json() == {"status": "ok", "postgres": "ok", "redis": "ok"}
