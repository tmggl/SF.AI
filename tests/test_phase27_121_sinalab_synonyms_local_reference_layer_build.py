"""Phase 27.121 — SinaLab Synonyms local reference layer build coverage."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "resources/external_sources/phase27_121_sinalab_synonyms_local_reference_layer_build_manifest.json"
VALIDATION = ROOT / "resources/external_sources/phase27_121_sinalab_synonyms_local_reference_layer_validation.json"
REPORT = ROOT / "artifacts/reports/phase27_121_sinalab_synonyms_local_reference_layer_build_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_121_SINALAB_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_DECISION.json"
DOC = ROOT / "docs/PHASE27_121_SINALAB_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_REPORT.md"


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase27_121_decision_allows_query_eval_gate_only() -> None:
    report = _json(REPORT)
    decision = _json(DECISION)

    assert report["phase"] == "Phase 27.121"
    assert report["status"] == (
        "PHASE27_121_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILT_GITIGNORED_NO_TRAINING"
    )
    assert report["decision"] == decision
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_122_SYNONYMS_REFERENCE_QUERY_AND_EVAL_GATE_NO_TRAINING"
    )
    assert decision["local_reference_layer_build_passed"] is True
    assert decision["local_reference_records_exist"] is True
    assert decision["raw_terms_commit_allowed"] is False
    assert decision["dialogue_corpus_allowed"] is False
    assert decision["tokenizer_vocab_allowed"] is False
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_transition_allowed"] is False
    assert "Phase 27.122" in decision["next_phase"]


def test_phase27_121_manifest_counts_and_hashes_only() -> None:
    manifest = _json(MANIFEST)

    assert manifest["phase"] == "Phase 27.121"
    assert manifest["build_scope"] == "local_reference_records_gitignored_terms_not_committed"
    assert manifest["reference_record_count"] == 1093
    assert manifest["eval_candidate_record_count"] == 685
    assert manifest["quality_band_counts"] == {"high": 685, "medium": 408, "low": 0}
    assert manifest["local_files"]["reference_records"]["line_count"] == 1093
    assert manifest["local_files"]["eval_candidates"]["line_count"] == 685
    assert manifest["local_terms_files_gitignored"] is True
    assert manifest["raw_terms_committed"] is False
    assert manifest["committed_manifest_contains_terms"] is False
    assert manifest["dialogue_corpus_written"] is False
    assert manifest["tokenizer_vocab_written"] is False
    assert manifest["training_started"] is False
    assert manifest["runtime_lookup_enabled"] is False


def test_phase27_121_validation_passes_without_training_or_runtime() -> None:
    validation = _json(VALIDATION)

    assert validation["passed"] is True
    assert all(validation["checks"].values())
    assert validation["raw_terms_published"] is False
    assert validation["reference_records_committed"] is False
    assert validation["training_allowed"] is False
    assert validation["runtime_release_allowed"] is False


def test_phase27_121_local_reference_records_are_gitignored() -> None:
    manifest = _json(MANIFEST)
    paths = [
        ROOT / manifest["local_files"]["reference_records"]["relative_path"],
        ROOT / manifest["local_files"]["eval_candidates"]["relative_path"],
    ]

    for path in paths:
        result = subprocess.run(
            ["git", "check-ignore", str(path.relative_to(ROOT))],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
        assert path.name in result.stdout


def test_phase27_121_committed_outputs_do_not_publish_raw_terms() -> None:
    report = _json(REPORT)

    assert report["training_started"] is False
    assert report["runtime_changed"] is False
    assert report["external_entries_imported"] is False
    assert report["reference_records_written_locally"] is True
    assert report["reference_records_committed"] is False
    assert report["corpus_changed"] is False
    assert report["tokenizer_changed"] is False
    assert report["raw_terms_published"] is False

    text = "\n".join(
        path.read_text(encoding="utf-8") for path in (MANIFEST, VALIDATION, REPORT, DECISION, DOC)
    )
    assert '"raw_terms_published": false' in text
    assert '"reference_records_committed": false' in text
    assert '"candidate_term":' not in text
    assert '"candidate_normalized":' not in text
    assert '"term":' not in text
    assert "raw terms in git" in text
    assert "Phase 27.122" in text
