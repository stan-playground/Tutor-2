import json
import logging
from contextlib import asynccontextmanager
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from tutor_copilot import web
from tutor_copilot.settings import Settings
from tutor_copilot.telemetry import configure_logging
from tutor_copilot.web import create_app


def test_local_settings_reject_other_database_names() -> None:
    with pytest.raises(ValueError, match="local development database"):
        Settings(database_name="other_database")


def test_live_and_error_logs_exclude_private_payloads(capsys) -> None:
    configure_logging()
    app = create_app()

    @app.post("/test-error/{private_path}")
    async def error(private_path: str) -> None:
        raise RuntimeError(f"PRIVATE_EXCEPTION_{private_path}")

    with TestClient(app) as client:
        live = client.get("/health/live")
        assert live.status_code == 200
        assert live.json() == {"status": "alive"}
        assert live.headers["Cache-Control"] == "no-store"
        failed = client.post(
            "/test-error/PRIVATE_PATH?text=PRIVATE_QUERY",
            headers={"X-Correlation-ID": "PRIVATE_HEADER"},
            json={"text": "PRIVATE_BODY"},
        )
        assert failed.status_code == 500
        assert failed.json() == {"status": "error"}
        assert failed.headers["Cache-Control"] == "no-store"
        assert UUID(failed.headers["X-Correlation-ID"])
        assert live.headers["X-Correlation-ID"] != failed.headers["X-Correlation-ID"]
    logging.getLogger("sqlalchemy.engine").error("PRIVATE_LIBRARY_EXCEPTION")
    logging.getLogger("uvicorn.access").info("PRIVATE_ACCESS_LOG")
    captured = capsys.readouterr()
    assert "PRIVATE" not in captured.out + captured.err + failed.text
    records = [json.loads(line) for line in captured.out.splitlines()]
    assert records[-1]["outcome"] == "stopped"
    assert records[-1]["correlation_id"] == records[0]["correlation_id"]
    failed_record = next(
        record
        for record in records
        if record["correlation_id"] == failed.headers["X-Correlation-ID"]
    )
    assert failed_record["correlation_id"] == failed.headers["X-Correlation-ID"]
    assert failed_record["outcome"] == "failed"
    assert failed_record["status_code"] == 500
    assert set(failed_record) == {
        "stage",
        "outcome",
        "correlation_id",
        "status_code",
        "duration_ms",
    }


def test_cleanup_failure_does_not_report_successful_shutdown(monkeypatch, capsys) -> None:
    configure_logging()
    original_resources = web.open_resources

    @asynccontextmanager
    async def failed_cleanup(settings):
        async with original_resources(settings) as resources:
            yield resources
        raise RuntimeError("synthetic cleanup failure")

    monkeypatch.setattr(web, "open_resources", failed_cleanup)
    with pytest.raises(RuntimeError, match="synthetic cleanup failure"), TestClient(create_app()):
        pass
    records = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    assert [record["outcome"] for record in records] == ["complete"]
