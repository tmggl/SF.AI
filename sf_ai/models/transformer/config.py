"""TransformerConfig and the SF model-size ladder.

Sizes are tuned for Apple Silicon (M4, 24GB unified). SF-10M is the smoke-test
size; only it should be trained first. Move up the ladder only after data
quality + tokenizer + loop have been validated on the previous tier.

Strict rule (locked by `sovereign=True`): nothing here ever loads external
weights. This dataclass exists ONLY to describe the random-initialized model.
"""

from __future__ import annotations

from dataclasses import dataclass


# Approximate parameter counts under standard SF settings (rounded). Used by
# tests and reports to sanity-check that the random model came out the right
# size — never to validate a "matching" pretrained model.
SF_MODEL_SIZES: dict[str, dict[str, int]] = {
    # name      d_model n_heads n_layers ff_mult
    "sf-10m":   {"d_model": 256,  "n_heads": 4,  "n_layers": 6,  "ff_mult": 4},
    "sf-50m":   {"d_model": 512,  "n_heads": 8,  "n_layers": 8,  "ff_mult": 4},
    "sf-120m":  {"d_model": 768,  "n_heads": 12, "n_layers": 12, "ff_mult": 4},
    "sf-350m":  {"d_model": 1024, "n_heads": 16, "n_layers": 24, "ff_mult": 4},
    "sf-700m":  {"d_model": 1280, "n_heads": 20, "n_layers": 28, "ff_mult": 4},
}


@dataclass(frozen=True)
class TransformerConfig:
    vocab_size: int = 8000
    max_seq_len: int = 1024
    d_model: int = 256
    n_heads: int = 4
    n_layers: int = 6
    ff_mult: int = 4
    dropout: float = 0.0
    rope_base: float = 10000.0
    tie_weights: bool = True
    init_std: float = 0.02
    sovereign: bool = True
    name: str = "sf-10m"

    def __post_init__(self) -> None:
        if not self.sovereign:
            raise ValueError(
                "SF.AI models cannot opt out of sovereignty. sovereign must remain True."
            )
        if self.d_model % self.n_heads != 0:
            raise ValueError(
                f"d_model ({self.d_model}) must be divisible by n_heads ({self.n_heads})"
            )
        if self.head_dim % 2 != 0:
            raise ValueError(
                f"head_dim ({self.head_dim}) must be even for RoPE"
            )
        if self.vocab_size < 16:
            raise ValueError("vocab_size must be >= 16")
        if self.max_seq_len < 8:
            raise ValueError("max_seq_len must be >= 8")
        if self.n_layers < 1:
            raise ValueError("n_layers must be >= 1")
        if self.ff_mult < 1:
            raise ValueError("ff_mult must be >= 1")
        if not (0.0 <= self.dropout < 1.0):
            raise ValueError("dropout must be in [0, 1)")

    @property
    def head_dim(self) -> int:
        return self.d_model // self.n_heads

    @property
    def ff_dim(self) -> int:
        # SwiGLU expects an even-ish hidden size; round to a multiple of 8.
        raw = self.d_model * self.ff_mult
        return (raw + 7) // 8 * 8


def config_for_size(
    name: str,
    *,
    vocab_size: int = 8000,
    max_seq_len: int = 1024,
    dropout: float = 0.0,
) -> TransformerConfig:
    """Build a TransformerConfig for one of the SF.AI size names."""
    if name not in SF_MODEL_SIZES:
        raise ValueError(
            f"unknown SF size {name!r}. choices: {sorted(SF_MODEL_SIZES)}"
        )
    spec = SF_MODEL_SIZES[name]
    return TransformerConfig(
        vocab_size=vocab_size,
        max_seq_len=max_seq_len,
        d_model=spec["d_model"],
        n_heads=spec["n_heads"],
        n_layers=spec["n_layers"],
        ff_mult=spec["ff_mult"],
        dropout=dropout,
        name=name,
    )
