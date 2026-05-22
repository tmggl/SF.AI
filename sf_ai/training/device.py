"""DeviceManager — pick an accelerator with sovereign-friendly fallback.

Priority order is configurable; default is "auto" which tries mps → cuda → cpu.
Torch is imported lazily so the SF.AI core remains importable on machines
without it. When torch is missing every selection falls through to "cpu"
with a note explaining the situation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DeviceInfo:
    name: str       # "cpu" | "mps" | "cuda"
    available: bool
    notes: str = ""


_VALID = {"auto", "cpu", "mps", "cuda"}


def _torch_available() -> bool:
    try:
        import torch  # noqa: F401

        return True
    except Exception:
        return False


class DeviceManager:
    """Sovereign-aware accelerator selector. No model knowledge here."""

    def __init__(self, preference: str = "auto") -> None:
        if preference not in _VALID:
            raise ValueError(
                f"invalid device preference {preference!r}; "
                f"expected one of {sorted(_VALID)}"
            )
        self.preference = preference

    # ----- internals -----

    def _mps_available(self) -> bool:
        try:
            import torch  # type: ignore[import-not-found]
        except Exception:
            return False
        return bool(getattr(torch.backends, "mps", None) and torch.backends.mps.is_available())

    def _cuda_available(self) -> bool:
        try:
            import torch  # type: ignore[import-not-found]
        except Exception:
            return False
        return bool(torch.cuda.is_available())

    # ----- public -----

    def is_torch_available(self) -> bool:
        return _torch_available()

    def select(self) -> DeviceInfo:
        if not self.is_torch_available():
            return DeviceInfo(
                name="cpu",
                available=True,
                notes=(
                    "torch not installed — falling back to cpu. "
                    "Install with `pip install -e \".[training]\"` for mps/cuda."
                ),
            )

        if self.preference == "cpu":
            return DeviceInfo(name="cpu", available=True, notes="forced by preference")

        if self.preference in {"auto", "mps"} and self._mps_available():
            return DeviceInfo(name="mps", available=True, notes="Apple Silicon GPU")

        if self.preference in {"auto", "cuda"} and self._cuda_available():
            return DeviceInfo(name="cuda", available=True, notes="NVIDIA CUDA")

        # Preference was explicit but unavailable → fall back to cpu with note.
        if self.preference == "mps":
            return DeviceInfo(
                name="cpu",
                available=True,
                notes="mps requested but unavailable on this machine",
            )
        if self.preference == "cuda":
            return DeviceInfo(
                name="cpu",
                available=True,
                notes="cuda requested but unavailable on this machine",
            )

        return DeviceInfo(name="cpu", available=True, notes="default")
