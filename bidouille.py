# import bm25s
# import fire
# from transformers import AutoModelForCausalLM, AutoTokenizer
import ast


def main():
    tree = ast.parse('print("hello World")')
    code_obj = compile(tree, filename="<ast>", mode="exec")
    
    exec(code_obj)

    # model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-0.6B")
    # Tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B")
    # txt_encode = Tokenizer.encode("Coucou")


if __name__ == "__main__":
    main()
