import bm25s
import fire

# def add(x, y):
#   return x + y


# def multiply(x, y):
#   return x * y

def main():
    # fire.Fire()
    # create corpus / c'est mon chunk
    corpus = [
        "a cat is a feline and likes to purr",
        "a dog is the human's best friend and loves to play",
        "a bird is a beautiful animal that can fly",
        "a fish is a animal who live in the sea",
        "Nisalmon is an animal who like is family very much"
    ]

    # tokenize le corpus
    corpus_tokens = bm25s.tokenize(corpus)
    retriever = bm25s.BM25(corpus=corpus)
    retriever.index(corpus_tokens)

    print("Le corpus tokens :/n")
    print(corpus_tokens)
    print()
    print("Retriever :/n")
    print(retriever.retrieve(bm25s.tokenize("what's Nisalmon like ?"), k=1))
    print()


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
