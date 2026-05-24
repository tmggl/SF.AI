"""Phase 27.80 — repair gate validation coverage."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.phase27_80_repair_gate_validation import (
    classify_family,
    validate_decoding_policy,
    validate_objective_spec,
)


ROOT = Path(__file__).resolve().parents[1]


def test_phase27_80_report_passes_gates_but_still_blocks_training() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/phase27_80_repair_gate_validation_report.json").read_text(
            encoding="utf-8"
        )
    )

    assert report["phase"] == "Phase 27.80"
    assert report["sovereignty_mode"] == "SF-native only"
    assert report["training_started"] is False
    assert report["tokenizer_training_started"] is False
    assert report["runtime_changed"] is False
    assert report["decision"]["new_training_allowed"] is False
    assert report["decision"]["runtime_release_allowed"] is False
    assert report["decision"]["sf50m_justified_transition"] is False
    assert "pretrained/open-weight model usage" in report["blocked_actions"]

    gates = {gate["gate"]: gate for gate in report["gates"]}
    assert gates["objective_spec_validator"]["passed"] is True
    assert gates["decoding_policy_config_validator"]["passed"] is True
    assert gates["heldout_shadow_canary_manifest_validator"]["passed"] is True
    assert gates["operator_contamination_regression_scan"]["passed"] is True
    assert gates["operator_contamination_regression_scan"]["hit_count"] == 0
    assert gates["curriculum_family_balance_dry_run"]["passed"] is True
    assert gates["family_confusion_matrix_builder"]["passed"] is True
    assert gates["curriculum_family_balance_dry_run"]["mode"] == "explicit_balanced_family_view"
    assert gates["curriculum_family_balance_dry_run"]["family_ratio_max_to_min"] == 1.0


def test_phase27_80_decision_file_matches_report() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/phase27_80_repair_gate_validation_report.json").read_text(
            encoding="utf-8"
        )
    )
    decision = json.loads(
        (ROOT / "artifacts/reports/PHASE27_80_REPAIR_GATE_VALIDATION_DECISION.json").read_text(
            encoding="utf-8"
        )
    )

    assert decision == report["decision"]
    assert decision["decision_id"] == "PHASE27_80_REPAIR_GATE_VALIDATION_DECISION"
    assert decision["engineering_decision"] == "GATES_PASSED_REPAIR_IMPLEMENTATION_ALLOWED_NO_TRAINING"


def test_phase27_80_validators_accept_phase27_79_design() -> None:
    source = json.loads(
        (
            ROOT / "artifacts/reports/phase27_79_objective_curriculum_decoding_design_report.json"
        ).read_text(encoding="utf-8")
    )

    assert validate_objective_spec(source)["passed"] is True
    assert validate_decoding_policy(source)["passed"] is True


def test_phase27_80_family_classifier_covers_required_families() -> None:
    examples = {
        "وش الأخبار اليوم؟": "open_social",
        "يعني كيف أبدأ؟": "followup",
        "نظم وقتي اليوم": "planning",
        "أنا متوتر وش أسوي؟": "support",
        "ما معنى الشجاعة؟": "topic",
    }

    for text, family in examples.items():
        assert classify_family(text) == family
