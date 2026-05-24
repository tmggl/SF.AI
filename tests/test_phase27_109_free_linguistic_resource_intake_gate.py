"""Phase 27.109 — free linguistic resource intake gate coverage."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/reports/phase27_109_free_linguistic_resource_intake_gate_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_109_FREE_LINGUISTIC_RESOURCE_INTAKE_GATE_DECISION.json"
MANIFEST = ROOT / "resources/external_sources/free_linguistic_resources_manifest.json"
MASADER = ROOT / "resources/external_sources/masader_datasets_index_summary.json"
DOC = ROOT / "docs/PHASE27_109_FREE_LINGUISTIC_RESOURCE_INTAKE_GATE_REPORT.md"


def _json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase27_109_decision_is_metadata_only_no_training() -> None:
    report = _json(REPORT)
    decision = _json(DECISION)

    assert isinstance(report, dict)
    assert isinstance(decision, dict)
    assert report["phase"] == "Phase 27.109"
    assert report["status"] == "PHASE27_109_FREE_RESOURCE_INTAKE_READY_NO_TRAINING"
    assert report["decision"] == decision
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_110_QABAS_MASADER_TASHKEELA_LICENSED_INGESTION_DESIGN_NO_TRAINING"
    )
    assert decision["metadata_fetch_allowed"] is True
    assert decision["external_training_text_import_allowed"] is False
    assert decision["external_tokenizer_vocab_import_allowed"] is False
    assert decision["pretrained_weights_allowed"] is False
    assert decision["runtime_release_allowed"] is False


def test_phase27_109_manifest_contains_shortcut_sources() -> None:
    manifest = _json(MANIFEST)
    assert isinstance(manifest, list)
    by_id = {item["id"]: item for item in manifest}

    assert {"qabas", "masader", "tashkeela", "osian"} <= set(by_id)
    assert by_id["qabas"]["intake_decision"] == "candidate_vocabulary_and_topic_bootstrap"
    assert by_id["masader"]["intake_decision"] == "approved_metadata_catalogue_only"
    assert by_id["tashkeela"]["license"].startswith("CC BY 4.0")
    assert by_id["osian"]["intake_decision"] == "restricted_noncommercial_eval_or_vocabulary_only"
    assert all(item["training_text_allowed_now"] is False for item in manifest)
    assert all(item["tokenizer_vocab_allowed_now"] is False for item in manifest)


def test_phase27_109_masader_metadata_was_pulled_without_training_text() -> None:
    summary = _json(MASADER)

    assert isinstance(summary, dict)
    assert summary["source"].endswith("/repos/ARBML/masader/contents/datasets")
    assert summary["file_count"] is None or summary["file_count"] >= 500
    assert summary["note"] == "Metadata only. No external training text was imported."
    if summary["fetched"]:
        assert summary["candidate_preview_count"] > 0
        assert all("download_url" in item for item in summary["candidate_preview"])


def test_phase27_109_doc_names_next_phase() -> None:
    text = DOC.read_text(encoding="utf-8")

    assert "Phase 27.109" in text
    assert "PHASE27_109_FREE_LINGUISTIC_RESOURCE_INTAKE_GATE_DECISION" in text
    assert "Phase 27.110" in text
