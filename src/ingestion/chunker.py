from typing import List
from models import Chunk
import ast


def chunk_python(file_path : str, text : str, max_chunk_size : int) -> List[Chunk]:
    chunks = []
    tree = ast.parse(text)

    lines = text.split("\n")
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line) + 1)

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start = offsets[node.lineno - 1]
            end   = offsets[node.end_lineno - 1] + node.end_col_offset
            chunks.append(Chunk(
                file_path=file_path,
                first_character_index=start,
                last_character_index=end,
                text=text[start:end],
                chunk_type="python"
            ))
    return chunks


def chunk_markdown(file_path : str, text : str, max_chunk_size : int) -> List[Chunk]:
    chunks = []
    lines = text.split("\n")
    section_start = 0
    cursor = 0

    for i, line in enumerate(lines):
        if line.startswith("#") and i > 0:
            start = section_start
            end = cursor
            chunks.append(Chunk(
                file_path=file_path,
                first_character_index=start,
                last_character_index=end,
                text=text[start:end],
                chunk_type="markdown"
            ))
            section_start = cursor
            pass
        cursor += len(line) + 1
        if section_start < len(text):
            chunks.append(Chunk(
                file_path=file_path,
                first_character_index=section_start,
                last_character_index=len(text),
                text=text[section_start:],
                chunk_type="markdown"
            ))
    return chunks