"""Phase 27.117 — SinaLab Synonyms sample quality/dedupe coverage."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUALITY = ROOT / "resources/external_sources/phase27_117_sinalab_synonyms_sample_quality.json"
DEDUPE = ROOT / "resources/external_sources/phase27_117_sinalab_synonyms_dedupe_review.json"
REPORT = ROOT / "artifacts/reports/phase27_117_sinalab_synonyms_sample_quality_dedupe_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_117_SINALAB_SYNONYMS_SAMPLE_QUALITY_DEDUPE_DECISION.json"
DOC = ROOT / "docs/PHASE27_117_SINALAB_SYNONYMS_SAMPLE_QUALITY_DEDUPE_REPORT.md"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase27_117_decision_allows_only_reference_design_next() -> None:
    report = _json(REPORT)
    decision = _json(DECISION)

    assert report["phase"] == "Phase 27.117"
    assert report["status"] == "PHASE27_117_SYNONYMS_SAMPLE_QUALITY_DEDUPE_READY_NO_IMPORT"
    assert report["decision"] == decision
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_118_SYNONYMS_REFERENCE_EXTRACTION_DESIGN_NO_TRAINING"
    )
    assert decision["sample_quality_passed"] is True
    assert decision["dedupe_review_passed"] is True
    assert decision["raw_entry_import_allowed"] is False
    assert decision["external_training_text_import_allowed"] is False
    assert decision["external_tokenizer_vocab_import_allowed"] is False
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_transition_allowed"] is False
    assert "Phase 27.118" in decision["next_phase"]


def test_phase27_117_quality_is_aggregate_only() -> None:
    quality = _json(QUALITY)

    assert quality["phase"] == "Phase 27.117"
    assert quality["review_scope"] == "aggregate_quality_no_raw_terms_published"
    assert quality["total_candidate_rows"] == 3010
    assert quality["sample_window_rows"] == 200
    assert quality["arabic_term_rows"] == 3010
    assert quality["arabic_term_ratio"] == 1.0
    assert quality["empty_normalized_terms"] == 0
    assert quality["score_columns_present_min"] == 5
    assert quality["score_columns_present_max"] == 5
    assert quality["average_score_min"] == 0.0
    assert quality["average_score_max"] == 100.0
    assert quality["operator_vocabulary_exact_overlap_count"] == 1
    assert quality["operational_contamination_hits"] == 0
    assert quality["raw_terms_published"] is False
    assert quality["dialogue_corpus_written"] is False
    assert quality["tokenizer_vocab_written"] is False


def test_phase27_117_dedupe_counts_only_no_terms() -> None:
    dedupe = _json(DEDUPE)

    assert dedupe["phase"] == "Phase 27.117"
    assert dedupe["dedupe_scope"] == "counts_only_no_term_disclosure"
    assert dedupe["normalized_candidate_terms"] == 3010
    assert dedupe["unique_normalized_candidate_terms"] == 1697
    assert dedupe["internal_duplicate_terms"] == 1313
    assert dedupe["protected_saudi_terms_checked"] == 29
    assert dedupe["protected_saudi_exact_overlap_count"] == 1
    assert dedupe["saudi_seed_exact_overlap_count"] == 40
    assert dedupe["overlap_terms_published"] is False
    assert dedupe["raw_terms_published"] is False


def test_phase27_117_report_never_publishes_raw_terms() -> None:
    report_text = REPORT.read_text(encoding="utf-8")
    assert '"raw_terms_published": false' in report_text
    assert "PHASE27_117_SYNONYMS_SAMPLE_QUALITY_DEDUPE_READY_NO_IMPORT" in report_text
    # The report should contain aggregate labels, not source lexical rows.
    assert '"term":' not in report_text
    assert '"candidate":' not in report_text


def test_phase27_117_doc_names_next_phase_and_blocks() -> None:
    text = DOC.read_text(encoding="utf-8")

    assert "Phase 27.117" in text
    assert "PHASE27_117_SINALAB_SYNONYMS_SAMPLE_QUALITY_DEDUPE_DECISION" in text
    assert "ALLOW_PHASE27_118_SYNONYMS_REFERENCE_EXTRACTION_DESIGN_NO_TRAINING" in text
    assert "raw entry import" in text
    assert "Phase 27.118" in text
