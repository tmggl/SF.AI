"""Phase 27.115 — artifact gate and field mapping coverage."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "resources/external_sources/phase27_115_arabic_ontology_synonyms_artifact_gate.json"
MAPPING = ROOT / "resources/external_sources/phase27_115_arabic_ontology_synonyms_field_mapping_design.json"
REPORT = ROOT / "artifacts/reports/phase27_115_arabic_ontology_synonyms_artifact_gate_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_115_ARABIC_ONTOLOGY_SYNONYMS_ARTIFACT_GATE_DECISION.json"
DOC = ROOT / "docs/PHASE27_115_ARABIC_ONTOLOGY_SYNONYMS_ARTIFACT_GATE_REPORT.md"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase27_115_decision_allows_only_synonyms_quarantine_dry_run() -> None:
    report = _json(REPORT)
    decision = _json(DECISION)

    assert report["phase"] == "Phase 27.115"
    assert report["status"] == "PHASE27_115_ARTIFACT_GATE_READY_NO_IMPORT"
    assert report["decision"] == decision
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_116_SYNONYMS_ARTIFACT_QUARANTINE_SCHEMA_DRY_RUN_NO_IMPORT"
    )
    assert decision["arabic_ontology_decision"] == "BLOCK_IMPORT_REQUEST_ONLY_NO_DIRECT_ARTIFACT"
    assert decision["sinalab_synonyms_decision"] == "ALLOW_QUARANTINE_CHECKSUM_SCHEMA_DRY_RUN_ONLY"
    assert decision["raw_entry_import_allowed"] is False
    assert decision["external_training_text_import_allowed"] is False
    assert decision["external_tokenizer_vocab_import_allowed"] is False
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_transition_allowed"] is False
    assert "Phase 27.116" in decision["next_phase"]


def test_phase27_115_gate_blocks_import_and_training() -> None:
    gate = _json(GATE)
    by_id = {row["source_id"]: row for row in gate["sources"]}

    assert gate["metadata_only"] is True
    assert by_id["arabic_ontology"]["artifact_status"] == "request_only_no_direct_artifact"
    assert by_id["arabic_ontology"]["artifact_url"] is None
    assert by_id["arabic_ontology"]["raw_entry_import_allowed_now"] is False
    assert by_id["sinalab_synonyms"]["artifact_status"] == "artifact_candidate_located_import_still_blocked"
    assert by_id["sinalab_synonyms"]["artifact_file_signal"] == "Synonyms Dataset.xlsx"
    assert by_id["sinalab_synonyms"]["artifact_license_captured"] is True
    assert by_id["sinalab_synonyms"]["license"] == "CC-BY-4.0"
    assert by_id["sinalab_synonyms"]["artifact_checksum_captured"] is False
    for source in by_id.values():
        assert source["training_text_import_allowed_now"] is False
        assert source["tokenizer_vocab_import_allowed_now"] is False
    assert gate["global_blocks"]["new_training_allowed"] is False
    assert gate["global_blocks"]["raw_entries_in_corpus_allowed"] is False
    assert gate["global_blocks"]["pretrained_vocab_allowed"] is False


def test_phase27_115_field_mapping_is_reference_only() -> None:
    mapping = _json(MAPPING)
    assert mapping["phase"] == "Phase 27.115"
    assert set(mapping["mappings"]) == {"arabic_ontology", "sinalab_synonyms"}
    for source_mapping in mapping["mappings"].values():
        required = source_mapping["required_local_record_fields"]
        assert "training_allowed=false" in required
        assert "tokenizer_vocab_allowed=false" in required
        assert "dialogue_corpus_allowed=false" in required
        assert any("dialogue corpus" in lane for lane in source_mapping["blocked_lanes"])
    assert "artifact_checksum_recorded" in mapping["quality_gates_before_any_import"]
    assert "no_training_text_import" in mapping["quality_gates_before_any_import"]


def test_phase27_115_doc_records_blocked_and_next_phase() -> None:
    text = DOC.read_text(encoding="utf-8")

    assert "Phase 27.115" in text
    assert "PHASE27_115_ARABIC_ONTOLOGY_SYNONYMS_ARTIFACT_GATE_DECISION" in text
    assert "BLOCK_IMPORT_REQUEST_ONLY_NO_DIRECT_ARTIFACT" in text
    assert "ALLOW_QUARANTINE_CHECKSUM_SCHEMA_DRY_RUN_ONLY" in text
    assert "Phase 27.116" in text
