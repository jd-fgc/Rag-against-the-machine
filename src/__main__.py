import fire
from src.cli import StudentCLI


def main():
    try:
        fire.Fire(StudentCLI)
    except Exception:
        raise Exception


if __name__ == "__main__":
    main()
