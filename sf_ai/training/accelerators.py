"""Accelerator configuration knobs.

Phase 5.5 ships configuration only. The actual integration with torch's
autocast / GradScaler lives in Phase 6 where the training loop is built.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AcceleratorConfig:
    mixed_precision: bool = False                 # bf16/fp16 — start off until verified on MPS
    gradient_accumulation_steps: int = 1
    gradient_checkpointing: bool = False
    grad_clip: float = 1.0

    def __post_init__(self) -> None:
        if self.gradient_accumulation_steps < 1:
            raise ValueError("gradient_accumulation_steps must be >= 1")
        if self.grad_clip <= 0:
            raise ValueError("grad_clip must be > 0")
