"""Phase 27.114 — Arabic Ontology/Synonyms source cards coverage."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/reports/phase27_114_arabic_ontology_synonyms_source_cards_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_114_ARABIC_ONTOLOGY_SYNONYMS_SOURCE_CARDS_DECISION.json"
MATRIX = ROOT / "resources/external_sources/phase27_114_arabic_ontology_synonyms_license_matrix.json"
AO_CARD = ROOT / "resources/external_sources/source_cards/arabic_ontology_phase27_114.json"
SYN_CARD = ROOT / "resources/external_sources/source_cards/sinalab_synonyms_phase27_114.json"
DOC = ROOT / "docs/PHASE27_114_ARABIC_ONTOLOGY_SYNONYMS_SOURCE_CARDS_REPORT.md"


def _json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase27_114_decision_allows_only_artifact_gate_next() -> None:
    report = _json(REPORT)
    decision = _json(DECISION)

    assert isinstance(report, dict)
    assert isinstance(decision, dict)
    assert report["phase"] == "Phase 27.114"
    assert report["status"] == "PHASE27_114_SOURCE_CARDS_READY_NO_IMPORT"
    assert report["decision"] == decision
    assert decision["engineering_decision"] == "ALLOW_PHASE27_115_ARTIFACT_GATE_AND_FIELD_MAPPING_NO_IMPORT"
    assert decision["source_cards_created"] == ["arabic_ontology", "sinalab_synonyms"]
    assert decision["raw_entry_import_allowed"] is False
    assert decision["external_training_text_import_allowed"] is False
    assert decision["external_tokenizer_vocab_import_allowed"] is False
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False


def test_phase27_114_source_cards_are_complete_and_block_import() -> None:
    ao = _json(AO_CARD)
    syn = _json(SYN_CARD)

    assert ao["source_id"] == "arabic_ontology"
    assert syn["source_id"] == "sinalab_synonyms"
    assert ao["primary_license_signal"] == "CC-BY-4.0"
    assert syn["primary_license_signal"] == "CC-BY-4.0"
    assert "Arabic Ontology" in ao["evidence_snippet"]
    assert "Synonyms" in syn["evidence_snippet"]
    for card in (ao, syn):
        assert card["allowed_now"]["source_card"] is True
        assert card["allowed_now"]["artifact_download"] is False
        assert card["allowed_now"]["raw_entry_import"] is False
        assert card["allowed_now"]["training_text_import"] is False
        assert card["allowed_now"]["tokenizer_vocab_import"] is False
        assert "record_artifact_checksum" in card["required_before_import"]
        assert any(pattern.startswith("data/corpus/**/") for pattern in card["blocked_outputs_now"])


def test_phase27_114_license_matrix_has_no_import_permissions() -> None:
    rows = _json(MATRIX)
    assert isinstance(rows, list)
    by_id = {row["source_id"]: row for row in rows}

    assert set(by_id) == {"arabic_ontology", "sinalab_synonyms"}
    for row in rows:
        assert row["license"] == "CC-BY-4.0"
        assert row["license_is_permissive_candidate"] is True
        assert row["artifact_license_captured"] is False
        assert row["artifact_checksum_captured"] is False
        assert row["source_card_complete"] is True
        assert row["raw_entry_import_allowed_now"] is False
        assert row["training_text_allowed_now"] is False
        assert row["tokenizer_vocab_allowed_now"] is False
        assert row["next_allowed_action"] == "artifact_gate_and_field_mapping_only"


def test_phase27_114_doc_names_next_phase() -> None:
    text = DOC.read_text(encoding="utf-8")

    assert "Phase 27.114" in text
    assert "PHASE27_114_ARABIC_ONTOLOGY_SYNONYMS_SOURCE_CARDS_DECISION" in text
    assert "Arabic Ontology" in text
    assert "SinaLab Synonyms" in text
    assert "Phase 27.115" in text
