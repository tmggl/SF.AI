"""Phase 27.26–27.30 repair series reports."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _report(name: str) -> dict:
    return json.loads((ROOT / "artifacts/reports" / name).read_text(encoding="utf-8"))


def test_phase27_26_improves_heldout_but_blocks_runtime() -> None:
    report = _report("phase27_26_heldout_objective_repair_report.json")
    assert report["phase"] == "Phase 27.26"
    assert report["heldout"]["passed"] == 9
    assert report["micro_probe_regression"]["passed"] == 32
    assert report["runtime_allowed"] is False


def test_phase27_27_old_heldout_passes_but_shadow_blocks_runtime() -> None:
    report = _report("phase27_27_broader_heldout_repair_report.json")
    assert report["phase"] == "Phase 27.27"
    assert report["heldout_27_25"]["passed"] == 16
    assert report["shadow_27_27"]["passed"] == 9
    assert report["runtime_allowed"] is False


def test_phase27_28_intent_conditioning_improves_shadow() -> None:
    report = _report("phase27_28_intent_conditioned_repair_report.json")
    assert report["phase"] == "Phase 27.28"
    assert report["shadow_27_27"]["passed"] == 12
    assert report["micro_probe_regression"]["passed"] == 32
    assert report["runtime_allowed"] is False


def test_phase27_29_topic_conditioning_blocks_on_leakage() -> None:
    report = _report("phase27_29_topic_conditioned_definition_repair_report.json")
    assert report["phase"] == "Phase 27.29"
    assert report["definition_shadow_27_29"]["passed"] == 6
    assert report["training"]["shadow_prompt_leakage"]
    assert report["runtime_allowed"] is False


def test_phase27_30_fresh_mixed_shadow_blocks_runtime() -> None:
    report = _report("phase27_30_fresh_mixed_shadow_canary_report.json")
    assert report["phase"] == "Phase 27.30"
    assert report["fresh_mixed_shadow"]["passed"] == 16
    assert report["fresh_mixed_shadow"]["eval_records"] == 18
    assert report["runtime_allowed"] is False
    prompts = {row["prompt"] for row in report["failures"]}
    assert "شكرًا لمساعدتك" in prompts
    assert "كيفك اليوم" in prompts
