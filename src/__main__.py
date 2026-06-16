from ingestion.chunker import chunk_python, chunk_markdown, save_chunks
from ingestion.indexer import build_indexes
from retrieval.searcher import search_dataset
from evaluation.evaluator import evaluate
from generation.generator import load_model, answer_query, answer_data_set
from pathlib import Path
# import os
# import time
# import fire


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


def main():
    try:
        python_chunks = []
        markdown_chunks = []
        output_python = "data/processed/chunks/python_chunks.json"
        output_markdown = "data/processed/chunks/markdown_chunks.json"

        # Load and chunk vllm folder
        for file_path, text in loader_file():
            if file_path.suffix == ".py":
                chunks = chunk_python(str(file_path), text, 2000)
                python_chunks.extend(chunks)
            elif file_path.suffix == ".md":
                chunks = chunk_markdown(str(file_path), text, 2000)
                markdown_chunks.extend(chunks)
        save_chunks(python_chunks, output_python)
        save_chunks(markdown_chunks, output_markdown)

        # Indexing
        build_indexes("data/processed")

        # Retrieval
        search_dataset(
            dataset_path="data/datasets/UnansweredQuestions/dataset_docs_public.json",
            index_dir="data/processed",
            k=10,
            save_directory="data/output/search_results",
            index_type="markdown"
        )

        # Evaluation
        evaluate(
            student_answer_path="data/output/search_results/dataset_docs_public.json",
            dataset_path="data/datasets/AnsweredQuestions/dataset_docs_public.json",
            k=20,
            max_context_length=2000
        )

        # LLM
        model, tokenizer = load_model()
        response = answer_query(
            query="How does vLLM handle batching?",
            index_dir="data/processed",
            k=5,
            index_type="both",
            model=model,
            tokenizer=tokenizer
        )
        print(response)
        answer_data_set(
            student_search_results_path="data/output/search_results/dataset_docs_public.json",
            save_directory="data/output/search_results_and_answer"
        )

        # Debug
        # print(f"Python chunks: {len(python_chunks)}")
        # print(f"Markdown chunks: {len(markdown_chunks)}")
        # gros = [c for c in markdown_chunks if len(c.text) > 2000]
        # print(f"Chunks > 2000 chars: {len(gros)}")
        # print(f"Taille max: {max(len(c.text) for c in markdown_chunks)}")
    except Exception:
        raise Exception


if __name__ == "__main__":
    main()
