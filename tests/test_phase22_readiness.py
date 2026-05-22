"""Phase 22 — Gold Dialogue Corpus v2 readiness gate."""

from __future__ import annotations

import subprocess

from fastapi.testclient import TestClient

from apps.api.main import app
from sf_ai.datasets.phase22_readiness import build_phase22_readiness_decision


client = TestClient(app)


def test_phase22_readiness_reports_current_gap() -> None:
    decision = build_phase22_readiness_decision()
    assert decision.phase.startswith("Phase 22")
    assert decision.status == "NOT_READY_BUILD_GOLD_DIALOGUE_CORPUS_V2"
    assert decision.can_start_phase23 is False
    assert decision.training_records == 30
    assert decision.target_records == 500
    assert decision.remaining_records == 470
    assert decision.dialect_counts == {"saudi": 30}
    assert decision.missing_required_dialects == ("msa",)
    assert decision.synthetic_llm_data_allowed is False
    assert "corpus_below_phase22_target" in decision.blockers
    assert "missing_required_msa_or_saudi" in decision.blockers


def test_phase22_readiness_requires_balance_before_phase23() -> None:
    decision = build_phase22_readiness_decision()
    assert decision.min_per_dialect == 200
    assert decision.dialect_shortfalls["msa"] == 200
    assert decision.dialect_shortfalls["saudi"] == 170
    assert "dialect_balance_below_minimum" in decision.blockers


def test_phase22_endpoint() -> None:
    r = client.get("/system/phase22-readiness")
    assert r.status_code == 200
    body = r.json()
    assert body["phase"].startswith("Phase 22")
    assert body["status"] == "NOT_READY_BUILD_GOLD_DIALOGUE_CORPUS_V2"
    assert body["can_start_phase23"] is False
    assert body["training_records"] == 30
    assert body["target_records"] == 500
    assert body["allowed_dialects"] == ["msa", "saudi"]
    assert body["synthetic_llm_data_allowed"] is False


def test_phase22_cli_is_read_only() -> None:
    proc = subprocess.run(
        [".venv/bin/python", "scripts/phase22_readiness.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "Phase 22 Gold Dialogue Corpus v2 readiness" in proc.stdout
    assert "status                        : NOT_READY_BUILD_GOLD_DIALOGUE_CORPUS_V2" in proc.stdout
    assert "synthetic_llm_data_allowed    : false" in proc.stdout


def test_system_status_reports_phase22_component() -> None:
    r = client.get("/system/status")
    assert r.status_code == 200
    body = r.json()
    assert "Phase 22" in body["current_phase"]
    assert any(
        c["name"] == "phase22_readiness" and c["status"] == "active"
        for c in body["components"]
    )
