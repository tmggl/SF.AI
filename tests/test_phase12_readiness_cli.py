"""Read-only Phase 12 readiness CLI."""

from __future__ import annotations

import subprocess
import sys

from sf_ai.training.phase12_readiness import build_phase12_readiness_decision


def test_phase12_readiness_decision_blocks_training_permission() -> None:
    decision = build_phase12_readiness_decision()

    assert decision.preflight_pass is True
    assert decision.training_permission_granted is True
    assert decision.can_train_now is False
    assert decision.action == "PHASE12_V1_COMPLETED_CONTINUE_PHASE22_CORPUS_TARGET"
    assert decision.required_permission_phrase == "ابدأ Phase 12"
    assert decision.required_confirmation_flag == "--confirm-phase12-permission"
    assert decision.corpus_training_ready == 280
    assert decision.corpus_dialect_counts == {"msa": 200, "saudi": 80}
    assert decision.required_dialects == ("msa", "saudi")
    assert decision.missing_required_dialects == ()
    assert decision.language_balance_status == "READY_MSA_AND_SAUDI"
    assert decision.protected_terms_total == 30
    assert decision.protected_terms_covered == 30
    assert "artifacts/tokenizers/sf_bpe/v1/vocab.json" in decision.artifacts_present
    assert "artifacts/tokenizers/sf_bpe/v1/merges.txt" in decision.artifacts_present


def test_phase12_readiness_script_reports_stop_before_training() -> None:
    proc = subprocess.run(
        [sys.executable, "scripts/phase12_readiness.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert proc.returncode == 0
    assert "preflight_pass                : true" in proc.stdout
    assert "can_train_now                 : false" in proc.stdout
    assert "training_permission_granted   : true" in proc.stdout
    assert "required_confirmation_flag    : --confirm-phase12-permission" in proc.stdout
    assert "action                        : PHASE12_V1_COMPLETED_CONTINUE_PHASE22_CORPUS_TARGET" in proc.stdout
    assert "missing_required_dialects     : none" in proc.stdout
    assert "language_balance_status       : READY_MSA_AND_SAUDI" in proc.stdout
    assert "artifacts:" in proc.stdout
    assert "artifacts/tokenizers/sf_bpe/v1/vocab.json" in proc.stdout
