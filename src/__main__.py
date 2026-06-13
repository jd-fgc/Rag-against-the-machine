from ingestion.indexer import loader_file
from ingestion.chunker import chunk_python, chunk_markdown
# import os
# import time
# import fire
# import ast


def main():
    try:
        path = "data/raw/vllm-0.10.1"

        for file_path, text in loader_file():
            if file_path.suffix == ".py":
                chunks = chunk_python(str(file_path), text, 2000)
                for chunk in chunks[:2]:
                    print(chunk.file_path)
                    print(chunk.first_character_index, chunk.last_character_index)
                    print(chunk.text[:100])
                    print("---")
            elif file_path.suffix == ".md":
                chunks = chunk_markdown(str(file_path), text, 2000)
                for chunk in chunks:
                    print(chunk.file_path)
                    print(chunk.first_character_index, chunk.last_character_index)
                    print(chunk.text[:100])
                    print("---")
    except Exception:
        raise Exception


if __name__ == "__main__":
    main()
