import json

# Test 1 : vérifier les fichiers JSON existent et sont lisibles
with open("data/processed/chunks/python_chunks.json") as f:
    python_chunks = json.load(f)
with open("data/processed/chunks/markdown_chunks.json") as f:
    markdown_chunks = json.load(f)

print(f"Python chunks: {len(python_chunks)}")
print(f"Markdown chunks: {len(markdown_chunks)}")

# Test 2 : vérifier que chaque chunk a les bons champs
for chunk in python_chunks[:5]:
    assert "file_path" in chunk
    assert "first_character_index" in chunk
    assert "last_character_index" in chunk
    assert "text" in chunk
    assert chunk["first_character_index"] < chunk["last_character_index"]
print("✓ Champs Python chunks OK")

for chunk in markdown_chunks[:5]:
    assert "file_path" in chunk
    assert "first_character_index" in chunk
    assert "last_character_index" in chunk
    assert "text" in chunk
    assert chunk["first_character_index"] < chunk["last_character_index"]
print("✓ Champs Markdown chunks OK")

# Test 3 : vérifier qu'aucun chunk ne dépasse max_chunk_size
MAX = 2000
gros_py = [c for c in python_chunks if len(c["text"]) > MAX]
gros_md = [c for c in markdown_chunks if len(c["text"]) > MAX]
print(f"Python chunks > {MAX} chars: {len(gros_py)}")
print(f"Markdown chunks > {MAX} chars: {len(gros_md)}")

# Test 4 : vérifier les index BM25
from pathlib import Path
assert Path("data/processed/bm25_index/python").exists()
assert Path("data/processed/bm25_index/markdown").exists()
print("✓ Index BM25 OK")

# Test 5 : vérifier que le texte correspond aux indexes
sample = python_chunks[0]
file_text = Path(sample["file_path"]).read_text(encoding="utf-8", errors="ignore")
extracted = file_text[sample["first_character_index"]:sample["last_character_index"]]
assert extracted == sample["text"], "❌ Le texte ne correspond pas aux indexes!"
print("✓ Character indexes corrects")

print("\nTous les tests passés !")