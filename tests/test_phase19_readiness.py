"""Phase 19 — SF-50M readiness gate."""

from __future__ import annotations

import subprocess
import sys

from sf_ai.training.phase19_readiness import build_phase19_readiness_decision


def test_phase19_readiness_reports_current_corpus_passes_size_gate() -> None:
    decision = build_phase19_readiness_decision()

    assert decision.phase.startswith("Phase 19")
    assert decision.target_model == "sf-50m"
    assert decision.training_records == 8645
    assert decision.min_training_records == 5000
    assert decision.status == "READY_FOR_SF50M_TRAINING"
    assert decision.can_start_training is True
    assert decision.lab_experiment_allowed is True
    assert "corpus_too_small_for_sf50m" not in decision.blockers
    assert "missing_required_msa_or_saudi_balance" not in decision.blockers
    assert decision.action == "START_SF50M_TRAINING"


def test_phase19_readiness_cli_is_read_only() -> None:
    proc = subprocess.run(
        [sys.executable, "scripts/phase19_readiness.py"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert proc.returncode == 0
    assert "SF.AI — Phase 19 readiness decision" in proc.stdout
    assert "can_start_training            : true" in proc.stdout
    assert "corpus_too_small_for_sf50m" not in proc.stdout
