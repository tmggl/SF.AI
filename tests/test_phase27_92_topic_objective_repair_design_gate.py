"""Phase 27.92 — topic-objective repair design gate tests."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.phase27_92_topic_objective_repair_design_gate import (
    build_report,
    parse_args,
)

ROOT = Path(__file__).resolve().parents[1]


def test_phase27_92_design_gate_allows_only_next_gate_encoding(tmp_path: Path) -> None:
    args = parse_args(
        [
            "--report",
            str(tmp_path / "report.json"),
            "--decision",
            str(tmp_path / "decision.json"),
            "--spec",
            str(tmp_path / "spec.json"),
            "--doc",
            str(tmp_path / "report.md"),
        ]
    )
    report, spec = build_report(args)
    decision = report["decision"]

    assert report["phase"] == "Phase 27.92"
    assert report["status"] == "PHASE27_92_TOPIC_OBJECTIVE_REPAIR_DESIGN_READY_NO_TRAINING"
    assert report["design_ready"] is True
    assert decision["decision_id"] == "PHASE27_92_TOPIC_OBJECTIVE_REPAIR_DESIGN_DECISION"
    assert decision["engineering_decision"] == "ALLOW_PHASE27_93_TOPIC_OBJECTIVE_GATE_ENCODING_NO_TRAINING"
    assert decision["new_training_allowed"] is False
    assert decision["topic_gate_encoding_allowed"] is True
    assert decision["runtime_release_allowed"] is False
    assert decision["ui_release_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["tokenizer_retrain_allowed"] is False
    assert decision["next_phase"].startswith("Phase 27.93")
    assert "الموضوع المطلوب: <topic_term>" in spec["conditioning_lines"]
    assert set(spec["target_terms"]) >= {
        "الوفاء",
        "التعاون",
        "الصبر",
        "الاحترام",
        "الهدوء",
        "الصدق",
        "الصداقة",
        "الشجاعة",
    }
    assert spec["canary_design"]["known_topic_canary_min"] == "18/20"
    assert spec["canary_design"]["fresh_topic_shadow_min"] == "16/20"
    assert spec["canary_design"]["all_family_regression_min"] == "45/50"


def test_phase27_92_artifacts_match_decision_and_spec() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/phase27_92_topic_objective_repair_design_gate_report.json")
        .read_text(encoding="utf-8")
    )
    decision = json.loads(
        (ROOT / "artifacts/reports/PHASE27_92_TOPIC_OBJECTIVE_REPAIR_DESIGN_DECISION.json")
        .read_text(encoding="utf-8")
    )
    spec = json.loads(
        (ROOT / "artifacts/reports/phase27_92_topic_objective_repair_spec.json")
        .read_text(encoding="utf-8")
    )

    assert report["decision"] == decision
    assert report["objective_spec"] == spec
    assert decision["new_training_allowed"] is False
    assert decision["topic_gate_encoding_allowed"] is True
    assert spec["blocked"] == [
        "training before Phase 27.93 gate encoding",
        "runtime release",
        "SF-50M transition",
        "tokenizer retrain",
        "pretrained/open-weight usage",
    ]
