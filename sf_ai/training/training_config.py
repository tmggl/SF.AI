"""TrainingConfig — immutable contract for a SF.AI training run.

`sovereign` is locked to True. Any attempt to construct a config with
`sovereign=False` raises immediately. `validate()` performs extra sanity
checks across the numeric fields.

This file is the single place where someone might be tempted to "just for a
quick experiment" disable sovereignty. The validator prevents that.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field

from sf_ai.training.accelerators import AcceleratorConfig
from sf_ai.training.optimizers import OptimizerSpec


_ALLOWED_SIZES: frozenset[str] = frozenset(
    {"sf-10m", "sf-50m", "sf-120m", "sf-350m", "sf-700m"}
)


@dataclass(frozen=True)
class TrainingConfig:
    model_name: str = "sf-10m"
    vocab_size: int = 8000
    max_seq_len: int = 512
    batch_size: int = 8
    epochs: int = 1
    seed: int = 1337
    device: str = "auto"   # auto | cpu | mps | cuda
    optimizer: OptimizerSpec = field(default_factory=OptimizerSpec)
    accelerator: AcceleratorConfig = field(default_factory=AcceleratorConfig)
    sovereign: bool = True
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.sovereign:
            raise ValueError(
                "SF.AI training cannot opt out of sovereignty "
                "(set sovereign=True; this field cannot be False)"
            )
        if self.model_name not in _ALLOWED_SIZES:
            raise ValueError(
                f"unknown model_name {self.model_name!r}; "
                f"allowed: {sorted(_ALLOWED_SIZES)}"
            )
        if self.vocab_size < 256:
            raise ValueError("vocab_size must be >= 256")
        if self.max_seq_len < 8:
            raise ValueError("max_seq_len must be >= 8")
        if self.batch_size < 1:
            raise ValueError("batch_size must be >= 1")
        if self.epochs < 1:
            raise ValueError("epochs must be >= 1")
        if self.device not in {"auto", "cpu", "mps", "cuda"}:
            raise ValueError(f"invalid device {self.device!r}")

    def hash(self) -> str:
        """Stable hash of the config — used in CheckpointMetadata.config_hash."""
        payload = json.dumps(self.to_dict(), sort_keys=True, ensure_ascii=False)
        return hashlib.blake2b(payload.encode("utf-8"), digest_size=16).hexdigest()

    def to_dict(self) -> dict:
        return asdict(self)
