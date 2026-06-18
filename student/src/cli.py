from tqdm import tqdm


class StudentCLI:

    def index(self, repo_path: str = "data/raw/vllm-0.10.1",
              output_dir: str = "data/processed",
              max_chunk_size: int = 2000) -> None:
        from src.ingestion.chunker import chunk_python, chunk_markdown, save_chunks
        from src.ingestion.indexer import loader_file, build_indexes
        python_chunks = []
        markdown_chunks = []
        for file_path, text in tqdm(loader_file(repo_path), desc="Chunking files"):
            if file_path.suffix == ".py":
                chunks = chunk_python(str(file_path), text, max_chunk_size)
                python_chunks.extend(chunks)
            elif file_path.suffix == ".md":
                chunks = chunk_markdown(str(file_path), text, max_chunk_size)
                markdown_chunks.extend(chunks)
        save_chunks(python_chunks, f"{output_dir}/chunks/python_chunks.json")
        save_chunks(markdown_chunks, f"{output_dir}/chunks/markdown_chunks.json")
        build_indexes(output_dir)
        print("Ingestion complete! Indices saved under data/processed/")

    def search(self, query: str, index_dir: str = "data/processed",
               k: int = 10, index_type: str = "both") -> None:
        from src.retrieval.searcher import search_query
        if not query or not query.strip():
            print("Empty query, no results.")
            return
        results = search_query(query, index_dir, k, index_type)
        for r in results:
            print(f"{r.file_path} [{r.first_character_index}:{r.last_character_index}]")

    def search_dataset(self, dataset_path: str,
                       index_dir: str = "data/processed",
                       k: int = 10,
                       save_directory: str = "data/output/search_results",
                       index_type: str = "both") -> None:
        from src.retrieval.searcher import search_dataset
        search_dataset(dataset_path, index_dir, k, save_directory, index_type)

    def answer(self, query: str, index_dir: str = "data/processed",
               k: int = 10, index_type: str = "both") -> None:
        from src.generation.generator import load_model, answer_query
        model, tokenizer = load_model()
        print(answer_query(query, index_dir, k, index_type, model, tokenizer))

    def answer_dataset(self, student_search_results_path: str,
                       save_directory: str = "data/output/search_results_and_answer") -> None:
        from src.generation.generator import answer_data_set
        answer_data_set(student_search_results_path, save_directory)

    def evaluate(self, student_answer_path: str, dataset_path: str,
                 k: int = 10, max_context_length: int = 2000) -> None:
        from src.evaluation.evaluator import evaluate
        evaluate(student_answer_path, dataset_path, k, max_context_length)
