"""Phase 27.85 — explicit family conditioning objective design coverage."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _report() -> dict:
    return json.loads(
        (
            ROOT
            / "artifacts/reports/phase27_85_explicit_family_conditioning_objective_design_report.json"
        ).read_text(encoding="utf-8")
    )


def test_phase27_85_design_allows_renderer_gate_but_blocks_training() -> None:
    report = _report()

    assert report["phase"] == "Phase 27.85"
    assert report["status"] == "PHASE27_85_EXPLICIT_FAMILY_CONDITIONING_DESIGN_READY_NO_TRAINING"
    assert report["training_started"] is False
    assert report["runtime_changed"] is False
    assert report["design_ready"] is True

    decision = report["decision"]
    assert decision["engineering_decision"] == "ALLOW_PHASE27_86_RENDERER_GATE_IMPLEMENTATION_NO_TRAINING"
    assert decision["renderer_implementation_allowed"] is True
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert "Phase 27.86" in decision["next_phase"]


def test_phase27_85_family_labels_are_explicit_arabic_context() -> None:
    spec = _report()["objective_spec"]

    assert spec["family_labels"] == {
        "open_social": "سوالف",
        "followup": "متابعة",
        "planning": "تنظيم",
        "support": "دعم",
        "topic": "موضوع",
    }
    preview = spec["examples"]["planning"]["rendered_preview"]
    assert "النطاق: سعودي" in preview
    assert "عائلة الحوار: تنظيم" in preview
    assert "المستخدم:" in preview
    assert "المساعد:" in preview


def test_phase27_85_keeps_conditioning_context_masked_from_assistant_loss() -> None:
    spec = _report()["objective_spec"]

    assert "context only" in spec["rendering_rule"]
    assert "conditioning lines and user turns remain masked" in spec["assistant_loss_rule"]
    assert spec["canary_thresholds"]["overall_min_pass"] == 55
    assert spec["canary_thresholds"]["dominant_family_share_max"] == 0.35
