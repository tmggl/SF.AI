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
    no_repeat_ngram_size: int = 0
    repetition_penalty: float = 1.0

    def __post_init__(self) -> None:
        if self.max_new_tokens < 1:
            raise ValueError("max_new_tokens must be >= 1")
        if self.temperature <= 0:
            raise ValueError("temperature must be > 0")
        if self.top_k < 0:
            raise ValueError("top_k must be >= 0")
        if self.no_repeat_ngram_size < 0:
            raise ValueError("no_repeat_ngram_size must be >= 0")
        if self.repetition_penalty < 1.0:
            raise ValueError("repetition_penalty must be >= 1.0")


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
        next_logits = _apply_decoding_controls(logits[:, -1, :], seq, config)
        next_token = next_logits.argmax(dim=-1, keepdim=True)
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
        logits = _apply_decoding_controls(logits, seq, config)

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


def _apply_decoding_controls(
    logits: torch.Tensor,
    seq: torch.Tensor,
    config: GenerationConfig,
) -> torch.Tensor:
    out = logits.clone()
    if config.repetition_penalty > 1.0:
        _apply_repetition_penalty_(out, seq, config.repetition_penalty)
    if config.no_repeat_ngram_size > 0:
        _apply_no_repeat_ngram_(out, seq, config.no_repeat_ngram_size)
    return out


def _apply_repetition_penalty_(
    logits: torch.Tensor,
    seq: torch.Tensor,
    penalty: float,
) -> None:
    for row_idx in range(seq.shape[0]):
        seen = set(int(x) for x in seq[row_idx].detach().cpu().tolist())
        for token_id in seen:
            value = logits[row_idx, token_id]
            logits[row_idx, token_id] = value / penalty if value > 0 else value * penalty


def _apply_no_repeat_ngram_(
    logits: torch.Tensor,
    seq: torch.Tensor,
    ngram_size: int,
) -> None:
    if ngram_size <= 0:
        return
    if seq.shape[1] < ngram_size - 1:
        return
    for row_idx in range(seq.shape[0]):
        tokens = [int(x) for x in seq[row_idx].detach().cpu().tolist()]
        banned = _banned_next_tokens(tokens, ngram_size)
        if banned:
            logits[row_idx, list(banned)] = float("-inf")


def _banned_next_tokens(tokens: list[int], ngram_size: int) -> set[int]:
    if ngram_size == 1:
        return set(tokens)
    if len(tokens) < ngram_size - 1:
        return set()
    prefix = tuple(tokens[-(ngram_size - 1):])
    banned: set[int] = set()
    for idx in range(0, len(tokens) - ngram_size + 1):
        ngram = tuple(tokens[idx:idx + ngram_size])
        if ngram[:-1] == prefix:
            banned.add(ngram[-1])
    return banned
