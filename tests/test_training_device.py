"""Phase 5.5 — DeviceManager + schedules + accelerator/optimizer specs."""

from __future__ import annotations

import math

import pytest

from sf_ai.training import (
    AcceleratorConfig,
    DeviceInfo,
    DeviceManager,
    constant_with_warmup,
    inverse_sqrt,
    linear_warmup_cosine,
)
from sf_ai.training.optimizers import OptimizerSpec


# ---------- DeviceManager ----------

def test_device_manager_rejects_invalid_preference() -> None:
    with pytest.raises(ValueError):
        DeviceManager(preference="tpu")  # type: ignore[arg-type]


def test_device_manager_select_returns_device_info() -> None:
    mgr = DeviceManager(preference="cpu")
    info = mgr.select()
    assert isinstance(info, DeviceInfo)
    assert info.name == "cpu"
    assert info.available is True


def test_device_manager_auto_falls_back_when_torch_missing() -> None:
    mgr = DeviceManager(preference="auto")
    info = mgr.select()
    # On this test machine torch may or may not be installed. Either way,
    # the manager must return a valid DeviceInfo and never crash.
    assert info.name in {"cpu", "mps", "cuda"}
    assert info.available is True


def test_device_manager_explicit_cpu_is_honored() -> None:
    info = DeviceManager(preference="cpu").select()
    assert info.name == "cpu"


def test_device_manager_explicit_cuda_unavailable_falls_back() -> None:
    # On macOS there's no CUDA. The manager should fall back to cpu with a note.
    info = DeviceManager(preference="cuda").select()
    if info.name == "cuda":
        # If we're somehow on a CUDA box, the test still passes.
        assert info.available
    else:
        assert info.name == "cpu"
        assert "cuda" in info.notes.lower() or info.notes


# ---------- schedules ----------

def test_constant_with_warmup() -> None:
    assert constant_with_warmup(0, warmup_steps=10, lr=1e-3) == pytest.approx(1e-4)
    assert constant_with_warmup(5, warmup_steps=10, lr=1e-3) == pytest.approx(6e-4)
    assert constant_with_warmup(20, warmup_steps=10, lr=1e-3) == pytest.approx(1e-3)


def test_linear_warmup_cosine_peaks_then_decays() -> None:
    peak = 1.0
    # During warmup: increases from ~0 to peak.
    warm_mid = linear_warmup_cosine(5, warmup_steps=10, total_steps=100, peak_lr=peak)
    assert 0.0 < warm_mid < peak
    # At end of warmup: should hit peak.
    at_peak = linear_warmup_cosine(9, warmup_steps=10, total_steps=100, peak_lr=peak)
    assert at_peak == pytest.approx(peak, rel=1e-6)
    # At the end: decays to min_lr.
    at_end = linear_warmup_cosine(100, warmup_steps=10, total_steps=100, peak_lr=peak, min_lr=0.1)
    assert at_end == pytest.approx(0.1, rel=1e-6)


def test_inverse_sqrt_warmup_then_decay() -> None:
    peak = 1.0
    at_warmup_end = inverse_sqrt(9, warmup_steps=10, peak_lr=peak)
    assert at_warmup_end == pytest.approx(peak, rel=1e-6)
    later = inverse_sqrt(100, warmup_steps=10, peak_lr=peak)
    assert later == pytest.approx(peak * math.sqrt(10 / 100), rel=1e-6)
    assert later < peak


# ---------- AcceleratorConfig ----------

def test_accelerator_defaults_are_safe() -> None:
    cfg = AcceleratorConfig()
    assert cfg.mixed_precision is False
    assert cfg.gradient_accumulation_steps == 1
    assert cfg.gradient_checkpointing is False


def test_accelerator_rejects_zero_accumulation() -> None:
    with pytest.raises(ValueError):
        AcceleratorConfig(gradient_accumulation_steps=0)


def test_accelerator_rejects_nonpositive_grad_clip() -> None:
    with pytest.raises(ValueError):
        AcceleratorConfig(grad_clip=0.0)


# ---------- OptimizerSpec ----------

def test_optimizer_spec_defaults_to_adamw() -> None:
    spec = OptimizerSpec()
    assert spec.name == "adamw"
    assert spec.lr > 0


def test_optimizer_spec_rejects_unknown_name() -> None:
    with pytest.raises(ValueError):
        OptimizerSpec(name="sgd")


def test_optimizer_spec_rejects_bad_values() -> None:
    with pytest.raises(ValueError):
        OptimizerSpec(lr=0.0)
    with pytest.raises(ValueError):
        OptimizerSpec(weight_decay=-1.0)
