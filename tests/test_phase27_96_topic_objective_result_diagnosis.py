"""Phase 27.96 — topic-objective result diagnosis coverage."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.phase27_96_topic_objective_result_diagnosis import (
    DEFAULT_REPORT,
    build_report,
    parse_args,
)

ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "artifacts/reports/PHASE27_96_TOPIC_OBJECTIVE_RESULT_DIAGNOSIS_DECISION.json"


def test_phase27_96_diagnoses_topic_variable_binding_without_training() -> None:
    report = build_report(parse_args([]))
    decision = report["decision"]

    assert report["phase"] == "Phase 27.96"
    assert report["status"] == (
        "PHASE27_96_DIAGNOSED_TOPIC_VARIABLE_BINDING_FAILURE_NO_TRAINING"
    )
    assert report["training_started"] is False
    assert report["runtime_changed"] is False
    assert report["score_summary"]["known_topic"] == "10/16"
    assert report["score_summary"]["fresh_topic"] == "4/10"
    assert report["score_summary"]["all_family"] == "33/50"
    assert report["diagnosis_signals"]["guard_blocked_topic_failures"] == 0
    assert report["diagnosis_signals"]["wrong_topic_substitution_count"] == 11
    assert report["diagnosis_signals"]["topic_variable_binding_failure"] is True

    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["tokenizer_retrain_allowed"] is False
    assert decision["topic_copy_objective_design_allowed"] is True
    assert "Phase 27.97" in decision["next_phase"]


def test_phase27_96_prioritizes_objective_over_capacity() -> None:
    report = json.loads(Path(DEFAULT_REPORT).read_text(encoding="utf-8"))
    weights = report["root_cause_weights"]

    assert weights["topic_variable_binding_failure"] == 34
    assert weights["assistant_target_copy_objective_weak"] == 22
    assert weights["model_capacity"] == 3
    assert weights["tokenizer"] == 3
    assert weights["topic_variable_binding_failure"] > weights["model_capacity"]


def test_phase27_96_decision_artifact_matches_report() -> None:
    report = json.loads(Path(DEFAULT_REPORT).read_text(encoding="utf-8"))
    decision = json.loads(DECISION.read_text(encoding="utf-8"))

    assert report["decision"] == decision
    assert decision["engineering_decision"] == (
        "DESIGN_TOPIC_COPY_CONTRASTIVE_OBJECTIVE_BEFORE_ANY_TRAINING"
    )
    assert report["topic_failure_counts"]["wrong_topic_substitutions"]["الصداقة"] == 6
