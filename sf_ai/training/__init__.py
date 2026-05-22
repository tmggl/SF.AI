"""sf_ai.training — sovereign training infrastructure (Phase 5.5).

Modules:
- device       : select cpu/mps/cuda with safe fallback
- accelerators : mixed-precision + grad accumulation/checkpointing config
- checkpoints  : metadata-first checkpoint manager (sovereign-aware)
- schedules    : pure-math learning-rate schedules
- optimizers   : lazy torch optimizer factory (no torch import at top level)
- training_config : immutable dataclass that locks sovereignty on

Importing this package does NOT import torch. Torch is required only when
you call functions that actually build optimizers or move tensors.
"""

from sf_ai.training.accelerators import AcceleratorConfig
from sf_ai.training.checkpoints import (
    CheckpointManager,
    CheckpointMetadata,
    SovereigntyError,
)
from sf_ai.training.device import DeviceInfo, DeviceManager
from sf_ai.training.schedules import (
    constant_with_warmup,
    inverse_sqrt,
    linear_warmup_cosine,
)
from sf_ai.training.training_config import TrainingConfig

__all__ = [
    "AcceleratorConfig",
    "CheckpointManager",
    "CheckpointMetadata",
    "DeviceInfo",
    "DeviceManager",
    "SovereigntyError",
    "TrainingConfig",
    "constant_with_warmup",
    "inverse_sqrt",
    "linear_warmup_cosine",
]
