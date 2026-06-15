# RAG

- [X] Ingest le dossier vllm
    - [X] Lire tous les fichiers .py et .md
- [ ] et l'indexer en base de données
- [ ] rechercher dans la base de données et extraire le code ou documentation pertinents avec la question (BM25)
- [ ] Répondre a la question en utilisant le LLM en tenant compte du context
- [ ] utiliser le recall ?


fonction build_indexes(output_dir):

    1. charger les chunks depuis les JSON
       → lire data/processed/chunks/python_chunks.json
       → lire data/processed/chunks/markdown_chunks.json

    2. extraire juste le texte de chaque chunk
       → corpus_python = [chunk["text"] for chunk in python_chunks]
       → corpus_markdown = [chunk["text"] for chunk in markdown_chunks]

    3. construire l'index BM25 pour chaque corpus
       → tokenize le corpus
       → index avec bm25s.BM25()

    4. sauvegarder les deux index sur disque
       → bm25s a une méthode .save() intégrée