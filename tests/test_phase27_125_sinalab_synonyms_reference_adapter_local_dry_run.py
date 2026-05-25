"""Phase 27.125 — SinaLab Synonyms adapter local dry-run gate coverage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "resources/external_sources/phase27_125_sinalab_synonyms_reference_adapter_local_dry_run_metrics.json"
GATE = ROOT / "resources/external_sources/phase27_125_sinalab_synonyms_reference_adapter_local_dry_run_gate.json"
REPORT = ROOT / "artifacts/reports/phase27_125_sinalab_synonyms_reference_adapter_local_dry_run_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_125_SINALAB_SYNONYMS_REFERENCE_ADAPTER_LOCAL_DRY_RUN_DECISION.json"
DOC = ROOT / "docs/PHASE27_125_SINALAB_SYNONYMS_REFERENCE_ADAPTER_LOCAL_DRY_RUN_REPORT.md"


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase27_125_decision_allows_runtime_policy_design_only() -> None:
    report = _json(REPORT)
    decision = _json(DECISION)

    assert report["phase"] == "Phase 27.125"
    assert report["status"] == "PHASE27_125_SYNONYMS_REFERENCE_ADAPTER_LOCAL_DRY_RUN_READY_NO_RUNTIME"
    assert report["decision"] == decision
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_126_SYNONYMS_REFERENCE_RUNTIME_POLICY_DESIGN_NO_ACTIVATION"
    )
    assert decision["local_dry_run_passed"] is True
    assert decision["reference_runtime_policy_design_allowed_next"] is True
    assert decision["runtime_lookup_activation_allowed"] is False
    assert decision["chat_integration_allowed"] is False
    assert decision["raw_terms_commit_allowed"] is False
    assert decision["query_rows_commit_allowed"] is False
    assert decision["dialogue_corpus_allowed"] is False
    assert decision["tokenizer_vocab_allowed"] is False
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_transition_allowed"] is False
    assert "Phase 27.126" in decision["next_phase"]


def test_phase27_125_metrics_are_counts_only_and_redacted() -> None:
    metrics = _json(METRICS)

    assert metrics["phase"] == "Phase 27.125"
    assert metrics["scope"] == "local_reference_adapter_dry_run_counts_only"
    assert metrics["adapter_class"] == "SinaLabSynonymsReferenceAdapter"
    assert metrics["reference_record_count"] == 1093
    assert metrics["eval_query_count"] == 685
    assert metrics["adapter_record_count"] == 1093
    assert metrics["adapter_index_key_count"] == 1093
    assert metrics["reference_quality_band_counts"] == {"high": 685, "medium": 408, "low": 0}
    assert metrics["eval_quality_band_counts"] == {"high": 685, "medium": 0, "low": 0}
    assert metrics["exact_lookup_hits"] == 685
    assert metrics["exact_lookup_rate"] == 1.0
    assert metrics["missing_lookup_count"] == 0
    assert metrics["redacted_lookup_count"] == 685
    assert metrics["redaction_rate"] == 1.0
    assert metrics["term_leak_count"] == 0
    assert metrics["unique_result_hash_count"] == 685
    assert metrics["observed_hash_lengths"] == [64]
    assert metrics["raw_source_records_loaded_locally"] is True
    assert metrics["raw_terms_published"] is False
    assert metrics["query_rows_published"] is False
    assert metrics["runtime_lookup_enabled"] is False
    assert metrics["chat_integration_enabled"] is False
    assert metrics["dialogue_corpus_written"] is False
    assert metrics["tokenizer_vocab_written"] is False
    assert metrics["training_started"] is False


def test_phase27_125_gate_blocks_activation_training_and_scaling() -> None:
    gate = _json(GATE)

    assert gate["gate_passed"] is True
    assert all(gate["preconditions"].values())
    assert gate["reference_runtime_policy_design_allowed_next"] is True
    assert gate["runtime_lookup_activation_allowed"] is False
    assert gate["chat_integration_allowed"] is False
    assert gate["raw_terms_commit_allowed"] is False
    assert gate["query_rows_commit_allowed"] is False
    assert gate["dialogue_corpus_allowed"] is False
    assert gate["tokenizer_vocab_allowed"] is False
    assert gate["training_allowed"] is False
    assert gate["runtime_release_allowed"] is False
    assert gate["sf50m_transition_allowed"] is False


def test_phase27_125_committed_outputs_do_not_publish_source_terms() -> None:
    report = _json(REPORT)

    assert report["adapter_code_changed"] is False
    assert report["runtime_changed"] is False
    assert report["runtime_lookup_enabled"] is False
    assert report["chat_integration_enabled"] is False
    assert report["raw_source_records_loaded_locally"] is True
    assert report["query_rows_committed"] is False
    assert report["reference_records_committed"] is False
    assert report["corpus_changed"] is False
    assert report["tokenizer_changed"] is False
    assert report["training_started"] is False
    assert report["raw_terms_published"] is False

    text = "\n".join(path.read_text(encoding="utf-8") for path in (METRICS, GATE, REPORT, DECISION, DOC))
    assert '"candidate_term":' not in text
    assert '"candidate_normalized":' not in text
    assert '"term":' not in text
    assert "raw terms in git" in text
    assert "query rows in git" in text
    assert "Phase 27.126" in text
