from typing import List
from src.models import Chunk
from pathlib import Path
import ast
import json


def save_chunks(chunks: List[Chunk], output_path: str) -> None:
    """Save a list of chunks to a JSON file.

    Args:
        chunks: List of Chunk objects to save.
        output_path: Full path to the output JSON file.
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump([chunk.model_dump() for chunk in chunks], f, indent=4)


def chunk_python(file_path: str, text: str,
                 max_chunk_size: int) -> List[Chunk]:
    """Chunk a Python file using AST node boundaries.

    Top-level classes and functions become individual chunks.
    If a node exceeds max_chunk_size, its children (methods) are
    chunked individually. Falls back to hard cut if needed.

    Args:
        file_path: Path to the Python source file.
        text: Full content of the file.
        max_chunk_size: Maximum allowed chunk size in characters.

    Returns:
        List of Chunk objects.
    """
    chunks = []
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []

    lines = text.split("\n")
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line) + 1)

    def hard_cut(start: int, end: int) -> None:
        p_cursor = start
        while p_cursor < end:
            chunk_end = min(p_cursor + max_chunk_size, end)
            chunks.append(Chunk(
                file_path=file_path,
                first_character_index=p_cursor,
                last_character_index=chunk_end,
                text=f"# {file_path}\n{text[p_cursor:chunk_end]}",
                chunk_type="python"
            ))
            p_cursor += max_chunk_size

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef,
                             ast.AsyncFunctionDef, ast.ClassDef)):
            start = offsets[node.lineno - 1]
            assert node.end_lineno is not None
            assert node.end_col_offset is not None
            end = offsets[node.end_lineno - 1] + node.end_col_offset
            if (end - start) <= max_chunk_size:
                chunks.append(Chunk(
                    file_path=file_path,
                    first_character_index=start,
                    last_character_index=end,
                    text=f"# {file_path}\n{text[start:end]}",
                    chunk_type="python"
                ))
            else:
                children = [
                    c for c in ast.iter_child_nodes(node)
                    if isinstance(c, (ast.FunctionDef, ast.AsyncFunctionDef))
                ]
                if children:
                    for child in children:
                        c_start = offsets[child.lineno - 1]
                        assert child.end_lineno is not None
                        assert child.end_col_offset is not None
                        c_end = (offsets[child.end_lineno - 1] +
                                 child.end_col_offset)
                        if (c_end - c_start) <= max_chunk_size:
                            chunks.append(Chunk(
                                file_path=file_path,
                                first_character_index=c_start,
                                last_character_index=c_end,
                                text=f"# {file_path}\n{text[c_start:c_end]}",
                                chunk_type="python"
                            ))
                        else:
                            hard_cut(c_start, c_end)
                else:
                    hard_cut(start, end)
    return chunks


def chunk_markdown(file_path: str, text: str,
                   max_chunk_size: int) -> List[Chunk]:
    """Chunk a Markdown file by heading boundaries.

    Each section (heading + content until the next heading) becomes one chunk.
    Sections exceeding max_chunk_size are split on paragraph boundaries,
    with a hard cut fallback for paragraphs that are still too large.

    Args:
        file_path: Path to the Markdown file.
        text: Full content of the file.
        max_chunk_size: Maximum allowed chunk size in characters.

    Returns:
        List of Chunk objects.
    """
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
                                last_character_index=(local_cursor +
                                                      len(paragraph)),
                                chunk_type="markdown",
                                text=paragraph
                            ))
                        else:
                            p_cursor = 0
                            while p_cursor < len(paragraph):
                                chunk_text = (paragraph[p_cursor:p_cursor +
                                                        max_chunk_size])
                                chunks.append(Chunk(
                                    file_path=file_path,
                                    first_character_index=(local_cursor +
                                                           p_cursor),
                                    last_character_index=(local_cursor +
                                                          p_cursor +
                                                          len(chunk_text)),
                                    text=chunk_text,
                                    chunk_type="markdown"
                                ))
                                p_cursor += max_chunk_size
                    local_cursor += len(paragraph) + 2
            section_start = cursor
            pass
        cursor += len(line) + 1
    if section_start < len(text):
        remaining = text[section_start:]
        if len(remaining) <= max_chunk_size:
            chunks.append(Chunk(
                file_path=file_path,
                first_character_index=section_start,
                last_character_index=len(text),
                text=remaining,
                chunk_type="markdown"
            ))
        else:
            paragraphs = remaining.split("\n\n")
            local_cursor = section_start
            for paragraph in paragraphs:
                if paragraph.strip():
                    if len(paragraph) <= max_chunk_size:
                        chunks.append(Chunk(
                            file_path=file_path,
                            first_character_index=local_cursor,
                            last_character_index=local_cursor + len(paragraph),
                            text=paragraph,
                            chunk_type="markdown"
                        ))
                    else:
                        p_cursor = 0
                        while p_cursor < len(paragraph):
                            chunk_text = (paragraph[p_cursor:p_cursor +
                                                    max_chunk_size])
                            chunks.append(Chunk(
                                file_path=file_path,
                                first_character_index=local_cursor + p_cursor,
                                last_character_index=(local_cursor + p_cursor +
                                                      len(chunk_text)),
                                text=chunk_text,
                                chunk_type="markdown"
                            ))
                            p_cursor += max_chunk_size
                local_cursor += len(paragraph) + 2
    return chunks
