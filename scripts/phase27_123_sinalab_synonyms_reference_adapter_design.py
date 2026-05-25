#!/usr/bin/env python3
"""Phase 27.123 — SinaLab Synonyms reference adapter design.

Design-only phase. It defines the adapter contract and redaction policy for a
future local reference adapter. It does not read local term records, does not
activate runtime lookup, and does not write corpus/tokenizer/training artifacts.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources/external_sources"
REPORT_DIR = ROOT / "artifacts/reports"
DOCS_DIR = ROOT / "docs"

PHASE27_122_DECISION = (
    REPORT_DIR / "PHASE27_122_SINALAB_SYNONYMS_REFERENCE_QUERY_EVAL_GATE_DECISION.json"
)
PHASE27_122_GATE = RESOURCE_DIR / "phase27_122_sinalab_synonyms_reference_query_eval_gate.json"
PHASE27_122_METRICS = RESOURCE_DIR / "phase27_122_sinalab_synonyms_reference_query_eval_metrics.json"

SPEC = RESOURCE_DIR / "phase27_123_sinalab_synonyms_reference_adapter_spec.json"
POLICY = RESOURCE_DIR / "phase27_123_sinalab_synonyms_reference_adapter_policy.json"
GATE = RESOURCE_DIR / "phase27_123_sinalab_synonyms_reference_adapter_design_gate.json"
REPORT = REPORT_DIR / "phase27_123_sinalab_synonyms_reference_adapter_design_report.json"
DECISION = REPORT_DIR / "PHASE27_123_SINALAB_SYNONYMS_REFERENCE_ADAPTER_DESIGN_DECISION.json"
DOC = DOCS_DIR / "PHASE27_123_SINALAB_SYNONYMS_REFERENCE_ADAPTER_DESIGN_REPORT.md"


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _spec(metrics: dict[str, Any]) -> dict[str, Any]:
    return {
        "phase": "Phase 27.123",
        "spec_id": "PHASE27_123_SINALAB_SYNONYMS_REFERENCE_ADAPTER_SPEC",
        "source_id": "sinalab_synonyms",
        "adapter_name": "SinaLabSynonymsReferenceAdapter",
        "design_scope": "contract_only_no_runtime_activation",
        "input_contract": {
            "query_text": "Arabic text supplied by caller; normalized internally",
            "max_results": "positive integer, default 5, capped by policy",
            "min_quality_band": "high|medium, default high",
            "include_terms_in_runtime_response": False,
        },
        "internal_lookup_contract": {
            "reference_layer_required": True,
            "reference_records_count": metrics["reference_record_count"],
            "unique_normalized_index_keys": metrics["unique_normalized_index_keys"],
            "duplicate_normalized_index_keys": metrics["duplicate_normalized_index_keys"],
            "exact_lookup_rate_observed": metrics["exact_lookup_rate"],
            "quality_match_rate_observed": metrics["quality_band_match_rate"],
        },
        "output_contract": {
            "committed_reports": "counts, booleans, hashes, and aggregate metrics only",
            "runtime_adapter_output_future": "redacted aggregate signals only until activation gate",
            "raw_terms_in_committed_output": False,
            "query_rows_in_committed_output": False,
            "corpus_records_from_adapter": False,
            "tokenizer_vocab_from_adapter": False,
        },
        "failure_modes": [
            "reference_layer_missing",
            "query_not_arabic",
            "quality_threshold_not_met",
            "result_redaction_required",
            "runtime_activation_blocked",
        ],
    }


def _policy(metrics: dict[str, Any]) -> dict[str, Any]:
    return {
        "phase": "Phase 27.123",
        "policy_id": "PHASE27_123_SINALAB_SYNONYMS_REFERENCE_ADAPTER_POLICY",
        "source_id": "sinalab_synonyms",
        "language_track": ["msa", "saudi"],
        "max_results_default": 5,
        "max_results_cap": 10,
        "default_quality_band": "high",
        "minimum_metrics_required": {
            "reference_record_count": metrics["reference_record_count"],
            "eval_query_count": metrics["eval_query_count"],
            "exact_lookup_rate": 1.0,
            "quality_band_match_rate": 1.0,
            "duplicate_normalized_index_keys": 0,
        },
        "redaction_policy": {
            "raw_terms_in_git": False,
            "query_rows_in_git": False,
            "raw_reference_rows_in_git": False,
            "future_runtime_term_display": "blocked_until_explicit_runtime_lookup_gate",
            "logs_may_contain_terms": False,
        },
        "allowed_next": [
            "adapter_skeleton_code_without_runtime_wiring",
            "adapter_unit_tests_with_synthetic_non_source_terms",
            "counts_only_eval_report",
        ],
        "blocked_now": [
            "runtime_lookup_activation",
            "chat_module_integration",
            "data/corpus writes",
            "tokenizer vocab or merges",
            "training text import",
            "checkpoint writes",
            "SF-50M transition",
        ],
    }


def _gate(
    *,
    decision122: dict[str, Any],
    gate122: dict[str, Any],
    metrics: dict[str, Any],
    spec: dict[str, Any],
    policy: dict[str, Any],
) -> dict[str, Any]:
    preconditions = {
        "phase27_122_allows_adapter_design": decision122["engineering_decision"]
        == "ALLOW_PHASE27_123_SYNONYMS_REFERENCE_ADAPTER_DESIGN_NO_RUNTIME",
        "phase27_122_gate_passed": gate122["gate_passed"] is True,
        "metrics_support_adapter_design": metrics["exact_lookup_rate"] == 1.0
        and metrics["quality_band_match_rate"] == 1.0,
        "spec_blocks_raw_terms": spec["output_contract"]["raw_terms_in_committed_output"] is False,
        "spec_blocks_query_rows": spec["output_contract"]["query_rows_in_committed_output"] is False,
        "spec_blocks_corpus_and_tokenizer": spec["output_contract"]["corpus_records_from_adapter"] is False
        and spec["output_contract"]["tokenizer_vocab_from_adapter"] is False,
        "policy_blocks_runtime_activation": "runtime_lookup_activation" in policy["blocked_now"],
        "policy_blocks_chat_integration": "chat_module_integration" in policy["blocked_now"],
        "policy_blocks_training": "training text import" in policy["blocked_now"],
        "policy_redacts_terms_and_logs": policy["redaction_policy"]["raw_terms_in_git"] is False
        and policy["redaction_policy"]["logs_may_contain_terms"] is False,
    }
    passed = all(preconditions.values())
    return {
        "phase": "Phase 27.123",
        "gate_id": "PHASE27_123_SINALAB_SYNONYMS_REFERENCE_ADAPTER_DESIGN_GATE",
        "source_id": "sinalab_synonyms",
        "gate_passed": passed,
        "preconditions": preconditions,
        "adapter_skeleton_allowed_next": passed,
        "runtime_lookup_activation_allowed": False,
        "chat_integration_allowed": False,
        "raw_terms_commit_allowed": False,
        "query_rows_commit_allowed": False,
        "dialogue_corpus_allowed": False,
        "tokenizer_vocab_allowed": False,
        "training_allowed": False,
        "runtime_release_allowed": False,
        "sf50m_transition_allowed": False,
    }


def _decision(gate: dict[str, Any]) -> dict[str, Any]:
    passed = gate["gate_passed"] is True
    return {
        "decision_id": "PHASE27_123_SINALAB_SYNONYMS_REFERENCE_ADAPTER_DESIGN_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_124_SYNONYMS_REFERENCE_ADAPTER_SKELETON_NO_RUNTIME"
            if passed
            else "BLOCK_PHASE27_124_REPAIR_REFERENCE_ADAPTER_DESIGN"
        ),
        "adapter_design_passed": passed,
        "adapter_skeleton_allowed_next": passed,
        "runtime_lookup_activation_allowed": False,
        "chat_integration_allowed": False,
        "raw_terms_commit_allowed": False,
        "query_rows_commit_allowed": False,
        "dialogue_corpus_allowed": False,
        "tokenizer_vocab_allowed": False,
        "new_training_allowed": False,
        "runtime_release_allowed": False,
        "sf50m_transition_allowed": False,
        "next_phase": (
            "Phase 27.124 — Synonyms Reference Adapter Skeleton, no runtime"
            if passed
            else "Phase 27.123b — Reference Adapter Design Repair"
        ),
    }


def _write_doc(report: dict[str, Any]) -> None:
    spec = report["spec"]
    policy = report["policy"]
    decision = report["decision"]
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Phase 27.123 — Synonyms Reference Adapter Design",
                "",
                "## الخلاصة",
                "",
                "تم تصميم عقد adapter فقط. لا يوجد كود adapter، ولا runtime wiring،",
                "ولا قراءة terms في هذه المرحلة.",
                "",
                "## القرار",
                "",
                "```text",
                decision["decision_id"],
                decision["engineering_decision"],
                "```",
                "",
                "## Adapter Contract",
                "",
                f"- adapter: `{spec['adapter_name']}`",
                f"- max results default: `{policy['max_results_default']}`",
                f"- max results cap: `{policy['max_results_cap']}`",
                f"- default quality band: `{policy['default_quality_band']}`",
                "- output committed reports: counts/booleans/hashes only.",
                "",
                "## الممنوع",
                "",
                "- raw terms in git.",
                "- query rows in git.",
                "- runtime lookup activation.",
                "- chat module integration.",
                "- data/corpus writes.",
                "- tokenizer vocab/merges.",
                "- training.",
                "- SF-50M transition.",
                "",
                "## الملفات",
                "",
                f"- `{SPEC.relative_to(ROOT)}`",
                f"- `{POLICY.relative_to(ROOT)}`",
                f"- `{GATE.relative_to(ROOT)}`",
                f"- `{REPORT.relative_to(ROOT)}`",
                f"- `{DECISION.relative_to(ROOT)}`",
                "",
                "## التالي",
                "",
                "```text",
                decision["next_phase"],
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )


def build_report() -> dict[str, Any]:
    decision122 = _read_json(PHASE27_122_DECISION)
    if not decision122["engineering_decision"].startswith("ALLOW_PHASE27_123"):
        raise RuntimeError("Phase 27.122 does not allow Phase 27.123")
    gate122 = _read_json(PHASE27_122_GATE)
    metrics = _read_json(PHASE27_122_METRICS)
    spec = _spec(metrics)
    policy = _policy(metrics)
    gate = _gate(
        decision122=decision122,
        gate122=gate122,
        metrics=metrics,
        spec=spec,
        policy=policy,
    )
    decision = _decision(gate)
    report = {
        "phase": "Phase 27.123",
        "status": "PHASE27_123_SYNONYMS_REFERENCE_ADAPTER_DESIGN_READY_NO_RUNTIME",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "language_track": ["msa", "saudi"],
        "dictionary_track": "Saudi Seed v1",
        "spec": spec,
        "policy": policy,
        "gate": gate,
        "decision": decision,
        "adapter_code_written": False,
        "runtime_changed": False,
        "runtime_lookup_enabled": False,
        "chat_integration_enabled": False,
        "query_rows_committed": False,
        "reference_records_committed": False,
        "corpus_changed": False,
        "tokenizer_changed": False,
        "training_started": False,
        "raw_terms_published": False,
    }
    _write_json(SPEC, spec)
    _write_json(POLICY, policy)
    _write_json(GATE, gate)
    _write_json(REPORT, report)
    _write_json(DECISION, decision)
    _write_doc(report)
    return report


def main() -> int:
    report = build_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return (
        0
        if report["status"] == "PHASE27_123_SYNONYMS_REFERENCE_ADAPTER_DESIGN_READY_NO_RUNTIME"
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
