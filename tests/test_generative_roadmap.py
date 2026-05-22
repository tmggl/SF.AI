"""Phase 21 — generative roadmap documentation guardrails."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_generative_roadmap_names_quality_milestones() -> None:
    text = (ROOT / "docs/GENERATIVE_ROADMAP.md").read_text(encoding="utf-8")
    assert "Phase 24" in text
    assert "SF-10M v0.2" in text
    assert "Phase 26" in text
    assert "SF-25M v0.1" in text
    assert "Phase 28" in text
    assert "SF-50M v0.1" in text


def test_execution_plan_extends_through_phase_30() -> None:
    text = (ROOT / "docs/EXECUTION_PLAN.md").read_text(encoding="utf-8")
    for phase in range(21, 31):
        assert f"Phase {phase}" in text
    assert "Continuous Improvement Loop" in text


def test_current_goals_explain_template_vs_generator_path() -> None:
    text = (ROOT / "docs/CURRENT_GOALS.md").read_text(encoding="utf-8")
    assert "أول توليد خام: Phase 13" in text
    assert "أول تدريب جودة مفيد قادم: Phase 24" in text
    assert "أول فرصة لحوار قصير مولّد يقنعك: Phase 26" in text
    assert "أول هدف رسمي لحوار مولّد مقنع ومستقر نسبيًا: Phase 28" in text
