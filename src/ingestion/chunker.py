from typing import List
import ast


def chunk_python(file_path : str, text : str, max_chunk_size : int) -> List[Chunk]:
    result = []

    text_parse = ast.parse(text)
    


def chunk_markdown(file_path : str, text : str, max_chunk_size : int) -> List[Chunk]:
    pass
