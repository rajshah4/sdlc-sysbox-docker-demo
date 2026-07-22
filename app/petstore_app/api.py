"""Containerized Petstore API used by the Sysbox SDLC demo."""

from __future__ import annotations

import os
import time
from contextlib import asynccontextmanager
from pathlib import Path

import psycopg
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://petstore:petstore-demo-only@localhost:5432/petstore"
)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
RACE_DELAY_SECONDS = float(os.getenv("ADOPTION_RACE_DELAY_SECONDS", "0.35"))
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "db" / "001_schema.sql"


class AdoptionRequest(BaseModel):
    pet_id: str
    adopter_email: str


def initialize_database() -> None:
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    with psycopg.connect(DATABASE_URL, autocommit=True) as connection:
        connection.execute(schema)


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(title="Sysbox Petstore", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    with psycopg.connect(DATABASE_URL) as connection:
        connection.execute("SELECT 1").fetchone()
    redis.Redis.from_url(REDIS_URL).ping()
    return {"status": "ok", "postgres": "ok", "redis": "ok"}


@app.get("/api/pets")
def list_pets() -> list[dict[str, object]]:
    with psycopg.connect(DATABASE_URL) as connection:
        rows = connection.execute(
            "SELECT id, name, species, status, adoption_fee_cents FROM pets ORDER BY id"
        ).fetchall()
    return [
        {
            "id": row[0],
            "name": row[1],
            "species": row[2],
            "status": row[3],
            "adoption_fee_cents": row[4],
        }
        for row in rows
    ]


@app.post("/api/adoptions", status_code=201)
def create_adoption(request: AdoptionRequest) -> dict[str, object]:
    """Create an adoption atomically.

    Uses SELECT FOR UPDATE to lock the pet row within a single transaction,
    ensuring that only one concurrent request can adopt the same pet.
    The database UNIQUE constraint on adoptions.pet_id provides a durable
    invariant independent of application timing.
    """
    if "@" not in request.adopter_email:
        raise HTTPException(status_code=422, detail="valid adopter email required")

    time.sleep(RACE_DELAY_SECONDS)

    with psycopg.connect(DATABASE_URL) as connection:
        pet = connection.execute(
            "SELECT status, adoption_fee_cents FROM pets WHERE id = %s FOR UPDATE",
            (request.pet_id,),
        ).fetchone()
        if pet is None:
            raise HTTPException(status_code=404, detail="pet not found")
        if pet[0] != "available":
            raise HTTPException(status_code=409, detail="pet is no longer available")

        adoption_id = connection.execute(
            "INSERT INTO adoptions (pet_id, adopter_email) VALUES (%s, %s) RETURNING id",
            (request.pet_id, request.adopter_email),
        ).fetchone()[0]
        connection.execute(
            "UPDATE pets SET status = 'pending' WHERE id = %s", (request.pet_id,)
        )
        connection.commit()

    redis.Redis.from_url(REDIS_URL).delete("available-pets")
    return {
        "id": adoption_id,
        "pet_id": request.pet_id,
        "adoption_fee_cents": pet[1],
        "status": "accepted",
    }


@app.post("/api/demo/reset")
def reset_demo() -> dict[str, str]:
    """Reset deterministic demo data; this endpoint is not for production use."""
    with psycopg.connect(DATABASE_URL) as connection:
        connection.execute("TRUNCATE adoptions RESTART IDENTITY")
        connection.execute(
            "UPDATE pets SET status = CASE WHEN id = 'pet-103' THEN 'pending' ELSE 'available' END"
        )
        connection.commit()
    redis.Redis.from_url(REDIS_URL).flushdb()
    return {"status": "reset"}


@app.get("/api/demo/adoptions/{pet_id}")
def adoption_count(pet_id: str) -> dict[str, object]:
    with psycopg.connect(DATABASE_URL) as connection:
        count = connection.execute(
            "SELECT count(*) FROM adoptions WHERE pet_id = %s", (pet_id,)
        ).fetchone()[0]
    return {"pet_id": pet_id, "count": count}
