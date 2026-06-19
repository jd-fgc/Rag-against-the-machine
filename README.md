*This project has been created as part of the 42 curriculum by jduviau.*

# RAG against the machine

## Description

This project implements a **Retrieval-Augmented Generation (RAG)** system that can answer questions about the vLLM codebase. The system indexes the vLLM repository, retrieves relevant code snippets and documentation for any given question, and generates accurate natural language answers using a local LLM (Qwen/Qwen3-0.6B).

The goal is to demonstrate that a small, efficient RAG pipeline can outperform a standalone LLM on domain-specific questions by grounding answers in retrieved source material rather than relying on potentially outdated model knowledge.

## System Architecture

The pipeline consists of four main components that work in sequence:

```
vLLM Repository
      ↓
[Ingestion & Chunking]  →  chunks saved to data/processed/chunks/
      ↓
[BM25 Indexing]         →  indexes saved to data/processed/bm25_index/
      ↓
[Retrieval]             →  top-k chunks retrieved for a query
      ↓
[Answer Generation]     →  Qwen3-0.6B generates answer from context
```

**Ingestion** (`src/ingestion/`): Reads all `.py` and `.md` files from the vLLM repository, applies file-type-specific chunking strategies, and saves chunks as JSON.

**Indexing** (`src/ingestion/indexer.py`): Builds two separate BM25 indexes — one for Python code chunks and one for Markdown documentation chunks — using the `bm25s` library.

**Retrieval** (`src/retrieval/searcher.py`): Loads the pre-built BM25 indexes and retrieves the top-k most relevant chunks for a given query. Each result includes `file_path`, `first_character_index`, and `last_character_index` for precise source tracking.

**Answer Generation** (`src/generation/generator.py`): Loads Qwen/Qwen3-0.6B via HuggingFace Transformers, builds a prompt from the retrieved context, and generates a concise, grounded answer.

## Chunking Strategy

Two distinct chunking strategies are implemented depending on file type:

**Python files (AST-based chunking)**

Python files are parsed using Python's built-in `ast` module. Each top-level class and function becomes a separate chunk. If a node exceeds `max_chunk_size` (default: 2000 characters), its child methods are chunked individually. This preserves semantic boundaries — a chunk always corresponds to a complete, meaningful unit of code rather than an arbitrary slice.

Character positions (`first_character_index`, `last_character_index`) are computed by pre-calculating line offsets and using `node.lineno` / `node.end_lineno` from the AST.

**Markdown files (heading-based chunking)**

Markdown files are split on heading boundaries (`#`, `##`, `###`). Each section (heading + content until the next heading) becomes one chunk. If a section exceeds `max_chunk_size`, it is further split on paragraph boundaries (`\n\n`). If individual paragraphs still exceed the limit, a hard cut is applied.

**Chunk size impact**

- Too small: chunks lose context, BM25 has fewer keywords to match on, retrieval quality drops.
- Too large: chunks become noisy, the relevant signal is diluted, and the LLM context window fills up with irrelevant content.
- 2000 characters is a good balance for vLLM's codebase: most functions fit in one chunk, and sections are semantically coherent.

## Retrieval Method

**BM25 (Best Match 25)** via the `bm25s` library.

BM25 is a probabilistic ranking function that scores documents based on the frequency of query terms within each document, normalized by document length. It rewards chunks where query terms appear frequently relative to the overall corpus frequency — rare, specific terms score higher than common words.

Two separate indexes are maintained:
- `data/processed/bm25_index/python/` for code chunks
- `data/processed/bm25_index/markdown/` for documentation chunks

At query time, the query is tokenized and scored against the relevant index (or both). The top-k scoring chunks are returned as `MinimalSource` objects.

BM25 was chosen over TF-IDF because it handles term saturation better (diminishing returns for repeated terms) and normalizes for document length, which is important given the variable size of code chunks.

## Performance Analysis

Results on the public dataset (100 questions each):

| Dataset | Recall@5 | Recall@10 | Recall@20 |
|---------|----------|-----------|-----------|
| Docs    | ~0.80    | ~0.84     | ~0.84     |
| Code    | TBD      | TBD       | TBD       |

The docs dataset exceeds the 80% Recall@5 threshold. The two-index approach (separate Python and Markdown indexes) significantly improves precision compared to a single unified index.

