"""Phase 14 SF-10M v0.1 report checks."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def test_phase14_report_records_limited_success() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/sf_10m_training_report.json").read_text(
            encoding="utf-8"
        )
    )

    assert report["phase"] == "Phase 14 — SF-10M v0.1 Training Run"
    assert report["status"] == "COMPLETED_WITH_LIMITS"
    assert report["tokenizer"]["path"] == "artifacts/tokenizers/sf_bpe/v1"
    assert report["model"]["random_init"] is True
    assert report["model"]["pretrained_weights_used"] is False
    assert report["training_args"]["steps_requested"] == 80
    assert report["training_args"]["steps_completed"] == 33
    assert report["loss"]["decreased"] is True
    assert report["decision"]["phase14_training_passed"] is True
    assert report["decision"]["suitable_for_chat_runtime"] is False


def test_phase14_generation_sample_documents_repetition_limit() -> None:
    sample = (ROOT / "artifacts/samples/sf_10m_generations.md").read_text(
        encoding="utf-8"
    )
    assert "وش" in sample
    assert "perplexity=59.01" in sample
    assert "must not replace ChatModule" in sample
