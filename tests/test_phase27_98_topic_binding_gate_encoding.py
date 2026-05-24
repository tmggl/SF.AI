"""Phase 27.98 — topic binding gate encoding coverage."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.phase27_98_topic_binding_gate_encoding import (
    DEFAULT_REPORT,
    build_report,
    parse_args,
)

ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "artifacts/reports/PHASE27_98_TOPIC_BINDING_GATE_ENCODING_DECISION.json"
CANARY = ROOT / "eval/prompts/phase27_98_topic_binding_contrastive_canary.json"


def test_phase27_98_gate_passes_after_phase27_99_metadata_repair() -> None:
    report, canary = build_report(parse_args([]))
    decision = report["decision"]

    assert report["phase"] == "Phase 27.98"
    assert report["training_started"] is False
    assert report["runtime_changed"] is False
    assert report["encoded_gate_passed"] is True
    assert report["metadata_ready"] is True
    assert report["copy_anchor_ready"] is True
    assert report["training_ready"] is True
    assert report["metadata_audit"]["missing_topic_term_records"] == 0

    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_100_BOUNDED_TOPIC_BINDING_REPAIR_TRAINING"
    )
    assert decision["new_training_allowed"] is True
    assert decision["data_repair_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["tokenizer_retrain_allowed"] is False
    assert "Phase 27.100" in decision["next_phase"]

    assert canary["coverage"]["prompt_count"] == 26
    assert canary["coverage"]["known_count"] == 16
    assert canary["coverage"]["fresh_count"] == 10
    assert canary["coverage"]["all_terms_covered"] is True
    assert canary["coverage"]["all_dialects_covered"] is True


def test_phase27_98_renderer_and_mask_probes_pass() -> None:
    report, _ = build_report(parse_args([]))

    assert report["renderer_probe"]["passed"] is True
    assert report["mask_probe"]["passed"] is True
    assert report["stream_probe"]["has_topic_sample_in_training_stream"] is True
    assert report["canary_ready"] is True
    assert report["topic_round_robin_probe"]["blocked_for_training"] is False


def test_phase27_98_artifacts_match_decision_and_canary() -> None:
    report = json.loads(Path(DEFAULT_REPORT).read_text(encoding="utf-8"))
    decision = json.loads(DECISION.read_text(encoding="utf-8"))
    canary = json.loads(CANARY.read_text(encoding="utf-8"))

    assert report["decision"] == decision
    assert report["canary_manifest_path"] == (
        "eval/prompts/phase27_98_topic_binding_contrastive_canary.json"
    )
    assert canary["suite_id"] == "phase27_98_topic_binding_contrastive_canary"
    assert decision["new_training_allowed"] is True
    assert decision["data_repair_allowed"] is False
