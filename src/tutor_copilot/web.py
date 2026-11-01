import time
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from uuid import uuid4

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from tutor_copilot.auth import install_auth
from tutor_copilot.intake import router
from tutor_copilot.runtime import open_resources, readiness
from tutor_copilot.settings import Settings
from tutor_copilot.telemetry import Outcome, configure_logging, observe


def create_app(settings: Settings | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        correlation_id = uuid4()
        async with open_resources(settings or Settings()) as resources:
            app.state.resources = resources
            observe("startup", "complete", correlation_id)
            yield
        observe("startup", "stopped", correlation_id)

    app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)
    app.state.settings = settings or Settings()
    install_auth(app)
    app.include_router(router)

    @app.exception_handler(RequestValidationError)
    async def invalid_input(request: Request, error: RequestValidationError) -> JSONResponse:
        return JSONResponse({"detail": "Invalid request fields"}, status_code=422)

    @app.exception_handler(IntegrityError)
    async def conflict(request: Request, error: IntegrityError) -> JSONResponse:
        return JSONResponse({"detail": "Record identity conflict"}, status_code=409)

    @app.middleware("http")
    async def request_metadata(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        correlation_id = uuid4()
        started = time.monotonic()
        outcome: Outcome
        try:
            response = await call_next(request)
            outcome = "complete" if response.status_code < 500 else "failed"
        except Exception:
            # Exception strings can include SQL parameters or imported learner text.
            response = JSONResponse({"status": "error"}, status_code=500)
            outcome = "failed"
        response.headers["X-Correlation-ID"] = str(correlation_id)
        response.headers["Cache-Control"] = "no-store"
        observe(
            "request",
            outcome,
            correlation_id,
            status_code=response.status_code,
            duration_ms=round((time.monotonic() - started) * 1000),
        )
        return response

    @app.get("/health/live")
    async def live() -> dict[str, str]:
        return {"status": "alive"}

    @app.get("/health/ready")
    async def ready(request: Request) -> JSONResponse:
        database, cache = await readiness(request.app.state.resources)
        status = "unavailable" if not database else "ready" if cache else "degraded"
        return JSONResponse(
            {"status": status, "database": database, "cache": cache},
            status_code=200 if database else 503,
        )

    return app


def main() -> None:
    configure_logging()
    uvicorn.run(create_app(), host="127.0.0.1", port=8000, access_log=False, log_config=None)
