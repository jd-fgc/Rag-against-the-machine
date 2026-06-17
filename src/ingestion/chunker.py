from typing import List
from src.models import Chunk
from pathlib import Path
import ast
import json


def save_chunks(chunks: List[Chunk], output_path: str) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump([chunk.model_dump() for chunk in chunks], f, indent=4)



def chunk_python(file_path: str, text: str, max_chunk_size: int) -> List[Chunk]:
    chunks = []
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []

    lines = text.split("\n")
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line) + 1)

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start = offsets[node.lineno - 1]
            end = offsets[node.end_lineno - 1] + node.end_col_offset
            if (end - start) <= max_chunk_size:
                chunks.append(Chunk(
                    file_path=file_path,
                    first_character_index=start,
                    last_character_index=end,
                    text=text[start:end],
                    chunk_type="python"
                ))
            else:
                children = [
                    c for c in ast.iter_child_nodes(node)
                    if isinstance(c, (ast.FunctionDef, ast.AsyncFunctionDef))
                ]
                for child in children:
                    c_start = offsets[child.lineno - 1]
                    c_end = offsets[child.end_lineno - 1] + child.end_col_offset
                    chunks.append(Chunk(
                        file_path=file_path,
                        first_character_index=c_start,
                        last_character_index=c_end,
                        text=text[c_start:c_end],
                        chunk_type="python"
                    ))
    return chunks


def chunk_markdown(file_path: str, text: str, max_chunk_size: int) -> List[Chunk]:
    chunks = []
    lines = text.split("\n")
    section_start = 0
    cursor = 0

    for i, line in enumerate(lines):
        if line.startswith("#") and i > 0:
            start = section_start
            end = cursor
            if (end - start) <= max_chunk_size:
                chunks.append(Chunk(
                    file_path=file_path,
                    first_character_index=start,
                    last_character_index=end,
                    text=text[start:end],
                    chunk_type="markdown"
                ))
            else:
                paragraphs = text[start:end].split("\n\n")
                local_cursor = start
                for paragraph in paragraphs:
                    if paragraph.strip():
                        if len(paragraph) <= max_chunk_size:
                            chunks.append(Chunk(
                                file_path=file_path,
                                first_character_index=local_cursor,
                                last_character_index=local_cursor + len(paragraph),
                                chunk_type="markdown",
                                text=paragraph
                            ))
                        else:
                            p_cursor = 0
                            while p_cursor < len(paragraph):
                                chunk_text = paragraph[p_cursor:p_cursor + max_chunk_size]
                                chunks.append(Chunk(
                                    file_path=file_path,
                                    first_character_index=local_cursor + p_cursor,
                                    last_character_index=local_cursor + p_cursor + len(chunk_text),
                                    text=chunk_text,
                                    chunk_type="markdown"
                                ))
                                p_cursor += max_chunk_size
                    local_cursor += len(paragraph) + 2
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
