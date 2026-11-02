"""Explicit maintenance publication of separately permissioned, reviewed shared material."""

import argparse
import asyncio
import json
from pathlib import Path
from typing import Literal, Self

from pydantic import model_validator
from sqlalchemy.ext.asyncio import create_async_engine

from tutor_copilot.embeddings import LocalEmbeddings
from tutor_copilot.materials import MaterialWrite, describe_target, save_material
from tutor_copilot.schemas import Text
from tutor_copilot.settings import Settings


class SharedPublication(MaterialWrite):
    reviewer_ref: Text
    reviewer_qualification: Literal["qualified_english_tutor"]
    sharing_permission_ref: Text

    @model_validator(mode="after")
    def reviewed_material(self) -> Self:
        if not self.material.reviewed:
            raise ValueError("Shared publication requires reviewed material")
        return self


async def publish(data: SharedPublication, settings: Settings) -> dict[str, object]:
    embeddings = LocalEmbeddings()
    engine = create_async_engine(
        settings.database_url,
        hide_parameters=True,
        connect_args={"connect_timeout": 3, "options": "-c statement_timeout=3000"},
    )
    try:
        vector = None
        if data.material.available:
            vector = await embeddings.embed(
                describe_target(data.material.target)
                + "\n"
                + data.material.content
                + "\n"
                + data.material.instructions,
                passage=True,
            )
        async with engine.begin() as connection:
            return await save_material(
                connection,
                None,
                data,
                vector,
                reviewer_ref=data.reviewer_ref,
                sharing_permission_ref=data.sharing_permission_ref,
            )
    finally:
        await engine.dispose()
        await embeddings.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Publish a reviewed, permissioned shared bank version"
    )
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    try:
        data = SharedPublication.model_validate_json(args.file.read_text())
        result = asyncio.run(publish(data, Settings()))
    except Exception:
        # Validation/provider/database exception text can include imported material.
        raise SystemExit("Shared material publication failed") from None
    print(json.dumps(result))
