"""Phase 21 — generative roadmap documentation guardrails."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_generative_roadmap_names_quality_milestones() -> None:
    text = (ROOT / "docs/GENERATIVE_ROADMAP.md").read_text(encoding="utf-8")
    assert "Phase 24" in text
    assert "SF-10M v0.2" in text
    assert "Phase 26" in text
    assert "SF-50M v0.1" in text
    assert "Phase 28" in text
    assert "SF-120M v0.1" in text


def test_execution_plan_extends_through_phase_30() -> None:
    text = (ROOT / "docs/EXECUTION_PLAN.md").read_text(encoding="utf-8")
    for phase in range(21, 31):
        assert f"Phase {phase}" in text
    assert "Continuous Improvement Loop" in text


def test_current_goals_explain_template_vs_generator_path() -> None:
    text = (ROOT / "docs/CURRENT_GOALS.md").read_text(encoding="utf-8")
    assert "أول توليد خام: Phase 13" in text
    assert "أول تدريب جودة مفيد اكتمل في Phase 24" in text
    assert "أول فرصة لحوار قصير مولّد يقنعك: بعد إصلاح assistant-target/loss masking" in text
    assert "أول قفزة أكبر بعد نجاح الحوار: Phase 28 مع `SF-120M`" in text


def test_progressive_scaling_strategy_is_governed() -> None:
    scaling = (ROOT / "docs/SCALING_STRATEGY.md").read_text(encoding="utf-8")
    constitution = (ROOT / "docs/PROJECT_CONSTITUTION.md").read_text(encoding="utf-8")
    rules = (ROOT / "docs/ENGINEERING_RULES.md").read_text(encoding="utf-8")
    lifecycle = (ROOT / "docs/PROJECT_LIFECYCLE.md").read_text(encoding="utf-8")
    plan = (ROOT / "docs/EXECUTION_PLAN.md").read_text(encoding="utf-8")

    required = [
        "Progressive Scaling Strategy",
        "لا يتم رفع حجم النموذج إلا بعد نجاح المرحلة الحالية",
        "SF-10M",
        "SF-50M",
        "SF-120M",
        "SF-350M",
        "SF-700M",
        "SF-1B+",
        "corpus readiness",
        "tokenization audit",
        "evaluation suite",
        "safety checks",
        "runtime quality",
        "hallucination checks",
        "repetition checks",
        "resource readiness",
    ]
    for doc in (scaling, constitution, rules, lifecycle, plan):
        for phrase in required:
            assert phrase in doc
