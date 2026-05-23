"""Tokenizer configuration dataclasses."""

from __future__ import annotations

from dataclasses import dataclass, field

# Default special tokens; order matters — IDs are assigned in this order.
DEFAULT_SPECIAL_TOKENS: tuple[str, ...] = ("<pad>", "<bos>", "<eos>", "<unk>")
# End-of-word marker used during BPE training. Kept ASCII so it round-trips
# through UTF-8 cleanly. Not a special token in the public vocab.
END_OF_WORD: str = "</w>"


@dataclass(frozen=True)
class TokenizerConfig:
    vocab_size: int = 8000
    min_frequency: int = 2
    special_tokens: tuple[str, ...] = field(default_factory=lambda: DEFAULT_SPECIAL_TOKENS)
    lowercase: bool = False           # Arabic is case-insensitive by nature
    protected_terms: tuple[str, ...] = ()
    protected_joiner: str = "▁"
    # If True the tokenizer treats each byte as a base unit (good for code
    # and rare characters). If False, each Unicode codepoint is one base
    # unit. SF.AI defaults to codepoint mode for cleaner Arabic handling.
    byte_level: bool = False

    def __post_init__(self) -> None:
        if self.vocab_size <= len(self.special_tokens):
            raise ValueError("vocab_size must be larger than the special-tokens set")
        if self.min_frequency < 1:
            raise ValueError("min_frequency must be >= 1")
        if not self.protected_joiner or self.protected_joiner.isspace():
            raise ValueError("protected_joiner must be a non-whitespace string")
