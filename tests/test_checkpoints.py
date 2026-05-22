"""Phase 5.5 — CheckpointManager + sovereignty enforcement."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from sf_ai.training import CheckpointManager, CheckpointMetadata, SovereigntyError


def test_save_and_load_metadata(tmp_path: Path) -> None:
    mgr = CheckpointManager(root=tmp_path)
    meta = CheckpointMetadata(step=100, epoch=1, model_name="sf-10m")
    ckpt_dir = mgr.save_metadata("step_100", meta)
    assert ckpt_dir.exists()
    assert (ckpt_dir / "meta.json").exists()

    loaded = mgr.load_metadata("step_100")
    assert loaded.step == 100
    assert loaded.epoch == 1
    assert loaded.model_name == "sf-10m"
    assert loaded.sf_origin is True


def test_metadata_rejects_non_sovereign_construction() -> None:
    with pytest.raises(SovereigntyError):
        CheckpointMetadata(step=1, epoch=0, model_name="sf-10m", sf_origin=False)


def test_assert_sovereign_passes_for_sf_origin(tmp_path: Path) -> None:
    mgr = CheckpointManager(root=tmp_path)
    mgr.save_metadata("ok", CheckpointMetadata(step=0, epoch=0, model_name="sf-10m"))
    mgr.assert_sovereign("ok")   # should not raise


def test_assert_sovereign_raises_on_tampered_meta(tmp_path: Path) -> None:
    mgr = CheckpointManager(root=tmp_path)
    mgr.save_metadata("ok", CheckpointMetadata(step=0, epoch=0, model_name="sf-10m"))
    # Tamper with meta on disk.
    meta_path = tmp_path / "ok" / "meta.json"
    data = json.loads(meta_path.read_text(encoding="utf-8"))
    data["sf_origin"] = False
    meta_path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(SovereigntyError):
        mgr.assert_sovereign("ok")


def test_list_checkpoints(tmp_path: Path) -> None:
    mgr = CheckpointManager(root=tmp_path)
    mgr.save_metadata("a", CheckpointMetadata(step=10, epoch=0, model_name="sf-10m"))
    mgr.save_metadata("b", CheckpointMetadata(step=20, epoch=0, model_name="sf-10m"))
    # A directory without meta.json shouldn't be listed.
    (tmp_path / "no_meta").mkdir()
    names = mgr.list_checkpoints()
    assert "a" in names
    assert "b" in names
    assert "no_meta" not in names


def test_load_missing_meta_raises(tmp_path: Path) -> None:
    mgr = CheckpointManager(root=tmp_path)
    with pytest.raises(FileNotFoundError):
        mgr.load_metadata("nope")


def test_save_metadata_refuses_when_state_skipped_sovereign() -> None:
    # Constructing a metadata with sf_origin=False already raises, so
    # save_metadata can't be reached with non-sovereign meta. This double-
    # checks by trying the post-init bypass via dataclasses.
    import dataclasses
    meta = CheckpointMetadata(step=1, epoch=0, model_name="sf-10m")
    # Pydantic doesn't apply; this is a stdlib dataclass. `replace` triggers
    # __post_init__, so this should raise.
    with pytest.raises(SovereigntyError):
        dataclasses.replace(meta, sf_origin=False)
