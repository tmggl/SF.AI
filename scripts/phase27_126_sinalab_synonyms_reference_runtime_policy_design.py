#!/usr/bin/env python3
"""Phase 27.126 — SinaLab Synonyms runtime policy design.

Design-only phase. It defines a future runtime activation policy for the local
reference adapter. It does not activate lookup, does not wire ChatModule, does
not read raw reference records, and does not write corpus/tokenizer/training
artifacts.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources/external_sources"
REPORT_DIR = ROOT / "artifacts/reports"
DOCS_DIR = ROOT / "docs"

PHASE27_125_DECISION = (
    REPORT_DIR / "PHASE27_125_SINALAB_SYNONYMS_REFERENCE_ADAPTER_LOCAL_DRY_RUN_DECISION.json"
)
PHASE27_125_GATE = (
    RESOURCE_DIR / "phase27_125_sinalab_synonyms_reference_adapter_local_dry_run_gate.json"
)
PHASE27_125_METRICS = (
    RESOURCE_DIR / "phase27_125_sinalab_synonyms_reference_adapter_local_dry_run_metrics.json"
)

POLICY = RESOURCE_DIR / "phase27_126_sinalab_synonyms_reference_runtime_policy.json"
GATE = RESOURCE_DIR / "phase27_126_sinalab_synonyms_reference_runtime_policy_design_gate.json"
REPORT = REPORT_DIR / "phase27_126_sinalab_synonyms_reference_runtime_policy_design_report.json"
DECISION = REPORT_DIR / "PHASE27_126_SINALAB_SYNONYMS_REFERENCE_RUNTIME_POLICY_DESIGN_DECISION.json"
DOC = DOCS_DIR / "PHASE27_126_SINALAB_SYNONYMS_REFERENCE_RUNTIME_POLICY_DESIGN_REPORT.md"


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _policy(metrics: dict[str, Any]) -> dict[str, Any]:
    return {
        "phase": "Phase 27.126",
        "policy_id": "PHASE27_126_SINALAB_SYNONYMS_REFERENCE_RUNTIME_POLICY",
        "source_id": "sinalab_synonyms",
        "policy_scope": "future_runtime_policy_design_no_activation",
        "language_track": ["msa", "saudi"],
        "source_license_mode": "reference_only_counts_hashes_until_activation_gate",
        "minimum_activation_prerequisites": {
            "local_dry_run_passed": True,
            "reference_record_count": metrics["reference_record_count"],
            "eval_query_count": metrics["eval_query_count"],
            "exact_lookup_rate": 1.0,
            "redaction_rate": 1.0,
            "term_leak_count": 0,
            "observed_hash_lengths": [64],
            "heldout_runtime_policy_tests_required": True,
            "chat_integration_gate_required": True,
            "sensitive_log_scan_required": True,
        },
        "runtime_response_policy": {
            "default_mode": "disabled",
            "allowed_future_output": "aggregate_signal_only",
            "raw_term_display_allowed": False,
            "query_row_display_allowed": False,
            "result_hash_display_allowed": True,
            "max_results_default": 5,
            "max_results_cap": 10,
            "min_quality_band_default": "high",
            "fallback_to_template_allowed": False,
        },
        "logging_policy": {
            "logs_may_contain_raw_query": False,
            "logs_may_contain_raw_terms": False,
            "logs_may_contain_query_rows": False,
            "logs_may_contain_hashes_and_counts": True,
            "sensitive_scan_before_commit": True,
        },
        "allowed_next": [
            "runtime_policy_enforcement_tests_no_activation",
            "adapter_disabled_runtime_guard",
            "counts_only_policy_report",
        ],
        "blocked_until_separate_gate": [
            "runtime_lookup_activation",
            "chat_module_integration",
            "ui_term_display",
            "raw_terms_commit",
            "query_rows_commit",
            "data/corpus writes",
            "tokenizer vocab or merges",
            "training text import",
            "checkpoint writes",
            "SF-50M transition",
        ],
    }


def _gate(
    *,
    decision125: dict[str, Any],
    gate125: dict[str, Any],
    metrics125: dict[str, Any],
    policy: dict[str, Any],
) -> dict[str, Any]:
    prereq = policy["minimum_activation_prerequisites"]
    runtime_policy = policy["runtime_response_policy"]
    logging_policy = policy["logging_policy"]
    preconditions = {
        "phase27_125_allows_runtime_policy_design": decision125["engineering_decision"]
        == "ALLOW_PHASE27_126_SYNONYMS_REFERENCE_RUNTIME_POLICY_DESIGN_NO_ACTIVATION",
        "phase27_125_gate_passed": gate125["gate_passed"] is True,
        "metrics_support_policy_design": metrics125["exact_lookup_rate"] == 1.0
        and metrics125["redaction_rate"] == 1.0
        and metrics125["term_leak_count"] == 0,
        "policy_requires_separate_chat_gate": prereq["chat_integration_gate_required"] is True,
        "policy_keeps_default_runtime_disabled": runtime_policy["default_mode"] == "disabled",
        "policy_blocks_raw_term_display": runtime_policy["raw_term_display_allowed"] is False,
        "policy_blocks_query_rows": runtime_policy["query_row_display_allowed"] is False,
        "policy_forbids_template_masking": runtime_policy["fallback_to_template_allowed"] is False,
        "policy_blocks_raw_logs": logging_policy["logs_may_contain_raw_terms"] is False
        and logging_policy["logs_may_contain_query_rows"] is False
        and logging_policy["logs_may_contain_raw_query"] is False,
        "policy_blocks_training_and_scaling": "training text import"
        in policy["blocked_until_separate_gate"]
        and "SF-50M transition" in policy["blocked_until_separate_gate"],
    }
    passed = all(preconditions.values())
    return {
        "phase": "Phase 27.126",
        "gate_id": "PHASE27_126_SINALAB_SYNONYMS_REFERENCE_RUNTIME_POLICY_DESIGN_GATE",
        "source_id": "sinalab_synonyms",
        "gate_passed": passed,
        "preconditions": preconditions,
        "runtime_policy_enforcement_allowed_next": passed,
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
        "decision_id": "PHASE27_126_SINALAB_SYNONYMS_REFERENCE_RUNTIME_POLICY_DESIGN_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_127_SYNONYMS_REFERENCE_RUNTIME_POLICY_ENFORCEMENT_NO_ACTIVATION"
            if passed
            else "BLOCK_PHASE27_127_REPAIR_REFERENCE_RUNTIME_POLICY_DESIGN"
        ),
        "runtime_policy_design_passed": passed,
        "runtime_policy_enforcement_allowed_next": passed,
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
            "Phase 27.127 — Synonyms Reference Runtime Policy Enforcement, no activation"
            if passed
            else "Phase 27.126b — Reference Runtime Policy Design Repair"
        ),
    }


def _write_doc(report: dict[str, Any]) -> None:
    policy = report["policy"]
    decision = report["decision"]
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Phase 27.126 — Synonyms Reference Runtime Policy Design",
                "",
                "## الخلاصة",
                "",
                "تم تصميم سياسة runtime مستقبلية فقط. لا تفعيل lookup، لا ChatModule،",
                "لا واجهة، لا corpus/tokenizer/training.",
                "",
                "## القرار",
                "",
                "```text",
                decision["decision_id"],
                decision["engineering_decision"],
                "```",
                "",
                "## Runtime Policy",
                "",
                f"- default mode: `{policy['runtime_response_policy']['default_mode']}`",
                f"- allowed future output: `{policy['runtime_response_policy']['allowed_future_output']}`",
                f"- raw term display allowed: `{policy['runtime_response_policy']['raw_term_display_allowed']}`",
                f"- query row display allowed: `{policy['runtime_response_policy']['query_row_display_allowed']}`",
                f"- fallback template masking allowed: `{policy['runtime_response_policy']['fallback_to_template_allowed']}`",
                "",
                "## Logging Policy",
                "",
                f"- logs may contain raw query: `{policy['logging_policy']['logs_may_contain_raw_query']}`",
                f"- logs may contain raw terms: `{policy['logging_policy']['logs_may_contain_raw_terms']}`",
                f"- logs may contain query rows: `{policy['logging_policy']['logs_may_contain_query_rows']}`",
                f"- logs may contain hashes/counts: `{policy['logging_policy']['logs_may_contain_hashes_and_counts']}`",
                "",
                "## الممنوع",
                "",
                "- runtime lookup activation.",
                "- chat module integration.",
                "- raw terms/query rows in git.",
                "- UI term display.",
                "- data/corpus writes.",
                "- tokenizer vocab/merges.",
                "- training.",
                "- SF-50M transition.",
                "",
                "## الملفات",
                "",
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
    decision125 = _read_json(PHASE27_125_DECISION)
    if decision125["engineering_decision"] != (
        "ALLOW_PHASE27_126_SYNONYMS_REFERENCE_RUNTIME_POLICY_DESIGN_NO_ACTIVATION"
    ):
        raise RuntimeError("Phase 27.125 does not allow Phase 27.126")
    gate125 = _read_json(PHASE27_125_GATE)
    metrics125 = _read_json(PHASE27_125_METRICS)
    policy = _policy(metrics125)
    gate = _gate(
        decision125=decision125,
        gate125=gate125,
        metrics125=metrics125,
        policy=policy,
    )
    decision = _decision(gate)
    report = {
        "phase": "Phase 27.126",
        "status": "PHASE27_126_SYNONYMS_REFERENCE_RUNTIME_POLICY_DESIGN_READY_NO_ACTIVATION",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "language_track": ["msa", "saudi"],
        "dictionary_track": "Saudi Seed v1",
        "policy": policy,
        "gate": gate,
        "decision": decision,
        "adapter_code_changed": False,
        "runtime_changed": False,
        "runtime_lookup_enabled": False,
        "chat_integration_enabled": False,
        "raw_source_records_loaded": False,
        "query_rows_committed": False,
        "reference_records_committed": False,
        "corpus_changed": False,
        "tokenizer_changed": False,
        "training_started": False,
        "raw_terms_published": False,
    }
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
        if report["status"]
        == "PHASE27_126_SYNONYMS_REFERENCE_RUNTIME_POLICY_DESIGN_READY_NO_ACTIVATION"
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
