"""Phase 27.123 — SinaLab Synonyms reference adapter design coverage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "resources/external_sources/phase27_123_sinalab_synonyms_reference_adapter_spec.json"
POLICY = ROOT / "resources/external_sources/phase27_123_sinalab_synonyms_reference_adapter_policy.json"
GATE = ROOT / "resources/external_sources/phase27_123_sinalab_synonyms_reference_adapter_design_gate.json"
REPORT = ROOT / "artifacts/reports/phase27_123_sinalab_synonyms_reference_adapter_design_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_123_SINALAB_SYNONYMS_REFERENCE_ADAPTER_DESIGN_DECISION.json"
DOC = ROOT / "docs/PHASE27_123_SINALAB_SYNONYMS_REFERENCE_ADAPTER_DESIGN_REPORT.md"


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase27_123_decision_allows_adapter_skeleton_only() -> None:
    report = _json(REPORT)
    decision = _json(DECISION)

    assert report["phase"] == "Phase 27.123"
    assert report["status"] == "PHASE27_123_SYNONYMS_REFERENCE_ADAPTER_DESIGN_READY_NO_RUNTIME"
    assert report["decision"] == decision
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_124_SYNONYMS_REFERENCE_ADAPTER_SKELETON_NO_RUNTIME"
    )
    assert decision["adapter_design_passed"] is True
    assert decision["adapter_skeleton_allowed_next"] is True
    assert decision["runtime_lookup_activation_allowed"] is False
    assert decision["chat_integration_allowed"] is False
    assert decision["raw_terms_commit_allowed"] is False
    assert decision["query_rows_commit_allowed"] is False
    assert decision["dialogue_corpus_allowed"] is False
    assert decision["tokenizer_vocab_allowed"] is False
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_transition_allowed"] is False
    assert "Phase 27.124" in decision["next_phase"]


def test_phase27_123_adapter_spec_is_counts_only_contract() -> None:
    spec = _json(SPEC)

    assert spec["phase"] == "Phase 27.123"
    assert spec["adapter_name"] == "SinaLabSynonymsReferenceAdapter"
    assert spec["design_scope"] == "contract_only_no_runtime_activation"
    assert spec["input_contract"]["include_terms_in_runtime_response"] is False
    assert spec["internal_lookup_contract"]["reference_records_count"] == 1093
    assert spec["internal_lookup_contract"]["unique_normalized_index_keys"] == 1093
    assert spec["internal_lookup_contract"]["duplicate_normalized_index_keys"] == 0
    assert spec["internal_lookup_contract"]["exact_lookup_rate_observed"] == 1.0
    assert spec["internal_lookup_contract"]["quality_match_rate_observed"] == 1.0
    assert spec["output_contract"]["raw_terms_in_committed_output"] is False
    assert spec["output_contract"]["query_rows_in_committed_output"] is False
    assert spec["output_contract"]["corpus_records_from_adapter"] is False
    assert spec["output_contract"]["tokenizer_vocab_from_adapter"] is False


def test_phase27_123_policy_blocks_runtime_training_and_publication() -> None:
    policy = _json(POLICY)
    gate = _json(GATE)

    assert policy["max_results_default"] == 5
    assert policy["max_results_cap"] == 10
    assert policy["default_quality_band"] == "high"
    assert policy["minimum_metrics_required"]["eval_query_count"] == 685
    assert policy["minimum_metrics_required"]["exact_lookup_rate"] == 1.0
    assert policy["minimum_metrics_required"]["quality_band_match_rate"] == 1.0
    assert policy["redaction_policy"]["raw_terms_in_git"] is False
    assert policy["redaction_policy"]["query_rows_in_git"] is False
    assert policy["redaction_policy"]["logs_may_contain_terms"] is False
    assert "adapter_skeleton_code_without_runtime_wiring" in policy["allowed_next"]
    assert "adapter_unit_tests_with_synthetic_non_source_terms" in policy["allowed_next"]
    assert "runtime_lookup_activation" in policy["blocked_now"]
    assert "chat_module_integration" in policy["blocked_now"]
    assert "training text import" in policy["blocked_now"]
    assert "SF-50M transition" in policy["blocked_now"]

    assert gate["gate_passed"] is True
    assert all(gate["preconditions"].values())
    assert gate["adapter_skeleton_allowed_next"] is True
    assert gate["runtime_lookup_activation_allowed"] is False
    assert gate["chat_integration_allowed"] is False
    assert gate["training_allowed"] is False
    assert gate["runtime_release_allowed"] is False
    assert gate["sf50m_transition_allowed"] is False


def test_phase27_123_committed_outputs_do_not_publish_terms_or_query_rows() -> None:
    report = _json(REPORT)

    assert report["adapter_code_written"] is False
    assert report["runtime_changed"] is False
    assert report["runtime_lookup_enabled"] is False
    assert report["chat_integration_enabled"] is False
    assert report["query_rows_committed"] is False
    assert report["reference_records_committed"] is False
    assert report["corpus_changed"] is False
    assert report["tokenizer_changed"] is False
    assert report["training_started"] is False
    assert report["raw_terms_published"] is False

    text = "\n".join(
        path.read_text(encoding="utf-8") for path in (SPEC, POLICY, GATE, REPORT, DECISION, DOC)
    )
    assert '"candidate_term":' not in text
    assert '"candidate_normalized":' not in text
    assert '"term":' not in text
    assert "raw terms in git" in text
    assert "query rows in git" in text
    assert "Phase 27.124" in text
