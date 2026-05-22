"""Phase 5.5 — TrainingConfig (sovereignty locked, validation)."""

from __future__ import annotations

import dataclasses

import pytest

from sf_ai.training import AcceleratorConfig, TrainingConfig
from sf_ai.training.optimizers import OptimizerSpec


def test_default_config_is_sovereign() -> None:
    cfg = TrainingConfig()
    assert cfg.sovereign is True
    assert cfg.model_name == "sf-10m"
    assert cfg.device == "auto"


def test_cannot_disable_sovereignty() -> None:
    with pytest.raises(ValueError):
        TrainingConfig(sovereign=False)


def test_cannot_disable_sovereignty_via_replace() -> None:
    cfg = TrainingConfig()
    with pytest.raises(ValueError):
        dataclasses.replace(cfg, sovereign=False)


def test_rejects_unknown_model_size() -> None:
    with pytest.raises(ValueError):
        TrainingConfig(model_name="sf-1b")


def test_rejects_bad_numeric_values() -> None:
    with pytest.raises(ValueError):
        TrainingConfig(vocab_size=10)
    with pytest.raises(ValueError):
        TrainingConfig(max_seq_len=1)
    with pytest.raises(ValueError):
        TrainingConfig(batch_size=0)
    with pytest.raises(ValueError):
        TrainingConfig(epochs=0)
    with pytest.raises(ValueError):
        TrainingConfig(device="tpu")


def test_hash_is_stable_and_changes_with_config() -> None:
    a = TrainingConfig(model_name="sf-10m", batch_size=8)
    b = TrainingConfig(model_name="sf-10m", batch_size=8)
    assert a.hash() == b.hash()
    c = TrainingConfig(model_name="sf-10m", batch_size=16)
    assert a.hash() != c.hash()


def test_carries_nested_specs() -> None:
    cfg = TrainingConfig(
        optimizer=OptimizerSpec(lr=1e-3),
        accelerator=AcceleratorConfig(mixed_precision=True),
    )
    assert cfg.optimizer.lr == pytest.approx(1e-3)
    assert cfg.accelerator.mixed_precision is True


def test_to_dict_includes_sovereign_flag() -> None:
    d = TrainingConfig().to_dict()
    assert d["sovereign"] is True
    assert d["model_name"] == "sf-10m"
