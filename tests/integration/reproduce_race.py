"""Return success only when the intentionally vulnerable baseline race occurs."""

from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor

import httpx


base = os.getenv("PETSTORE_API_URL", "http://api:8000").rstrip("/")
httpx.post(f"{base}/api/demo/reset", timeout=10).raise_for_status()
payloads = [
    {"pet_id": "pet-100", "adopter_email": "alex@example.com"},
    {"pet_id": "pet-100", "adopter_email": "blair@example.com"},
]
with ThreadPoolExecutor(max_workers=2) as pool:
    responses = list(
        pool.map(
            lambda body: httpx.post(f"{base}/api/adoptions", json=body, timeout=10),
            payloads,
        )
    )
statuses = sorted(response.status_code for response in responses)
count = httpx.get(f"{base}/api/demo/adoptions/pet-100", timeout=10).json()["count"]
print(f"concurrent_statuses={statuses}")
print(f"stored_adoptions={count}")
if statuses == [201, 201] and count == 2:
    print("BUG REPRODUCED: two customers adopted the same last pet")
    raise SystemExit(0)
print("BUG NOT REPRODUCED: the invariant may already be protected")
raise SystemExit(1)
