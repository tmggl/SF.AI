"""train_tokenizer — small wrapper around Phase 5.5 BPE trainer.

Keeps a single training entrypoint per phase that lives next to the model
training script. Internally it just calls `train_bpe_from_corpus`.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from sf_ai.models.tokenizer import TokenizerConfig, train_bpe_from_corpus


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Train SF-BPE from SF.AI corpus")
    p.add_argument("--corpus", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--vocab-size", type=int, default=8000)
    p.add_argument("--min-frequency", type=int, default=2)
    p.add_argument("--byte-level", action="store_true")
    p.add_argument("--lowercase", action="store_true")
    p.add_argument("--name", default="sf_bpe")
    return p.parse_args(argv)


def run(argv: list[str]) -> int:
    args = parse_args(argv)
    cfg = TokenizerConfig(
        vocab_size=args.vocab_size,
        min_frequency=args.min_frequency,
        byte_level=args.byte_level,
        lowercase=args.lowercase,
    )
    try:
        tok = train_bpe_from_corpus(
            corpus_root=args.corpus,
            output_dir=args.out,
            config=cfg,
            name=args.name,
        )
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(f"saved tokenizer at {args.out} (vocab={len(tok)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))
