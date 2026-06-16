
def 


# inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
# outputs = model.generate(
#     **inputs,
#     max_new_tokens=200,
#     do_sample=False
# )
# response = tokenizer.decode(outputs[0], skip_special_tokens=True)
# Le flux c'est :
# prompt (str) → tokenizer → tenseurs → model.generate → tokens → tokenizer.decode → réponse (str)

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