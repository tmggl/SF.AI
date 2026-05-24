"""Phase 27.90 — bounded round-robin repair result coverage."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.phase27_90_bounded_round_robin_repair import (
    DEFAULT_REPORT,
    build_report,
    parse_args,
)


def test_phase27_90_report_blocks_runtime_and_requires_diagnosis() -> None:
    args = parse_args([])
    report = build_report(args)

    assert report["phase"] == "Phase 27.90"
    assert report["status"] == "PHASE27_90_TRAINED_RUNTIME_BLOCKED_DIAGNOSIS_REQUIRED"
    decision = report["decision"]
    assert decision["training_completed"] is True
    assert decision["runtime_release_allowed"] is False
    assert decision["heldout_runtime_gate_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["tokenizer_retrain_allowed"] is False
    assert decision["best_checkpoint_by_fresh_shadow"] == "sf-10m-step1800"
    assert decision["best_fresh_shadow_passed"] == 35
    assert decision["best_fresh_shadow_total"] == 50
    assert decision["heldout_gate_threshold"] == 45
    assert "Phase 27.91" in decision["next_phase"]


def test_phase27_90_improves_over_phase27_87_but_topic_still_weak() -> None:
    report = json.loads(Path(DEFAULT_REPORT).read_text(encoding="utf-8"))
    best = next(
        row for row in report["checkpoints"]
        if row["checkpoint"] == report["decision"]["best_checkpoint_by_fresh_shadow"]
    )

    assert best["summary"]["passed"] == 35
    assert best["summary"]["family_summary"]["open_social"]["passed"] == 9
    assert best["summary"]["family_summary"]["planning"]["passed"] == 10
    assert best["summary"]["family_summary"]["topic"]["passed"] == 1
    assert best["summary"]["reason_counts"]["expected_terms_missing"] == 13
