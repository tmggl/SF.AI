"""Phase 27.126 — SinaLab Synonyms runtime policy design coverage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "resources/external_sources/phase27_126_sinalab_synonyms_reference_runtime_policy.json"
GATE = ROOT / "resources/external_sources/phase27_126_sinalab_synonyms_reference_runtime_policy_design_gate.json"
REPORT = ROOT / "artifacts/reports/phase27_126_sinalab_synonyms_reference_runtime_policy_design_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_126_SINALAB_SYNONYMS_REFERENCE_RUNTIME_POLICY_DESIGN_DECISION.json"
DOC = ROOT / "docs/PHASE27_126_SINALAB_SYNONYMS_REFERENCE_RUNTIME_POLICY_DESIGN_REPORT.md"


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase27_126_decision_allows_enforcement_tests_only() -> None:
    report = _json(REPORT)
    decision = _json(DECISION)

    assert report["phase"] == "Phase 27.126"
    assert report["status"] == "PHASE27_126_SYNONYMS_REFERENCE_RUNTIME_POLICY_DESIGN_READY_NO_ACTIVATION"
    assert report["decision"] == decision
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_127_SYNONYMS_REFERENCE_RUNTIME_POLICY_ENFORCEMENT_NO_ACTIVATION"
    )
    assert decision["runtime_policy_design_passed"] is True
    assert decision["runtime_policy_enforcement_allowed_next"] is True
    assert decision["runtime_lookup_activation_allowed"] is False
    assert decision["chat_integration_allowed"] is False
    assert decision["raw_terms_commit_allowed"] is False
    assert decision["query_rows_commit_allowed"] is False
    assert decision["dialogue_corpus_allowed"] is False
    assert decision["tokenizer_vocab_allowed"] is False
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_transition_allowed"] is False
    assert "Phase 27.127" in decision["next_phase"]


def test_phase27_126_policy_requires_disabled_redacted_runtime() -> None:
    policy = _json(POLICY)

    prereq = policy["minimum_activation_prerequisites"]
    runtime = policy["runtime_response_policy"]
    logging = policy["logging_policy"]

    assert policy["policy_scope"] == "future_runtime_policy_design_no_activation"
    assert prereq["reference_record_count"] == 1093
    assert prereq["eval_query_count"] == 685
    assert prereq["exact_lookup_rate"] == 1.0
    assert prereq["redaction_rate"] == 1.0
    assert prereq["term_leak_count"] == 0
    assert prereq["observed_hash_lengths"] == [64]
    assert prereq["chat_integration_gate_required"] is True
    assert prereq["sensitive_log_scan_required"] is True

    assert runtime["default_mode"] == "disabled"
    assert runtime["allowed_future_output"] == "aggregate_signal_only"
    assert runtime["raw_term_display_allowed"] is False
    assert runtime["query_row_display_allowed"] is False
    assert runtime["result_hash_display_allowed"] is True
    assert runtime["max_results_default"] == 5
    assert runtime["max_results_cap"] == 10
    assert runtime["min_quality_band_default"] == "high"
    assert runtime["fallback_to_template_allowed"] is False

    assert logging["logs_may_contain_raw_query"] is False
    assert logging["logs_may_contain_raw_terms"] is False
    assert logging["logs_may_contain_query_rows"] is False
    assert logging["logs_may_contain_hashes_and_counts"] is True
    assert logging["sensitive_scan_before_commit"] is True

    assert "runtime_policy_enforcement_tests_no_activation" in policy["allowed_next"]
    assert "runtime_lookup_activation" in policy["blocked_until_separate_gate"]
    assert "chat_module_integration" in policy["blocked_until_separate_gate"]
    assert "training text import" in policy["blocked_until_separate_gate"]
    assert "SF-50M transition" in policy["blocked_until_separate_gate"]


def test_phase27_126_gate_blocks_activation_training_and_scaling() -> None:
    gate = _json(GATE)

    assert gate["gate_passed"] is True
    assert all(gate["preconditions"].values())
    assert gate["runtime_policy_enforcement_allowed_next"] is True
    assert gate["runtime_lookup_activation_allowed"] is False
    assert gate["chat_integration_allowed"] is False
    assert gate["raw_terms_commit_allowed"] is False
    assert gate["query_rows_commit_allowed"] is False
    assert gate["dialogue_corpus_allowed"] is False
    assert gate["tokenizer_vocab_allowed"] is False
    assert gate["training_allowed"] is False
    assert gate["runtime_release_allowed"] is False
    assert gate["sf50m_transition_allowed"] is False


def test_phase27_126_committed_outputs_do_not_publish_source_terms() -> None:
    report = _json(REPORT)

    assert report["adapter_code_changed"] is False
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

    text = "\n".join(path.read_text(encoding="utf-8") for path in (POLICY, GATE, REPORT, DECISION, DOC))
    assert '"candidate_term":' not in text
    assert '"candidate_normalized":' not in text
    assert '"term":' not in text
    assert "raw terms/query rows in git" in text
    assert "Phase 27.127" in text
