"""Mandatory SF-native Objective/Curriculum/Decoding plan gate."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/reports/PHASE27_OBJECTIVE_CURRICULUM_DECODING_PLAN.json"
DOC = ROOT / "docs/PHASE27_OBJECTIVE_CURRICULUM_DECODING_PLAN.md"


def _report() -> dict:
    return json.loads(REPORT.read_text(encoding="utf-8"))


def test_phase27_plan_blocks_training_runtime_scaling_and_tokenizer() -> None:
    report = _report()
    decision = report["decision"]
    assert report["report_id"] == "PHASE27_OBJECTIVE_CURRICULUM_DECODING_PLAN"
    assert report["phase"] == "Phase 27.79"
    assert report["active_track"] == "SF-native Objective/Curriculum/Decoding Acceleration Track"
    assert report["training_started"] is False
    assert report["tokenizer_training_started"] is False
    assert report["runtime_changed"] is False
    assert decision["new_training_allowed"] is False
    assert decision["tokenizer_retrain_allowed"] is False
    assert decision["sf50m_allowed"] is False
    assert decision["runtime_release_allowed"] is False


def test_phase27_plan_defines_assistant_only_family_conditioned_objective() -> None:
    objective = _report()["objective_plan"]
    assert objective["name"] == "family_conditioned_assistant_only_objective_v2"
    assert objective["loss_scope"] == "assistant_text_and_eos_only"
    assert objective["eos_required"] is True
    assert "النطاق: سعودي" in objective["example"]
    assert "عائلة الحوار: تنظيم" in objective["example"]
    assert "المستخدم: كيف أنظم يومي؟" in objective["example"]
    assert "المساعد: اكتب ثلاث مهام، وابدأ بالأهم لمدة قصيرة. <eos>" in objective["example"]
    assert "user_line" in objective["loss_excludes"]


def test_phase27_plan_requires_round_robin_curriculum_and_guarded_decoding() -> None:
    report = _report()
    curriculum = report["curriculum_plan"]
    decoding = report["decoding_policy"]
    assert curriculum["required_families"] == [
        "open_social",
        "followup",
        "planning",
        "support",
        "topic",
    ]
    assert curriculum["window_balance_gate"]["fail_if_missing_any_family"] is True
    assert "stop_at_eos" in decoding["controls"]
    assert "no_repeat_ngram" in decoding["controls"]
    assert "topic_substitution_guard" in decoding["controls"]
    assert "template_masking_forbidden" in decoding["controls"]


def test_phase27_plan_defers_amp_lora_and_preference_optimization() -> None:
    tooling = _report()["acceleration_tooling"]
    assert tooling["mps_amp_plan"]["amp_allowed_after_smoke_test_only"] is True
    assert tooling["mps_amp_plan"]["disable_amp_if_unstable"] is True
    assert tooling["logging"]["local_only"] is True
    assert "family_accuracy" in tooling["logging"]["required_metrics"]
    assert tooling["lora_gate"]["status"] == "deferred"
    assert tooling["lora_gate"]["allowed_only_on_sf_native_models"] is True
    assert tooling["preference_optimization_gate"]["status"] == "deferred"
    assert tooling["preference_optimization_gate"]["external_model_preferences_forbidden"] is True


def test_phase27_plan_doc_exists_and_names_next_bounded_training_gate() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "PHASE27_OBJECTIVE_CURRICULUM_DECODING_PLAN" in text
    assert "Phase 27.80 — Bounded SF-10M Family-Conditioned Repair Training" in text
    assert "RUNTIME_RELEASE_ALLOWED=true" in text
