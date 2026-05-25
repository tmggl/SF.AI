"""Phase 27.118 — SinaLab Synonyms reference extraction design coverage."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "resources/external_sources/phase27_118_sinalab_synonyms_reference_extraction_design.json"
GATE = ROOT / "resources/external_sources/phase27_118_sinalab_synonyms_reference_extraction_gate.json"
REPORT = ROOT / "artifacts/reports/phase27_118_sinalab_synonyms_reference_extraction_design_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_118_SINALAB_SYNONYMS_REFERENCE_EXTRACTION_DESIGN_DECISION.json"
DOC = ROOT / "docs/PHASE27_118_SINALAB_SYNONYMS_REFERENCE_EXTRACTION_DESIGN_REPORT.md"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase27_118_decision_allows_only_counts_dry_run_next() -> None:
    report = _json(REPORT)
    decision = _json(DECISION)

    assert report["phase"] == "Phase 27.118"
    assert report["status"] == "PHASE27_118_SYNONYMS_REFERENCE_EXTRACTION_DESIGN_READY_NO_IMPORT"
    assert report["decision"] == decision
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_119_SYNONYMS_REFERENCE_EXTRACTION_DRY_RUN_COUNTS_NO_TRAINING"
    )
    assert decision["reference_extraction_design_passed"] is True
    assert decision["raw_entry_import_allowed"] is False
    assert decision["external_training_text_import_allowed"] is False
    assert decision["external_tokenizer_vocab_import_allowed"] is False
    assert decision["raw_terms_publish_allowed"] is False
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_transition_allowed"] is False
    assert "Phase 27.119" in decision["next_phase"]


def test_phase27_118_design_is_reference_only_and_uses_phase27_117_counts() -> None:
    design = _json(DESIGN)
    findings = design["input_findings"]

    assert design["phase"] == "Phase 27.118"
    assert design["target_lane"] == "reference_layer_only"
    assert findings["candidate_rows"] == 3010
    assert findings["unique_normalized_candidate_terms"] == 1697
    assert findings["internal_duplicate_terms"] == 1313
    assert findings["saudi_seed_exact_overlap_count"] == 40
    assert "dialogue_corpus" in design["explicitly_not"]
    assert "tokenizer_vocab" in design["explicitly_not"]
    assert "training_text" in design["explicitly_not"]
    assert design["future_record_schema"]["training_allowed"] is False
    assert design["future_record_schema"]["dialogue_corpus_allowed"] is False
    assert design["future_record_schema"]["tokenizer_vocab_allowed"] is False
    assert design["future_record_schema"]["runtime_lookup_allowed"] is False


def test_phase27_118_filter_and_storage_policy_block_raw_terms() -> None:
    design = _json(DESIGN)
    policy = design["filter_policy"]
    storage = design["storage_policy"]

    assert policy["minimum_average_score_for_reference"] == 40.0
    assert policy["minimum_average_score_for_eval_candidate"] == 70.0
    assert policy["collapse_internal_duplicates"] is True
    assert policy["drop_exact_overlap_with_saudi_seed_v1"] is True
    assert policy["drop_exact_overlap_with_protected_saudi_terms"] is True
    assert policy["publish_raw_terms_to_git"] is False
    assert "candidate_term_values" in storage["committed_outputs_blocked"]
    assert "jsonl_with_terms" in storage["committed_outputs_blocked"]
    assert "training_corpus" in storage["committed_outputs_blocked"]
    assert "counts_summary" in storage["committed_outputs_allowed_next"]


def test_phase27_118_gate_blocks_training_runtime_and_vocab() -> None:
    gate = _json(GATE)

    assert gate["design_ready"] is True
    assert gate["reference_layer_only"] is True
    assert gate["raw_terms_publish_allowed"] is False
    assert gate["training_allowed"] is False
    assert gate["tokenizer_vocab_allowed"] is False
    assert gate["dialogue_corpus_allowed"] is False
    assert gate["runtime_release_allowed"] is False
    assert "Phase 27.119" in gate["next_phase_allowed_if_passed"]


def test_phase27_118_report_never_publishes_raw_terms() -> None:
    report_text = REPORT.read_text(encoding="utf-8")

    assert '"raw_terms_published": false' in report_text
    assert "PHASE27_118_SYNONYMS_REFERENCE_EXTRACTION_DESIGN_READY_NO_IMPORT" in report_text
    assert '"candidate_term": "Arabic candidate term; allowed only in local reference artifact, not corpus"' in report_text
    assert '"candidate":' not in report_text


def test_phase27_118_doc_names_next_phase_and_blocks() -> None:
    text = DOC.read_text(encoding="utf-8")

    assert "Phase 27.118" in text
    assert "PHASE27_118_SINALAB_SYNONYMS_REFERENCE_EXTRACTION_DESIGN_DECISION" in text
    assert "ALLOW_PHASE27_119_SYNONYMS_REFERENCE_EXTRACTION_DRY_RUN_COUNTS_NO_TRAINING" in text
    assert "data/corpus" in text
    assert "Phase 27.119" in text
