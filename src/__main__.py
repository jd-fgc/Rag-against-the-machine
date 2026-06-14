from ingestion.indexer import loader_file, save_chunks
from ingestion.chunker import chunk_python, chunk_markdown
# import os
# import time
# import fire


def main():
    try:
        python_chunks = []
        markdown_chunks = []
        output_python = "data/processed/chunks/python_chunks.json"
        output_markdown = "data/processed/chunks/markdown_chunks.json"

        for file_path, text in loader_file():
            if file_path.suffix == ".py":
                chunks = chunk_python(str(file_path), text, 2000)
                python_chunks.extend(chunks)
            elif file_path.suffix == ".md":
                chunks = chunk_markdown(str(file_path), text, 2000)
                markdown_chunks.extend(chunks)
        save_chunks(python_chunks, output_python)
        save_chunks(markdown_chunks, output_markdown)

        # Debug
        print(f"Python chunks: {len(python_chunks)}")
        print(f"Markdown chunks: {len(markdown_chunks)}")
        gros = [c for c in markdown_chunks if len(c.text) > 2000]
        print(f"Chunks > 2000 chars: {len(gros)}")
        print(f"Taille max: {max(len(c.text) for c in markdown_chunks)}")
    except Exception:
        raise Exception


if __name__ == "__main__":
    main()
