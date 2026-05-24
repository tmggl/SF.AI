#!/usr/bin/env python3
"""Phase 27.114 — Arabic Ontology/Synonyms source cards, no import/training.

Phase 27.113 allowed only source-card/license-matrix work for Arabic Ontology
and SinaLab Synonyms. This script creates those governance artifacts without
downloading lexical entries, building tokenizer vocab, or starting training.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources/external_sources"
REPORT_DIR = ROOT / "artifacts/reports"

PHASE27_113_EVIDENCE = RESOURCE_DIR / "phase27_113_lexical_alternatives_evidence.json"
PHASE27_113_MANIFEST = RESOURCE_DIR / "phase27_113_permissive_lexical_alternatives_manifest.json"

SOURCE_CARD_DIR = RESOURCE_DIR / "source_cards"
ARABIC_ONTOLOGY_CARD = SOURCE_CARD_DIR / "arabic_ontology_phase27_114.json"
SYNONYMS_CARD = SOURCE_CARD_DIR / "sinalab_synonyms_phase27_114.json"
LICENSE_MATRIX = RESOURCE_DIR / "phase27_114_arabic_ontology_synonyms_license_matrix.json"
REPORT = REPORT_DIR / "phase27_114_arabic_ontology_synonyms_source_cards_report.json"
DECISION = REPORT_DIR / "PHASE27_114_ARABIC_ONTOLOGY_SYNONYMS_SOURCE_CARDS_DECISION.json"
DOC = ROOT / "docs/PHASE27_114_ARABIC_ONTOLOGY_SYNONYMS_SOURCE_CARDS_REPORT.md"


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _manifest_row(manifest: list[dict[str, Any]], source_id: str) -> dict[str, Any]:
    for row in manifest:
        if row["source_id"] == source_id:
            return row
    raise ValueError(f"Missing manifest row: {source_id}")


def _sinalab_snippet(evidence: dict[str, Any], key: str) -> str:
    for source in evidence["sources"]:
        if source["id"] == "sinalab_resources":
            return source["snippets"][key]
    raise ValueError("Missing SinaLab evidence")


def _source_card(
    row: dict[str, Any],
    *,
    evidence_snippet: str,
    artifact_expectation: str,
    allowed_future_lane: str,
) -> dict[str, Any]:
    return {
        "source_id": row["source_id"],
        "name": row["name"],
        "source_type": row["source_type"],
        "primary_url": row["url"],
        "primary_license_signal": row["observed_license"],
        "primary_signal_summary": row["primary_signal"],
        "evidence_snippet": evidence_snippet,
        "language_scope": ["msa"],
        "dialect_scope": ["msa"],
        "intended_future_use": allowed_future_lane,
        "artifact_expectation": artifact_expectation,
        "allowed_now": {
            "source_card": True,
            "license_matrix": True,
            "artifact_download": False,
            "raw_entry_import": False,
            "training_text_import": False,
            "tokenizer_vocab_import": False,
            "runtime_lookup": False,
        },
        "required_before_import": [
            "capture_primary_download_license",
            "record_artifact_url",
            "record_artifact_checksum",
            "field_mapping_design",
            "sample_quality_review",
            "dedupe_against_saudi_seed_v1",
            "no_tokenizer_vocab_import",
            "no_dialogue_corpus_contamination",
        ],
        "blocked_outputs_now": [
            f"data/corpus/**/{row['source_id']}*.jsonl",
            f"resources/lexicons/imported/{row['source_id']}/*.jsonl",
            f"artifacts/tokenizers/**/{row['source_id']}*",
        ],
    }


def _license_matrix(cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for card in cards:
        rows.append(
            {
                "source_id": card["source_id"],
                "license": card["primary_license_signal"],
                "license_is_permissive_candidate": card["primary_license_signal"] == "CC-BY-4.0",
                "artifact_license_captured": False,
                "artifact_checksum_captured": False,
                "source_card_complete": True,
                "raw_entry_import_allowed_now": False,
                "training_text_allowed_now": False,
                "tokenizer_vocab_allowed_now": False,
                "eval_allowed_after_artifact_gate": True,
                "next_allowed_action": "artifact_gate_and_field_mapping_only",
                "why": (
                    "Primary resources page is promising, but SF.AI requires "
                    "downloadable artifact license/checksum and mapping review before import."
                ),
            }
        )
    return rows


def _decision(cards: list[dict[str, Any]], matrix: list[dict[str, Any]]) -> dict[str, Any]:
    ready = (
        len(cards) == 2
        and all(row["source_card_complete"] for row in matrix)
        and all(not row["raw_entry_import_allowed_now"] for row in matrix)
        and all(not row["tokenizer_vocab_allowed_now"] for row in matrix)
    )
    return {
        "decision_id": "PHASE27_114_ARABIC_ONTOLOGY_SYNONYMS_SOURCE_CARDS_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_115_ARTIFACT_GATE_AND_FIELD_MAPPING_NO_IMPORT"
            if ready
            else "BLOCK_PHASE27_115_REPAIR_SOURCE_CARDS"
        ),
        "source_cards_created": [card["source_id"] for card in cards],
        "raw_entry_import_allowed": False,
        "external_training_text_import_allowed": False,
        "external_tokenizer_vocab_import_allowed": False,
        "new_training_allowed": False,
        "runtime_release_allowed": False,
        "next_phase": (
            "Phase 27.115 — Arabic Ontology/Synonyms Artifact Gate and Field Mapping, no training"
            if ready
            else "Phase 27.114b — Source Card Repair"
        ),
    }


def _write_doc(report: dict[str, Any]) -> None:
    decision = report["decision"]
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Phase 27.114 — Arabic Ontology/Synonyms Source Cards",
                "",
                "## الخلاصة",
                "",
                "أُنشئت source cards وlicense matrix لـ Arabic Ontology وSinaLab Synonyms.",
                "لا يوجد import فعلي ولا تدريب.",
                "",
                "## القرار",
                "",
                "```text",
                decision["decision_id"],
                decision["engineering_decision"],
                "```",
                "",
                "## المصدران",
                "",
                "- `arabic_ontology`: مرشح concept/topic semantics بعد artifact gate.",
                "- `sinalab_synonyms`: مرشح semantic alternatives/eval بعد artifact gate.",
                "",
                "## الممنوع الآن",
                "",
                "- تنزيل artifact أو raw entries.",
                "- إدخال corpus.",
                "- tokenizer vocab أو merges.",
                "- تدريب أو runtime release.",
                "",
                "## الملفات",
                "",
                f"- `{ARABIC_ONTOLOGY_CARD.relative_to(ROOT)}`",
                f"- `{SYNONYMS_CARD.relative_to(ROOT)}`",
                f"- `{LICENSE_MATRIX.relative_to(ROOT)}`",
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
    evidence = _read_json(PHASE27_113_EVIDENCE)
    manifest = _read_json(PHASE27_113_MANIFEST)
    arabic_ontology = _source_card(
        _manifest_row(manifest, "arabic_ontology"),
        evidence_snippet=_sinalab_snippet(evidence, "arabic_ontology"),
        artifact_expectation="Arabic Ontology downloadable/API resource, exact artifact URL not captured yet.",
        allowed_future_lane="concept/topic semantics and eval probes after artifact gate",
    )
    synonyms = _source_card(
        _manifest_row(manifest, "sinalab_synonyms"),
        evidence_snippet=_sinalab_snippet(evidence, "synonyms"),
        artifact_expectation="Synonyms dataset artifact, exact artifact URL not captured yet.",
        allowed_future_lane="semantic alternatives/eval probes after artifact gate",
    )
    cards = [arabic_ontology, synonyms]
    matrix = _license_matrix(cards)
    decision = _decision(cards, matrix)
    report = {
        "phase": "Phase 27.114",
        "status": "PHASE27_114_SOURCE_CARDS_READY_NO_IMPORT",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "language_track": ["msa", "saudi"],
        "source_cards": cards,
        "license_matrix": matrix,
        "decision": decision,
        "training_started": False,
        "runtime_changed": False,
        "external_entries_imported": False,
    }
    _write_json(ARABIC_ONTOLOGY_CARD, arabic_ontology)
    _write_json(SYNONYMS_CARD, synonyms)
    _write_json(LICENSE_MATRIX, matrix)
    _write_json(REPORT, report)
    _write_json(DECISION, decision)
    _write_doc(report)
    return report


def main() -> int:
    report = build_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PHASE27_114_SOURCE_CARDS_READY_NO_IMPORT" else 1


if __name__ == "__main__":
    raise SystemExit(main())
