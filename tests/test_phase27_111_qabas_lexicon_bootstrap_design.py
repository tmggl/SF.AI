"""Phase 27.111 — Qabas lexicon bootstrap design coverage."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/reports/phase27_111_qabas_lexicon_bootstrap_design_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_111_QABAS_LEXICON_BOOTSTRAP_DESIGN_DECISION.json"
DESIGN = ROOT / "resources/external_sources/phase27_111_qabas_lexicon_bootstrap_design.json"
SOURCE_CARD = ROOT / "resources/external_sources/qabas_source_card_phase27_111.json"
DOC = ROOT / "docs/PHASE27_111_QABAS_LEXICON_BOOTSTRAP_DESIGN_REPORT.md"
README = ROOT / "resources/lexicons/imported/qabas_bootstrap/README.md"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase27_111_blocks_actual_qabas_import_until_license_resolution() -> None:
    report = _json(REPORT)
    decision = _json(DECISION)

    assert report["phase"] == "Phase 27.111"
    assert report["status"] == "PHASE27_111_QABAS_BOOTSTRAP_DESIGN_READY_IMPORT_BLOCKED"
    assert report["decision"] == decision
    assert decision["engineering_decision"] == "BLOCK_QABAS_IMPORT_ALLOW_PHASE27_112_LICENSE_RESOLUTION_GATE"
    assert decision["license_conflict_detected"] is True
    assert decision["qabas_design_allowed"] is True
    assert decision["qabas_term_import_allowed_now"] is False
    assert decision["external_training_text_import_allowed"] is False
    assert decision["external_tokenizer_vocab_import_allowed"] is False
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False


def test_phase27_111_source_card_captures_license_conflict() -> None:
    card = _json(SOURCE_CARD)

    assert card["source_id"] == "qabas"
    assert card["masader_license"] == "Apache-1.0"
    assert card["observed_primary_license"] == "CC-BY-ND-4.0"
    assert card["license_conflict"] is True
    assert card["allowed_now"]["schema_design"] is True
    assert card["allowed_now"]["raw_entry_import"] is False
    assert card["allowed_now"]["training_text_import"] is False
    assert card["allowed_now"]["tokenizer_vocab_import"] is False
    assert "resolve_apache_vs_cc_by_nd_conflict" in card["required_next_gates"]


def test_phase27_111_design_has_field_mapping_and_no_prohibited_outputs() -> None:
    design = _json(DESIGN)

    assert design["actual_qabas_entries_imported"] is False
    assert design["qabas_design_allowed"] is True
    assert design["qabas_term_import_allowed_now"] is False
    assert {item["sf_field"] for item in design["field_mapping"]} >= {
        "term",
        "root",
        "pos",
        "priority_score",
    }
    assert any(gate["gate"] == "no_tokenizer_vocab_import" for gate in design["gates"])
    assert "data/corpus/**/qabas*.jsonl" in design["future_outputs"]["prohibited_outputs_now"]
    assert "resources/lexicons/imported/qabas_bootstrap/*.jsonl" in design["future_outputs"]["prohibited_outputs_now"]


def test_phase27_111_docs_and_placeholder_are_explicitly_no_import() -> None:
    doc = DOC.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")

    assert "Phase 27.111" in doc
    assert "PHASE27_111_QABAS_LEXICON_BOOTSTRAP_DESIGN_DECISION" in doc
    assert "Phase 27.112" in doc
    assert "No Qabas entries are imported" in readme
    assert "No tokenizer vocab or merges are imported" in readme
