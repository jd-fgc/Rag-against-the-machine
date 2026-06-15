import bm25s
import json


def build_indexes(output_dir: str):
    with open('data/processed/chunks/python_chunks.json', 'r') as f:
        python_chunks = json.load(f)
    with open('data/processed/chunks/markdown_chunks.json', 'r') as f:
        markdown_chunk = json.load(f)

    corpus_python = [chunk["text"] for chunk in python_chunks]
    corpus_markdown = [chunk["text"] for chunk in markdown_chunk]

    