"""Phase 27.113 — permissive lexical alternatives intake gate coverage."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/reports/phase27_113_permissive_lexical_alternatives_intake_gate_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_113_PERMISSIVE_LEXICAL_ALTERNATIVES_INTAKE_GATE_DECISION.json"
MANIFEST = ROOT / "resources/external_sources/phase27_113_permissive_lexical_alternatives_manifest.json"
EVIDENCE = ROOT / "resources/external_sources/phase27_113_lexical_alternatives_evidence.json"
DOC = ROOT / "docs/PHASE27_113_PERMISSIVE_LEXICAL_ALTERNATIVES_INTAKE_GATE_REPORT.md"


def _json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase27_113_decision_allows_only_source_cards_next() -> None:
    report = _json(REPORT)
    decision = _json(DECISION)

    assert isinstance(report, dict)
    assert isinstance(decision, dict)
    assert report["phase"] == "Phase 27.113"
    assert report["status"] == "PHASE27_113_PERMISSIVE_LEXICAL_ALTERNATIVES_READY_NO_IMPORT"
    assert report["decision"] == decision
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_114_SOURCE_CARDS_FOR_ARABIC_ONTOLOGY_AND_SYNONYMS_NO_IMPORT"
    )
    assert decision["allowed_source_card_candidates"] == ["arabic_ontology", "sinalab_synonyms"]
    assert decision["qabas_import_allowed"] is False
    assert decision["arabic_wordnet_v4_import_allowed"] is False
    assert decision["external_training_text_import_allowed"] is False
    assert decision["external_tokenizer_vocab_import_allowed"] is False
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False


def test_phase27_113_manifest_classifies_allowed_and_blocked_sources() -> None:
    rows = _json(MANIFEST)
    assert isinstance(rows, list)
    by_id = {row["source_id"]: row for row in rows}

    assert by_id["arabic_ontology"]["observed_license"] == "CC-BY-4.0"
    assert by_id["arabic_ontology"]["decision"] == "allow_phase27_114_source_card_and_license_matrix_no_import"
    assert by_id["sinalab_synonyms"]["decision"] == "allow_phase27_114_source_card_and_license_matrix_no_import"
    assert by_id["salma_wsd"]["lane"] == "eval_candidate_not_lexicon"
    assert by_id["arabic_wordnet_v4"]["lane"] == "blocked_model_derived"
    assert by_id["arabic_wordnet_v4"]["lexical_import_allowed_next"] is False
    assert by_id["omw_arabic_wordnet_v2"]["lane"] == "restricted_sharealike"
    assert by_id["qabas"]["lane"] == "reference_only"
    assert all(row["training_text_allowed_next"] is False for row in rows)
    assert all(row["tokenizer_vocab_allowed_next"] is False for row in rows)


def test_phase27_113_evidence_contains_license_and_model_derivation_signals() -> None:
    evidence = _json(EVIDENCE)
    by_id = {item["id"]: item for item in evidence["sources"]}

    assert "Arabic Ontology" in by_id["sinalab_resources"]["snippets"]["arabic_ontology"]
    assert "Synonyms" in by_id["sinalab_resources"]["snippets"]["synonyms"]
    assert "CC BY 4.0" in by_id["arabic_wordnet_v4_linguist"]["snippets"]["license"]
    assert "Gemini 3 Pro Preview" in by_id["arabic_wordnet_v4_linguist"]["snippets"]["methodology"]
    assert "Arabic WordNet (AWN v2)" in by_id["omw_v1"]["snippets"]["arabic_awn_v2"]
    assert "cc-by-4.0" in by_id["salma_huggingface"]["snippets"]["license"]


def test_phase27_113_doc_names_next_phase() -> None:
    text = DOC.read_text(encoding="utf-8")

    assert "Phase 27.113" in text
    assert "PHASE27_113_PERMISSIVE_LEXICAL_ALTERNATIVES_INTAKE_GATE_DECISION" in text
    assert "Arabic Ontology" in text
    assert "Gemini" in text
    assert "Phase 27.114" in text
