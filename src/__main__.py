import os
import time
import fire

def add(x, y):
  return x + y


def multiply(x, y):
  return x * y


def main():
    fire.Fire()


if __name__ == "__main__":
    main()



# import pathlib

# def loader():
#     try:
#         folder_name = "vllm-0.10.1"
#         path = pathlib.Path(folder_name)
#         for file in path.rglob("*"):
#             if file.suffix != ".py" and file.suffix != ".md":
#                 continue
#             file.read_text()
#     except Exception:
        