**Performance constraints met:**
- Indexing time: ~2 seconds (well under 5 minutes)
- Cold start latency: ~3 seconds (under 60 seconds)
- Warm retrieval: under 90 seconds for 1000 questions

## Design Decisions

**Two separate BM25 indexes** — Code and documentation have very different vocabulary. A unified index would cause documentation terms to compete with code identifiers. Separating them allows the retrieval to be tuned per dataset type.

**AST-based Python chunking** — Fixed-size character splitting would cut functions in half, breaking semantic units. AST parsing ensures chunks are always syntactically complete.

**Qwen/Qwen3-0.6B** — Small enough to run on a single consumer GPU (GTX 1650, 4GB VRAM) in float16, fast enough for batch answer generation. The model is loaded once and reused across all questions in `answer_dataset`.

**GPU/CPU auto-detection** — `load_model()` automatically detects CUDA availability and adjusts dtype accordingly (`float16` on GPU, `float32` on CPU), ensuring compatibility across machines.

**Lazy imports in CLI** — Each CLI command imports only what it needs. This means `uv run python -m src search` does not import torch or load any model, keeping startup time minimal for retrieval-only operations.

## Challenges Faced

**Duplicate files via symlinks** — `pathlib.rglob()` follows symlinks and returned the same files multiple times. Fixed by tracking resolved paths in a `seen` set using `file_path.resolve()`.

**Qwen3 thinking mode** — Qwen3 defaults to a chain-of-thought "thinking" mode that produces verbose, structured outputs unsuitable for direct answers. Fixed by passing `enable_thinking=False` to `apply_chat_template()`.

**Character index tracking in chunking** — The sujet requires precise `first_character_index` / `last_character_index` per chunk. AST nodes provide line numbers, not character positions. Solved by pre-computing a line offset table from the raw file content.

**Large Markdown sections** — Some vLLM documentation sections exceed 10,000 characters with no paragraph breaks (mostly code blocks). Handled with a fallback hard cut after paragraph splitting.

## Instructions

### Requirements

- Python 3.10+
- `uv` package manager
- GPU recommended (GTX 1650 or better, 4GB VRAM minimum) — CPU also supported

### Installation

```bash
git clone <repo>
cd <repo>
uv sync
```

Place the vLLM repository at `data/raw/vllm-0.10.1/` and datasets at `data/datasets/`.

### Usage

**Index the repository** (run once):
```bash
uv run --active python -m src index
uv run --active python -m src index --max_chunk_size 2000
```

**Search for a single query:**
```bash
uv run --active python -m src search "How to configure OpenAI server?" --k 10
```

**Process a full dataset:**
```bash
uv run --active python -m src search_dataset --dataset_path data/datasets/UnansweredQuestions/dataset_docs_public.json --k 10 --save_directory data/output/search_results
```

**Answer a single question:**
```bash
uv run --active python -m src answer "How does vLLM handle batching?" --k 10
```

**Generate answers for a dataset:**
```bash
uv run --active python -m src answer_dataset --student_search_results_path data/output/search_results/dataset_docs_public.json
```

**Evaluate retrieval quality:**
```bash
uv run --active python -m src evaluate --student_answer_path data/output/search_results/dataset_docs_public.json --dataset_path data/datasets/AnsweredQuestions/dataset_docs_public.json --k 10
```

## Resources

- [BM25S library](https://github.com/xhluca/bm25s) — Fast BM25 implementation used for indexing and retrieval
- [Qwen3 model card](https://huggingface.co/Qwen/Qwen3-0.6B) — Default LLM used for answer generation
- [Python AST documentation](https://docs.python.org/3/library/ast.html) — Used for intelligent Python code chunking
- [RAG survey paper](https://arxiv.org/abs/2312.10997) — Overview of RAG architectures and techniques
- [vLLM repository](https://github.com/vllm-project/vllm) — The knowledge base indexed by this system

### AI Usage

Claude (Anthropic) was used throughout this project as a learning assistant and pair programmer:
- Explaining RAG concepts, BM25 algorithm, and AST parsing
- Helping debug issues (symlink duplicates, Qwen thinking mode, character index tracking)
- Reviewing code structure and suggesting improvements