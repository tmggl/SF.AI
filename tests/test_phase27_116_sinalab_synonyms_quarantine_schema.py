"""Phase 27.116 — SinaLab Synonyms quarantine/schema dry-run coverage."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "resources/external_sources/phase27_116_sinalab_synonyms_quarantine_manifest.json"
SCHEMA = ROOT / "resources/external_sources/phase27_116_sinalab_synonyms_schema_dry_run.json"
ATTRIBUTION = ROOT / "resources/external_sources/phase27_116_sinalab_synonyms_attribution.json"
REPORT = ROOT / "artifacts/reports/phase27_116_sinalab_synonyms_quarantine_schema_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_116_SINALAB_SYNONYMS_QUARANTINE_SCHEMA_DECISION.json"
DOC = ROOT / "docs/PHASE27_116_SINALAB_SYNONYMS_QUARANTINE_SCHEMA_REPORT.md"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase27_116_decision_allows_only_sample_quality_review_next() -> None:
    report = _json(REPORT)
    decision = _json(DECISION)

    assert report["phase"] == "Phase 27.116"
    assert report["status"] == "PHASE27_116_SYNONYMS_QUARANTINE_SCHEMA_READY_NO_IMPORT"
    assert report["decision"] == decision
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_117_SYNONYMS_SAMPLE_QUALITY_AND_DEDUPE_REVIEW_NO_TRAINING"
    )
    assert decision["quarantine_checksum_recorded"] is True
    assert decision["schema_dry_run_passed"] is True
    assert decision["raw_entry_import_allowed"] is False
    assert decision["external_training_text_import_allowed"] is False
    assert decision["external_tokenizer_vocab_import_allowed"] is False
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_transition_allowed"] is False
    assert "Phase 27.117" in decision["next_phase"]


def test_phase27_116_manifest_records_checksum_and_blocks_import() -> None:
    manifest = _json(MANIFEST)

    assert manifest["phase"] == "Phase 27.116"
    assert manifest["source_id"] == "sinalab_synonyms"
    assert manifest["artifact_name"] == "Synonyms Dataset.xlsx"
    assert manifest["sha256"] == "a8622546d057f60d2cee0db3b8fdc79cf30303db6ae83001be1634215bb00035"
    assert manifest["size_bytes"] > 300_000
    assert manifest["license"] == "CC-BY-4.0"
    assert manifest["raw_artifact_git_ignored"] is True
    assert manifest["allowed_now"]["quarantine_download"] is True
    assert manifest["allowed_now"]["schema_dry_run"] is True
    assert manifest["allowed_now"]["raw_entry_import"] is False
    assert manifest["allowed_now"]["dialogue_corpus_write"] is False
    assert manifest["allowed_now"]["tokenizer_vocab_import"] is False
    assert manifest["allowed_now"]["training"] is False


def test_phase27_116_schema_is_metadata_only() -> None:
    schema = _json(SCHEMA)
    assert schema["phase"] == "Phase 27.116"
    assert schema["parser"] == "stdlib_zip_xml_metadata_only"
    assert schema["raw_row_values_saved"] is False
    assert schema["dialogue_corpus_written"] is False
    assert schema["tokenizer_vocab_written"] is False
    assert len(schema["sheets"]) == 1
    sheet = schema["sheets"][0]
    assert sheet["name"] == "Sheet1"
    assert sheet["dimension_ref"] == "A1:I4511"
    assert sheet["estimated_rows"] == 4511
    assert sheet["estimated_columns"] == 9
    assert sheet["raw_rows_exported"] is False
    assert sheet["header_columns"][:2] == ["SynsetNo", "RowID"]
    assert sheet["header_columns"][-1] == "Average"


def test_phase27_116_attribution_is_not_training_permission() -> None:
    attribution = _json(ATTRIBUTION)

    assert attribution["source_id"] == "sinalab_synonyms"
    assert attribution["license"] == "CC-BY-4.0"
    assert attribution["training_allowed"] is False
    assert attribution["tokenizer_vocab_allowed"] is False
    assert attribution["dialogue_corpus_allowed"] is False
    assert "Mustafa Jarrar" in attribution["authors"]


def test_phase27_116_doc_names_next_phase_and_blocks() -> None:
    text = DOC.read_text(encoding="utf-8")

    assert "Phase 27.116" in text
    assert "PHASE27_116_SINALAB_SYNONYMS_QUARANTINE_SCHEMA_DECISION" in text
    assert "ALLOW_PHASE27_117_SYNONYMS_SAMPLE_QUALITY_AND_DEDUPE_REVIEW_NO_TRAINING" in text
    assert "raw entry import" in text
    assert "Phase 27.117" in text
