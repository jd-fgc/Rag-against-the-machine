




# fonction answer_query(query, index_dir, k, index_type):

#     1. récupérer les chunks via search_query()
#     2. construire un contexte = concaténer le texte des chunks
#     3. construire un prompt pour Qwen
#     4. générer la réponse avec le modèle
#     5. retourner la réponse

# Prompt

# Tu es un assistant expert sur vLLM.
# Réponds à la question en te basant uniquement sur le contexte fourni.

# Contexte :
# [tes chunks de texte]

# Question : [la question]
# Réponse :