# import bm25s
# import fire
from transformers import AutoModelForCausalLM, AutoTokenizer


# def add(x, y):
#     return x + y


# def multiply(x, y):
#     return x * y


# def printpopo(mot):
#     return f"c'est le mot : {mot}"


def main():
    text = ("Qu'est-ce que le Lorem Ipsum?"
            ""
            "Le Lorem Ipsum est simplement du faux texte employé dans la composition "
            "et la mise en page avant impression. "
            "Le Lorem Ipsum est le faux texte standard de l'imprimerie depuis les années 1500, "
            "quand un imprimeur anonyme assembla ensemble des morceaux de texte pour réaliser "
            "un livre spécimen de polices de texte. "
            "Il n'a pas fait que survivre cinq siècles, mais s'est aussi adapté "
            "à la bureautique informatique, sans que son contenu n'en soit modifié. "
            "Il a été popularisé dans les années 1960 grâce à la vente de feuilles Letraset "
            "contenant des passages du Lorem Ipsum, et, plus récemment, "
            "par son inclusion dans des applications de mise en page de texte, "
            "comme Aldus PageMaker.")
    txt_parse = ast.parse(text)

    # model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-0.6B")
    # Tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B")
    # txt_encode = Tokenizer.encode("Coucou")

    # print(txt_encode)

    # txt_decode = Tokenizer.decode(txt_encode)
    # print(txt_decode)
    # fire.Fire({
    #     "add": add,
    #     "multiply": multiply,
    #     "popo": printpopo
    # })
    # create corpus / c'est mon chunk
    # corpus = [
    #     "a cat is a feline and likes to purr",
    #     "a dog is the human's best friend and loves to play",
    #     "a bird is a beautiful animal that can fly",
    #     "a fish is a animal who live in the sea",
    #     "Nisalmon is an animal who like is family very much"
    # ]

    # # tokenize le corpus
    # corpus_tokens = bm25s.tokenize(corpus)
    # retriever = bm25s.BM25(corpus=corpus)
    # retriever.index(corpus_tokens)

    # print("Le corpus tokens :/n")
    # print(corpus_tokens)
    # print()
    # print("Retriever :/n")
    # print(retriever.retrieve(bm25s.tokenize("what's Nisalmon like ?"), k=1))
    # print()


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
