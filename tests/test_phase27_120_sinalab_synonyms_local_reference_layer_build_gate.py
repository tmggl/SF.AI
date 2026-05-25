"""Phase 27.120 — SinaLab Synonyms local reference layer build gate coverage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "resources/external_sources/phase27_120_sinalab_synonyms_local_reference_layer_build_gate.json"
SCHEMA = ROOT / "resources/external_sources/phase27_120_sinalab_synonyms_local_reference_layer_schema.json"
REPORT = ROOT / "artifacts/reports/phase27_120_sinalab_synonyms_local_reference_layer_build_gate_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_120_SINALAB_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_GATE_DECISION.json"
DOC = ROOT / "docs/PHASE27_120_SINALAB_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_GATE_REPORT.md"
REF_GITIGNORE = (
    ROOT / "resources/external_sources/reference_layers/sinalab_synonyms/.gitignore"
)
REF_README = ROOT / "resources/external_sources/reference_layers/sinalab_synonyms/README.md"


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase27_120_decision_allows_only_gitignored_local_build_next() -> None:
    report = _json(REPORT)
    decision = _json(DECISION)

    assert report["phase"] == "Phase 27.120"
    assert report["status"] == (
        "PHASE27_120_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_GATE_READY_NO_IMPORT"
    )
    assert report["decision"] == decision
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_121_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_GITIGNORED_NO_TRAINING"
    )
    assert decision["build_gate_passed"] is True
    assert decision["local_reference_records_allowed_next"] is True
    assert decision["raw_terms_commit_allowed"] is False
    assert decision["dialogue_corpus_allowed"] is False
    assert decision["tokenizer_vocab_allowed"] is False
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_transition_allowed"] is False
    assert "Phase 27.121" in decision["next_phase"]


def test_phase27_120_gate_uses_counts_and_blocks_training_runtime() -> None:
    gate = _json(GATE)
    preconditions = gate["preconditions"]

    assert gate["phase"] == "Phase 27.120"
    assert gate["gate_passed"] is True
    assert all(preconditions.values())
    assert gate["storage_mode"] == "local_gitignored_reference_layer_only"
    assert gate["max_local_reference_records_next"] == 1093
    assert gate["max_local_eval_candidate_records_next"] == 685
    assert gate["raw_terms_commit_allowed"] is False
    assert gate["local_reference_records_allowed_next"] is True
    assert gate["dialogue_corpus_allowed"] is False
    assert gate["tokenizer_vocab_allowed"] is False
    assert gate["training_allowed"] is False
    assert gate["runtime_release_allowed"] is False
    assert gate["sf50m_transition_allowed"] is False
    assert "raw terms in committed files" in gate["blocked_outputs"]


def test_phase27_120_schema_is_values_free_and_local_only() -> None:
    schema = _json(SCHEMA)

    assert schema["schema_id"] == "PHASE27_120_SINALAB_SYNONYMS_LOCAL_REFERENCE_LAYER_SCHEMA"
    assert schema["storage_mode"] == "local_gitignored_reference_layer_only"
    assert "candidate_term" in schema["record_fields_allowed_locally_next"]
    assert schema["field_policy"]["training_allowed"] is False
    assert schema["field_policy"]["dialogue_corpus_allowed"] is False
    assert schema["field_policy"]["tokenizer_vocab_allowed"] is False
    assert schema["field_policy"]["runtime_lookup_allowed"] is False
    assert schema["committed_schema_contains_raw_terms"] is False
    assert schema["committed_schema_contains_record_values"] is False


def test_phase27_120_reference_layer_path_is_gitignored() -> None:
    ignore_text = REF_GITIGNORE.read_text(encoding="utf-8")
    readme_text = REF_README.read_text(encoding="utf-8")

    assert "*" in ignore_text
    assert "!.gitignore" in ignore_text
    assert "!README.md" in ignore_text
    assert "Raw/reference records with terms must stay gitignored" in readme_text
    assert "No corpus, tokenizer, training" in readme_text


def test_phase27_120_report_and_doc_do_not_publish_raw_terms() -> None:
    report = _json(REPORT)

    assert report["training_started"] is False
    assert report["runtime_changed"] is False
    assert report["external_entries_imported"] is False
    assert report["reference_records_written"] is False
    assert report["corpus_changed"] is False
    assert report["tokenizer_changed"] is False
    assert report["raw_terms_published"] is False

    report_text = REPORT.read_text(encoding="utf-8")
    doc_text = DOC.read_text(encoding="utf-8")
    assert '"raw_terms_published": false' in report_text
    assert '"reference_records_written": false' in report_text
    assert '"term":' not in report_text
    assert '"candidate_term": "Arabic candidate term' in report_text
    assert "Phase 27.121" in doc_text
    assert "raw terms in git" in doc_text
    assert "data/corpus" in doc_text
