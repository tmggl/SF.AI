"""Phase 27.110 — licensed ingestion design coverage."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/reports/phase27_110_licensed_ingestion_design_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_110_LICENSED_INGESTION_DESIGN_DECISION.json"
DESIGN = ROOT / "resources/external_sources/phase27_110_licensed_ingestion_design.json"
MATRIX = ROOT / "resources/external_sources/phase27_110_license_matrix.json"
SELECTED = ROOT / "resources/external_sources/selected_masader_metadata"
DOC = ROOT / "docs/PHASE27_110_LICENSED_INGESTION_DESIGN_REPORT.md"


def _json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase27_110_decision_allows_qabas_design_only() -> None:
    report = _json(REPORT)
    decision = _json(DECISION)

    assert isinstance(report, dict)
    assert isinstance(decision, dict)
    assert report["phase"] == "Phase 27.110"
    assert report["status"] == "PHASE27_110_LICENSED_INGESTION_DESIGN_READY_NO_TRAINING"
    assert report["decision"] == decision
    assert decision["engineering_decision"] == "ALLOW_PHASE27_111_QABAS_LEXICON_BOOTSTRAP_NO_TRAINING"
    assert decision["external_training_text_import_allowed"] is False
    assert decision["external_tokenizer_vocab_import_allowed"] is False
    assert decision["qabas_lexicon_bootstrap_design_allowed"] is True
    assert decision["tashkeela_training_allowed"] is False
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False


def test_phase27_110_license_matrix_blocks_unsafe_sources() -> None:
    rows = _json(MATRIX)
    assert isinstance(rows, list)
    by_file = {row["masader_file"]: row for row in rows}

    assert by_file["qabas.json"]["lane"] == "lexicon_bootstrap"
    assert by_file["qabas.json"]["vocabulary_terms_allowed_next"] is True
    assert by_file["qabas.json"]["training_text_allowed_next"] is False
    assert by_file["qabas.json"]["license"] == "Apache-1.0"

    assert by_file["tashkeela.json"]["decision"] == "block_training_until_license_conflict_resolved"
    assert by_file["tashkeela.json"]["training_text_allowed_next"] is False
    assert by_file["tashkeela.json"]["eval_allowed_next"] is True

    assert by_file["osian.json"]["lane"] == "restricted_noncommercial"
    assert by_file["saudinewsnet.json"]["lane"] == "restricted_noncommercial"
    assert by_file["saudi_novel_corpus.json"]["lane"] == "blocked_unknown_license"
    assert by_file["alc__arabic_learner_corpus.json"]["lane"] == "blocked_paid_or_custom"
    assert all(row["training_text_allowed_next"] is False for row in rows)


def test_phase27_110_selected_metadata_is_local_and_complete() -> None:
    report = _json(REPORT)
    design = _json(DESIGN)
    rows = _json(MATRIX)

    assert isinstance(report, dict)
    assert isinstance(design, dict)
    assert isinstance(rows, list)
    assert report == design
    assert report["selected_metadata_count"] == 10
    assert SELECTED.exists()
    assert len(list(SELECTED.glob("*.json"))) == 10
    assert (SELECTED / "qabas.json").exists()
    assert (SELECTED / "tashkeela.json").exists()


def test_phase27_110_doc_names_next_phase() -> None:
    text = DOC.read_text(encoding="utf-8")

    assert "Phase 27.110" in text
    assert "PHASE27_110_LICENSED_INGESTION_DESIGN_DECISION" in text
    assert "Phase 27.111" in text
