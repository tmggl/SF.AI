"""Phase 19 — SF-50M readiness gate."""

from __future__ import annotations

import subprocess
import sys

from sf_ai.training.phase19_readiness import build_phase19_readiness_decision


def test_phase19_readiness_reports_current_corpus_is_too_small() -> None:
    decision = build_phase19_readiness_decision()

    assert decision.phase.startswith("Phase 19")
    assert decision.target_model == "sf-50m"
    assert decision.training_records == 500
    assert decision.min_training_records == 5000
    assert decision.can_start_training is False
    assert decision.lab_experiment_allowed is True
    assert "corpus_too_small_for_sf50m" in decision.blockers
    assert "missing_required_msa_or_saudi_balance" not in decision.blockers
    assert decision.action == "FOLLOW_PHASE23_24_AND_CONTINUE_CORPUS_SCALING_BEFORE_SF50M"


def test_phase19_readiness_cli_is_read_only() -> None:
    proc = subprocess.run(
        [sys.executable, "scripts/phase19_readiness.py"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert proc.returncode == 0
    assert "SF.AI — Phase 19 readiness decision" in proc.stdout
    assert "can_start_training            : false" in proc.stdout
    assert "corpus_too_small_for_sf50m" in proc.stdout
