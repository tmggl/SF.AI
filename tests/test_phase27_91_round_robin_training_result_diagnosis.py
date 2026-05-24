"""Phase 27.91 — round-robin training result diagnosis coverage."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.phase27_91_round_robin_training_result_diagnosis import (
    DEFAULT_REPORT,
    build_report,
    parse_args,
)


def test_phase27_91_diagnoses_topic_collapse_and_blocks_training() -> None:
    report = build_report(parse_args([]))

    assert report["phase"] == "Phase 27.91"
    assert report["status"] == "PHASE27_91_DIAGNOSED_TOPIC_COLLAPSE_NO_TRAINING"
    assert report["failure_count"] == 15
    assert report["failure_family_counts"]["topic"] == 9
    assert report["failure_bucket_counts"]["topic_semantic_collapse"] == 7
    assert report["failure_bucket_counts"]["topic_repetition_collapse"] == 2
    decision = report["decision"]
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["tokenizer_retrain_allowed"] is False
    assert decision["topic_repair_design_allowed"] is True
    assert "Phase 27.92" in decision["next_phase"]


def test_phase27_91_report_artifact_matches_decision() -> None:
    report = json.loads(Path(DEFAULT_REPORT).read_text(encoding="utf-8"))
    assert report["root_cause_weights"]["topic_semantic_collapse"] == 48
    assert report["root_cause_weights"]["model_capacity"] == 4
    assert report["decision"]["engineering_decision"] == (
        "DESIGN_TOPIC_OBJECTIVE_REPAIR_GATE_BEFORE_ANY_TRAINING"
    )
