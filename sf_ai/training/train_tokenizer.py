"""train_tokenizer — small wrapper around Phase 5.5 BPE trainer.

Keeps a single training entrypoint per phase that lives next to the model
training script. Internally it just calls `train_bpe_from_corpus`.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from sf_ai.models.tokenizer import TokenizerConfig, train_bpe_from_corpus


PHASE12_PERMISSION_ERROR = (
    "Phase 12 tokenizer training requires explicit permission. "
    "Re-run with --confirm-phase12-permission only after Sami says: "
    '"ابدأ Phase 12".'
)
TOKENIZER_PERMISSION_ERROR = (
    "Tokenizer training requires an explicit phase confirmation flag. "
    "Use --confirm-phase12-permission for Phase 12 v1 or "
    "--confirm-phase23-tokenizer for Phase 23 v2."
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Train SF-BPE from SF.AI corpus")
    p.add_argument("--corpus", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--vocab-size", type=int, default=8000)
    p.add_argument("--min-frequency", type=int, default=2)
    p.add_argument("--byte-level", action="store_true")
    p.add_argument("--lowercase", action="store_true")
    p.add_argument("--name", default="sf_bpe")
    p.add_argument(
        "--confirm-phase12-permission",
        action="store_true",
        help=(
            "Required gate: pass only after Sami explicitly approves "
            "starting Phase 12 tokenizer training."
        ),
    )
    p.add_argument(
        "--confirm-phase23-tokenizer",
        action="store_true",
        help=(
            "Required gate for Phase 23 tokenizer v2 retraining after "
            "Phase 22 completion gate passes."
        ),
    )
    return p.parse_args(argv)


def run(argv: list[str]) -> int:
    args = parse_args(argv)
    if not (args.confirm_phase12_permission or args.confirm_phase23_tokenizer):
        print(f"error: {TOKENIZER_PERMISSION_ERROR}", file=sys.stderr)
        return 2

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
