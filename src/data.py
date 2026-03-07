import numpy as np
import torch
from pathlib import Path
from torch.utils.data import Dataset, DataLoader
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace

from .config import TrainConfig, ModelConfig


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Corpus not found: {path}")
    return path.read_text(encoding="utf-8")


def train_tokenizer(corpus_path: Path, tokenizer_path: Path, vocab_size: int) -> Tokenizer:
    print(f"Training BPE tokenizer from {corpus_path} with vocab_size={vocab_size}")
    tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
    tokenizer.pre_tokenizer = Whitespace()
    trainer = BpeTrainer(
        vocab_size=vocab_size,
        special_tokens=["[PAD]", "[UNK]", "[BOS]", "[EOS]"],
    )

    with open(corpus_path, "r", encoding="utf-8") as f:
        tokenizer.train_from_iterator(f, trainer=trainer)

    tokenizer.save(str(tokenizer_path))
    return tokenizer


def load_or_train_tokenizer(cfg: TrainConfig, model_cfg: ModelConfig) -> Tokenizer:
    cfg.ckpt_dir.mkdir(parents=True, exist_ok=True)
    if cfg.tokenizer_path.exists():
        print(f"Loading tokenizer from {cfg.tokenizer_path}")
        return Tokenizer.from_file(str(cfg.tokenizer_path))
    else:
        return train_tokenizer(cfg.data_path, cfg.tokenizer_path, model_cfg.vocab_size)


def encode_text(tokenizer: Tokenizer, text: str) -> np.ndarray:
    ids = tokenizer.encode(text).ids
    return np.array(ids, dtype=np.int64)


def decode_ids(tokenizer: Tokenizer, ids: np.ndarray) -> str:
    return tokenizer.decode(ids.tolist())


class TextDataset(Dataset):
    def __init__(self, data_ids: np.ndarray, block_size: int):
        self.data = data_ids
        self.block_size = block_size

    def __len__(self) -> int:
        return max(0, len(self.data) - self.block_size)

    def __getitem__(self, idx: int):
        x = self.data[idx:idx + self.block_size]
        y = self.data[idx + 1:idx + 1 + self.block_size]
        return torch.tensor(x, dtype=torch.long), torch.tensor(y, dtype=torch.long)


def create_dataloaders(cfg: TrainConfig, model_cfg: ModelConfig, tokenizer: Tokenizer):
    text = read_text(cfg.data_path)
    ids = encode_text(tokenizer, text)

    n = int(0.9 * len(ids))
    train_ids = ids[:n]
    val_ids = ids[n:]

    train_ds = TextDataset(train_ids, model_cfg.block_size)
    val_ds = TextDataset(val_ids, model_cfg.block_size)

    train_loader = DataLoader(
        train_ds,
        batch_size=cfg.batch_size,
        shuffle=True,
        num_workers=cfg.num_workers,
        pin_memory=True,
    )
    val_loader = DataLoader(
        val_ds,
        batch_size=cfg.batch_size,
        shuffle=False,
        num_workers=cfg.num_workers,
        pin_memory=True,
    )
    return train_loader, val_loader
