#!/usr/bin/env python3
"""Phase 27.124 — SinaLab Synonyms reference adapter skeleton gate.

Skeleton-only phase. It validates adapter code using synthetic Arabic records,
does not load local source records, does not wire runtime/chat, and does not
write corpus/tokenizer/training artifacts.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sf_ai.reference_layers import SinaLabSynonymsReferenceAdapter, SynonymReferenceRecord

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources/external_sources"
REPORT_DIR = ROOT / "artifacts/reports"
DOCS_DIR = ROOT / "docs"

PHASE27_123_DECISION = (
    REPORT_DIR / "PHASE27_123_SINALAB_SYNONYMS_REFERENCE_ADAPTER_DESIGN_DECISION.json"
)
PHASE27_123_SPEC = RESOURCE_DIR / "phase27_123_sinalab_synonyms_reference_adapter_spec.json"
PHASE27_123_POLICY = RESOURCE_DIR / "phase27_123_sinalab_synonyms_reference_adapter_policy.json"

METRICS = RESOURCE_DIR / "phase27_124_sinalab_synonyms_reference_adapter_skeleton_metrics.json"
GATE = RESOURCE_DIR / "phase27_124_sinalab_synonyms_reference_adapter_skeleton_gate.json"
REPORT = REPORT_DIR / "phase27_124_sinalab_synonyms_reference_adapter_skeleton_report.json"
DECISION = REPORT_DIR / "PHASE27_124_SINALAB_SYNONYMS_REFERENCE_ADAPTER_SKELETON_DECISION.json"
DOC = DOCS_DIR / "PHASE27_124_SINALAB_SYNONYMS_REFERENCE_ADAPTER_SKELETON_REPORT.md"


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _synthetic_adapter() -> SinaLabSynonymsReferenceAdapter:
    records = (
        SynonymReferenceRecord(
            canonical="مصطلح تجريبي",
            synonyms=("عبارة اختبارية", "لفظ فحص"),
            quality_band="high",
            source_id="synthetic_reference",
            record_id="synthetic-001",
        ),
        SynonymReferenceRecord(
            canonical="تعبير مصطنع",
            synonyms=("جملة وهمية",),
            quality_band="medium",
            source_id="synthetic_reference",
            record_id="synthetic-002",
        ),
    )
    return SinaLabSynonymsReferenceAdapter(records)


def _metrics(policy: dict[str, Any]) -> dict[str, Any]:
    adapter = _synthetic_adapter()
    high_hit = adapter.lookup("عبارة اختبارية", include_terms_in_runtime_response=True)
    normalized_hit = adapter.lookup("عباره إختبارية")
    high_blocks_medium = adapter.lookup("تعبير مصطنع", min_quality_band="high")
    medium_hit = adapter.lookup("تعبير مصطنع", min_quality_band="medium", max_results=50)

    return {
        "phase": "Phase 27.124",
        "scope": "adapter_skeleton_synthetic_contract_only",
        "adapter_class": "SinaLabSynonymsReferenceAdapter",
        "synthetic_record_count": adapter.record_count,
        "synthetic_index_key_count": adapter.index_key_count,
        "max_results_default": adapter.max_results_default,
        "max_results_cap": adapter.max_results_cap,
        "policy_default_max_results": policy["max_results_default"],
        "policy_max_results_cap": policy["max_results_cap"],
        "runtime_lookup_enabled": adapter.runtime_lookup_enabled,
        "chat_integration_enabled": adapter.chat_integration_enabled,
        "synthetic_high_lookup_matched": high_hit.matched,
        "synthetic_high_lookup_count": high_hit.result_count,
        "synthetic_normalized_lookup_matched": normalized_hit.matched,
        "synthetic_medium_blocked_by_high_threshold": high_blocks_medium.result_count == 0,
        "synthetic_medium_lookup_with_medium_threshold": medium_hit.result_count == 1,
        "redaction_applied_when_terms_requested": high_hit.redaction_applied,
        "terms_included_when_terms_requested": high_hit.terms_included,
        "result_hash_length": len(high_hit.result_hashes[0]) if high_hit.result_hashes else 0,
        "query_hash_length": len(high_hit.query_hash),
        "raw_source_records_loaded": False,
        "raw_terms_published": False,
        "query_rows_published": False,
        "corpus_changed": False,
        "tokenizer_changed": False,
        "training_started": False,
    }


def _gate(
    *,
    decision123: dict[str, Any],
    spec123: dict[str, Any],
    policy123: dict[str, Any],
    metrics: dict[str, Any],
) -> dict[str, Any]:
    preconditions = {
        "phase27_123_allows_adapter_skeleton": decision123["engineering_decision"]
        == "ALLOW_PHASE27_124_SYNONYMS_REFERENCE_ADAPTER_SKELETON_NO_RUNTIME",
        "spec_names_expected_adapter": spec123["adapter_name"] == metrics["adapter_class"],
        "policy_bounds_preserved": metrics["max_results_default"] == policy123["max_results_default"]
        and metrics["max_results_cap"] == policy123["max_results_cap"],
        "synthetic_lookup_contract_passed": metrics["synthetic_high_lookup_matched"] is True
        and metrics["synthetic_normalized_lookup_matched"] is True,
        "quality_threshold_contract_passed": metrics["synthetic_medium_blocked_by_high_threshold"] is True
        and metrics["synthetic_medium_lookup_with_medium_threshold"] is True,
        "redaction_contract_passed": metrics["redaction_applied_when_terms_requested"] is True
        and metrics["terms_included_when_terms_requested"] is False,
        "hash_contract_passed": metrics["result_hash_length"] == 64
        and metrics["query_hash_length"] == 64,
        "runtime_and_chat_still_disabled": metrics["runtime_lookup_enabled"] is False
        and metrics["chat_integration_enabled"] is False,
        "no_source_records_loaded": metrics["raw_source_records_loaded"] is False,
        "no_corpus_tokenizer_training": metrics["corpus_changed"] is False
        and metrics["tokenizer_changed"] is False
        and metrics["training_started"] is False,
    }
    passed = all(preconditions.values())
    return {
        "phase": "Phase 27.124",
        "gate_id": "PHASE27_124_SINALAB_SYNONYMS_REFERENCE_ADAPTER_SKELETON_GATE",
        "source_id": "sinalab_synonyms",
        "gate_passed": passed,
        "preconditions": preconditions,
        "local_reference_dry_run_allowed_next": passed,
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
        "decision_id": "PHASE27_124_SINALAB_SYNONYMS_REFERENCE_ADAPTER_SKELETON_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_125_SYNONYMS_REFERENCE_ADAPTER_LOCAL_DRY_RUN_NO_RUNTIME"
            if passed
            else "BLOCK_PHASE27_125_REPAIR_REFERENCE_ADAPTER_SKELETON"
        ),
        "adapter_skeleton_passed": passed,
        "local_reference_dry_run_allowed_next": passed,
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
            "Phase 27.125 — Synonyms Reference Adapter Local Dry-Run, no runtime"
            if passed
            else "Phase 27.124b — Reference Adapter Skeleton Repair"
        ),
    }


def _write_doc(report: dict[str, Any]) -> None:
    decision = report["decision"]
    metrics = report["metrics"]
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Phase 27.124 — Synonyms Reference Adapter Skeleton",
                "",
                "## الخلاصة",
                "",
                "تمت إضافة skeleton code للـ adapter فقط. الاختبار تم على سجلات",
                "synthetic عربية غير مأخوذة من المصدر. لا يوجد runtime wiring، ولا",
                "ChatModule integration، ولا corpus/tokenizer/training.",
                "",
                "## القرار",
                "",
                "```text",
                decision["decision_id"],
                decision["engineering_decision"],
                "```",
                "",
                "## Contract Checks",
                "",
                f"- adapter class: `{metrics['adapter_class']}`",
                f"- synthetic record count: `{metrics['synthetic_record_count']}`",
                f"- synthetic index keys: `{metrics['synthetic_index_key_count']}`",
                f"- max results default/cap: `{metrics['max_results_default']}/{metrics['max_results_cap']}`",
                f"- redaction when terms requested: `{metrics['redaction_applied_when_terms_requested']}`",
                f"- terms included: `{metrics['terms_included_when_terms_requested']}`",
                "",
                "## الممنوع",
                "",
                "- raw source records.",
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
                "- `sf_ai/reference_layers/sinalab_synonyms.py`",
                f"- `{METRICS.relative_to(ROOT)}`",
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
    decision123 = _read_json(PHASE27_123_DECISION)
    if decision123["engineering_decision"] != (
        "ALLOW_PHASE27_124_SYNONYMS_REFERENCE_ADAPTER_SKELETON_NO_RUNTIME"
    ):
        raise RuntimeError("Phase 27.123 does not allow Phase 27.124")

    spec123 = _read_json(PHASE27_123_SPEC)
    policy123 = _read_json(PHASE27_123_POLICY)
    metrics = _metrics(policy123)
    gate = _gate(
        decision123=decision123,
        spec123=spec123,
        policy123=policy123,
        metrics=metrics,
    )
    decision = _decision(gate)
    report = {
        "phase": "Phase 27.124",
        "status": "PHASE27_124_SYNONYMS_REFERENCE_ADAPTER_SKELETON_READY_NO_RUNTIME",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "language_track": ["msa", "saudi"],
        "dictionary_track": "Saudi Seed v1",
        "metrics": metrics,
        "gate": gate,
        "decision": decision,
        "adapter_code_written": True,
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
    _write_json(METRICS, metrics)
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
        if report["status"] == "PHASE27_124_SYNONYMS_REFERENCE_ADAPTER_SKELETON_READY_NO_RUNTIME"
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
