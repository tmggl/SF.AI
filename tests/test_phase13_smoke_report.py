"""Phase 13 smoke training report checks."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def test_phase13_smoke_report_records_success_and_limits() -> None:
    report_path = ROOT / "artifacts/reports/smoke_training_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert report["status"] == "COMPLETED_WITH_LIMITS"
    assert report["training_permission"]["granted"] is True
    assert report["tokenizer"]["path"] == "artifacts/tokenizers/sf_bpe/v1"
    assert report["model"]["random_init"] is True
    assert report["model"]["pretrained_weights_used"] is False
    assert report["loss"]["decreased"] is True
    assert report["decision"]["phase13_smoke_training_passed"] is True
    assert report["decision"]["suitable_for_chat_runtime"] is False


def test_phase13_smoke_generation_sample_is_present() -> None:
    sample = (ROOT / "artifacts/samples/smoke_generations.md").read_text(
        encoding="utf-8"
    )
    assert "وش" in sample
    assert "generation is non-empty" in sample
    assert "not wired into ChatModule" in sample
