from typing import List
from models import MinimalSource
import json
import bm25s


def search_query(query: List, index_dir: int, k, index_type: str):
    with open('data/processed/chunks/python_chunks.json', 'r') as f:
        python_chunks = json.load(f)
    with open('data/processed/chunks/markdown_chunks.json') as f:
        markdown_chunks = json.load(f)

    retriever_python = bm25s.BM25.load('data/processed/bm25_index/python')
    retriever_markdown = bm25s.BM25.load('data/processed/bm25_index/markdown')

    result = []

    if index_type in ("python", "both"):
        query_token = bm25s.tokenize([query])
        indices, scores = retriever_python.retrieve(query_token, k=k)
        for idx in indices[0]:  # indices[0] car une seule query
            chunk = python_chunks[idx]
            result.append(MinimalSource(
                file_path=chunk["file_path"],
                first_character_index=chunk["first_character_index"],
                last_character_index=chunk["last_character_index"]
            ))
    if index_type in ("markdown", "both"):
        