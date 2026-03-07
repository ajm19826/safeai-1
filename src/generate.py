import argparse
import torch
from pathlib import Path
from tokenizers import Tokenizer

from .config import ModelConfig
from .model import GPTModel
from .data import encode_text, decode_ids


def load_checkpoint(path: Path):
    ckpt = torch.load(path, map_location="cpu")
    cfg = ModelConfig(**ckpt["model_cfg"])
    model = GPTModel(cfg)
    model.load_state_dict(ckpt["model_state"])
    model.eval()
    tokenizer = Tokenizer.from_file(ckpt["tokenizer_path"])
    return model, tokenizer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ckpt", type=str, default="checkpoints/llm_125m.pt")
    parser.add_argument("--prompt", type=str, default="Hello")
    parser.add_argument("--max_new_tokens", type=int, default=100)
    args = parser.parse_args()

    ckpt_path = Path(args.ckpt)
    if not ckpt_path.exists():
        raise FileNotFoundError(f"Checkpoint not found: {ckpt_path}")

    model, tokenizer = load_checkpoint(ckpt_path)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    prompt_ids = encode_text(tokenizer, args.prompt)
    prompt_tensor = torch.tensor(prompt_ids, dtype=torch.long).unsqueeze(0).to(device)

    with torch.no_grad():
        out = model.generate(prompt_tensor, max_new_tokens=args.max_new_tokens)

    out_ids = out[0].cpu().numpy()
    text = decode_ids(tokenizer, out_ids)
    print(text)
