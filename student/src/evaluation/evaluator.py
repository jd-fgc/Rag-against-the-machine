from typing import Any
import json


def evaluate(student_answer_path: str, dataset_path: str, k: int,
             max_context_length: int) -> None:
    """Evaluate search results against ground truth using recall@k.

    Args:
        student_answer_path: Path to the student search results JSON.
        dataset_path: Path to the answered questions dataset JSON.
        k: Number of retrieved results used.
        max_context_length: Maximum context length used during retrieval.
    """
    try:
        with open(student_answer_path) as f:
            student_data = json.load(f)
        with open(dataset_path) as f:
            ground_truth = json.load(f)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return

    gt_by_id = {}
    for question in ground_truth["rag_questions"]:
        gt_by_id[question["question_id"]] = question["sources"]

    scores = []
    for result in student_data["search_results"]:
        qid = result["question_id"]
        retrieved = result["retrieved_sources"]
        correct = gt_by_id.get(qid, [])
        found = 0
        for gt_source in correct:
            for ret_source in retrieved:
                if has_overlap(gt_source, ret_source):
                    found += 1
                    break
        score = found / len(correct) if correct else 0
        scores.append(score)
    recall = sum(scores) / len(scores) if scores else 0
    print(f"Questions evaluated: {len(scores)}")
    print(f"Recall@{k}: {recall:.3f}")


def has_overlap(gt_source: dict, ret_source: dict) -> Any:
    """Check if a retrieved source overlaps with a ground truth source.

    A source is considered found if there is at least 5% character overlap
    between the retrieved source and the ground truth source.

    Args:
        gt_source: Ground truth source with file_path and character indexes.
        ret_source: Retrieved source with file_path and character indexes.

    Returns:
        True if overlap is at least 5%, False otherwise.
    """
    if gt_source["file_path"] != ret_source["file_path"]:
        return False
    overlap_start = max(gt_source["first_character_index"],
                        ret_source["first_character_index"])
    overlap_end = min(gt_source["last_character_index"],
                      ret_source["last_character_index"])
    if overlap_end <= overlap_start:
        return False
    overlap_length = overlap_end - overlap_start
    gt_length = (gt_source["last_character_index"] -
                 gt_source["first_character_index"])
    return (overlap_length / gt_length) >= 0.05
