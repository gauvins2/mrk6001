import time
from datetime import datetime as dt
from langchain_ollama import OllamaLLM

def do_ollama(the_prompt, the_model):
    # insert code here
    ollama = OllamaLLM(model=the_model)
    try:
        the_response = ollama.invoke(the_prompt)
    except ollama.OllamaError as e:
        print(f"Error: {e}")
        quit()

    return the_response

if __name__ == "__main__":
    the_models = ["gemma2:27b", "deepseek-r1:32b", "deepseek-r1", "mistral-nemo", "qwen2.5:32b", "phi4"]
    # compute the time it takes to run the code
    # insert code here
    the_prompt_1 = "In this sentence, which animal is faster: The quick brown fox jumps over the lazy dog."
    the_prompt_2 = "Which animal is taller, a giraffe or a mouse?"
    for a_model in the_models:
       
        start_time = time.time()
        the_response = do_ollama(the_prompt_1, a_model)
        end_time = time.time()
        duration_1 = end_time - start_time

        # print(the_response)

        start_time = time.time()
        # run again to see how fast the model can infer, once loaded
        the_response = do_ollama(the_prompt_2, a_model)
        end_time = time.time()
        duration_2 = end_time - start_time
        # print(the_response)
        print('-' * 50)
        print(f"{a_model} -- Time elapsed 1: {duration_1} seconds  -- Time elapsed 2: {duration_2} seconds")
        print('-' * 50)
