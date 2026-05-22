"""Lazy optimizer factory.

Torch is imported inside the factory so importing this module on a torch-less
machine never fails. Phase 6 will exercise these when the training loop lands.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OptimizerSpec:
    name: str = "adamw"
    lr: float = 3.0e-4
    betas: tuple[float, float] = (0.9, 0.95)
    weight_decay: float = 0.1
    eps: float = 1.0e-8

    def __post_init__(self) -> None:
        if self.lr <= 0:
            raise ValueError("lr must be > 0")
        if self.weight_decay < 0:
            raise ValueError("weight_decay must be >= 0")
        if self.name.lower() != "adamw":
            # SF.AI Phase 5.5 only enumerates AdamW. Add more deliberately.
            raise ValueError(f"unsupported optimizer: {self.name!r}")


def build_optimizer(params, spec: OptimizerSpec):  # type: ignore[no-untyped-def]
    """Build a torch optimizer from `spec`. Imports torch only when called."""
    try:
        import torch  # type: ignore[import-not-found]
    except Exception as e:
        raise RuntimeError(
            "torch is required to build optimizers. "
            "Install with `pip install -e \".[training]\"`"
        ) from e
    return torch.optim.AdamW(
        params,
        lr=spec.lr,
        betas=spec.betas,
        weight_decay=spec.weight_decay,
        eps=spec.eps,
    )
