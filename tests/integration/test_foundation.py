import asyncio
import json
import os
import select
import signal
import subprocess
import sys
from uuid import uuid4

from conftest import migrate
from fastapi.testclient import TestClient
from redis.asyncio import Redis
from sqlalchemy import create_engine, text

from tutor_copilot.runtime import cache_ready, open_resources, readiness
from tutor_copilot.settings import Settings
from tutor_copilot.web import create_app


def test_migration_round_trip_and_real_vector_operation(database) -> None:
    migrate(database)
    migrate(database)
    engine = create_engine(database.database_url)
    try:
        with engine.connect() as connection:
            assert connection.scalar(text("SELECT version_num FROM alembic_version")) == "0004"
            assert connection.scalar(text("SELECT '[1,2,3]'::vector <-> '[1,2,4]'::vector")) == 1.0
        migrate(database, "base")
        with engine.connect() as connection:
            assert not connection.scalar(
                text("SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector')")
            )
        migrate(database)
    finally:
        engine.dispose()


def test_api_requires_migration_and_then_reports_ready(database) -> None:
    with TestClient(create_app(database)) as client:
        assert client.get("/health/live").status_code == 200
        missing = client.get("/health/ready")
        assert missing.status_code == 503
        assert missing.json()["database"] is False
        migrate(database)
        ready = client.get("/health/ready")
        assert ready.status_code == 200
        assert ready.json() == {"status": "ready", "database": True, "cache": True}


def test_redis_real_ttl_and_no_persistence() -> None:
    async def exercise():
        async with open_resources(Settings()) as resources:
            assert await cache_ready(resources.cache)
            config = await resources.cache.config_get("save", "appendonly")
            assert config == {"save": "", "appendonly": "no"}
            key = f"tc-test:{uuid4().hex}"
            try:
                await resources.cache.set(key, "synthetic-vector", ex=86400)
                assert await resources.cache.get(key) == "synthetic-vector"
                assert 0 < await resources.cache.ttl(key) <= 86400
            finally:
                await resources.cache.delete(key)

    asyncio.run(exercise())


def test_cache_outage_is_bounded_and_database_remains_ready(database) -> None:
    migrate(database)

    async def exercise():
        async with open_resources(database) as resources:
            unavailable = Redis(host="127.0.0.1", port=1, socket_connect_timeout=0.2)
            try:
                resources.cache = unavailable
                async with asyncio.timeout(5):
                    assert await readiness(resources) == (True, False)
            finally:
                await unavailable.aclose()

    asyncio.run(exercise())


def worker_process(settings, *, check=False):
    script = (
        "import asyncio,sys; "
        "from tutor_copilot.settings import Settings; "
        "from tutor_copilot.telemetry import configure_logging; "
        "from tutor_copilot.worker import run; "
        "configure_logging(); "
        f"sys.exit(asyncio.run(run(check={check!r}, settings=Settings(sys.argv[1]))))"
    )
    return subprocess.Popen(
        [sys.executable, "-u", "-c", script, settings.database_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_worker_refuses_unmigrated_database(database) -> None:
    process = worker_process(database, check=True)
    out, err = process.communicate(timeout=10)
    assert process.returncode == 1
    assert json.loads(out)["outcome"] == "unavailable"
    assert err == ""


def test_worker_startup_and_graceful_shutdown(database) -> None:
    migrate(database)
    process = worker_process(database)
    try:
        assert select.select([process.stdout], [], [], 10)[0], "Worker did not become ready"
        first = json.loads(process.stdout.readline())
        assert first["outcome"] == "ready"
        assert process.poll() is None
        os.kill(process.pid, signal.SIGTERM)
        out, err = process.communicate(timeout=10)
        assert process.returncode == 0
        last = json.loads(out)
        assert last["outcome"] == "stopped"
        assert last["correlation_id"] == first["correlation_id"]
        assert err == ""
    finally:
        if process.poll() is None:
            process.kill()
            process.communicate(timeout=5)
