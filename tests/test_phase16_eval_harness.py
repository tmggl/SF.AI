"""Phase 16 evaluation harness checks."""

from __future__ import annotations

import json
from pathlib import Path

from sf_ai.evaluation import load_eval_cases, run_phase16_eval


ROOT = Path(__file__).resolve().parent.parent


def test_phase16_prompt_suites_are_msa_or_saudi_only() -> None:
    cases = load_eval_cases(
        [
            ROOT / "eval/prompts/saudi_msa_chat_v1.jsonl",
            ROOT / "eval/prompts/safety_v1.jsonl",
        ]
    )
    assert len(cases) == 15
    assert {c.suite for c in cases} == {"saudi_msa_chat_v1", "safety_v1"}
    assert {c.dialect for c in cases} <= {"msa", "saudi"}


def test_phase16_eval_passes_but_blocks_runtime_activation() -> None:
    cases = load_eval_cases(
        [
            ROOT / "eval/prompts/saudi_msa_chat_v1.jsonl",
            ROOT / "eval/prompts/safety_v1.jsonl",
        ]
    )
    report = run_phase16_eval(cases)
    assert report.status == "PASS_WITH_RUNTIME_BLOCKED"
    assert report.total_cases == 15
    assert report.passed_cases == 15
    assert report.failed_cases == 0
    assert report.runtime_activation_allowed is False
    assert report.generator_gate["candidate"] == "sf_10m_v0_1"
    assert report.generator_gate["repetition_detected"] is True
    assert report.lexicon_policy["runtime_focus"] == ["msa", "saudi"]


def test_phase16_report_artifact_matches_latest_gate() -> None:
    report = json.loads(
        (ROOT / "eval/reports/sf_10m_eval_v1.json").read_text(encoding="utf-8")
    )
    assert report["phase"] == "Phase 16 — Evaluation, Safety, and Saudi/MSA Style Harness"
    assert report["status"] == "PASS_WITH_RUNTIME_BLOCKED"
    assert report["passed_cases"] == report["total_cases"] == 15
    assert report["runtime_activation_allowed"] is False
    assert report["suites"] == {"saudi_msa_chat_v1": 10, "safety_v1": 5}
