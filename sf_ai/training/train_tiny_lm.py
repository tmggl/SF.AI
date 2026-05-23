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
from sf_ai.datasets.chat_dataset import _dialect_condition_lines
from sf_ai.datasets.splits import iter_split_samples
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

ASSISTANT_EOS_TOKEN = "<eos>"


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
    loss_scope: str = "full",
    split_manifest: str | Path | None = None,
    split_name: str = "train",
) -> Iterator[tuple[torch.Tensor, torch.Tensor]]:
    """Stream (input_ids, targets) batches from a chat corpus."""
    pool_ids: list[int] = []
    pool_labels: list[int] = []
    texts = _iter_training_texts(
        dataset,
        stream_format=stream_format,
        split_manifest=split_manifest,
        split_name=split_name,
    )
    for text in texts:
        ids, labels = _encode_training_text(
            tokenizer,
            text,
            stream_format=stream_format,
            loss_scope=loss_scope,
        )
        if not ids or not labels:
            continue
        pool_ids.extend(ids)
        pool_labels.extend(labels)
        while len(pool_ids) >= batch_size * (seq_len + 1):
            need = batch_size * (seq_len + 1)
            id_chunk = pool_ids[:need]
            label_chunk = pool_labels[:need]
            del pool_ids[:need]
            del pool_labels[:need]
            ids_tensor = torch.tensor(id_chunk, dtype=torch.long, device=device)
            labels_tensor = torch.tensor(label_chunk, dtype=torch.long, device=device)
            ids_tensor = ids_tensor.view(batch_size, seq_len + 1)
            labels_tensor = labels_tensor.view(batch_size, seq_len + 1)
            targets = labels_tensor[:, 1:]
            if loss_scope == "assistant" and bool((targets != -100).sum().item() == 0):
                continue
            yield ids_tensor[:, :-1], targets


def _encode_training_text(
    tokenizer,
    text: str,
    *,
    stream_format: str,
    loss_scope: str,
) -> tuple[list[int], list[int]]:
    ids = tokenizer.encode(text)
    if loss_scope == "full" or stream_format != "dialogue":
        return ids, list(ids)
    if loss_scope != "assistant":
        raise ValueError(f"unsupported loss_scope: {loss_scope}")
    return _encode_assistant_target_dialogue(tokenizer, text)


def _iter_training_texts(
    dataset: ChatDataset,
    *,
    stream_format: str,
    split_manifest: str | Path | None = None,
    split_name: str = "train",
) -> Iterator[str]:
    if split_manifest is None:
        if stream_format == "dialogue":
            yield from dataset.iter_dialogue_texts()
        else:
            yield from (msg.content for msg in dataset.iter_messages())
        return

    for sample in iter_split_samples(dataset.root, split_manifest, split_name=split_name):
        messages = sample.messages if hasattr(sample, "messages") else sample.to_messages()
        if stream_format == "dialogue":
            lines: list[str] = []
            lines.extend(_dialect_condition_lines(sample))
            for msg in messages:
                content = msg.content.strip()
                if not content:
                    continue
                if msg.role == "user":
                    lines.append(f"المستخدم: {content}")
                elif msg.role == "assistant":
                    lines.append(f"المساعد: {content}")
                elif msg.role == "system":
                    lines.append(f"النظام: {content}")
            if lines:
                yield "\n".join(lines) + "\n"
        else:
            for msg in messages:
                if msg.content.strip():
                    yield msg.content


def _encode_assistant_target_dialogue(tokenizer, text: str) -> tuple[list[int], list[int]]:
    """Encode dialogue while masking non-assistant target tokens.

    Labels align token-for-token with ids. Later batching shifts labels by one
    position, so the loss only trains predictions whose *target* token belongs
    to assistant content, not the user's prompt or role markers.
    """
    ids: list[int] = []
    labels: list[int] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("المساعد:"):
            prefix = "المساعد:"
            content = line[len(prefix):].strip()
            prefix_ids = tokenizer.encode(prefix)
            content_ids = tokenizer.encode(content)
            ids.extend(prefix_ids)
            labels.extend([-100] * len(prefix_ids))
            ids.extend(content_ids)
            labels.extend(content_ids)
            eos_id = _token_id(tokenizer, ASSISTANT_EOS_TOKEN)
            if eos_id is not None:
                ids.append(eos_id)
                labels.append(eos_id)
        else:
            line_ids = tokenizer.encode(line)
            ids.extend(line_ids)
            labels.extend([-100] * len(line_ids))
    return ids, labels


def _token_id(tokenizer, token: str) -> int | None:  # type: ignore[no-untyped-def]
    """Return a tokenizer special-token ID when available."""
    vocab = getattr(tokenizer, "vocab", None)
    if callable(vocab):
        vocab = vocab()
    if isinstance(vocab, dict):
        value = vocab.get(token)
        return int(value) if value is not None else None
    return None


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
    p.add_argument("--loss-scope", choices=["full", "assistant"], default="full",
                   help="assistant masks user/context tokens and trains only assistant reply tokens")
    p.add_argument("--split-manifest", type=Path, default=None,
                   help="Optional deterministic split manifest produced by build_dialogue_split")
    p.add_argument("--split-name", choices=["train", "eval"], default="train",
                   help="Split to stream when --split-manifest is provided")
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
            loss_scope=args.loss_scope,
            split_manifest=args.split_manifest,
            split_name=args.split_name,
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
            f"epochs={args.epochs} stream_format={args.stream_format} "
            f"loss_scope={args.loss_scope} split={args.split_name if args.split_manifest else 'none'}"
        ),
    )
    ckpt_mgr.save_metadata(name, meta)
    ckpt_mgr.save_state(name, model.state_dict(), allow_overwrite=True)
    print(f"  saved checkpoint: {name}")


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))
