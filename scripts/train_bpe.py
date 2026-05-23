#!/usr/bin/env python3
"""SF.AI — Train the sovereign SF-BPE tokenizer from your corpus.

Usage:
    python scripts/train_bpe.py \\
        --corpus data/corpus/chat/jsonl \\
        --out artifacts/tokenizers/sf_bpe/v1 \\
        --vocab-size 8000 \\
        --confirm-phase12-permission

REFUSES to start training if the corpus is empty. Place your dialogue data
under data/corpus/chat/jsonl/ first (see docs/DATASET_FORMAT.md).

NEVER load vocab/merges from any external tokenizer. The training produces
SF-origin artifacts only.

Also refuses to start tokenizer training unless the command includes the
explicit phase confirmation flag for the current phase.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.models.tokenizer import (  # noqa: E402
    TokenizerConfig,
    train_bpe_from_corpus,
)
from sf_ai.models.tokenizer.policy_audit import load_plain_terms  # noqa: E402
from sf_ai.training.train_tokenizer import TOKENIZER_PERMISSION_ERROR  # noqa: E402


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Train sovereign SF-BPE tokenizer")
    p.add_argument("--corpus", required=True, help="Path to corpus root (e.g. data/corpus/chat/jsonl)")
    p.add_argument("--out", required=True, help="Output directory for vocab/merges/meta")
    p.add_argument("--vocab-size", type=int, default=8000, help="Target vocab size")
    p.add_argument("--min-frequency", type=int, default=2, help="Drop tokens below this freq")
    p.add_argument("--byte-level", action="store_true", help="Use byte-level base alphabet")
    p.add_argument("--lowercase", action="store_true", help="Lowercase pre-tokenized words")
    p.add_argument("--name", default="sf_bpe", help="Logical name for meta.json")
    p.add_argument(
        "--protected-terms",
        type=Path,
        default=None,
        help="Optional SF.AI-owned protected terms/phrases file; not pretrained vocab.",
    )
    p.add_argument(
        "--confirm-phase12-permission",
        action="store_true",
        help="Required after explicit Sami approval to start Phase 12 tokenizer training",
    )
    p.add_argument(
        "--confirm-phase23-tokenizer",
        action="store_true",
        help="Required to start Phase 23 tokenizer v2 after Phase 22 completion gate",
    )
    args = p.parse_args(argv)

    if not (args.confirm_phase12_permission or args.confirm_phase23_tokenizer):
        print(f"error: {TOKENIZER_PERMISSION_ERROR}", file=sys.stderr)
        return 2

    config = TokenizerConfig(
        vocab_size=args.vocab_size,
        min_frequency=args.min_frequency,
        byte_level=args.byte_level,
        lowercase=args.lowercase,
        protected_terms=tuple(load_plain_terms(args.protected_terms))
        if args.protected_terms
        else (),
    )

    print(f"SF.AI — training BPE tokenizer")
    print(f"  corpus     : {args.corpus}")
    print(f"  output     : {args.out}")
    print(f"  vocab_size : {args.vocab_size}")
    print(f"  byte_level : {args.byte_level}")
    print(f"  protected  : {args.protected_terms or '-'}")

    try:
        tok = train_bpe_from_corpus(
            corpus_root=args.corpus,
            output_dir=args.out,
            config=config,
            name=args.name,
        )
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    stats = tok.stats
    if stats is not None:
        print(
            f"  done: vocab={len(tok)}, merges={stats.merges_learned}, "
            f"words_seen={stats.words_seen}, unique_words={stats.unique_words}"
        )
    print(f"saved to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
