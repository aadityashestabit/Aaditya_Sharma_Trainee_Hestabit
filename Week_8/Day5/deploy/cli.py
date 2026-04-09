# Usage:
#   Single question:
#     python cli.py "What are the symptoms of diabetes?"
#
#   Interactive chat mode:
#     python cli.py --interactive

import argparse
import sys
from llama_cpp import Llama
import config

def load_model():
    try:
        print(f"Loading model from {config.MODEL_PATH}...")
        model = Llama(
            model_path   = config.MODEL_PATH,
            n_ctx        = config.N_CTX,
            n_threads    = config.N_THREADS,
            n_gpu_layers = config.N_GPU_LAYERS,
            verbose      = False
        )
        print("Model loaded.\n")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)


def build_prompt(messages, system):
    prompt = f"<|system|>\n{system}\n"
    for msg in messages:
        if msg["role"] == "user":
            prompt += f"<|user|>\n{msg['content']}\n"
        elif msg["role"] == "assistant":
            prompt += f"<|assistant|>\n{msg['content']}\n"
    prompt += "<|assistant|>\n"
    return prompt


def ask(model, messages, system, max_tokens, temperature, top_p, top_k):
    try:
        prompt = build_prompt(messages, system)
        output = model(
            prompt,
            max_tokens     = max_tokens,
            temperature    = temperature,
            top_p          = top_p,
            top_k          = top_k,
            repeat_penalty = 1.3,
            stop           = ["<|user|>", "<|system|>"]
        )
        return output["choices"][0]["text"].strip()
    except Exception as e:
        return f"Error: {e}"


def single_question(model, question, args):
    messages = [{"role": "user", "content": question}]
    print("Answer:")
    response = ask(
        model, messages, args.system,
        args.max_tokens, args.temperature, args.top_p, args.top_k
    )
    print(response)


def interactive_mode(model, args):
    print("Medical Assistant - Interactive Mode")
    print("Type 'exit' or 'quit' to stop.")
    print("Type 'clear' to reset conversation history.")
    print("-" * 40)

    messages = []

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("Exiting.")
            break

        if user_input.lower() == "clear":
            messages = []
            print("Conversation cleared.")
            continue

        messages.append({"role": "user", "content": user_input})

        response = ask(
            model, messages, args.system,
            args.max_tokens, args.temperature, args.top_p, args.top_k
        )

        print(f"\nAssistant: {response}")

        # add response to history so next turn has context
        messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Medical LLM CLI")

    parser.add_argument(
        "question",
        nargs   = "?",
        help    = "Single question to ask the model"
    )
    parser.add_argument(
        "--interactive",
        action  = "store_true",
        help    = "Start interactive chat mode"
    )
    parser.add_argument("--system",      default=config.SYSTEM_PROMPT,          help="System prompt")
    parser.add_argument("--max_tokens",  default=config.DEFAULT_MAX_TOKENS,  type=int,   help="Max tokens")
    parser.add_argument("--temperature", default=config.DEFAULT_TEMPERATURE, type=float, help="Temperature")
    parser.add_argument("--top_p",       default=config.DEFAULT_TOP_P,       type=float, help="Top-p")
    parser.add_argument("--top_k",       default=config.DEFAULT_TOP_K,       type=int,   help="Top-k")

    args = parser.parse_args()

    # must provide either a question or --interactive
    if not args.question and not args.interactive:
        parser.print_help()
        sys.exit(1)

    model = load_model()

    if args.interactive:
        interactive_mode(model, args)
    else:
        single_question(model, args.question, args)