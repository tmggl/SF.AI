"""Causal self-attention with RoPE — sovereign, written from scratch.

RoPE is implemented inline (no `from_pretrained`, no external utility). The
sin/cos cache is built lazily per (seq_len, head_dim, device) tuple.
"""

from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F


def build_rope_cache(
    seq_len: int, head_dim: int, base: float = 10000.0, device: torch.device | str = "cpu",
) -> tuple[torch.Tensor, torch.Tensor]:
    """Return (cos, sin) of shape (seq_len, head_dim // 2)."""
    if head_dim % 2 != 0:
        raise ValueError("head_dim must be even for RoPE")
    half = head_dim // 2
    inv_freq = 1.0 / (base ** (torch.arange(0, half, dtype=torch.float32, device=device) / half))
    pos = torch.arange(seq_len, dtype=torch.float32, device=device)
    freqs = torch.outer(pos, inv_freq)   # (seq, half)
    return torch.cos(freqs), torch.sin(freqs)


def _rotate_half(x: torch.Tensor) -> torch.Tensor:
    # x has last dim = head_dim; split into even / odd halves and rotate.
    x1, x2 = x.chunk(2, dim=-1)
    return torch.cat((-x2, x1), dim=-1)


def apply_rope(x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
    """Apply RoPE to a (batch, n_heads, seq, head_dim) tensor.

    cos/sin: (seq, head_dim/2). They're broadcast to (1, 1, seq, head_dim).
    """
    # Duplicate to full head_dim so the rotation matches our split.
    cos_full = torch.cat((cos, cos), dim=-1).unsqueeze(0).unsqueeze(0)
    sin_full = torch.cat((sin, sin), dim=-1).unsqueeze(0).unsqueeze(0)
    return (x * cos_full) + (_rotate_half(x) * sin_full)


class CausalSelfAttention(nn.Module):
    """Multi-head causal self-attention with RoPE."""

    def __init__(self, d_model: int, n_heads: int, dropout: float = 0.0) -> None:
        super().__init__()
        if d_model % n_heads != 0:
            raise ValueError("d_model must be divisible by n_heads")
        self.d_model = d_model
        self.n_heads = n_heads
        self.head_dim = d_model // n_heads

        self.qkv_proj = nn.Linear(d_model, 3 * d_model, bias=False)
        self.out_proj = nn.Linear(d_model, d_model, bias=False)
        self.dropout = dropout

    def forward(
        self,
        x: torch.Tensor,            # (B, T, C)
        cos: torch.Tensor,           # (T, head_dim/2)
        sin: torch.Tensor,           # (T, head_dim/2)
    ) -> torch.Tensor:
        B, T, C = x.shape
        qkv = self.qkv_proj(x)        # (B, T, 3C)
        q, k, v = qkv.chunk(3, dim=-1)
        # (B, T, C) -> (B, n_heads, T, head_dim)
        q = q.view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        k = k.view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        v = v.view(B, T, self.n_heads, self.head_dim).transpose(1, 2)

        # RoPE on q, k only (not v).
        q = apply_rope(q, cos, sin)
        k = apply_rope(k, cos, sin)

        # Use the fused scaled-dot-product attention when available (it picks
        # the best backend per device — flash on CUDA, plain SDPA on MPS/CPU).
        attn = F.scaled_dot_product_attention(
            q, k, v,
            attn_mask=None,
            dropout_p=self.dropout if self.training else 0.0,
            is_causal=True,
        )
        # (B, n_heads, T, head_dim) -> (B, T, C)
        out = attn.transpose(1, 2).contiguous().view(B, T, C)
        return self.out_proj(out)
