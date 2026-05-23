"""train_tiny_lm — SF.AI native LM training scaffold (Phase 6).

THIS DOES NOT RUN TRAINING ON ITS OWN. It builds the model + optimizer +
scheduler + checkpoint manager from a config, exposes a `train_one_step`
helper for testing, and provides a `run()` that streams over a corpus
only when the user supplies a dataset. If the corpus is empty the script
refuses to start — by design.

When the user is ready:

    python sf_ai/training/train_tiny_lm.py \\
        --tokenizer artifacts/tokenizers/sf_bpe/v1 \\
        --corpus data/corpus/chat/jsonl \\
        --size sf-10m --steps 200 --batch-size 4
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections.abc import Iterator
from pathlib import Path

import torch
import torch.nn as nn

from sf_ai.datasets import ChatDataset
from sf_ai.models.tokenizer import BPETokenizer, CharTokenizer
from sf_ai.models.transformer import (
    TinyTransformer,
    config_for_size,
    cross_entropy_lm,
)
from sf_ai.training.checkpoints import CheckpointManager, CheckpointMetadata
from sf_ai.training.device import DeviceManager
from sf_ai.training.optimizers import OptimizerSpec, build_optimizer
from sf_ai.training.schedules import linear_warmup_cosine


def load_sovereign_tokenizer(path: str | Path):  # type: ignore[no-untyped-def]
    """Load a tokenizer artifact; refuse non-sovereign vocab files."""
    p = Path(path)
    meta = p / "meta.json"
    if not meta.exists():
        raise ValueError(f"missing meta.json at {p}; cannot verify sovereignty")
    info = json.loads(meta.read_text(encoding="utf-8"))
    if not info.get("sf_origin", False):
        raise ValueError(f"refusing to load non-sovereign tokenizer at {p}")
    kind = info.get("tokenizer_type", "bpe")
    if kind == "char":
        return CharTokenizer.load(p)
    return BPETokenizer.load(p)


def iter_token_batches(
    tokenizer,
    dataset: ChatDataset,
    *,
    batch_size: int,
    seq_len: int,
    device: torch.device,
    stream_format: str = "dialogue",
) -> Iterator[tuple[torch.Tensor, torch.Tensor]]:
    """Stream (input_ids, targets) batches from a chat corpus."""
    pool: list[int] = []
    texts = (
        dataset.iter_dialogue_texts()
        if stream_format == "dialogue"
        else (msg.content for msg in dataset.iter_messages())
    )
    for text in texts:
        ids = tokenizer.encode(text)
        if not ids:
            continue
        pool.extend(ids)
        while len(pool) >= batch_size * (seq_len + 1):
            chunk = pool[: batch_size * (seq_len + 1)]
            del pool[: batch_size * (seq_len + 1)]
            t = torch.tensor(chunk, dtype=torch.long, device=device)
            t = t.view(batch_size, seq_len + 1)
            yield t[:, :-1], t[:, 1:]


def train_one_step(
    model: TinyTransformer,
    inputs: torch.Tensor,
    targets: torch.Tensor,
    optimizer: torch.optim.Optimizer,
    grad_clip: float = 1.0,
) -> float:
    """One training step. Returns the loss as a float for logging."""
    model.train()
    optimizer.zero_grad(set_to_none=True)
    logits = model(inputs)
    loss = cross_entropy_lm(logits, targets)
    loss.backward()
    if grad_clip and grad_clip > 0:
        nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
    optimizer.step()
    return float(loss.detach().cpu())


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Train SF.AI native LM (Phase 6)")
    p.add_argument("--tokenizer", type=Path, required=True,
                   help="Path to SF-BPE or CharTokenizer artifact (sf_origin=true)")
    p.add_argument("--corpus", type=Path, required=True,
                   help="Root containing *.jsonl chat corpus")
    p.add_argument("--size", type=str, default="sf-10m",
                   help="SF model size (sf-10m / sf-50m / sf-120m / sf-350m / sf-700m)")
    p.add_argument("--seq-len", type=int, default=256)
    p.add_argument("--batch-size", type=int, default=4)
    p.add_argument("--steps", type=int, default=100,
                   help="How many gradient steps to run (Phase 6 starts very small)")
    p.add_argument("--epochs", type=int, default=1,
                   help="Maximum passes over the corpus; use >1 for quality runs")
    p.add_argument("--lr", type=float, default=3e-4)
    p.add_argument("--warmup", type=int, default=20)
    p.add_argument("--min-lr", type=float, default=1e-5)
    p.add_argument("--grad-clip", type=float, default=1.0)
    p.add_argument("--device", type=str, default="auto",
                   choices=["auto", "cpu", "mps", "cuda"])
    p.add_argument("--checkpoints", type=Path,
                   default=Path("artifacts/checkpoints"))
    p.add_argument("--checkpoint-name", type=str, default="sf-10m-step0")
    p.add_argument("--save-every", type=int, default=50)
    p.add_argument("--seed", type=int, default=1337)
    p.add_argument("--stream-format", choices=["dialogue", "messages"], default="dialogue",
                   help="dialogue keeps role-marked samples together; messages preserves legacy flat streaming")
    p.add_argument("--dry-run", action="store_true",
                   help="Build everything but skip the training loop")
    return p.parse_args(argv)


def run(argv: list[str]) -> int:
    args = parse_args(argv)
    torch.manual_seed(args.seed)

    device = DeviceManager(preference=args.device).select()
    print(f"device: {device.name} ({device.notes})")

    tok = load_sovereign_tokenizer(args.tokenizer)
    vocab_size = len(tok)
    print(f"tokenizer: {args.tokenizer} (vocab={vocab_size}) sf_origin=true")

    cfg = config_for_size(args.size, vocab_size=vocab_size, max_seq_len=args.seq_len)
    model = TinyTransformer(cfg)
    print(
        f"model: {cfg.name} d_model={cfg.d_model} n_heads={cfg.n_heads} "
        f"n_layers={cfg.n_layers} params={model.num_parameters():,}"
    )

    dataset = ChatDataset(root=args.corpus)
    if not dataset.jsonl_files():
        print(
            f"error: corpus at {args.corpus} is empty. Place chat data "
            "(Phase 5 format) before training.",
            file=sys.stderr,
        )
        return 1

    if args.dry_run:
        print("dry-run: model + dataset are wired. Skipping training loop.")
        return 0

    torch_device = torch.device(device.name)
    model.to(torch_device)
    optimizer = build_optimizer(model.parameters(), OptimizerSpec(lr=args.lr))

    ckpt_mgr = CheckpointManager(args.checkpoints)

    if args.epochs < 1:
        print("error: --epochs must be >= 1", file=sys.stderr)
        return 2

    step = 0
    started = time.time()
    losses: list[float] = []
    epoch = 0
    for epoch in range(args.epochs):
        produced_in_epoch = 0
        for inputs, targets in iter_token_batches(
            tok,
            dataset,
            batch_size=args.batch_size,
            seq_len=args.seq_len,
            device=torch_device,
            stream_format=args.stream_format,
        ):
            produced_in_epoch += 1
            # Set LR per step.
            lr_now = linear_warmup_cosine(
                step,
                warmup_steps=args.warmup,
                total_steps=args.steps,
                peak_lr=args.lr,
                min_lr=args.min_lr,
            )
            for g in optimizer.param_groups:
                g["lr"] = lr_now

            loss = train_one_step(model, inputs, targets, optimizer, grad_clip=args.grad_clip)
            losses.append(loss)
            step += 1
            if step % max(1, args.steps // 10) == 0 or step == 1:
                print(
                    f"epoch {epoch + 1:>3d} | step {step:>5d} | "
                    f"lr {lr_now:.2e} | loss {loss:.4f}"
                )

            if args.save_every > 0 and step % args.save_every == 0:
                _save(ckpt_mgr, model, args, step, epoch=epoch)

            if step >= args.steps:
                break
        if produced_in_epoch == 0:
            break
        if step >= args.steps:
            break

    elapsed = time.time() - started
    print(f"\nfinished {step} steps in {elapsed:.1f}s | last loss {losses[-1] if losses else 'n/a'}")
    if step > 0:
        _save(ckpt_mgr, model, args, step, epoch=epoch)
    return 0


def _save(ckpt_mgr: CheckpointManager, model: TinyTransformer, args, step: int, *, epoch: int) -> None:  # type: ignore[no-untyped-def]
    name = f"{args.size}-step{step}"
    meta = CheckpointMetadata(
        step=step,
        epoch=epoch + 1,
        model_name=args.size,
        config_hash="",
        notes=(
            f"seed={args.seed} batch={args.batch_size} seq={args.seq_len} "
            f"epochs={args.epochs} stream_format={args.stream_format}"
        ),
    )
    ckpt_mgr.save_metadata(name, meta)
    ckpt_mgr.save_state(name, model.state_dict(), allow_overwrite=True)
    print(f"  saved checkpoint: {name}")


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))
