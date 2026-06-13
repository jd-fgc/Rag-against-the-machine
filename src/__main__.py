from ingestion.indexer import loader_file
# import os
# import time
# import fire
# import ast


def main():
    try:
        test = loader_file()
        for line in test:
            print(test)
    except Exception:
        raise Exception


if __name__ == "__main__":
    main()
