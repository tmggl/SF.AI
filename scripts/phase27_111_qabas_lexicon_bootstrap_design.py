#!/usr/bin/env python3
"""Phase 27.111 — Qabas lexicon bootstrap design, no import/training.

This phase designs how SF.AI may later use Qabas for lexicon/topic/protected
term bootstrap without importing Qabas entries yet.

Important: Phase 27.110 found Masader metadata saying Apache-1.0. A primary
SinaLab resources page lists Qabas as CC-BY-ND-4.0. Because of that conflict,
this phase intentionally blocks actual term import until a later primary
license resolution gate.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources/external_sources"
REPORT_DIR = ROOT / "artifacts/reports"

QABAS_METADATA = RESOURCE_DIR / "selected_masader_metadata/qabas.json"
LICENSE_MATRIX = RESOURCE_DIR / "phase27_110_license_matrix.json"
DESIGN = RESOURCE_DIR / "phase27_111_qabas_lexicon_bootstrap_design.json"
SOURCE_CARD = RESOURCE_DIR / "qabas_source_card_phase27_111.json"
REPORT = REPORT_DIR / "phase27_111_qabas_lexicon_bootstrap_design_report.json"
DECISION = REPORT_DIR / "PHASE27_111_QABAS_LEXICON_BOOTSTRAP_DESIGN_DECISION.json"
DOC = ROOT / "docs/PHASE27_111_QABAS_LEXICON_BOOTSTRAP_DESIGN_REPORT.md"
README = ROOT / "resources/lexicons/imported/qabas_bootstrap/README.md"


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _qabas_row(matrix: list[dict[str, Any]]) -> dict[str, Any]:
    for row in matrix:
        if row.get("source_id") == "qabas":
            return row
    raise ValueError("Qabas row missing from Phase 27.110 license matrix")


def _source_card(metadata: dict[str, Any], matrix_row: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": "qabas",
        "name": metadata.get("Name", "Qabas"),
        "source_type": "lexicon",
        "language_scope": ["msa"],
        "dialect_scope": ["msa"],
        "masader_metadata_file": "resources/external_sources/selected_masader_metadata/qabas.json",
        "masader_license": matrix_row.get("license"),
        "masader_link": matrix_row.get("link"),
        "primary_resource_page": "https://sina.birzeit.edu/resources/",
        "primary_qabas_page": "https://sina.birzeit.edu/qabas",
        "paper": metadata.get("Paper Link"),
        "observed_primary_license": "CC-BY-ND-4.0",
        "license_conflict": True,
        "license_conflict_summary": (
            "Masader metadata lists Apache-1.0, while the SinaLab resources page "
            "lists Qabas under CC-BY-ND-4.0. Actual term import is blocked until "
            "the downloadable artifact license is captured and reviewed."
        ),
        "allowed_now": {
            "metadata_reference": True,
            "schema_design": True,
            "field_mapping_design": True,
            "raw_entry_import": False,
            "training_text_import": False,
            "tokenizer_vocab_import": False,
            "runtime_lookup": False,
        },
        "required_next_gates": [
            "capture_downloadable_artifact_license",
            "resolve_apache_vs_cc_by_nd_conflict",
            "verify_no_no_derivatives_block_on_adapted_lexicon_use",
            "deduplicate_against_saudi_seed_v1",
            "quality_sample_review_before_any_import",
        ],
    }


def _design(source_card: dict[str, Any]) -> dict[str, Any]:
    field_mapping = [
        {
            "qabas_field": "lemma",
            "sf_field": "term",
            "use": "candidate term after license resolution",
            "allowed_now": False,
        },
        {
            "qabas_field": "root",
            "sf_field": "root",
            "use": "morphology hint, not model target",
            "allowed_now": False,
        },
        {
            "qabas_field": "part_of_speech",
            "sf_field": "pos",
            "use": "filter nouns/verbs/function words for coverage analysis",
            "allowed_now": False,
        },
        {
            "qabas_field": "definitions_or_senses",
            "sf_field": "notes",
            "use": "blocked from corpus; possible source-card reference only after license review",
            "allowed_now": False,
        },
        {
            "qabas_field": "frequency_or_linked_corpora",
            "sf_field": "priority_score",
            "use": "ranking signal only, no corpus contexts imported",
            "allowed_now": False,
        },
    ]
    gates = [
        {
            "gate": "license_resolution",
            "required": True,
            "blocks": ["raw_entry_import", "protected_terms_activation", "topic_bank_activation"],
        },
        {
            "gate": "no_tokenizer_vocab_import",
            "required": True,
            "rule": "Qabas terms may never be imported as pretrained BPE vocab or merges.",
        },
        {
            "gate": "deduplicate_against_saudi_seed_v1",
            "required": True,
            "rule": "Saudi Seed v1 remains authoritative for Saudi dialect terms.",
        },
        {
            "gate": "msa_only_filter",
            "required": True,
            "rule": "Only MSA lemma metadata may be considered; linked dialect corpora contexts are blocked.",
        },
        {
            "gate": "quality_sample_review",
            "required": True,
            "rule": "Any later import starts as reviewed candidate resources, not training corpus.",
        },
    ]
    future_outputs = {
        "source_card": "resources/external_sources/qabas_source_card_phase27_111.json",
        "candidate_terms_after_license_gate": "resources/lexicons/imported/qabas_bootstrap/qabas_candidate_terms.jsonl",
        "candidate_topics_after_license_gate": "resources/lexicons/imported/qabas_bootstrap/qabas_topic_candidates.jsonl",
        "candidate_protected_terms_after_license_gate": (
            "resources/tokenization/qabas_protected_terms_candidates.txt"
        ),
        "prohibited_outputs_now": [
            "data/corpus/**/qabas*.jsonl",
            "artifacts/tokenizers/**/qabas*",
            "resources/lexicons/imported/qabas_bootstrap/*.jsonl",
        ],
    }
    return {
        "phase": "Phase 27.111",
        "status": "PHASE27_111_QABAS_BOOTSTRAP_DESIGN_READY_IMPORT_BLOCKED",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "language_track": ["msa", "saudi"],
        "lexicon_track": "Saudi Seed v1 primary + Qabas candidate after license resolution",
        "source_card": source_card,
        "field_mapping": field_mapping,
        "gates": gates,
        "future_outputs": future_outputs,
        "actual_qabas_entries_imported": False,
        "training_started": False,
        "runtime_changed": False,
        "external_training_text_import_allowed": False,
        "external_tokenizer_vocab_import_allowed": False,
        "qabas_term_import_allowed_now": False,
        "qabas_design_allowed": True,
    }


def _decision(design: dict[str, Any]) -> dict[str, Any]:
    return {
        "decision_id": "PHASE27_111_QABAS_LEXICON_BOOTSTRAP_DESIGN_DECISION",
        "engineering_decision": "BLOCK_QABAS_IMPORT_ALLOW_PHASE27_112_LICENSE_RESOLUTION_GATE",
        "license_conflict_detected": design["source_card"]["license_conflict"],
        "qabas_design_allowed": True,
        "qabas_term_import_allowed_now": False,
        "external_training_text_import_allowed": False,
        "external_tokenizer_vocab_import_allowed": False,
        "new_training_allowed": False,
        "runtime_release_allowed": False,
        "next_phase": "Phase 27.112 — Qabas Primary License Resolution Gate, no training",
    }


def _write_doc(design: dict[str, Any], decision: dict[str, Any]) -> None:
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Phase 27.111 — Qabas Lexicon Bootstrap Design",
                "",
                "## الخلاصة",
                "",
                "صُمم مسار Qabas كمعجم مساعد للمفردات والموضوعات، لكن لم يتم",
                "استيراد أي مدخلات فعلية لأن الترخيص الأساسي يحتاج حسمًا.",
                "",
                "## قرار المرحلة",
                "",
                "```text",
                decision["decision_id"],
                decision["engineering_decision"],
                "```",
                "",
                "## سبب الحجب",
                "",
                "- Masader metadata تعرض Qabas بترخيص `Apache-1.0`.",
                "- صفحة SinaLab resources تعرض Qabas بترخيص `CC-BY-ND-4.0`.",
                "- لذلك يمنع المشروع أي import فعلي حتى تثبت رخصة artifact القابل للتحميل.",
                "",
                "## المسموح الآن",
                "",
                "- source card.",
                "- field mapping design.",
                "- dedupe/quality gates.",
                "- تخطيط مسارات candidate terms/topics بعد حل الترخيص.",
                "",
                "## الممنوع الآن",
                "",
                "- إدخال raw Qabas entries.",
                "- إدخال Qabas في `data/corpus`.",
                "- استعمال Qabas كـ tokenizer vocab أو merges.",
                "- تدريب أو runtime release.",
                "",
                "## الملفات",
                "",
                f"- `{SOURCE_CARD.relative_to(ROOT)}`",
                f"- `{DESIGN.relative_to(ROOT)}`",
                f"- `{REPORT.relative_to(ROOT)}`",
                f"- `{DECISION.relative_to(ROOT)}`",
                f"- `{README.relative_to(ROOT)}`",
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


def _write_readme() -> None:
    README.parent.mkdir(parents=True, exist_ok=True)
    README.write_text(
        "\n".join(
            [
                "# Qabas Bootstrap Placeholder",
                "",
                "This directory is intentionally a design placeholder only.",
                "",
                "- No Qabas entries are imported here in Phase 27.111.",
                "- No tokenizer vocab or merges are imported.",
                "- No training corpus is produced from Qabas.",
                "- Actual import is blocked until Phase 27.112 resolves the primary license conflict.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def build_report() -> dict[str, Any]:
    metadata = _read_json(QABAS_METADATA)
    matrix = _read_json(LICENSE_MATRIX)
    source_card = _source_card(metadata, _qabas_row(matrix))
    design = _design(source_card)
    decision = _decision(design)
    report = {**design, "decision": decision}

    _write_json(SOURCE_CARD, source_card)
    _write_json(DESIGN, design)
    _write_json(REPORT, report)
    _write_json(DECISION, decision)
    _write_doc(design, decision)
    _write_readme()
    return report


def main() -> int:
    report = build_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PHASE27_111_QABAS_BOOTSTRAP_DESIGN_READY_IMPORT_BLOCKED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
