import fire
from src.cli import StudentCLI


def main() -> None:
    """Entry point for the RAG against the machine CLI.

    Usage:
        uv run --active python -m src index
        uv run --active python -m src search "How does vLLM handle batching?"
        uv run --active python -m src answer "How does vLLM handle batching?"
        uv run --active python -m src search_dataset \
            --dataset_path data/datasets/...
        uv run --active python -m src answer_dataset \
            --student_search_results_path ...
        uv run --active python -m src evaluate \
            --student_answer_path ... --dataset_path ...
    """
    try:
        fire.Fire(StudentCLI)
    except KeyboardInterrupt:
        print("\nInterrupted.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
