"""An allowlist at the console export boundary, including third-party logs."""

import json
import logging
from logging.config import dictConfig
from typing import Literal
from uuid import UUID

Stage = Literal["request", "worker", "startup"]
Outcome = Literal["ready", "degraded", "unavailable", "complete", "failed", "stopped"]


class MetadataFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return isinstance(getattr(record, "metadata_line", None), str)


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {"metadata": {"()": MetadataFilter}},
            "formatters": {"metadata": {"format": "%(metadata_line)s"}},
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "filters": ["metadata"],
                    "formatter": "metadata",
                }
            },
            "root": {"handlers": ["console"], "level": "INFO"},
            "loggers": {
                "uvicorn": {"handlers": [], "propagate": True},
                "uvicorn.error": {"handlers": [], "propagate": True},
                "uvicorn.access": {"handlers": [], "propagate": True},
            },
        }
    )


def observe(
    stage: Stage,
    outcome: Outcome,
    correlation_id: UUID,
    *,
    status_code: int | None = None,
    duration_ms: int | None = None,
) -> None:
    logging.getLogger("tutor_copilot").info(
        "",
        extra={
            "metadata_line": json.dumps(
                {
                    "stage": stage,
                    "outcome": outcome,
                    "correlation_id": str(correlation_id),
                    "status_code": status_code,
                    "duration_ms": duration_ms,
                }
            )
        },
    )
