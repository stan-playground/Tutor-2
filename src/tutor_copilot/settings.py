"""Local synthetic development configuration; no credential or dotenv loading."""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_name: str = "tutor_copilot"

    def __post_init__(self) -> None:
        if not re.fullmatch(r"tutor_copilot|tc_test_[a-f0-9]{32}", self.database_name):
            raise ValueError("Use the local development database or an isolated test database")

    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg://tutor_dev@127.0.0.1:55432/{self.database_name}"

    @property
    def redis_url(self) -> str:
        return "redis://127.0.0.1:56379/0"
