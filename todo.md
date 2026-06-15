# RAG

- [X] Ingest le dossier vllm
    - [X] Lire tous les fichiers .py et .md
- [X] et l'indexer en base de données
- [ ] rechercher dans la base de données et extraire le code ou documentation pertinents avec la question (BM25)
- [ ] Répondre a la question en utilisant le LLM en tenant compte du context
- [ ] utiliser le recall ?


fonction search_query(query, index_dir, k, index_type):

    1. charger les chunks JSON (python et/ou markdown)
    2. charger les index BM25 sauvegardés
    3. tokenizer la query
    4. faire la recherche → retourne les indices des top-k chunks
    5. utiliser ces indices pour récupérer les vrais chunks
    6. retourner une liste de MinimalSource