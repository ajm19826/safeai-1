import torch
from torch import optim
from tqdm import tqdm

from .config import ModelConfig, TrainConfig
from .data import load_or_train_tokenizer, create_dataloaders
from .model import GPTModel


def main():
    train_cfg = TrainConfig()
    model_cfg = ModelConfig()

    torch.manual_seed(train_cfg.seed)
    device = train_cfg.device if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    print(f"Approx params: {model_cfg.approx_params / 1e6:.1f}M")

    tokenizer = load_or_train_tokenizer(train_cfg, model_cfg)
    train_loader, val_loader = create_dataloaders(train_cfg, model_cfg, tokenizer)

    model = GPTModel(model_cfg).to(device)
    optimizer = optim.AdamW(
        model.parameters(),
        lr=train_cfg.learning_rate,
        weight_decay=train_cfg.weight_decay,
    )

    scaler = torch.cuda.amp.GradScaler(enabled=(device == "cuda"))

    best_val_loss = float("inf")
    train_cfg.ckpt_dir.mkdir(parents=True, exist_ok=True)

    for step in tqdm(range(train_cfg.max_iters), desc="Training"):
        model.train()
        for xb, yb in train_loader:
            xb = xb.to(device)
            yb = yb.to(device)

            optimizer.zero_grad(set_to_none=True)
            with torch.cuda.amp.autocast(enabled=(device == "cuda")):
                _, loss = model(xb, yb)

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            break

        if step % train_cfg.eval_interval == 0:
            model.eval()
            with torch.no_grad():
                val_losses = []
                for xb, yb in val_loader:
                    xb = xb.to(device)
                    yb = yb.to(device)
                    _, val_loss = model(xb, yb)
                    val_losses.append(val_loss.item())
                    if len(val_losses) >= 10:
                        break
                mean_val = sum(val_losses) / len(val_losses)
            print(f"\nStep {step}: train loss {loss.item():.4f}, val loss {mean_val:.4f}")

            if mean_val < best_val_loss:
                best_val_loss = mean_val
                ckpt = {
                    "model_state": model.state_dict(),
                    "model_cfg": model_cfg.__dict__,
                    "tokenizer_path": str(train_cfg.tokenizer_path),
                }
                torch.save(ckpt, train_cfg.ckpt_path)
                print(f"Saved checkpoint to {train_cfg.ckpt_path}")

    print("Training finished.")
