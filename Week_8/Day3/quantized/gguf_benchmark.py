from llama_cpp import Llama
import time

llm = Llama(model_path="model.gguf", n_threads=4, verbose=False, n_ctx=2048)

# use the same chat format as training
prompt = """<|system|>
You are a helpful medical assistant.
<|user|>
What are the symptoms of diabetes?
<|assistant|>
"""

start     = time.time()
out       = llm(prompt, max_tokens=100, stop=["<|user|>"])
elapsed   = round(time.time() - start, 2)
tokens    = out['usage']['completion_tokens']
tok_per_s = round(tokens / elapsed, 2)

print(f'Tokens generated : {tokens}')
print(f'Time taken       : {elapsed}s')
print(f'Speed            : {tok_per_s} tok/s')
print(f'Response         : {out["choices"][0]["text"]}')