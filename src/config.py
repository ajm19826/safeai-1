from dataclasses import dataclass
from pathlib import Path

@dataclass
class ModelConfig:
    vocab_size: int = 32000
    n_embd: int = 768
    n_head: int = 12
    n_layer: int = 12
    block_size: int = 512
    dropout: float = 0.1

    @property
    def approx_params(self) -> int:
        emb = self.vocab_size * self.n_embd + self.block_size * self.n_embd
        per_layer = 12 * (self.n_embd ** 2)
        blocks = per_layer * self.n_layer
        head = self.n_embd * self.vocab_size
        return emb + blocks + head


@dataclass
class TrainConfig:
    data_path: Path = Path("examples/corpus.txt")
    tokenizer_path: Path = Path("checkpoints/tokenizer.json")
    ckpt_dir: Path = Path("checkpoints")
    ckpt_path: Path = Path("checkpoints/llm_125m.pt")

    batch_size: int = 8
    max_iters: int = 50000
    eval_interval: int = 1000
    learning_rate: float = 3e-4
    weight_decay: float = 0.1
    device: str = "cuda"
    seed: int = 42

    block_size: int = 512
    num_workers: int = 2
