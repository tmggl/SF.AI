#!/usr/bin/env python3
"""Phase 27.120 — SinaLab Synonyms local reference layer build gate.

Gate-only phase. It does not read the raw XLSX, does not build reference
records, does not publish raw terms, and does not touch corpus/tokenizer/training.
It turns Phase 27.119 counts into a precise permission boundary for a later
local, gitignored reference-layer build.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources/external_sources"
REPORT_DIR = ROOT / "artifacts/reports"
DOCS_DIR = ROOT / "docs"

PHASE27_119_DECISION = (
    REPORT_DIR / "PHASE27_119_SINALAB_SYNONYMS_REFERENCE_DRY_RUN_COUNTS_DECISION.json"
)
PHASE27_119_COUNTS = RESOURCE_DIR / "phase27_119_sinalab_synonyms_reference_dry_run_counts.json"
PHASE27_119_FILTERS = RESOURCE_DIR / "phase27_119_sinalab_synonyms_filter_drop_counts.json"
PHASE27_118_DESIGN = RESOURCE_DIR / "phase27_118_sinalab_synonyms_reference_extraction_design.json"

REFERENCE_DIR = RESOURCE_DIR / "reference_layers/sinalab_synonyms"
REFERENCE_GITIGNORE = REFERENCE_DIR / ".gitignore"

GATE = RESOURCE_DIR / "phase27_120_sinalab_synonyms_local_reference_layer_build_gate.json"
SCHEMA = RESOURCE_DIR / "phase27_120_sinalab_synonyms_local_reference_layer_schema.json"
REPORT = REPORT_DIR / "phase27_120_sinalab_synonyms_local_reference_layer_build_gate_report.json"
DECISION = REPORT_DIR / "PHASE27_120_SINALAB_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_GATE_DECISION.json"
DOC = DOCS_DIR / "PHASE27_120_SINALAB_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_GATE_REPORT.md"


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _reference_gitignore_ready() -> bool:
    if not REFERENCE_GITIGNORE.exists():
        return False
    text = REFERENCE_GITIGNORE.read_text(encoding="utf-8")
    return "*" in text and "!.gitignore" in text and "!README.md" in text


def _schema(design: dict[str, Any]) -> dict[str, Any]:
    future_schema = design["future_record_schema"]
    return {
        "phase": "Phase 27.120",
        "schema_id": "PHASE27_120_SINALAB_SYNONYMS_LOCAL_REFERENCE_LAYER_SCHEMA",
        "source_id": "sinalab_synonyms",
        "storage_mode": "local_gitignored_reference_layer_only",
        "record_fields_allowed_locally_next": [
            "record_id",
            "source_id",
            "artifact_sha256",
            "source_row_number",
            "synset_number",
            "row_id",
            "candidate_term",
            "candidate_normalized",
            "linguist_scores",
            "average_score",
            "quality_band",
            "license",
            "attribution_required",
            "training_allowed",
            "dialogue_corpus_allowed",
            "tokenizer_vocab_allowed",
            "runtime_lookup_allowed",
        ],
        "field_policy": {
            "candidate_term": future_schema["candidate_term"],
            "candidate_normalized": future_schema["candidate_normalized"],
            "quality_band": future_schema["quality_band"],
            "license": future_schema["license"],
            "training_allowed": False,
            "dialogue_corpus_allowed": False,
            "tokenizer_vocab_allowed": False,
            "runtime_lookup_allowed": False,
        },
        "committed_schema_contains_raw_terms": False,
        "committed_schema_contains_record_values": False,
    }


def _gate(
    *,
    decision119: dict[str, Any],
    counts: dict[str, Any],
    filters: dict[str, Any],
    design: dict[str, Any],
    schema: dict[str, Any],
) -> dict[str, Any]:
    preconditions = {
        "phase27_119_allows_reference_build_gate": decision119["engineering_decision"]
        == "ALLOW_PHASE27_120_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_GATED_NO_TRAINING",
        "artifact_sha256_verified": counts["artifact_sha256_verified"] is True,
        "dry_run_counts_passed": decision119["dry_run_counts_passed"] is True,
        "reference_candidates_available": counts["reference_candidate_count_after_filters"] > 0,
        "eval_candidates_available": counts["eval_candidate_count_after_filters"] > 0,
        "raw_terms_not_published_in_phase27_119": counts["raw_terms_published"] is False
        and filters["raw_terms_published"] is False,
        "reference_records_not_written_yet": counts["reference_records_written"] is False,
        "training_not_started": counts["training_started"] is False,
        "dialogue_corpus_not_written": counts["dialogue_corpus_written"] is False,
        "tokenizer_vocab_not_written": counts["tokenizer_vocab_written"] is False,
        "design_blocks_training_and_runtime": {
            "training_text" in design["explicitly_not"],
            "runtime_release" in design["explicitly_not"],
            design["future_record_schema"]["training_allowed"] is False,
            design["future_record_schema"]["runtime_lookup_allowed"] is False,
        }
        == {True},
        "local_reference_dir_gitignored": _reference_gitignore_ready(),
        "schema_is_values_free": schema["committed_schema_contains_record_values"] is False,
    }
    passed = all(preconditions.values())
    return {
        "phase": "Phase 27.120",
        "gate_id": "PHASE27_120_SINALAB_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_GATE",
        "source_id": "sinalab_synonyms",
        "gate_passed": passed,
        "preconditions": preconditions,
        "reference_layer_path": str(REFERENCE_DIR.relative_to(ROOT)),
        "storage_mode": "local_gitignored_reference_layer_only",
        "max_local_reference_records_next": counts["reference_candidate_count_after_filters"],
        "max_local_eval_candidate_records_next": counts["eval_candidate_count_after_filters"],
        "committed_outputs_allowed_next": [
            "local_build_manifest_counts_only",
            "local_build_schema_manifest",
            "local_build_attribution_manifest",
            "local_build_validation_report_without_terms",
        ],
        "local_outputs_allowed_next_but_gitignored": [
            "reference_records_jsonl_with_terms",
            "reference_eval_candidates_jsonl_with_terms",
        ],
        "blocked_outputs": [
            "data/corpus writes",
            "tokenizer vocab or merges",
            "training text import",
            "checkpoint writes",
            "runtime lookup activation",
            "raw terms in committed files",
            "SF-50M transition",
        ],
        "raw_terms_commit_allowed": False,
        "local_reference_records_allowed_next": passed,
        "dialogue_corpus_allowed": False,
        "tokenizer_vocab_allowed": False,
        "training_allowed": False,
        "runtime_release_allowed": False,
        "sf50m_transition_allowed": False,
    }


def _decision(gate: dict[str, Any]) -> dict[str, Any]:
    passed = gate["gate_passed"] is True
    return {
        "decision_id": "PHASE27_120_SINALAB_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_GATE_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_121_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_GITIGNORED_NO_TRAINING"
            if passed
            else "BLOCK_PHASE27_121_REPAIR_LOCAL_REFERENCE_LAYER_BUILD_GATE"
        ),
        "build_gate_passed": passed,
        "local_reference_records_allowed_next": passed,
        "raw_terms_commit_allowed": False,
        "external_training_text_import_allowed": False,
        "external_tokenizer_vocab_import_allowed": False,
        "dialogue_corpus_allowed": False,
        "tokenizer_vocab_allowed": False,
        "new_training_allowed": False,
        "runtime_release_allowed": False,
        "sf50m_transition_allowed": False,
        "next_phase": (
            "Phase 27.121 — Synonyms Local Reference Layer Build, gitignored, no training"
            if passed
            else "Phase 27.120b — Local Reference Layer Build Gate Repair"
        ),
    }


def _write_doc(report: dict[str, Any]) -> None:
    gate = report["gate"]
    decision = report["decision"]
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Phase 27.120 — Synonyms Local Reference Layer Build Gate",
                "",
                "## الخلاصة",
                "",
                "تمت بوابة بناء reference layer محلي فقط. لا يوجد بناء records في هذه المرحلة،",
                "ولا raw terms في git، ولا corpus/tokenizer/training/runtime.",
                "",
                "## القرار",
                "",
                "```text",
                decision["decision_id"],
                decision["engineering_decision"],
                "```",
                "",
                "## Gate",
                "",
                f"- gate passed: `{gate['gate_passed']}`",
                f"- reference path: `{gate['reference_layer_path']}`",
                f"- max local reference records next: `{gate['max_local_reference_records_next']}`",
                f"- max local eval candidates next: `{gate['max_local_eval_candidate_records_next']}`",
                f"- storage mode: `{gate['storage_mode']}`",
                "",
                "## المسموح في المرحلة التالية فقط",
                "",
                "- بناء records محلية داخل مسار gitignored.",
                "- كتابة manifests/reports committed تحتوي counts/schema فقط.",
                "- منع raw terms من أي ملف مرفوع.",
                "",
                "## الممنوع",
                "",
                "- data/corpus writes.",
                "- tokenizer vocab/merges.",
                "- training.",
                "- runtime lookup activation.",
                "- SF-50M transition.",
                "- raw terms in committed files.",
                "- raw terms in git.",
                "",
                "## الملفات",
                "",
                f"- `{GATE.relative_to(ROOT)}`",
                f"- `{SCHEMA.relative_to(ROOT)}`",
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
    decision119 = _read_json(PHASE27_119_DECISION)
    if not decision119["engineering_decision"].startswith("ALLOW_PHASE27_120"):
        raise RuntimeError("Phase 27.119 does not allow Phase 27.120")
    counts = _read_json(PHASE27_119_COUNTS)
    filters = _read_json(PHASE27_119_FILTERS)
    design = _read_json(PHASE27_118_DESIGN)
    schema = _schema(design)
    gate = _gate(
        decision119=decision119,
        counts=counts,
        filters=filters,
        design=design,
        schema=schema,
    )
    decision = _decision(gate)
    report = {
        "phase": "Phase 27.120",
        "status": "PHASE27_120_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_GATE_READY_NO_IMPORT",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "language_track": ["msa", "saudi"],
        "dictionary_track": "Saudi Seed v1",
        "schema": schema,
        "gate": gate,
        "decision": decision,
        "training_started": False,
        "runtime_changed": False,
        "external_entries_imported": False,
        "reference_records_written": False,
        "corpus_changed": False,
        "tokenizer_changed": False,
        "raw_terms_published": False,
    }
    _write_json(SCHEMA, schema)
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
        if report["status"] == "PHASE27_120_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_GATE_READY_NO_IMPORT"
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
