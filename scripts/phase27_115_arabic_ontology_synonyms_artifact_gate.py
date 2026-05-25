#!/usr/bin/env python3
"""Phase 27.115 — Arabic Ontology/Synonyms artifact gate + field mapping.

This phase is deliberately metadata-only. It records artifact availability,
import blockers, and future field mappings without downloading lexical entries,
adding corpus data, modifying tokenizer artifacts, or starting training.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources/external_sources"
REPORT_DIR = ROOT / "artifacts/reports"
DOCS_DIR = ROOT / "docs"

PHASE27_114_MATRIX = RESOURCE_DIR / "phase27_114_arabic_ontology_synonyms_license_matrix.json"
AO_CARD = RESOURCE_DIR / "source_cards/arabic_ontology_phase27_114.json"
SYN_CARD = RESOURCE_DIR / "source_cards/sinalab_synonyms_phase27_114.json"

GATE = RESOURCE_DIR / "phase27_115_arabic_ontology_synonyms_artifact_gate.json"
FIELD_MAPPING = RESOURCE_DIR / "phase27_115_arabic_ontology_synonyms_field_mapping_design.json"
REPORT = REPORT_DIR / "phase27_115_arabic_ontology_synonyms_artifact_gate_report.json"
DECISION = REPORT_DIR / "PHASE27_115_ARABIC_ONTOLOGY_SYNONYMS_ARTIFACT_GATE_DECISION.json"
DOC = DOCS_DIR / "PHASE27_115_ARABIC_ONTOLOGY_SYNONYMS_ARTIFACT_GATE_REPORT.md"


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _source_cards_complete() -> bool:
    matrix = _read_json(PHASE27_114_MATRIX)
    return (
        isinstance(matrix, list)
        and len(matrix) == 2
        and all(row["source_card_complete"] for row in matrix)
        and all(row["raw_entry_import_allowed_now"] is False for row in matrix)
    )


def _artifact_gate() -> dict[str, Any]:
    return {
        "phase": "Phase 27.115",
        "gate_id": "PHASE27_115_ARABIC_ONTOLOGY_SYNONYMS_ARTIFACT_GATE",
        "metadata_only": True,
        "source_page_evidence": [
            {
                "url": "https://sina.birzeit.edu/resources/",
                "observed": [
                    "Arabic Ontology is listed as CC-BY-4.0 on the SinaLab resources page.",
                    "Synonyms is listed as CC-BY-4.0 on the SinaLab resources page.",
                    "Arabic Ontology download/API access is exposed through Google Forms/API-token flows.",
                    "Synonyms points to https://github.com/SinaLab/Synonyms.",
                ],
            },
            {
                "url": "https://sina.birzeit.edu/synonyms/",
                "observed": [
                    "Synonyms page points to GitHub for the dataset artifact.",
                    "The page has a separate MIT-looking signal near the web/demo section; "
                    "repo LICENSE/README still state CC-BY-4.0 for the dataset.",
                ],
            },
            {
                "url": "https://github.com/SinaLab/Synonyms",
                "observed": [
                    "Repository metadata license is NOASSERTION via GitHub API.",
                    "Repository LICENSE text says Creative Commons Attribution 4.0 International.",
                    "Repository README says License: CC-BY-4.0.",
                    "Repository root contains README.md, LICENSE, and Synonyms Dataset.xlsx.",
                ],
            },
        ],
        "sources": [
            {
                "source_id": "arabic_ontology",
                "artifact_status": "request_only_no_direct_artifact",
                "artifact_url": None,
                "request_or_access_urls": [
                    "https://ontology.birzeit.edu/about",
                    "https://docs.google.com/forms/d/e/1FAIpQLSfg1kJlUzmxldCCW2pJOOkrSxYDD8F5UIffhJcYsVTRFXZ7qQ/viewform?usp=sf_link",
                ],
                "artifact_license_captured": False,
                "artifact_checksum_captured": False,
                "raw_entry_import_allowed_now": False,
                "training_text_import_allowed_now": False,
                "tokenizer_vocab_import_allowed_now": False,
                "why": (
                    "There is no direct downloadable artifact captured. Access appears request/API-token "
                    "based, so SF.AI cannot import entries until a concrete artifact, license, checksum, "
                    "and permission path are recorded."
                ),
                "next_allowed_action": "manual_permission_or_api_metadata_design_only",
            },
            {
                "source_id": "sinalab_synonyms",
                "artifact_status": "artifact_candidate_located_import_still_blocked",
                "artifact_url": "https://github.com/SinaLab/Synonyms",
                "artifact_file_signal": "Synonyms Dataset.xlsx",
                "artifact_license_captured": True,
                "license": "CC-BY-4.0",
                "license_evidence": [
                    "GitHub LICENSE: Creative Commons Attribution 4.0 International.",
                    "GitHub README: License: CC-BY-4.0.",
                    "SinaLab resources page: Synonyms (CC-BY-4.0).",
                ],
                "license_ambiguity": [
                    "GitHub API returns license.spdx_id=NOASSERTION.",
                    "The public synonyms web/demo page includes a MIT-looking signal; do not treat "
                    "that as dataset import permission without preserving CC-BY attribution.",
                ],
                "artifact_checksum_captured": False,
                "raw_entry_import_allowed_now": False,
                "training_text_import_allowed_now": False,
                "tokenizer_vocab_import_allowed_now": False,
                "why": (
                    "The repository and dataset artifact are located, but Phase 27.115 does not download "
                    "raw entries. Import still needs a quarantine download, checksum, schema/sample "
                    "inspection, attribution file, and no-corpus/no-tokenizer gates."
                ),
                "next_allowed_action": (
                    "Phase 27.116 — Synonyms artifact quarantine checksum and schema dry-run, "
                    "no corpus/training/tokenizer import"
                ),
            },
        ],
        "global_blocks": {
            "new_training_allowed": False,
            "runtime_release_allowed": False,
            "sf50m_transition_allowed": False,
            "external_dialogue_dataset_allowed": False,
            "pretrained_vocab_allowed": False,
            "raw_entries_in_corpus_allowed": False,
        },
    }


def _field_mapping_design() -> dict[str, Any]:
    return {
        "phase": "Phase 27.115",
        "mapping_id": "PHASE27_115_ARABIC_ONTOLOGY_SYNONYMS_FIELD_MAPPING_DESIGN",
        "purpose": (
            "Prepare future metadata/eval/lexical-support mappings without importing source entries "
            "into dialogue corpus or tokenizer vocab."
        ),
        "mappings": {
            "arabic_ontology": {
                "allowed_future_lanes": [
                    "topic/concept normalization support after permission/artifact gate",
                    "held-out evaluation prompts generated by SF.AI authors, not copied entries",
                    "runtime reference lookup only after explicit activation gate",
                ],
                "blocked_lanes": [
                    "dialogue corpus import",
                    "tokenizer vocabulary import",
                    "raw ontology dump inside data/corpus",
                    "training text generated from ontology rows without SF-authored review",
                ],
                "candidate_fields": {
                    "concept_id": "stable external concept identifier, if artifact/API exposes it",
                    "lemma_ar": "Arabic lemma/label; never imported as tokenizer vocab",
                    "synonyms": "semantic alternatives for evaluation/reference, not training text",
                    "hypernyms": "topic hierarchy/reference metadata",
                    "source_url": "source concept URL for attribution",
                    "license": "artifact-level license string",
                    "checksum": "artifact-level checksum before any local quarantine use",
                },
                "required_local_record_fields": [
                    "source_id",
                    "external_id",
                    "term",
                    "relation_type",
                    "target_term",
                    "license",
                    "attribution",
                    "artifact_checksum",
                    "training_allowed=false",
                    "tokenizer_vocab_allowed=false",
                    "dialogue_corpus_allowed=false",
                ],
            },
            "sinalab_synonyms": {
                "allowed_future_lanes": [
                    "semantic alternatives for evaluation canaries",
                    "topic-binding negative/positive checks after manual schema validation",
                    "lexical reference layer outside data/corpus",
                ],
                "blocked_lanes": [
                    "raw xlsx rows copied into dialogue corpus",
                    "pretrained tokenizer vocab/merge construction",
                    "automatic synthetic dialogue generation from dataset rows",
                    "runtime release before held-out quality gates",
                ],
                "candidate_fields": {
                    "synset_id": "source synset/concept grouping identifier, if present",
                    "base_synset_terms": "original synset terms, reference-only",
                    "candidate_synonym": "candidate synonym, reference/eval only",
                    "annotator_scores": "four linguist fuzzy scores, if exposed in artifact",
                    "aggregate_fuzzy_score": "computed/observed synonymy strength",
                    "source_url": "GitHub repository or artifact URL",
                    "license": "CC-BY-4.0 with attribution",
                    "checksum": "artifact checksum captured at quarantine time",
                },
                "required_local_record_fields": [
                    "source_id",
                    "external_synset_id",
                    "term",
                    "candidate",
                    "relation_type=synonym_candidate",
                    "score",
                    "license",
                    "attribution",
                    "artifact_checksum",
                    "training_allowed=false",
                    "tokenizer_vocab_allowed=false",
                    "dialogue_corpus_allowed=false",
                ],
            },
        },
        "quality_gates_before_any_import": [
            "artifact_checksum_recorded",
            "license_attribution_file_written",
            "schema_detected_without_copying_to_corpus",
            "sample_quality_review_passed",
            "dedupe_against_saudi_seed_v1",
            "operator_workflow_contamination_check",
            "no_pretrained_vocab_or_merges",
            "no_training_text_import",
        ],
    }


def _decision(gate: dict[str, Any], mapping: dict[str, Any]) -> dict[str, Any]:
    source_cards_ready = _source_cards_complete()
    by_id = {row["source_id"]: row for row in gate["sources"]}
    synonyms_ready_for_quarantine = (
        by_id["sinalab_synonyms"]["artifact_status"]
        == "artifact_candidate_located_import_still_blocked"
        and by_id["sinalab_synonyms"]["artifact_license_captured"] is True
        and by_id["sinalab_synonyms"]["raw_entry_import_allowed_now"] is False
    )
    arabic_ontology_blocked = (
        by_id["arabic_ontology"]["artifact_status"] == "request_only_no_direct_artifact"
        and by_id["arabic_ontology"]["raw_entry_import_allowed_now"] is False
    )
    design_ready = (
        "arabic_ontology" in mapping["mappings"]
        and "sinalab_synonyms" in mapping["mappings"]
        and "artifact_checksum_recorded" in mapping["quality_gates_before_any_import"]
    )
    passed = source_cards_ready and synonyms_ready_for_quarantine and arabic_ontology_blocked and design_ready
    return {
        "decision_id": "PHASE27_115_ARABIC_ONTOLOGY_SYNONYMS_ARTIFACT_GATE_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_116_SYNONYMS_ARTIFACT_QUARANTINE_SCHEMA_DRY_RUN_NO_IMPORT"
            if passed
            else "BLOCK_PHASE27_116_REPAIR_ARTIFACT_GATE"
        ),
        "arabic_ontology_decision": "BLOCK_IMPORT_REQUEST_ONLY_NO_DIRECT_ARTIFACT",
        "sinalab_synonyms_decision": "ALLOW_QUARANTINE_CHECKSUM_SCHEMA_DRY_RUN_ONLY",
        "raw_entry_import_allowed": False,
        "external_training_text_import_allowed": False,
        "external_tokenizer_vocab_import_allowed": False,
        "new_training_allowed": False,
        "runtime_release_allowed": False,
        "sf50m_transition_allowed": False,
        "next_phase": (
            "Phase 27.116 — Synonyms Artifact Quarantine Checksum and Schema Dry-Run, no import/training"
            if passed
            else "Phase 27.115b — Artifact Gate Repair"
        ),
    }


def _write_doc(report: dict[str, Any]) -> None:
    decision = report["decision"]
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Phase 27.115 — Arabic Ontology/Synonyms Artifact Gate",
                "",
                "## الخلاصة",
                "",
                "هذه مرحلة metadata-only. لم يتم تنزيل raw entries، ولم يُضاف أي corpus، ولم يبدأ تدريب.",
                "",
                "## القرار",
                "",
                "```text",
                decision["decision_id"],
                decision["engineering_decision"],
                "```",
                "",
                "## Arabic Ontology",
                "",
                "- القرار: `BLOCK_IMPORT_REQUEST_ONLY_NO_DIRECT_ARTIFACT`.",
                "- السبب: الوصول الظاهر عبر صفحة/نموذج طلب أو API token، ولا يوجد artifact مباشر مع checksum.",
                "",
                "## SinaLab Synonyms",
                "",
                "- القرار: `ALLOW_QUARANTINE_CHECKSUM_SCHEMA_DRY_RUN_ONLY`.",
                "- السبب: GitHub repo مرصود وفيه `LICENSE` و`README` و`Synonyms Dataset.xlsx`، لكن لا يوجد checksum بعد.",
                "- المسموح التالي فقط: تنزيل quarantine محسوب checksum + فحص schema بدون نقل raw rows إلى corpus.",
                "",
                "## الممنوع",
                "",
                "- training.",
                "- runtime release.",
                "- tokenizer vocab/merges من مصدر خارجي.",
                "- إدخال raw entries إلى `data/corpus`.",
                "- استخدام المصدر لتوليد حوارات تلقائية.",
                "",
                "## Field Mapping",
                "",
                "تم تصميم field mapping منفصل للمصدرين مع `training_allowed=false` و`tokenizer_vocab_allowed=false`.",
                "",
                "## الملفات",
                "",
                f"- `{GATE.relative_to(ROOT)}`",
                f"- `{FIELD_MAPPING.relative_to(ROOT)}`",
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
    # Read the previous source cards to make the phase fail loudly if Phase 27.114
    # evidence disappears.
    _read_json(AO_CARD)
    _read_json(SYN_CARD)
    gate = _artifact_gate()
    mapping = _field_mapping_design()
    decision = _decision(gate, mapping)
    report = {
        "phase": "Phase 27.115",
        "status": "PHASE27_115_ARTIFACT_GATE_READY_NO_IMPORT",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "language_track": ["msa", "saudi"],
        "dictionary_track": "Saudi Seed v1",
        "artifact_gate": gate,
        "field_mapping_design": mapping,
        "decision": decision,
        "training_started": False,
        "runtime_changed": False,
        "external_entries_imported": False,
        "corpus_changed": False,
        "tokenizer_changed": False,
    }
    _write_json(GATE, gate)
    _write_json(FIELD_MAPPING, mapping)
    _write_json(REPORT, report)
    _write_json(DECISION, decision)
    _write_doc(report)
    return report


def main() -> int:
    report = build_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PHASE27_115_ARTIFACT_GATE_READY_NO_IMPORT" else 1


if __name__ == "__main__":
    raise SystemExit(main())
