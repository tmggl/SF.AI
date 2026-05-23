"""Phase 27.13 — SF-10M v0.8 boundary/EOS wider training report."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_phase27_13_report_records_eval_improvement_but_blocks_runtime() -> None:
    report_path = ROOT / "artifacts/reports/sf_10m_v0_8_boundary_eos_training_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert report["phase"] == "Phase 27.13"
    assert report["status"] == "completed_eval_improved_generation_still_blocked"
    assert report["language_track"] == ["msa", "saudi"]
    assert report["lexicon_track"] == "Saudi Seed v1"
    assert report["training"]["boundary_eos_target"] is True
    assert report["training"]["dialect_conditioning"] is True
    assert report["eval"]["best_checkpoint"] == "sf-10m-step6000"
    assert report["eval"]["checkpoints"][-1]["loss"] == 3.1875
    assert report["generation_quality"]["passed"] == 3
    assert report["generation_quality"]["runtime_allowed"] is False
    assert report["quality_decision"]["activate_in_chat_ui"] is False
    assert report["quality_decision"]["start_sf50m"] is False
