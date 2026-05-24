"""Phase 27.105 — raw UI lab diagnosis and non-training repair."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/reports/phase27_105_raw_ui_lab_result_diagnosis_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_105_RAW_UI_LAB_RESULT_DIAGNOSIS_DECISION.json"
DOC = ROOT / "docs/PHASE27_105_RAW_UI_LAB_RESULT_DIAGNOSIS_REPORT.md"


def _report() -> dict:
    return json.loads(REPORT.read_text(encoding="utf-8"))


def test_phase27_105_diagnosis_blocks_training_and_scaling() -> None:
    report = _report()
    decision = json.loads(DECISION.read_text(encoding="utf-8"))

    assert report["phase"] == "Phase 27.105"
    assert report["status"] == "PHASE27_105_DIAGNOSED_RAW_UI_LAB_FAILURES_NO_TRAINING"
    assert report["decision"] == decision
    assert report["training_started"] is False
    assert report["official_runtime_release_allowed"] is False
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["pretrained_allowed"] is False
    assert "Phase 27.106" in decision["next_phase"]


def test_phase27_105_prioritizes_objective_and_conditioning_not_capacity() -> None:
    weights = _report()["root_cause_weights"]

    assert weights["social_subfamily_objective_missing"] == 28
    assert weights["topic_variant_and_orthography_conditioning_gap"] == 22
    assert weights["model_capacity"] == 5
    assert weights["social_subfamily_objective_missing"] > weights["model_capacity"]


def test_phase27_105_records_live_ui_generator_evidence() -> None:
    report = _report()
    probes = {row["prompt"]: row for row in report["live_probes_after_repair"]}

    assert report["live_probe_summary"]["generator_verified"] is True
    assert probes["الصداقه"]["result"] == "pass_after_prompt_normalization"
    assert probes["السلام عليكم"]["result"] == "fail_social_subfamily_missing"
    assert probes["الاخوه"]["result"] == "fail_topic_not_covered_and_general_collapse"
    assert all(row["generator"] == "sf_10m_phase27_81" for row in probes.values())


def test_phase27_105_docs_exist_and_name_next_phase() -> None:
    text = DOC.read_text(encoding="utf-8")

    assert "Phase 27.105" in text
    assert "ليست من `chat_patterns.py`" in text
    assert "Phase 27.106" in text
