"""Phase 27.122 — SinaLab Synonyms reference query/eval gate coverage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "resources/external_sources/phase27_122_sinalab_synonyms_reference_query_eval_metrics.json"
GATE = ROOT / "resources/external_sources/phase27_122_sinalab_synonyms_reference_query_eval_gate.json"
REPORT = ROOT / "artifacts/reports/phase27_122_sinalab_synonyms_reference_query_eval_gate_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_122_SINALAB_SYNONYMS_REFERENCE_QUERY_EVAL_GATE_DECISION.json"
DOC = ROOT / "docs/PHASE27_122_SINALAB_SYNONYMS_REFERENCE_QUERY_EVAL_GATE_REPORT.md"


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase27_122_decision_allows_adapter_design_only() -> None:
    report = _json(REPORT)
    decision = _json(DECISION)

    assert report["phase"] == "Phase 27.122"
    assert report["status"] == "PHASE27_122_SYNONYMS_REFERENCE_QUERY_EVAL_GATE_READY_NO_RUNTIME"
    assert report["decision"] == decision
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_123_SYNONYMS_REFERENCE_ADAPTER_DESIGN_NO_RUNTIME"
    )
    assert decision["query_eval_gate_passed"] is True
    assert decision["reference_adapter_design_allowed_next"] is True
    assert decision["raw_terms_commit_allowed"] is False
    assert decision["query_rows_commit_allowed"] is False
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["runtime_lookup_activation_allowed"] is False
    assert decision["sf50m_transition_allowed"] is False
    assert "Phase 27.123" in decision["next_phase"]


def test_phase27_122_metrics_are_counts_only_and_pass_lookup_eval() -> None:
    metrics = _json(METRICS)

    assert metrics["phase"] == "Phase 27.122"
    assert metrics["query_scope"] == "local_in_memory_query_eval_terms_not_committed"
    assert metrics["reference_record_count"] == 1093
    assert metrics["eval_query_count"] == 685
    assert metrics["unique_normalized_index_keys"] == 1093
    assert metrics["duplicate_normalized_index_keys"] == 0
    assert metrics["exact_lookup_hits"] == 685
    assert metrics["missing_lookup_count"] == 0
    assert metrics["exact_lookup_rate"] == 1.0
    assert metrics["quality_band_match_hits"] == 685
    assert metrics["quality_band_match_rate"] == 1.0
    assert metrics["reference_quality_band_counts"] == {"high": 685, "medium": 408, "low": 0}
    assert metrics["eval_quality_band_counts"] == {"high": 685, "medium": 0, "low": 0}
    assert metrics["raw_terms_published"] is False
    assert metrics["query_rows_published"] is False
    assert metrics["training_started"] is False
    assert metrics["runtime_lookup_enabled"] is False


def test_phase27_122_gate_blocks_runtime_training_and_term_publication() -> None:
    gate = _json(GATE)

    assert gate["gate_passed"] is True
    assert all(gate["preconditions"].values())
    assert gate["query_eval_ready_for_adapter_design"] is True
    assert gate["raw_terms_commit_allowed"] is False
    assert gate["query_rows_commit_allowed"] is False
    assert gate["dialogue_corpus_allowed"] is False
    assert gate["tokenizer_vocab_allowed"] is False
    assert gate["training_allowed"] is False
    assert gate["runtime_release_allowed"] is False
    assert gate["runtime_lookup_activation_allowed"] is False
    assert gate["sf50m_transition_allowed"] is False
    assert "runtime lookup activation" in gate["blocked_outputs"]
    assert "raw terms in git" in gate["blocked_outputs"]


def test_phase27_122_committed_outputs_do_not_publish_terms_or_query_rows() -> None:
    report = _json(REPORT)

    assert report["training_started"] is False
    assert report["runtime_changed"] is False
    assert report["runtime_lookup_enabled"] is False
    assert report["query_rows_committed"] is False
    assert report["reference_records_committed"] is False
    assert report["corpus_changed"] is False
    assert report["tokenizer_changed"] is False
    assert report["raw_terms_published"] is False

    text = "\n".join(path.read_text(encoding="utf-8") for path in (METRICS, GATE, REPORT, DECISION, DOC))
    assert '"raw_terms_published": false' in text
    assert '"query_rows_committed": false' in text
    assert '"candidate_term":' not in text
    assert '"candidate_normalized":' not in text
    assert '"term":' not in text
    assert "query rows in git" in text
    assert "Phase 27.123" in text
