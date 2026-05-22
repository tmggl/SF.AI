"""Generation — greedy + temperature/top-k sampling.

Phase 6 doesn't need beam search. Greedy and sampled token-by-token suffice
to verify the training loop on SF-10M experiments. Faster decoding (KV cache)
arrives when training proves the model is worth caching for.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn.functional as F


@dataclass(frozen=True)
class GenerationConfig:
    max_new_tokens: int = 64
    temperature: float = 1.0
    top_k: int = 0          # 0 disables top-k filtering
    eos_token_id: int | None = None

    def __post_init__(self) -> None:
        if self.max_new_tokens < 1:
            raise ValueError("max_new_tokens must be >= 1")
        if self.temperature <= 0:
            raise ValueError("temperature must be > 0")
        if self.top_k < 0:
            raise ValueError("top_k must be >= 0")


@torch.no_grad()
def greedy_generate(model, input_ids: torch.Tensor, config: GenerationConfig) -> torch.Tensor:  # type: ignore[no-untyped-def]
    """Argmax-only generation. Returns the full sequence (prompt + new tokens)."""
    if input_ids.dim() != 2:
        raise ValueError("input_ids must be (B, T)")
    model.eval()
    seq = input_ids
    for _ in range(config.max_new_tokens):
        # Truncate to max_seq_len from the right (keep the most recent tokens).
        ctx = seq[:, -model.config.max_seq_len:]
        logits = model(ctx)
        next_token = logits[:, -1, :].argmax(dim=-1, keepdim=True)
        seq = torch.cat([seq, next_token], dim=1)
        if config.eos_token_id is not None and (next_token == config.eos_token_id).all():
            break
    return seq


@torch.no_grad()
def sample_generate(model, input_ids: torch.Tensor, config: GenerationConfig) -> torch.Tensor:  # type: ignore[no-untyped-def]
    """Temperature + optional top-k sampling. Same return shape as greedy."""
    if input_ids.dim() != 2:
        raise ValueError("input_ids must be (B, T)")
    model.eval()
    seq = input_ids
    for _ in range(config.max_new_tokens):
        ctx = seq[:, -model.config.max_seq_len:]
        logits = model(ctx)[:, -1, :]
        logits = logits / config.temperature

        if config.top_k > 0:
            top_vals, _ = torch.topk(logits, k=config.top_k, dim=-1)
            cutoff = top_vals[..., -1:]
            logits = torch.where(
                logits < cutoff,
                torch.full_like(logits, float("-inf")),
                logits,
            )
        probs = F.softmax(logits, dim=-1)
        next_token = torch.multinomial(probs, num_samples=1)
        seq = torch.cat([seq, next_token], dim=1)
        if config.eos_token_id is not None and (next_token == config.eos_token_id).all():
            break
    return seq
