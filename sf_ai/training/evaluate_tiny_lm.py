"""evaluate_tiny_lm — quick perplexity + generation sanity check.

Loads a sovereign checkpoint + tokenizer, streams a small slice of the
corpus, computes average loss/perplexity, and prints a few generated lines
for human inspection.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch

from sf_ai.datasets import ChatDataset
from sf_ai.models.tokenizer import BPETokenizer, CharTokenizer
from sf_ai.models.transformer import (
    GenerationConfig,
    TinyTransformer,
    config_for_size,
    cross_entropy_lm,
    greedy_generate,
    perplexity,
    sample_generate,
)
from sf_ai.modules.chat.native_generator import extract_dialogue_reply
from sf_ai.training.checkpoints import CheckpointManager
from sf_ai.training.device import DeviceManager
from sf_ai.training.train_tiny_lm import iter_token_batches, load_sovereign_tokenizer


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Evaluate SF.AI native LM (Phase 6)")
    p.add_argument("--tokenizer", type=Path, required=True)
    p.add_argument("--corpus", type=Path, required=True)
    p.add_argument("--checkpoints", type=Path, default=Path("artifacts/checkpoints"))
    p.add_argument("--checkpoint-name", type=str, required=True)
    p.add_argument("--size", type=str, default="sf-10m")
    p.add_argument("--seq-len", type=int, default=256)
    p.add_argument("--batch-size", type=int, default=4)
    p.add_argument("--max-batches", type=int, default=20)
    p.add_argument("--device", type=str, default="auto")
    p.add_argument("--prompt", type=str, default="مرحبا")
    p.add_argument("--max-new-tokens", type=int, default=32)
    p.add_argument("--sample", action="store_true",
                   help="Use temperature/top-k sampling instead of greedy")
    p.add_argument("--temperature", type=float, default=1.0)
    p.add_argument("--top-k", type=int, default=20)
    p.add_argument("--stream-format", choices=["dialogue", "messages"], default="dialogue")
    p.add_argument("--chat-prompt", action="store_true",
                   help="Wrap prompt as المستخدم/المساعد dialogue before generation")
    return p.parse_args(argv)


def run(argv: list[str]) -> int:
    args = parse_args(argv)
    device = DeviceManager(preference=args.device).select()
    torch_device = torch.device(device.name)

    tok = load_sovereign_tokenizer(args.tokenizer)
    vocab_size = len(tok)
    cfg = config_for_size(args.size, vocab_size=vocab_size, max_seq_len=args.seq_len)
    model = TinyTransformer(cfg).to(torch_device)

    ckpt_mgr = CheckpointManager(args.checkpoints)
    ckpt_mgr.assert_sovereign(args.checkpoint_name)
    state = ckpt_mgr.load_state(args.checkpoint_name)
    model.load_state_dict(state)
    model.eval()

    dataset = ChatDataset(root=args.corpus)
    if not dataset.jsonl_files():
        print(f"error: corpus at {args.corpus} is empty.", file=sys.stderr)
        return 1

    # Eval loss / perplexity over a small slice.
    losses: list[float] = []
    seen = 0
    with torch.no_grad():
        for inputs, targets in iter_token_batches(
            tok, dataset, batch_size=args.batch_size, seq_len=args.seq_len,
            device=torch_device, stream_format=args.stream_format,
        ):
            logits = model(inputs)
            loss = cross_entropy_lm(logits, targets)
            losses.append(float(loss.cpu()))
            seen += 1
            if seen >= args.max_batches:
                break

    if losses:
        avg = sum(losses) / len(losses)
        ppl = perplexity(avg)
        print(f"batches={len(losses)} | loss={avg:.4f} | perplexity={ppl:.2f}")
    else:
        print("no batches produced — corpus may be too small")

    # A short generation sample.
    prompt = f"المستخدم: {args.prompt}\nالمساعد:" if args.chat_prompt else args.prompt
    prompt_ids = torch.tensor([tok.encode(prompt)], dtype=torch.long, device=torch_device)
    if prompt_ids.numel() == 0:
        print("(prompt produced no tokens — skipping generation)")
        return 0
    gen_cfg = GenerationConfig(max_new_tokens=args.max_new_tokens,
                                temperature=args.temperature, top_k=args.top_k)
    if args.sample:
        out = sample_generate(model, prompt_ids, gen_cfg)
    else:
        out = greedy_generate(model, prompt_ids, gen_cfg)
    decoded = tok.decode(out[0].cpu().tolist())
    if args.chat_prompt:
        decoded = extract_dialogue_reply(decoded, prompt)
    elif decoded.startswith(prompt):
        decoded = decoded[len(prompt):].strip()
    print("\n=== generation ===")
    print(decoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))
