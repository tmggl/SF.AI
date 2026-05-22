"""Loss + perplexity helpers for SF.AI native LM.

`cross_entropy_lm` accepts logits of shape (B, T, V) and targets (B, T)
where padding positions are marked with `ignore_index` (defaults to -100).
"""

from __future__ import annotations

import math

import torch
import torch.nn.functional as F


def cross_entropy_lm(
    logits: torch.Tensor,
    targets: torch.Tensor,
    *,
    ignore_index: int = -100,
    label_smoothing: float = 0.0,
) -> torch.Tensor:
    """Standard next-token CE loss. Returns a scalar."""
    if logits.dim() != 3:
        raise ValueError(f"expected logits of shape (B, T, V), got {tuple(logits.shape)}")
    if targets.dim() != 2:
        raise ValueError(f"expected targets of shape (B, T), got {tuple(targets.shape)}")
    B, T, V = logits.shape
    return F.cross_entropy(
        logits.reshape(B * T, V),
        targets.reshape(B * T),
        ignore_index=ignore_index,
        label_smoothing=label_smoothing,
    )


def perplexity(loss: torch.Tensor | float) -> float:
    """Convert a cross-entropy loss to perplexity."""
    if isinstance(loss, torch.Tensor):
        value = float(loss.detach().cpu())
    else:
        value = float(loss)
    # Clamp before exp() so big losses don't overflow to inf in tests/reports.
    return math.exp(min(value, 50.0))
