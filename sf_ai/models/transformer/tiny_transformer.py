"""TinyTransformer — SF.AI native decoder-only language model.

Phase 6 model. Always starts from random init. `from_pretrained` does not
exist; loading weights goes through SF.AI's CheckpointManager which itself
refuses any non-sovereign checkpoint.
"""

from __future__ import annotations

from pathlib import Path

import torch
import torch.nn as nn

from sf_ai.models.transformer.attention import build_rope_cache
from sf_ai.models.transformer.blocks import RMSNorm, TransformerBlock
from sf_ai.models.transformer.config import TransformerConfig


class TinyTransformer(nn.Module):
    """Decoder-only transformer with RoPE + RMSNorm + SwiGLU + weight tying."""

    def __init__(self, config: TransformerConfig) -> None:
        super().__init__()
        if not config.sovereign:
            raise ValueError("TinyTransformer requires sovereign config (sovereign=True)")
        self.config = config

        self.tok_embed = nn.Embedding(config.vocab_size, config.d_model)
        self.blocks = nn.ModuleList(
            [
                TransformerBlock(
                    d_model=config.d_model,
                    n_heads=config.n_heads,
                    ff_dim=config.ff_dim,
                    dropout=config.dropout,
                )
                for _ in range(config.n_layers)
            ]
        )
        self.norm_out = RMSNorm(config.d_model)
        if config.tie_weights:
            # Output projection shares parameters with the input embedding.
            self.lm_head = nn.Linear(config.d_model, config.vocab_size, bias=False)
            self.lm_head.weight = self.tok_embed.weight
        else:
            self.lm_head = nn.Linear(config.d_model, config.vocab_size, bias=False)

        # RoPE cache is built lazily on first forward (per device).
        self._rope_seq_len: int = 0
        self._rope_device: torch.device | None = None
        self.register_buffer("rope_cos", torch.empty(0), persistent=False)
        self.register_buffer("rope_sin", torch.empty(0), persistent=False)

        self.apply(self._init_weights)
        # Mark `sf_origin: true` on the module instance so loaders can verify.
        self.sf_origin: bool = True

    # ----- init -----

    def _init_weights(self, module: nn.Module) -> None:
        std = self.config.init_std
        if isinstance(module, nn.Linear):
            nn.init.normal_(module.weight, mean=0.0, std=std)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            nn.init.normal_(module.weight, mean=0.0, std=std)

    # ----- forward -----

    def _ensure_rope(self, seq_len: int, device: torch.device) -> None:
        if seq_len <= self._rope_seq_len and self._rope_device == device:
            return
        cos, sin = build_rope_cache(
            seq_len,
            self.config.head_dim,
            base=self.config.rope_base,
            device=device,
        )
        # Store as non-persistent buffers so they don't go into state_dict.
        self.rope_cos = cos
        self.rope_sin = sin
        self._rope_seq_len = seq_len
        self._rope_device = device

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        if input_ids.dim() != 2:
            raise ValueError(f"expected (B, T) input, got {tuple(input_ids.shape)}")
        B, T = input_ids.shape
        if T > self.config.max_seq_len:
            raise ValueError(
                f"sequence length {T} exceeds max_seq_len {self.config.max_seq_len}"
            )

        self._ensure_rope(T, input_ids.device)
        cos = self.rope_cos[:T]
        sin = self.rope_sin[:T]

        x = self.tok_embed(input_ids)
        for block in self.blocks:
            x = block(x, cos, sin)
        x = self.norm_out(x)
        return self.lm_head(x)

    # ----- info -----

    def num_parameters(self, *, exclude_embedding: bool = False) -> int:
        total = sum(p.numel() for p in self.parameters())
        if exclude_embedding:
            total -= self.tok_embed.weight.numel()
            if not self.config.tie_weights:
                total -= self.lm_head.weight.numel()
        return total

    # ----- save / load (sovereign) -----

    def save_state(self, path: str | Path) -> Path:
        """Save the state_dict only. Pair with CheckpointManager for metadata."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        torch.save(self.state_dict(), p)
        return p

    def load_state(self, path: str | Path, *, strict: bool = True) -> None:
        """Load a state_dict from disk. Refuses if the path looks external."""
        p = Path(path)
        if "huggingface" in str(p).lower() or "pretrained" in str(p).lower():
            raise ValueError(
                f"refusing to load from suspicious path {p!r} — "
                "SF.AI only loads checkpoints produced by SF.AI training."
            )
        state = torch.load(p, map_location="cpu", weights_only=True)
        self.load_state_dict(state, strict=strict)
