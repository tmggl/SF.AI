"""Phase 27.112 — Qabas primary license resolution gate coverage."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/reports/phase27_112_qabas_primary_license_resolution_gate_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_112_QABAS_PRIMARY_LICENSE_RESOLUTION_GATE_DECISION.json"
EVIDENCE = ROOT / "resources/external_sources/phase27_112_qabas_license_evidence.json"
DOC = ROOT / "docs/PHASE27_112_QABAS_PRIMARY_LICENSE_RESOLUTION_GATE_REPORT.md"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase27_112_blocks_qabas_import_as_reference_only() -> None:
    report = _json(REPORT)
    decision = _json(DECISION)

    assert report["phase"] == "Phase 27.112"
    assert report["status"] == "PHASE27_112_QABAS_REFERENCE_ONLY_IMPORT_BLOCKED"
    assert report["decision"] == decision
    assert decision["engineering_decision"] == (
        "BLOCK_QABAS_IMPORT_REFERENCE_ONLY_OPEN_PHASE27_113_PERMISSIVE_LEXICAL_ALTERNATIVES"
    )
    assert decision["masader_license"] == "Apache-1.0"
    assert decision["primary_license"] == "CC-BY-ND-4.0"
    assert decision["license_conflict_unresolved"] is True
    assert decision["no_derivatives_detected"] is True
    assert decision["qabas_raw_entry_import_allowed"] is False
    assert decision["qabas_reference_only_allowed"] is True
    assert decision["external_training_text_import_allowed"] is False
    assert decision["external_tokenizer_vocab_import_allowed"] is False
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False


def test_phase27_112_evidence_captures_primary_source_signals() -> None:
    evidence = _json(EVIDENCE)
    by_id = {item["id"]: item for item in evidence["sources"]}

    assert by_id["sinalab_resources"]["url"] == "https://sina.birzeit.edu/resources/"
    assert by_id["sinalab_resources"]["observed_license"] == "CC-BY-ND-4.0"
    assert any("Qabas Lexicon" in snippet for snippet in by_id["sinalab_resources"]["qabas_snippets"])
    assert by_id["qabas_page"]["observed_license"] == "not_explicit_in_page"
    assert by_id["qabas_about"]["observed_license"] == "not_explicit_in_page"


def test_phase27_112_doc_names_next_phase_and_prohibitions() -> None:
    text = DOC.read_text(encoding="utf-8")

    assert "Phase 27.112" in text
    assert "PHASE27_112_QABAS_PRIMARY_LICENSE_RESOLUTION_GATE_DECISION" in text
    assert "reference-only" in text
    assert "Phase 27.113" in text
    assert "tokenizer vocab" in text
