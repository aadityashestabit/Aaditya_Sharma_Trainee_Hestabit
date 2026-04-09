
import torch
import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

def load_model(model_path, quantization=None):
    try:
        if quantization == 'int8':
            config = BitsAndBytesConfig(load_in_8bit=True)
        elif quantization == 'int4':
            config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16
            )
        else:
            config = None

        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            quantization_config=config,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        tokenizer.pad_token = tokenizer.eos_token
        model.eval()
        return model, tokenizer
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None

def generate(model, tokenizer, question, max_new_tokens=100):
    try:
        prompt = (
            f"<|system|>\nYou are a helpful medical assistant.\n"
            f"<|user|>\n{question}\n"
            f"<|assistant|>\n"
        )
        inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
        with torch.no_grad():
            out = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
                use_cache=True
            )
        response = tokenizer.decode(
            out[0][inputs["input_ids"].shape[1]:],
            skip_special_tokens=True
        )
        return response
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path",   required=True,  help="Path to model")
    parser.add_argument("--question",     required=True,  help="Medical question")
    parser.add_argument("--quantization", default=None,   help="int4 or int8 or None")
    parser.add_argument("--max_tokens",   default=100, type=int)
    args = parser.parse_args()

    print(f"Loading model from {args.model_path}...")
    model, tokenizer = load_model(args.model_path, args.quantization)

    if model:
        print(f"Question: {args.question}")
        response = generate(model, tokenizer, args.question, args.max_tokens)
        print(f"Answer  : {response}")
