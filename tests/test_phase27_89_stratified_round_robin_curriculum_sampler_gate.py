"""Phase 27.89 — stratified round-robin sampler gate tests."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.phase27_89_stratified_round_robin_curriculum_sampler_gate import (
    DEFAULT_REPORT,
    build_report,
    parse_args,
)


def test_phase27_89_gate_passes_with_balanced_windows() -> None:
    args = parse_args([])
    report = build_report(args)

    assert report["phase"] == "Phase 27.89"
    assert report["status"] == (
        "PHASE27_89_STRATIFIED_ROUND_ROBIN_SAMPLER_GATE_PASSED_TRAINING_ALLOWED_NEXT"
    )
    assert report["decision"]["new_training_allowed"] is True
    assert report["decision"]["runtime_release_allowed"] is False
    assert report["decision"]["sf50m_justified_transition"] is False
    assert report["decision"]["required_training_flag"] == "--split-order family_round_robin"
    assert report["round_robin_first_1800_counts"]["topic"] >= 300
    for window in report["round_robin_windows"].values():
        assert window["total"] == 600
        assert window["missing_families"] == []
        assert window["min_family_count"] >= 80
        assert window["dominant_share"] <= 0.25


def test_phase27_89_report_artifact_matches_gate() -> None:
    assert DEFAULT_REPORT.exists()
    report = json.loads(Path(DEFAULT_REPORT).read_text(encoding="utf-8"))
    assert report["decision"]["engineering_decision"] == (
        "ALLOW_PHASE27_90_BOUNDED_SF10M_TRAINING_WITH_ROUND_ROBIN_SPLIT_ORDER"
    )
