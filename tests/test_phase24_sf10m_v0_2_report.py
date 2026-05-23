"""Phase 24 SF-10M v0.2 training report checks."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "artifacts/reports/sf_10m_v0_2_training_report.json"
SAMPLES = ROOT / "artifacts/samples/sf_10m_v0_2_generations.md"
DOC = ROOT / "docs/PHASE24_SF10M_V0_2_REPORT.md"


def test_phase24_report_records_quality_training_with_runtime_blocked() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert report["phase"] == "Phase 24 — SF-10M v0.2 Quality Training"
    assert report["status"] == "COMPLETED_WITH_LIMITS_RUNTIME_BLOCKED"
    assert report["tokenizer"]["path"] == "artifacts/tokenizers/sf_bpe/v2"
    assert report["tokenizer"]["sf_origin"] is True
    assert report["tokenizer"]["pretrained_tokenizer_used"] is False
    assert report["tokenizer"]["pretrained_vocab_used"] is False
    assert report["corpus"]["records"] == 500
    assert report["corpus"]["dialects"] == {"msa": 250, "saudi": 250}
    assert report["corpus"]["synthetic_llm_data_used"] is False
    assert report["model"]["random_init"] is True
    assert report["model"]["pretrained_weights_used"] is False
    assert report["model"]["external_llm_used"] is False
    assert report["training_args"]["steps_completed"] == 2000
    assert report["training_args"]["epochs"] == 25
    assert report["loss"]["decreased"] is True
    assert report["decision"]["phase24_training_passed"] is True
    assert report["decision"]["suitable_for_chat_runtime"] is False
    assert report["decision"]["broad_runtime_activation_allowed"] is False


def test_phase24_metrics_improve_but_quality_is_still_blocked() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert report["evaluation"]["loss"] == 2.5779
    assert report["evaluation"]["perplexity"] == 13.17
    assert report["evaluation"]["generation_non_empty"] is True
    assert report["comparison_with_v0_1"]["perplexity_improved"] is True
    assert report["generation_quality"]["less_meaning_where_repetition_than_v0_1"] is True
    assert report["generation_quality"]["still_incoherent"] is True
    assert report["generation_quality"]["contains_repetition"] is True
    assert report["generation_quality"]["runtime_blocked"] is True


def test_phase24_artifacts_document_generation_samples_and_decision() -> None:
    samples = SAMPLES.read_text(encoding="utf-8")
    doc = DOC.read_text(encoding="utf-8")

    assert "perplexity=13.17" in samples
    assert "must not replace the stable ChatModule" in samples
    assert "وش" in samples
    assert "مرحبا" in samples
    assert "اشرح" in samples

    assert "COMPLETED_WITH_LIMITS_RUNTIME_BLOCKED" in doc
    assert "Suitable for runtime chat: NO" in doc
    assert "Phase 25 canary" in doc
