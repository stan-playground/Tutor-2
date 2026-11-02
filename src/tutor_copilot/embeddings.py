"""Pinned, offline runtime embeddings; public weights are prepared explicitly."""

import asyncio
import json
import math
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from fastembed import TextEmbedding

MODEL = "BAAI/bge-small-en-v1.5"
MODEL_COMMIT = "aa8f8b060edb00e03bfdd08813a2949946c8ba55"
MODEL_DIRECTORY = Path(".highgrade/local/embeddings") / MODEL_COMMIT
DIMENSIONS = 384
CONFIG_REVISION = f"bge-small-en-v1.5-{MODEL_COMMIT}-fastembed-0.7.4-cpu-description-v2"
MODEL_FILES = [
    "config.json",
    "model_optimized.onnx",
    "special_tokens_map.json",
    "tokenizer.json",
    "tokenizer_config.json",
]


def validate_vector(value: Any) -> list[float]:
    if not isinstance(value, list) or len(value) != DIMENSIONS:
        raise ValueError("Invalid embedding dimensions")
    if any(type(item) not in (int, float) for item in value):
        raise ValueError("Invalid embedding values")
    try:
        vector = [float(item) for item in value]
    except OverflowError:
        raise ValueError("Invalid embedding values") from None
    # Keep cosine norm arithmetic safely inside pgvector's float32 range.
    if any(not math.isfinite(item) for item in vector) or not 1e-15 <= math.hypot(*vector) <= 1e15:
        raise ValueError("Invalid embedding norm")
    return vector


class LocalEmbeddings:
    def __init__(self) -> None:
        self.model: TextEmbedding | None = None
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="embedding")
        self.capacity = asyncio.Semaphore(1)

    def _encode(self, description: str, passage: bool) -> list[float]:
        if self.model is None:
            if not all((MODEL_DIRECTORY / name).is_file() for name in MODEL_FILES):
                raise ValueError("Run just embeddings-prepare before material retrieval")
            import onnxruntime  # type: ignore[import-untyped]

            onnxruntime.disable_telemetry_events()
            onnxruntime.set_default_logger_severity(3)
            from fastembed import TextEmbedding

            self.model = TextEmbedding(
                model_name=MODEL,
                specific_model_path=str(MODEL_DIRECTORY),
                cache_dir=str(MODEL_DIRECTORY),
                local_files_only=True,
                threads=2,
                providers=["CPUExecutionProvider"],
            )
        values = (
            self.model.passage_embed([description])
            if passage
            else self.model.query_embed(description)
        )
        return validate_vector(next(iter(values)).tolist())

    async def embed(self, description: str, *, passage: bool = False) -> list[float]:
        await asyncio.wait_for(self.capacity.acquire(), timeout=3)
        future = asyncio.get_running_loop().run_in_executor(
            self.executor, self._encode, description, passage
        )

        def finished(completed: asyncio.Future[list[float]]) -> None:
            # A cancelled caller must not release the model while inference still runs.
            if not completed.cancelled():
                completed.exception()
            self.capacity.release()

        future.add_done_callback(finished)
        return await asyncio.wait_for(asyncio.shield(future), timeout=30)

    async def close(self) -> None:
        await asyncio.to_thread(self.executor.shutdown, wait=True, cancel_futures=True)
        self.model = None


def prepare() -> None:
    from huggingface_hub import snapshot_download

    snapshot_download(
        repo_id="qdrant/bge-small-en-v1.5-onnx-q",
        revision=MODEL_COMMIT,
        allow_patterns=MODEL_FILES,
        local_dir=MODEL_DIRECTORY,
        cache_dir=".highgrade/local/huggingface",
        token=False,
    )
    print(
        json.dumps(
            {
                "status": "complete",
                "model": MODEL,
                "revision": MODEL_COMMIT,
                "dimensions": DIMENSIONS,
            }
        )
    )
