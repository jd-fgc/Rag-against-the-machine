from pathlib import Path


def loader():
    repo = Path("data/raw/vllm-0.10.1")
    for file_path in repo.rglob("*"):
        if file_path.suffix == ".py":
            # fichier python
        elif file_path.suffix == ".md":
            # fichier markdown