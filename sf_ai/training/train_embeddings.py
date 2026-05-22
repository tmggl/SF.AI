"""train_embeddings — note for Phase 6.

In SF.AI the model's input embedding IS the embedding training. The
TinyTransformer learns `nn.Embedding(vocab_size, d_model)` jointly with
the rest of the model, and (when `tie_weights=True`) the output projection
shares those same parameters. There is therefore no separate "train
embeddings" step here — it would be redundant.

If a separate encoder is needed later (e.g. for RAG retrieval in Phase 8),
that's a new module trained from scratch on SF.AI corpus, NOT a borrowed
sentence-transformer. See SOVEREIGN_ACCELERATION.md.
"""

from __future__ import annotations

import sys


def main() -> int:
    msg = (
        "SF.AI embeddings live inside TinyTransformer.tok_embed and are trained "
        "jointly with the model. There is no standalone embedding training step "
        "in Phase 6. See sf_ai/training/train_tiny_lm.py.\n\n"
        "If you need a separate sentence encoder later (Phase 8 RAG), it will be "
        "trained from scratch on SF.AI corpus only — never imported."
    )
    print(msg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
