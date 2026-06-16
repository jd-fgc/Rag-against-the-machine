from typing import List
from models import MinimalSource, MinimalSearchResults, StudentSearchResults
from pathlib import Path
import json
import bm25s


def search_query(query: str, index_dir: str, k: int, index_type: str) -> List[MinimalSource]:
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
        for idx in indices[0]:
            chunk = python_chunks[idx]
            result.append(MinimalSource(
                file_path=chunk["file_path"],
                first_character_index=chunk["first_character_index"],
                last_character_index=chunk["last_character_index"]
            ))
    if index_type in ("markdown", "both"):
        query_token = bm25s.tokenize([query])
        indices, scores = retriever_markdown.retrieve(query_token, k=k)
        for idx in indices[0]:
            chunk = markdown_chunks[idx]
            result.append(MinimalSource(
                file_path=chunk["file_path"],
                first_character_index=chunk["first_character_index"],
                last_character_index=chunk["last_character_index"]
            ))
    return result


def search_dataset(dataset_path, index_dir, k, save_directory, index_type):
    with open('data/processed/chunks/python_chunks.json', 'r') as f:
        python_chunks = json.load(f)
    with open('data/processed/chunks/markdown_chunks.json') as f:
        markdown_chunks = json.load(f)

    retriever_python = bm25s.BM25.load('data/processed/bm25_index/python')
    retriever_markdown = bm25s.BM25.load('data/processed/bm25_index/markdown')

    with open(dataset_path, 'r') as f:
        dataset = json.load(f)

    search_results = []
    for question in dataset["rag_questions"]:
        results = search_query(
            query=question["question"],
            index_dir=index_dir,
            k=k,
            index_type=index_type
        )
        search_results.append(MinimalSearchResults(
            question_id=question["question_id"],
            question=question["question"],
            retrieved_sources=results
        ))
    output = StudentSearchResults(search_results=search_results, k=k)
    Path(save_directory).mkdir(parents=True, exist_ok=True)
    output_path = Path(save_directory) / Path(dataset_path).name
    with open(output_path, "w") as f:
        f.write(output.model_dump_json(indent=2))



# fonction search_dataset(dataset_path, index_dir, k, save_directory, index_type):

#     1. charger une fois les chunks et les index BM25
#     2. lire le dataset JSON (liste de questions)
#     3. pour chaque question :
#            appeler search_query()
#            construire un MinimalSearchResults
#     4. construire un StudentSearchResults avec toute la liste
#     5. sauvegarder en JSON dans save_directory
