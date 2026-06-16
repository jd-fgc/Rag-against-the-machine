from transformers import AutoTokenizer, AutoModelForCausalLM
from retrieval.searcher import search_query
from pathlib import Path
import torch


def load_model():
    model_name = "Qwen/Qwen3-0.6B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        dtype=torch.float16,
        device_map="cuda"
    )
    return model, tokenizer


def generate_answer(prompt: str, model, tokenizer) -> str:
    inputs = tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt}],
        add_generation_prompt=True,
        enable_thinking=False,
        return_tensors="pt"
    ).to("cuda")
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        do_sample=False,
        repetition_penalty=1.3
    )
    input_length = inputs["input_ids"].shape[1]
    generated_tokens = outputs[0][input_length:]
    response = tokenizer.decode(generated_tokens, skip_special_tokens=True)
    return response.strip()
    return response


def answer_query(query: str, index_dir: str, k: int, index_type: str, model, tokenizer) -> str:
    sources = sources = search_query(query, index_dir, k, index_type)
    context_parts = []
    for source in sources:
        text = Path(source.file_path).read_text(encoding="utf-8", errors="ignore")
        chunk_text = text[source.first_character_index:source.last_character_index]
        context_parts.append(chunk_text)
    context = "\n\n".join(context_parts)
    prompt = f"""Answer the following question based only on the context provided. Be concise.

    Context:
    {context}

    Question: {query}
    Answer:"""
    return generate_answer(prompt, model, tokenizer)


def answer_data_set(student_search_results_path, save_directory):
    


# fonction answer_dataset(student_search_results_path, save_directory):

#     1. charger le modèle une seule fois
#     2. charger le fichier search_results JSON
#     3. pour chaque résultat :
#            récupérer le texte des sources (comme dans answer_query)
#            construire le prompt
#            générer la réponse
#            construire un MinimalAnswer
#     4. construire StudentSearchResultsAndAnswer
#     5. sauvegarder en JSON