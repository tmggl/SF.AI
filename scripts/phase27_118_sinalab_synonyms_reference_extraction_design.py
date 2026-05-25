#!/usr/bin/env python3
"""Phase 27.118 — SinaLab Synonyms reference extraction design.

Design-only phase. It turns the Phase 27.117 quality/dedupe findings into a
controlled extraction plan, without reading raw rows, writing a reference layer,
touching corpus/tokenizer artifacts, or training.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources/external_sources"
REPORT_DIR = ROOT / "artifacts/reports"
DOCS_DIR = ROOT / "docs"

PHASE27_117_DECISION = (
    REPORT_DIR / "PHASE27_117_SINALAB_SYNONYMS_SAMPLE_QUALITY_DEDUPE_DECISION.json"
)
PHASE27_117_QUALITY = RESOURCE_DIR / "phase27_117_sinalab_synonyms_sample_quality.json"
PHASE27_117_DEDUPE = RESOURCE_DIR / "phase27_117_sinalab_synonyms_dedupe_review.json"
PHASE27_116_MANIFEST = RESOURCE_DIR / "phase27_116_sinalab_synonyms_quarantine_manifest.json"

DESIGN = RESOURCE_DIR / "phase27_118_sinalab_synonyms_reference_extraction_design.json"
GATE = RESOURCE_DIR / "phase27_118_sinalab_synonyms_reference_extraction_gate.json"
REPORT = REPORT_DIR / "phase27_118_sinalab_synonyms_reference_extraction_design_report.json"
DECISION = REPORT_DIR / "PHASE27_118_SINALAB_SYNONYMS_REFERENCE_EXTRACTION_DESIGN_DECISION.json"
DOC = DOCS_DIR / "PHASE27_118_SINALAB_SYNONYMS_REFERENCE_EXTRACTION_DESIGN_REPORT.md"


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _design(manifest: dict[str, Any], quality: dict[str, Any], dedupe: dict[str, Any]) -> dict[str, Any]:
    return {
        "phase": "Phase 27.118",
        "design_id": "PHASE27_118_SINALAB_SYNONYMS_REFERENCE_EXTRACTION_DESIGN",
        "source_id": "sinalab_synonyms",
        "artifact_sha256": manifest["sha256"],
        "input_findings": {
            "candidate_rows": quality["total_candidate_rows"],
            "unique_normalized_candidate_terms": dedupe["unique_normalized_candidate_terms"],
            "internal_duplicate_terms": dedupe["internal_duplicate_terms"],
            "saudi_seed_exact_overlap_count": dedupe["saudi_seed_exact_overlap_count"],
            "protected_saudi_exact_overlap_count": dedupe["protected_saudi_exact_overlap_count"],
            "average_score_mean": quality["average_score_mean"],
            "average_score_median": quality["average_score_median"],
        },
        "target_lane": "reference_layer_only",
        "explicitly_not": [
            "dialogue_corpus",
            "tokenizer_vocab",
            "tokenizer_merges",
            "training_text",
            "runtime_release",
            "sf50m_transition",
        ],
        "future_record_schema": {
            "source_id": "constant:sinalab_synonyms",
            "artifact_sha256": "sha256 from Phase 27.116 manifest",
            "source_row_number": "local quarantine row number, never used as corpus id",
            "synset_number": "source grouping id when present",
            "row_id": "source row id when present",
            "candidate_term": "Arabic candidate term; allowed only in local reference artifact, not corpus",
            "candidate_normalized": "SF.AI normalization for dedupe/filtering",
            "linguist_scores": "L1..L4 numeric scores",
            "average_score": "source average score",
            "quality_band": "high>=70, medium>=40, low<40",
            "license": "CC-BY-4.0",
            "attribution_required": True,
            "training_allowed": False,
            "dialogue_corpus_allowed": False,
            "tokenizer_vocab_allowed": False,
            "runtime_lookup_allowed": False,
        },
        "filter_policy": {
            "minimum_average_score_for_reference": 40.0,
            "minimum_average_score_for_eval_candidate": 70.0,
            "drop_empty_normalized": True,
            "drop_non_arabic_terms": True,
            "collapse_internal_duplicates": True,
            "dedupe_key": "candidate_normalized",
            "on_duplicate": "keep_highest_average_score_and_first_source_row_number",
            "drop_exact_overlap_with_saudi_seed_v1": True,
            "drop_exact_overlap_with_protected_saudi_terms": True,
            "drop_operator_workflow_terms": True,
            "publish_raw_terms_to_git": False,
        },
        "storage_policy": {
            "local_reference_dir": "resources/external_sources/reference_layers/sinalab_synonyms/",
            "raw_reference_records_git_policy": "gitignored_or_not_created_until_explicit_gate",
            "committed_outputs_allowed_next": [
                "counts_summary",
                "quality_band_counts",
                "filter_drop_counts",
                "schema_manifest",
                "attribution_manifest",
            ],
            "committed_outputs_blocked": [
                "candidate_term_values",
                "raw_rows",
                "jsonl_with_terms",
                "tokenizer_vocab",
                "training_corpus",
            ],
        },
        "next_dry_run_requirements": [
            "verify_artifact_sha256_matches_phase27_116",
            "extract_counts_only",
            "report_high_medium_low_counts",
            "report_drop_counts_without_terms",
            "prove_no_data_corpus_writes",
            "prove_no_tokenizer_writes",
            "prove_no_training_started",
            "prove_no_raw_terms_published",
        ],
    }


def _gate(design: dict[str, Any]) -> dict[str, Any]:
    required_blocks = set(design["explicitly_not"])
    required_next = set(design["next_dry_run_requirements"])
    passed = (
        design["target_lane"] == "reference_layer_only"
        and {"dialogue_corpus", "tokenizer_vocab", "training_text"}.issubset(required_blocks)
        and "prove_no_raw_terms_published" in required_next
        and design["filter_policy"]["publish_raw_terms_to_git"] is False
        and design["future_record_schema"]["training_allowed"] is False
        and design["future_record_schema"]["tokenizer_vocab_allowed"] is False
    )
    return {
        "phase": "Phase 27.118",
        "gate_id": "PHASE27_118_SINALAB_SYNONYMS_REFERENCE_EXTRACTION_GATE",
        "design_ready": passed,
        "reference_layer_only": design["target_lane"] == "reference_layer_only",
        "raw_terms_publish_allowed": False,
        "training_allowed": False,
        "tokenizer_vocab_allowed": False,
        "dialogue_corpus_allowed": False,
        "runtime_release_allowed": False,
        "next_phase_allowed_if_passed": (
            "Phase 27.119 — Synonyms Reference Extraction Dry-Run Counts, no training"
        ),
        "blocked_if_failed": "Phase 27.118b — Reference Extraction Design Repair",
    }


def _decision(gate: dict[str, Any]) -> dict[str, Any]:
    passed = gate["design_ready"] is True
    return {
        "decision_id": "PHASE27_118_SINALAB_SYNONYMS_REFERENCE_EXTRACTION_DESIGN_DECISION",
        "engineering_decision": (
            "ALLOW_PHASE27_119_SYNONYMS_REFERENCE_EXTRACTION_DRY_RUN_COUNTS_NO_TRAINING"
            if passed
            else "BLOCK_PHASE27_119_REPAIR_REFERENCE_EXTRACTION_DESIGN"
        ),
        "reference_extraction_design_passed": passed,
        "raw_entry_import_allowed": False,
        "external_training_text_import_allowed": False,
        "external_tokenizer_vocab_import_allowed": False,
        "raw_terms_publish_allowed": False,
        "new_training_allowed": False,
        "runtime_release_allowed": False,
        "sf50m_transition_allowed": False,
        "next_phase": (
            "Phase 27.119 — Synonyms Reference Extraction Dry-Run Counts, no training"
            if passed
            else "Phase 27.118b — Reference Extraction Design Repair"
        ),
    }


def _write_doc(report: dict[str, Any]) -> None:
    design = report["design"]
    decision = report["decision"]
    findings = design["input_findings"]
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Phase 27.118 — Synonyms Reference Extraction Design",
                "",
                "## الخلاصة",
                "",
                "تم تصميم مسار reference extraction فقط، دون استخراج فعلي ودون نشر raw terms.",
                "الهدف أن تكون المرحلة التالية dry-run counts فقط قبل أي reference artifact حقيقي.",
                "",
                "## القرار",
                "",
                "```text",
                decision["decision_id"],
                decision["engineering_decision"],
                "```",
                "",
                "## Inputs",
                "",
                f"- candidate rows: `{findings['candidate_rows']}`",
                f"- unique normalized candidate terms: `{findings['unique_normalized_candidate_terms']}`",
                f"- internal duplicate terms: `{findings['internal_duplicate_terms']}`",
                f"- Saudi Seed exact overlap count: `{findings['saudi_seed_exact_overlap_count']}`",
                "",
                "## Design Rules",
                "",
                "- target lane: `reference_layer_only`.",
                "- drop exact overlap with Saudi Seed v1 and protected Saudi terms before any future use.",
                "- collapse duplicates by normalized term.",
                "- commit counts and manifests only in the next dry-run.",
                "- raw terms stay unpublished unless a later explicit gate allows a local reference artifact.",
                "",
                "## الممنوع",
                "",
                "- data/corpus writes.",
                "- tokenizer vocab/merges.",
                "- training.",
                "- runtime release.",
                "- raw terms in git reports.",
                "",
                "## الملفات",
                "",
                f"- `{DESIGN.relative_to(ROOT)}`",
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
    previous = _read_json(PHASE27_117_DECISION)
    if not previous["engineering_decision"].startswith("ALLOW_PHASE27_118"):
        raise RuntimeError("Phase 27.117 does not allow Phase 27.118")
    manifest = _read_json(PHASE27_116_MANIFEST)
    quality = _read_json(PHASE27_117_QUALITY)
    dedupe = _read_json(PHASE27_117_DEDUPE)
    design = _design(manifest, quality, dedupe)
    gate = _gate(design)
    decision = _decision(gate)
    report = {
        "phase": "Phase 27.118",
        "status": "PHASE27_118_SYNONYMS_REFERENCE_EXTRACTION_DESIGN_READY_NO_IMPORT",
        "strategy": "Sovereign Practical Acceleration Strategy v2",
        "sovereignty_mode": "SF-native only",
        "language_track": ["msa", "saudi"],
        "dictionary_track": "Saudi Seed v1",
        "design": design,
        "gate": gate,
        "decision": decision,
        "training_started": False,
        "runtime_changed": False,
        "external_entries_imported": False,
        "corpus_changed": False,
        "tokenizer_changed": False,
        "raw_terms_published": False,
    }
    _write_json(DESIGN, design)
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
        if report["status"] == "PHASE27_118_SYNONYMS_REFERENCE_EXTRACTION_DESIGN_READY_NO_IMPORT"
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
