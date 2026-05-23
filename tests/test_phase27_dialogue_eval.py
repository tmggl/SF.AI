"""Phase 27 — Dialogue Evaluation v2 + corpus expansion plan."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from sf_ai.evaluation import load_dialogue_scenarios, run_phase27_dialogue_eval


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/reports/phase27_dialogue_eval_v2_report.json"
client = TestClient(app)


def test_dialogue_v2_suite_is_multiturn_msa_saudi_only() -> None:
    scenarios = load_dialogue_scenarios(ROOT / "eval/prompts/dialogue_v2.json")
    assert len(scenarios) == 7
    assert sum(len(s.turns) for s in scenarios) == 19
    assert {s.dialect for s in scenarios} <= {"msa", "saudi"}
    assert {
        "social",
        "qa",
        "project_meta",
        "clarification",
        "safety",
        "tool_boundary",
        "followup",
    } <= {s.category for s in scenarios}
    assert any(t.required_response_terms for s in scenarios for t in s.turns)
    assert any(t.forbidden_response_terms for s in scenarios for t in s.turns)


def test_phase27_dialogue_eval_passes_baseline_but_blocks_scaling() -> None:
    report = run_phase27_dialogue_eval()
    assert report.status == "COMPLETED_DIALOGUE_EVAL_V2_BASELINE_PASS_EXPANSION_REQUIRED"
    assert report.total_scenarios == 7
    assert report.total_turns == 19
    assert report.passed_turns == 19
    assert report.failed_turns == 0
    assert report.dialogue_baseline_passed is True
    assert report.open_generator_ready is False
    assert report.can_reopen_sf50m_gate is False
    assert report.can_start_phase28 is False
    assert report.generator_modes == {"template": 19}
    assert report.phase26_status == "NOT_READY_EXPAND_CORPUS_AND_IMPROVE_SF10M"
    assert report.corpus_expansion_plan["current_records"] == 2143
    assert report.corpus_expansion_plan["target_records"] == 5000
    assert report.corpus_expansion_plan["remaining_records"] == 2857
    assert report.corpus_expansion_plan["needed_by_dialect"] == {
        "msa": 1451,
        "saudi": 1406,
    }
    assert "corpus_expansion_required" in report.blockers
    assert "sf50m_not_trained_or_validated" in report.blockers


def test_phase27_cli_writes_eval_and_artifact_reports() -> None:
    proc = subprocess.run(
        [sys.executable, "scripts/phase27_dialogue_eval.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "SF.AI — Phase 27 dialogue evaluation v2" in proc.stdout
    assert "turns                     : 19/19" in proc.stdout
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["status"] == "COMPLETED_DIALOGUE_EVAL_V2_BASELINE_PASS_EXPANSION_REQUIRED"
    assert report["can_start_phase28"] is False
    assert report["corpus_expansion_plan"]["remaining_records"] == 2857


def test_phase27_dialogue_eval_endpoint() -> None:
    r = client.get("/system/phase27-dialogue-eval")
    assert r.status_code == 200
    body = r.json()
    assert body["phase"].startswith("Phase 27")
    assert body["status"] == "COMPLETED_DIALOGUE_EVAL_V2_BASELINE_PASS_EXPANSION_REQUIRED"
    assert body["language_track"] == ["msa", "saudi"]
    assert body["passed_turns"] == body["total_turns"] == 19
    assert body["generator_modes"] == {"template": 19}
    assert body["open_generator_ready"] is False
    assert body["can_start_phase28"] is False
    assert body["corpus_expansion_plan"]["target_records"] == 5000
