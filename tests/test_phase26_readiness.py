"""Phase 26 — SF-50M readiness/scaling gate."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from sf_ai.training.phase26_readiness import build_phase26_scaling_decision


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/reports/phase26_sf50m_readiness_report.json"
client = TestClient(app)


def test_phase26_scaling_gate_blocks_sf50m_training_now() -> None:
    decision = build_phase26_scaling_decision()

    assert decision.phase.startswith("Phase 26")
    assert decision.status == "NOT_READY_IMPROVE_SF10M_AND_CANARY"
    assert decision.target_model == "sf-50m"
    assert decision.can_start_sf50m_training is False
    assert decision.corpus["training_records"] == 5543
    assert decision.corpus["min_training_records"] == 5000
    assert decision.corpus["dialects"] == {"msa": 2749, "saudi": 2794}
    assert decision.tokenizer["ready"] is True
    assert decision.phase24["training_passed"] is True
    assert decision.phase24["runtime_allowed"] is False
    assert decision.phase25["canary_guard_passed"] is True
    assert decision.phase25["open_chat_allowed"] is False
    assert decision.scaling_gates["corpus_readiness"] is True
    assert decision.scaling_gates["runtime_quality"] is False
    assert "corpus_below_sf50m_minimum" not in decision.blockers
    assert "phase25_real_model_blocked" in decision.blockers


def test_phase26_cli_writes_report_and_is_read_only() -> None:
    proc = subprocess.run(
        [sys.executable, "scripts/phase26_readiness.py"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "SF.AI — Phase 26 SF-50M readiness decision" in proc.stdout
    assert "can_start_sf50m_training      : false" in proc.stdout
    assert "corpus_below_sf50m_minimum" not in proc.stdout
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["status"] == "NOT_READY_IMPROVE_SF10M_AND_CANARY"
    assert report["can_start_sf50m_training"] is False
    assert report["target_config"]["name"] == "sf-50m"
    assert report["target_config"]["sovereign"] is True


def test_phase26_readiness_endpoint() -> None:
    r = client.get("/system/phase26-readiness")
    assert r.status_code == 200
    body = r.json()
    assert body["phase"].startswith("Phase 26")
    assert body["status"] == "NOT_READY_IMPROVE_SF10M_AND_CANARY"
    assert body["language_track"] == ["msa", "saudi"]
    assert body["can_start_sf50m_training"] is False
    assert body["corpus"]["training_records"] == 5543
    assert body["phase25"]["real_model_guard_reason"] == "malformed_token"
    assert body["scaling_gates"]["tokenization_audit"] is True
    assert body["scaling_gates"]["runtime_quality"] is False
