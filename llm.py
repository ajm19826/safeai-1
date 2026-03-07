import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.train import main as train_main
from src.generate import main as generate_main


def run_train():
    print("=== Running training ===")
    train_main()


def run_generate(prompt: str, max_new_tokens: int):
    print("=== Running generation ===")
    sys.argv = [
        "generate",
        "--prompt", prompt,
        "--max_new_tokens", str(max_new_tokens),
    ]
    generate_main()


def main():
    parser = argparse.ArgumentParser(description="125M LLM runner")
    parser.add_argument("--mode", type=str, default="train",
                        choices=["train", "generate"])
    parser.add_argument("--prompt", type=str, default="Hello")
    parser.add_argument("--max_new_tokens", type=int, default=100)

    args = parser.parse_args()

    if args.mode == "train":
        run_train()
    else:
        run_generate(args.prompt, args.max_new_tokens)


if __name__ == "__main__":
    main()
