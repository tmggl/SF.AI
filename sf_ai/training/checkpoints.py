"""CheckpointManager — metadata-first, sovereign-aware.

A SF.AI checkpoint is a directory containing at minimum a `meta.json`. The
actual model state (`state.pt` etc.) is optional from the manager's point
of view — Phase 6 will save it via torch. The manager guarantees:

- `sf_origin: true` on every saved meta.
- `assert_sovereign(name)` refuses anything missing the flag.
- Listing/loading helpers that never load weights silently.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path


class SovereigntyError(RuntimeError):
    """Raised when a checkpoint cannot be confirmed as SF.AI-origin."""


@dataclass
class CheckpointMetadata:
    step: int
    epoch: int
    model_name: str                       # e.g. "sf-10m" / "sf-50m"
    sf_origin: bool = True                # immutable: SF.AI checkpoints only
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    training_data_hash: str = ""          # blake2b over corpus file digests
    config_hash: str = ""                 # hash of TrainingConfig serialization
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.sf_origin:
            raise SovereigntyError(
                "SF.AI checkpoints cannot opt out of sovereignty "
                "(sf_origin must be True)"
            )


class CheckpointManager:
    META_FILE = "meta.json"
    STATE_FILE = "state.pt"

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    # ----- save / load (metadata) -----

    def save_metadata(self, name: str, meta: CheckpointMetadata) -> Path:
        if not meta.sf_origin:
            raise SovereigntyError("refusing to save non-sovereign checkpoint")
        ckpt_dir = self.root / name
        ckpt_dir.mkdir(parents=True, exist_ok=True)
        (ckpt_dir / self.META_FILE).write_text(
            json.dumps(asdict(meta), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return ckpt_dir

    def load_metadata(self, name: str) -> CheckpointMetadata:
        ckpt_dir = self.root / name
        meta_path = ckpt_dir / self.META_FILE
        if not meta_path.exists():
            raise FileNotFoundError(f"no meta.json at {ckpt_dir}")
        raw = json.loads(meta_path.read_text(encoding="utf-8"))
        meta = CheckpointMetadata(
            step=int(raw.get("step", 0)),
            epoch=int(raw.get("epoch", 0)),
            model_name=str(raw.get("model_name", "")),
            sf_origin=bool(raw.get("sf_origin", False)),
            created_at=str(raw.get("created_at", "")),
            training_data_hash=str(raw.get("training_data_hash", "")),
            config_hash=str(raw.get("config_hash", "")),
            notes=str(raw.get("notes", "")),
        )
        return meta

    # ----- sovereignty -----

    def assert_sovereign(self, name: str) -> None:
        meta = self.load_metadata(name)
        if not meta.sf_origin:
            raise SovereigntyError(
                f"checkpoint {name!r} is not marked sf_origin=true"
            )

    # ----- listing -----

    def list_checkpoints(self) -> list[str]:
        if not self.root.exists():
            return []
        names: list[str] = []
        for d in sorted(self.root.iterdir()):
            if d.is_dir() and (d / self.META_FILE).exists():
                names.append(d.name)
        return names

    # ----- state (optional — torch) -----

    def save_state(self, name: str, state_dict: dict, *, allow_overwrite: bool = False) -> Path:  # type: ignore[no-untyped-def]
        try:
            import torch  # type: ignore[import-not-found]
        except Exception as e:
            raise RuntimeError(
                "torch is required to save state. Install with [training] extras."
            ) from e
        ckpt_dir = self.root / name
        if not ckpt_dir.exists():
            raise FileNotFoundError(
                f"no checkpoint directory {ckpt_dir}. Call save_metadata first."
            )
        state_path = ckpt_dir / self.STATE_FILE
        if state_path.exists() and not allow_overwrite:
            raise FileExistsError(f"{state_path} exists; set allow_overwrite=True to replace")
        # Mark on disk that this state belongs to SF.AI before writing.
        self.assert_sovereign(name)
        torch.save(state_dict, state_path)
        return state_path

    def load_state(self, name: str):  # type: ignore[no-untyped-def]
        try:
            import torch  # type: ignore[import-not-found]
        except Exception as e:
            raise RuntimeError(
                "torch is required to load state. Install with [training] extras."
            ) from e
        self.assert_sovereign(name)
        state_path = self.root / name / self.STATE_FILE
        if not state_path.exists():
            raise FileNotFoundError(f"no state file at {state_path}")
        return torch.load(state_path, map_location="cpu")
