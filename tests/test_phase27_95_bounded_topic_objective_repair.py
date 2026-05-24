"""Phase 27.95 — bounded topic-objective repair coverage."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/reports/phase27_95_bounded_topic_objective_repair_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_95_BOUNDED_TOPIC_OBJECTIVE_REPAIR_DECISION.json"


def _report() -> dict:
    return json.loads(REPORT.read_text(encoding="utf-8"))


def test_phase27_95_report_blocks_runtime_and_sf50m() -> None:
    report = _report()
    decision = report["decision"]

    assert report["phase"] == "Phase 27.95"
    assert report["status"] == "PHASE27_95_TRAINED_RUNTIME_BLOCKED_DIAGNOSIS_REQUIRED"
    assert report["training_started"] is True
    assert report["training_completed"] is True
    assert report["runtime_changed"] is False
    assert decision["engineering_decision"] == "BLOCK_RUNTIME_DIAGNOSE_TOPIC_OBJECTIVE_REPAIR_RESULT"
    assert decision["runtime_release_allowed"] is False
    assert decision["ui_release_allowed"] is False
    assert decision["heldout_runtime_gate_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["tokenizer_retrain_allowed"] is False
    assert decision["next_phase"].startswith("Phase 27.96")


def test_phase27_95_best_checkpoint_and_scores_are_recorded() -> None:
    report = _report()
    decision = report["decision"]

    assert decision["best_checkpoint"] == "sf-10m-step1800"
    assert decision["known_topic"] == "10/16"
    assert decision["fresh_topic"] == "4/10"
    assert decision["all_family"] == "33/50"
    assert decision["required_gates"] == {
        "known_topic": "16/16",
        "fresh_topic": "8/10",
        "all_family": "45/50",
    }

    best = next(row for row in report["checkpoints"] if row["checkpoint"] == "sf-10m-step1800")
    assert best["known_topic_summary"]["passed"] == 10
    assert best["fresh_topic_summary"]["passed"] == 4
    assert best["all_family"]["summary"]["family_summary"]["topic"]["passed"] == 4


def test_phase27_95_decision_artifact_matches_report() -> None:
    report = _report()
    decision = json.loads(DECISION.read_text(encoding="utf-8"))

    assert report["decision"] == decision
    assert report["prompt_alignment_fix"].endswith("الموضوع المطلوب for topic prompts.")
    assert report["init_checkpoint"].endswith("sf-10m-step1800")
