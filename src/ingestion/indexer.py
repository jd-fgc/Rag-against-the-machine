from typing import List
from pathlib import Path
from models import Chunk
import json


SKIP_DIRS = {"__pycache__", ".git", "tests", "build", "dist", "benchmarks"}


def loader_file():
    repo = Path("data/raw/vllm-0.10.1")
    seen = set()

    for file_path in repo.rglob("*"):
        if any(part in SKIP_DIRS for part in file_path.parts):
            continue
        if not file_path.is_file():
            continue
        real_path = file_path.resolve()
        if real_path in seen:
            continue
        seen.add(real_path)
        if file_path.suffix in {".py", ".md"}:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
            yield file_path, text


def save_chunks(chunks: List[Chunk], output_path: str) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump([chunk.model_dump() for chunk in chunks], f)
