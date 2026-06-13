# RAG

- [ ] Ingest le dossier vllm
    - [ ] Lire tous les fichiers .py et .md
- [ ] et l'indexer en base de données
- [ ] rechercher dans la base de données et extraire le code ou documentation pertinents avec la question (BM25)
- [ ] Répondre a la question en utilisant le LLM en tenant compte du context
- [ ] utiliser le recall ?


fonction chunk_python(file_path, text, max_chunk_size):

    1. parser le texte avec ast.parse(text)

    2. précalculer les offsets de chaque ligne
       → liste où offsets[i] = position caractère du début de la ligne i

    3. pour chaque nœud top-level de l'arbre (classes, fonctions) :
       → calculer start = offsets[node.lineno - 1]
       → calculer end   = offsets[node.end_lineno] 
       
       → si (end - start) <= max_chunk_size :
             créer un chunk directement
         sinon :
             descendre dans les enfants (méthodes de la classe)
             créer un chunk par méthode

    4. retourner la liste de chunks