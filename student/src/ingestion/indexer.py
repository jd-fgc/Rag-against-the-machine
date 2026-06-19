from pathlib import Path
from typing import Generator
import bm25s
import json


SKIP_DIRS = {"__pycache__", ".git", "tests", "build", "dist", "benchmarks"}


def loader_file(repo_path: str) -> Generator:
    """Recursively yield Python and Markdown files from a repository.

    Skips common non-essential directories and deduplicates symlinks.

    Args:
        repo_path: Path to the repository root directory.

    Yields:
        Tuple of (file_path, text) for each .py and .md file found.
    """
    repo = Path(repo_path)
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


def build_indexes(output_dir: str) -> None:
    """Build and save BM25 indexes for Python and Markdown chunks.

    Reads chunk JSON files from output_dir/chunks/ and saves
    BM25 indexes to output_dir/bm25_index/.

    Args:
        output_dir: Path to the processed data directory.
    """
    with open(f'{output_dir}/chunks/python_chunks.json', 'r') as f:
        python_chunks = json.load(f)
    with open(f'{output_dir}/chunks/markdown_chunks.json', 'r') as f:
        markdown_chunk = json.load(f)

    corpus_python = [chunk["text"] for chunk in python_chunks]
    corpus_markdown = [chunk["text"] for chunk in markdown_chunk]

    retriever_python = bm25s.BM25()
    retriever_python.index(bm25s.tokenize(corpus_python))
    retriever_markdown = bm25s.BM25()
    retriever_markdown.index(bm25s.tokenize(corpus_markdown))

    retriever_python.save(f"{output_dir}/bm25_index/python")
    retriever_markdown.save(f"{output_dir}/bm25_index/markdown")
