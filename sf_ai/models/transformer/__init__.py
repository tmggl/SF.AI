"""sf_ai.models.transformer — Native SF.AI decoder-only transformer (Phase 6).

Architecture (no pretrained anything):
- Decoder-only stack
- RMSNorm pre-norm
- SwiGLU FFN
- Multi-head causal self-attention with RoPE
- Weight tying between input embedding and output projection
- Random initialization (Kaiming / scaled normal)

Everything starts from random weights. There is NO `from_pretrained()`. There
is no way to load external checkpoints into this model — only those produced
by SF.AI's own training loop (Phase 6+).
"""

from sf_ai.models.transformer.attention import CausalSelfAttention, build_rope_cache
from sf_ai.models.transformer.blocks import RMSNorm, SwiGLU, TransformerBlock
from sf_ai.models.transformer.config import (
    SF_MODEL_SIZES,
    TransformerConfig,
    config_for_size,
)
from sf_ai.models.transformer.generation import GenerationConfig, greedy_generate, sample_generate
from sf_ai.models.transformer.losses import cross_entropy_lm, perplexity
from sf_ai.models.transformer.tiny_transformer import TinyTransformer

__all__ = [
    "CausalSelfAttention",
    "GenerationConfig",
    "RMSNorm",
    "SF_MODEL_SIZES",
    "SwiGLU",
    "TinyTransformer",
    "TransformerBlock",
    "TransformerConfig",
    "build_rope_cache",
    "config_for_size",
    "cross_entropy_lm",
    "greedy_generate",
    "perplexity",
    "sample_generate",
]
