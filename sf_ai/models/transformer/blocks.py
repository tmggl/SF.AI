"""RMSNorm + SwiGLU + TransformerBlock — sovereign building blocks."""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F

from sf_ai.models.transformer.attention import CausalSelfAttention


class RMSNorm(nn.Module):
    """Root-mean-square layer norm (Zhang & Sennrich, 2019)."""

    def __init__(self, d: int, eps: float = 1e-6) -> None:
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(d))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # rms = sqrt(mean(x^2) + eps)
        rms = x.pow(2).mean(dim=-1, keepdim=True).add(self.eps).rsqrt()
        return self.weight * (x * rms)


class SwiGLU(nn.Module):
    """SwiGLU feed-forward block: F.silu(W1 x) * (W2 x) -> W3."""

    def __init__(self, d_model: int, ff_dim: int) -> None:
        super().__init__()
        self.w_gate = nn.Linear(d_model, ff_dim, bias=False)
        self.w_value = nn.Linear(d_model, ff_dim, bias=False)
        self.w_out = nn.Linear(ff_dim, d_model, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        gate = F.silu(self.w_gate(x))
        value = self.w_value(x)
        return self.w_out(gate * value)


class TransformerBlock(nn.Module):
    """One transformer block: pre-norm attn + pre-norm FFN, both residual."""

    def __init__(
        self,
        d_model: int,
        n_heads: int,
        ff_dim: int,
        dropout: float = 0.0,
        eps: float = 1e-6,
    ) -> None:
        super().__init__()
        self.norm1 = RMSNorm(d_model, eps=eps)
        self.attn = CausalSelfAttention(d_model, n_heads, dropout=dropout)
        self.norm2 = RMSNorm(d_model, eps=eps)
        self.ffn = SwiGLU(d_model, ff_dim)
        self.dropout = nn.Dropout(dropout) if dropout > 0 else nn.Identity()

    def forward(
        self,
        x: torch.Tensor,
        cos: torch.Tensor,
        sin: torch.Tensor,
    ) -> torch.Tensor:
        x = x + self.dropout(self.attn(self.norm1(x), cos, sin))
        x = x + self.dropout(self.ffn(self.norm2(x)))
        return x
