from pathlib import Path


SKIP_DIRS = {"__pycache__", ".git", "tests", "build", "dist", "benchmarks"}


def loader_file():
    repo = Path("data/raw/vllm-0.10.1")

    for file_path in repo.rglob("*"):
        if any(part in SKIP_DIRS for part in file_path.parts):
            continue
        elif file_path.suffix == {".py", ".md"}:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
            yield file_path, text
