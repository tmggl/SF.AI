"""sf_ai.models.tokenizer — Sovereign tokenizers (Phase 5.5).

Two implementations:
- CharTokenizer: character-level, smallest building block. Useful for the
  earliest experiments (SF-10M smoke tests).
- BPETokenizer: byte-pair encoding trained from SF.AI corpus ONLY. Saves
  vocab + merges + a `meta.json` that records `sf_origin: true` so future
  loaders can refuse non-sovereign artifacts.

NEVER load vocab/merges produced by any external tokenizer. Always train
from your own corpus. See docs/SOVEREIGN_ACCELERATION.md.
"""

from sf_ai.models.tokenizer.bpe_tokenizer import BPETokenizer
from sf_ai.models.tokenizer.char_tokenizer import CharTokenizer
from sf_ai.models.tokenizer.tokenizer_config import TokenizerConfig
from sf_ai.models.tokenizer.train_bpe_tokenizer import train_bpe_from_corpus

__all__ = [
    "BPETokenizer",
    "CharTokenizer",
    "TokenizerConfig",
    "train_bpe_from_corpus",
]
