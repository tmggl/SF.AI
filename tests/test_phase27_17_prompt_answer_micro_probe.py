"""Phase 27.17 — prompt-to-answer micro-probe report."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_phase27_17_micro_probe_records_breakthrough_but_blocks_runtime() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/phase27_17_prompt_answer_micro_probe_report.json")
        .read_text(encoding="utf-8")
    )

    assert report["phase"] == "Phase 27.17"
    assert report["status"] == "FAILED_PROMPT_ANSWER_MICRO_PROBE_BLOCK_RUNTIME"
    assert report["language_track"] == ["msa", "saudi"]
    assert report["lexicon_track"] == "Saudi Seed v1"
    assert report["records"] == 32
    assert report["records_by_dialect"] == {"msa": 16, "saudi": 16}
    assert report["training"]["packing_mode"] == "sample_isolated"
    assert report["passed"] == 27
    assert report["exact_clean"] == 28
    assert report["semantic_match"] == 29
    assert report["runtime_allowed"] is False
    assert report["sf50m_allowed"] is False


def test_phase27_17_failures_are_tokenization_or_decoding_hygiene() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/phase27_17_prompt_answer_micro_probe_report.json")
        .read_text(encoding="utf-8")
    )

    failed = [item for item in report["results"] if not item["passed"]]
    assert len(failed) == 5
    reasons = {item["reason"] for item in failed}
    assert {
        "guard:malformed_token",
        "guard:model_artifact_fragment",
        "not_exact_clean",
        "missing_semantic_terms",
    } <= reasons
