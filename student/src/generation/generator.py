from src.models import MinimalAnswer, StudentSearchResultsAndAnswer
from src.retrieval.searcher import search_query
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import Any, Tuple
from pathlib import Path
from tqdm import tqdm
import os
import torch
import json


def load_model() -> Tuple[Any, Any]:
    cache_dir = f"/goinfre/{os.getenv('USER')}/.cache/huggingface"
    model_name = "Qwen/Qwen3-0.6B"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        cache_dir=cache_dir,
        dtype=torch.float16 if device == "cuda" else torch.float32,
        device_map=device
    )
    return model, tokenizer


def generate_answer(prompt: str, model: Any, tokenizer: Any) -> str:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    inputs = tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt}],
        add_generation_prompt=True,
        enable_thinking=False,
        return_tensors="pt"
    ).to(device)
    try:
        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            do_sample=False,
            repetition_penalty=1.3
        )
        input_length = inputs["input_ids"].shape[1]
        generated_tokens = outputs[0][input_length:]
        response = str(tokenizer.decode(generated_tokens,
                                        skip_special_tokens=True))
        return response.strip()
    except Exception as e:
        return f"Generation error: {e}"


def answer_query(query: str, index_dir: str, k: int, index_type: str,
                 model: Any, tokenizer: Any) -> str:
    sources = search_query(query, index_dir, k, index_type)
    context_parts = []
    for source in sources:
        text = Path(source.file_path).read_text(encoding="utf-8",
                                                errors="ignore")
        chunk_text = text[
            source.first_character_index:source.last_character_index]
        context_parts.append(chunk_text)
    context = "\n\n".join(context_parts)
    prompt = (f"""Answer the following question based only on the
 context provided. Be concise.

    Context:
    {context}

    Question: {query}
    Answer:""")
    return generate_answer(prompt, model, tokenizer)


def answer_data_set(student_search_results_path: str,
                    save_directory: str) -> None:
    model, tokenizer = load_model()
    with open(student_search_results_path) as f:
        results_search = json.load(f)
    answers = []
    for result in tqdm(results_search["search_results"],
                       desc="Generating answers"):
        context_parts = []
        for source in result["retrieved_sources"]:
            try:
                file_text = Path(
                    source["file_path"]).read_text(
                        encoding="utf-8", errors="ignore")
                chunk_text = file_text[
                    source["first_character_index"]:source[
                        "last_character_index"]]
                context_parts.append(chunk_text)
            except OSError:
                continue
        context = "\n\n".join(context_parts)
        prompt = (f"""Answer the following question based only on the context
provided. Be concise.

        Context:
        {context}

        Question: {result["question"]}
        Answer:""")
        answer = generate_answer(prompt, model, tokenizer)

        answers.append(MinimalAnswer(
            question_id=result["question_id"],
            question_str=result["question"],
            retrieved_sources=result["retrieved_sources"],
            answer=answer
        ))
    output = StudentSearchResultsAndAnswer(
        search_results=answers,
        k=results_search["k"]
    )
    Path(save_directory).mkdir(parents=True, exist_ok=True)
    output_path = Path(save_directory) / Path(student_search_results_path).name
    with open(output_path, "w") as f:
        f.write(output.model_dump_json(indent=2))
    print(f"Saved to {output_path}")
