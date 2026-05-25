"""Phase 27.119 — SinaLab Synonyms reference dry-run counts coverage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
COUNTS = ROOT / "resources/external_sources/phase27_119_sinalab_synonyms_reference_dry_run_counts.json"
FILTERS = ROOT / "resources/external_sources/phase27_119_sinalab_synonyms_filter_drop_counts.json"
REPORT = ROOT / "artifacts/reports/phase27_119_sinalab_synonyms_reference_dry_run_counts_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_119_SINALAB_SYNONYMS_REFERENCE_DRY_RUN_COUNTS_DECISION.json"
DOC = ROOT / "docs/PHASE27_119_SINALAB_SYNONYMS_REFERENCE_DRY_RUN_COUNTS_REPORT.md"


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase27_119_decision_allows_only_gated_reference_build_next() -> None:
    report = _json(REPORT)
    decision = _json(DECISION)

    assert report["phase"] == "Phase 27.119"
    assert report["status"] == "PHASE27_119_SYNONYMS_REFERENCE_DRY_RUN_COUNTS_READY_NO_IMPORT"
    assert report["decision"] == decision
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_120_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_GATED_NO_TRAINING"
    )
    assert decision["dry_run_counts_passed"] is True
    assert decision["raw_entry_import_allowed"] is False
    assert decision["raw_terms_publish_allowed"] is False
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_transition_allowed"] is False
    assert "Phase 27.120" in decision["next_phase"]


def test_phase27_119_counts_are_counts_only_and_expected() -> None:
    counts = _json(COUNTS)

    assert counts["phase"] == "Phase 27.119"
    assert counts["artifact_sha256_verified"] is True
    assert counts["dry_run_scope"] == "counts_only_no_raw_terms_published"
    assert counts["input_candidate_rows"] == 3010
    assert counts["quality_band_counts_input"] == {
        "high": 916,
        "medium": 703,
        "low": 1391,
    }
    assert counts["eligible_before_duplicate_collapse"] == 1570
    assert counts["reference_candidate_count_after_filters"] == 1093
    assert counts["eval_candidate_count_after_filters"] == 685
    assert counts["quality_band_counts_after_filters"] == {
        "high": 685,
        "medium": 408,
        "low": 0,
    }
    assert counts["raw_terms_published"] is False
    assert counts["reference_records_written"] is False
    assert counts["dialogue_corpus_written"] is False
    assert counts["tokenizer_vocab_written"] is False
    assert counts["training_started"] is False


def test_phase27_119_filter_drop_counts_are_term_free() -> None:
    filters = _json(FILTERS)

    assert filters["filter_scope"] == "drop_counts_only_no_terms"
    assert filters["empty_normalized_drop_count"] == 0
    assert filters["non_arabic_drop_count"] == 0
    assert filters["score_below_reference_drop_count"] == 1391
    assert filters["protected_saudi_overlap_drop_count"] == 1
    assert filters["saudi_seed_overlap_drop_count"] == 81
    assert filters["operator_workflow_overlap_drop_count"] == 1
    assert filters["duplicate_dropped_after_filters"] == 316
    assert filters["duplicate_replaced_by_higher_score"] == 161
    assert filters["raw_terms_published"] is False
    assert filters["overlap_terms_published"] is False


def test_phase27_119_report_blocks_training_tokenizer_corpus_and_raw_terms() -> None:
    report = _json(REPORT)

    assert report["training_started"] is False
    assert report["runtime_changed"] is False
    assert report["external_entries_imported"] is False
    assert report["corpus_changed"] is False
    assert report["tokenizer_changed"] is False
    assert report["raw_terms_published"] is False

    text = REPORT.read_text(encoding="utf-8")
    assert '"raw_terms_published": false' in text
    assert '"reference_records_written": false' in text
    assert '"dialogue_corpus_written": false' in text
    assert '"tokenizer_vocab_written": false' in text
    assert '"training_started": false' in text
    assert '"term":' not in text
    assert '"candidate_term":' not in text
    assert '"raw_rows":' not in text


def test_phase27_119_doc_names_counts_and_next_phase() -> None:
    text = DOC.read_text(encoding="utf-8")

    assert "Phase 27.119" in text
    assert "dry-run counts" in text
    assert "PHASE27_119_SINALAB_SYNONYMS_REFERENCE_DRY_RUN_COUNTS_DECISION" in text
    assert "reference candidates after filters: `1093`" in text
    assert "eval candidates after filters: `685`" in text
    assert "Phase 27.120" in text
    assert "data/corpus" in text
