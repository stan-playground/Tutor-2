"""Process startup shell; queue processing is introduced with preparation requests."""

import argparse
import asyncio
import signal
from uuid import uuid4

from tutor_copilot.runtime import open_resources, readiness
from tutor_copilot.settings import Settings
from tutor_copilot.telemetry import configure_logging, observe


async def run(*, check: bool = False, settings: Settings | None = None) -> int:
    correlation_id = uuid4()
    async with open_resources(settings or Settings()) as resources:
        database, cache = await readiness(resources)
        if not database:
            observe("worker", "unavailable", correlation_id)
            return 1
        if check:
            observe("worker", "ready" if cache else "degraded", correlation_id)
            return 0
        stopped = asyncio.Event()
        loop = asyncio.get_running_loop()
        for signum in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(signum, stopped.set)
        try:
            observe("worker", "ready" if cache else "degraded", correlation_id)
            await stopped.wait()
        finally:
            for signum in (signal.SIGINT, signal.SIGTERM):
                loop.remove_signal_handler(signum)
        observe("worker", "stopped", correlation_id)
        return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check startup and exit")
    args = parser.parse_args()
    configure_logging()
    try:
        code = asyncio.run(run(check=args.check))
    except Exception:
        observe("worker", "failed", uuid4())
        code = 1
    raise SystemExit(code)
