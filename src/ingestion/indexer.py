from pathlib import Path
import bm25s
import json


SKIP_DIRS = {"__pycache__", ".git", "tests", "build", "dist", "benchmarks"}


def loader_file(repo_path: str):
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


def build_indexes(output_dir: str):
    with open('data/processed/chunks/python_chunks.json', 'r') as f:
        python_chunks = json.load(f)
    with open('data/processed/chunks/markdown_chunks.json', 'r') as f:
        markdown_chunk = json.load(f)

    corpus_python = [chunk["text"] for chunk in python_chunks]
    corpus_markdown = [chunk["text"] for chunk in markdown_chunk]

    retriever_python = bm25s.BM25()
    retriever_python.index(bm25s.tokenize(corpus_python))
    retriever_markdown = bm25s.BM25()
    retriever_markdown.index(bm25s.tokenize(corpus_markdown))

    retriever_python.save(f"{output_dir}/bm25_index/python")
    retriever_markdown.save(f"{output_dir}/bm25_index/markdown")
