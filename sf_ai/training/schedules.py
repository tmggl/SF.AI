"""Learning-rate schedules — pure math, no torch.

Each function takes a step (int) and returns the LR to use at that step.
They never raise; they clamp to safe ranges.
"""

from __future__ import annotations

import math


def constant_with_warmup(step: int, *, warmup_steps: int, lr: float) -> float:
    if warmup_steps <= 0 or step >= warmup_steps:
        return lr
    return lr * (step + 1) / warmup_steps


def linear_warmup_cosine(
    step: int,
    *,
    warmup_steps: int,
    total_steps: int,
    peak_lr: float,
    min_lr: float = 0.0,
) -> float:
    if step < 0:
        step = 0
    if total_steps <= 0:
        return peak_lr
    if step < warmup_steps:
        return peak_lr * (step + 1) / max(warmup_steps, 1)
    progress = (step - warmup_steps) / max(total_steps - warmup_steps, 1)
    progress = min(max(progress, 0.0), 1.0)
    cosine = 0.5 * (1.0 + math.cos(math.pi * progress))
    return min_lr + (peak_lr - min_lr) * cosine


def inverse_sqrt(
    step: int,
    *,
    warmup_steps: int,
    peak_lr: float,
    floor_lr: float = 0.0,
) -> float:
    if step < warmup_steps:
        # Linear warmup to peak.
        return peak_lr * (step + 1) / max(warmup_steps, 1)
    decay = math.sqrt(max(warmup_steps, 1) / max(step, 1))
    return max(peak_lr * decay, floor_lr)
