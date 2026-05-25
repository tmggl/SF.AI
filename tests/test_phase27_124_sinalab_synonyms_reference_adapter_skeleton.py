"""Phase 27.124 — SinaLab Synonyms reference adapter skeleton gate coverage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "resources/external_sources/phase27_124_sinalab_synonyms_reference_adapter_skeleton_metrics.json"
GATE = ROOT / "resources/external_sources/phase27_124_sinalab_synonyms_reference_adapter_skeleton_gate.json"
REPORT = ROOT / "artifacts/reports/phase27_124_sinalab_synonyms_reference_adapter_skeleton_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_124_SINALAB_SYNONYMS_REFERENCE_ADAPTER_SKELETON_DECISION.json"
DOC = ROOT / "docs/PHASE27_124_SINALAB_SYNONYMS_REFERENCE_ADAPTER_SKELETON_REPORT.md"


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase27_124_decision_allows_local_dry_run_only() -> None:
    report = _json(REPORT)
    decision = _json(DECISION)

    assert report["phase"] == "Phase 27.124"
    assert report["status"] == "PHASE27_124_SYNONYMS_REFERENCE_ADAPTER_SKELETON_READY_NO_RUNTIME"
    assert report["decision"] == decision
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_125_SYNONYMS_REFERENCE_ADAPTER_LOCAL_DRY_RUN_NO_RUNTIME"
    )
    assert decision["adapter_skeleton_passed"] is True
    assert decision["local_reference_dry_run_allowed_next"] is True
    assert decision["runtime_lookup_activation_allowed"] is False
    assert decision["chat_integration_allowed"] is False
    assert decision["raw_terms_commit_allowed"] is False
    assert decision["query_rows_commit_allowed"] is False
    assert decision["dialogue_corpus_allowed"] is False
    assert decision["tokenizer_vocab_allowed"] is False
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_transition_allowed"] is False
    assert "Phase 27.125" in decision["next_phase"]


def test_phase27_124_metrics_are_synthetic_and_redacted() -> None:
    metrics = _json(METRICS)

    assert metrics["phase"] == "Phase 27.124"
    assert metrics["scope"] == "adapter_skeleton_synthetic_contract_only"
    assert metrics["adapter_class"] == "SinaLabSynonymsReferenceAdapter"
    assert metrics["synthetic_record_count"] == 2
    assert metrics["synthetic_index_key_count"] == 5
    assert metrics["max_results_default"] == 5
    assert metrics["max_results_cap"] == 10
    assert metrics["synthetic_high_lookup_matched"] is True
    assert metrics["synthetic_normalized_lookup_matched"] is True
    assert metrics["synthetic_medium_blocked_by_high_threshold"] is True
    assert metrics["synthetic_medium_lookup_with_medium_threshold"] is True
    assert metrics["redaction_applied_when_terms_requested"] is True
    assert metrics["terms_included_when_terms_requested"] is False
    assert metrics["result_hash_length"] == 64
    assert metrics["query_hash_length"] == 64
    assert metrics["raw_source_records_loaded"] is False
    assert metrics["raw_terms_published"] is False
    assert metrics["query_rows_published"] is False
    assert metrics["corpus_changed"] is False
    assert metrics["tokenizer_changed"] is False
    assert metrics["training_started"] is False


def test_phase27_124_gate_blocks_runtime_chat_training_and_scaling() -> None:
    gate = _json(GATE)

    assert gate["gate_passed"] is True
    assert all(gate["preconditions"].values())
    assert gate["local_reference_dry_run_allowed_next"] is True
    assert gate["runtime_lookup_activation_allowed"] is False
    assert gate["chat_integration_allowed"] is False
    assert gate["raw_terms_commit_allowed"] is False
    assert gate["query_rows_commit_allowed"] is False
    assert gate["dialogue_corpus_allowed"] is False
    assert gate["tokenizer_vocab_allowed"] is False
    assert gate["training_allowed"] is False
    assert gate["runtime_release_allowed"] is False
    assert gate["sf50m_transition_allowed"] is False


def test_phase27_124_committed_outputs_do_not_publish_source_terms() -> None:
    report = _json(REPORT)

    assert report["adapter_code_written"] is True
    assert report["runtime_changed"] is False
    assert report["runtime_lookup_enabled"] is False
    assert report["chat_integration_enabled"] is False
    assert report["raw_source_records_loaded"] is False
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
    assert "Phase 27.125" in text
