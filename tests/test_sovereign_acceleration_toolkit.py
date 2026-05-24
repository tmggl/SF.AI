"""Coverage for the sovereign acceleration toolkit loadout."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_acceleration_toolkit_report_is_ready_without_pretrained_shortcuts() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/sovereign_acceleration_toolkit_report.json").read_text(
            encoding="utf-8"
        )
    )
    assert report["status"] == "READY"
    assert report["training_allowed"] is False
    assert report["pretrained_weights_loaded"] is False
    assert report["external_ai_api_used"] is False
    assert report["external_dialogue_data_used"] is False
    assert report["missing_tools"] == []
    assert report["risky_importable_shortcuts"] == []
    for tool in ("torch", "numpy", "tensorboard", "tqdm", "psutil", "safetensors", "rich"):
        assert report["tools"][tool]["installed"] is True


def test_acceleration_toolkit_documents_phase27_80_prerequisite() -> None:
    doc = (ROOT / "docs/SOVEREIGN_ACCELERATION_TOOLKIT_LOADED.md").read_text(encoding="utf-8")
    assert "ليست مرحلة تدريب" in doc
    assert "لا نستخدمها لاستيراد عقل جاهز" in doc
    assert "Phase 27.80" in doc
