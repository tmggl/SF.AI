"""Phase 22 — Gold Dialogue Corpus v2 readiness gate."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from sf_ai.datasets.phase22_readiness import (
    build_phase22_collection_plan,
    build_phase22_completion_gate,
    build_phase22_next_batch_brief,
    build_phase22_readiness_decision,
)

client = TestClient(app)
ROOT = Path(__file__).resolve().parents[1]


def test_phase22_readiness_reports_current_gap() -> None:
    decision = build_phase22_readiness_decision()
    assert decision.phase.startswith("Phase 22")
    assert decision.status == "READY_FOR_PHASE23_TOKENIZER_V2"
    assert decision.can_start_phase23 is True
    assert decision.training_records == 9125
    assert decision.target_records == 500
    assert decision.remaining_records == 0
    assert decision.dialect_counts == {"msa": 4535, "saudi": 4590}
    assert decision.missing_required_dialects == ()
    assert decision.synthetic_llm_data_allowed is False
    assert decision.blockers == ()
    assert "missing_required_msa_or_saudi" not in decision.blockers


def test_phase22_readiness_requires_balance_before_phase23() -> None:
    decision = build_phase22_readiness_decision()
    assert decision.min_per_dialect == 200
    assert decision.dialect_shortfalls["msa"] == 0
    assert decision.dialect_shortfalls["saudi"] == 0
    assert "dialect_balance_below_minimum" not in decision.blockers


def test_phase22_endpoint() -> None:
    r = client.get("/system/phase22-readiness")
    assert r.status_code == 200
    body = r.json()
    assert body["phase"].startswith("Phase 22")
    assert body["status"] == "READY_FOR_PHASE23_TOKENIZER_V2"
    assert body["can_start_phase23"] is True
    assert body["training_records"] == 9125
    assert body["target_records"] == 500
    assert body["allowed_dialects"] == ["msa", "saudi"]
    assert body["synthetic_llm_data_allowed"] is False


def test_phase22_collection_plan_calculates_real_quotas() -> None:
    plan = build_phase22_collection_plan()
    assert plan.status == "COLLECTION_COMPLETE_READY_FOR_PHASE23_RECHECK"
    assert plan.current_records == 9125
    assert plan.remaining_records == 0
    assert plan.batch_size == 25
    assert plan.estimated_batches == 0
    assert plan.quota_by_dialect == {}
    assert plan.flexible_records_after_minimums == 0
    assert plan.synthetic_llm_data_allowed is False
    assert any("No external or unprovenanced synthetic LLM data" in rule for rule in plan.review_rules)
    assert len(plan.planned_batches) == 0


def test_phase22_collection_plan_endpoint() -> None:
    r = client.get("/system/phase22-collection-plan?batch_size=50")
    assert r.status_code == 200
    body = r.json()
    assert body["phase"].startswith("Phase 22")
    assert body["batch_size"] == 50
    assert body["estimated_batches"] == 0
    assert body["quota_by_dialect"] == {}
    assert body["synthetic_llm_data_allowed"] is False
    assert len(body["planned_batches"]) == 0


def test_phase22_next_batch_brief_points_to_next_saudi_batch() -> None:
    brief = build_phase22_next_batch_brief()
    assert brief.status == "NO_BATCHES_REMAINING_RECHECK_READINESS"
    assert brief.next_batch is None
    assert "All planned batches are complete" in brief.why_this_batch
    assert brief.acceptance_checklist == ()
    assert brief.suggested_topics == ()
    assert brief.after_export_commands == ("make phase22-readiness", "make phase22-completion-gate")
    assert any("Do not start Phase 23" in warning for warning in brief.warnings)


def test_phase22_msa_authoring_bank_is_not_training_data() -> None:
    path = ROOT / "resources/phase22_authoring/msa_prompt_bank_v1.json"
    raw = json.loads(path.read_text(encoding="utf-8"))
    assert raw["training_allowed"] is False
    assert raw["synthetic_llm_data"] is False
    assert raw["corpus_record"] is False
    assert raw["dialect_scope"] == ["msa"]
    assert len(raw["dialects"]["msa"]) >= 80
    assert "Do not copy this file into data/corpus/chat/jsonl." in raw["notes"]


def test_phase22_next_batch_endpoint() -> None:
    r = client.get("/system/phase22-next-batch")
    assert r.status_code == 200
    body = r.json()
    assert body["phase"].startswith("Phase 22")
    assert body["status"] == "NO_BATCHES_REMAINING_RECHECK_READINESS"
    assert body["next_batch"] is None
    assert body["suggested_topics"] == []
    assert body["warnings"]
    assert body["after_export_commands"] == ["make phase22-readiness", "make phase22-completion-gate"]


def test_phase22_completion_gate_blocks_advancement_until_complete() -> None:
    gate = build_phase22_completion_gate()
    assert gate.status == "PHASE22_COMPLETE_READY_FOR_PHASE23"
    assert gate.can_advance_phase23 is True
    assert gate.readiness_status == "READY_FOR_PHASE23_TOKENIZER_V2"
    assert gate.training_records == 9125
    assert gate.target_records == 500
    assert gate.remaining_records == 0
    assert gate.current_next_batch is None
    assert gate.completion_checks["corpus_target_met"] is True
    assert gate.completion_checks["required_dialects_present"] is True
    assert gate.completion_checks["dialect_balance_met"] is True
    assert gate.completion_checks["no_corpus_governance_issues"] is True
    assert gate.missing_requirements == ()
    assert any("phase22-completion-gate" in item for item in gate.required_before_advance)


def test_phase22_completion_gate_endpoint() -> None:
    r = client.get("/system/phase22-completion-gate")
    assert r.status_code == 200
    body = r.json()
    assert body["phase"].startswith("Phase 22")
    assert body["status"] == "PHASE22_COMPLETE_READY_FOR_PHASE23"
    assert body["can_advance_phase23"] is True
    assert body["current_next_batch"] is None
    assert body["completion_checks"]["corpus_target_met"] is True
    assert body["missing_requirements"] == []


def test_phase22_cli_is_read_only() -> None:
    proc = subprocess.run(
        [".venv/bin/python", "scripts/phase22_readiness.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "Phase 22 Gold Dialogue Corpus v2 readiness" in proc.stdout
    assert "status                        : READY_FOR_PHASE23_TOKENIZER_V2" in proc.stdout
    assert "synthetic_llm_data_allowed    : false" in proc.stdout


def test_phase22_collection_plan_cli_is_read_only() -> None:
    proc = subprocess.run(
        [".venv/bin/python", "scripts/phase22_collection_plan.py", "--batch-size", "50"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "Phase 22 collection plan" in proc.stdout
    assert "estimated_batches             : 0" in proc.stdout
    assert "planned batches:" in proc.stdout
    assert "#01" not in proc.stdout
    assert "synthetic_llm_data_allowed    : false" in proc.stdout


def test_phase22_next_batch_cli_is_read_only() -> None:
    proc = subprocess.run(
        [".venv/bin/python", "scripts/phase22_next_batch.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "Phase 22 next batch" in proc.stdout
    assert "status                        : NO_BATCHES_REMAINING_RECHECK_READINESS" in proc.stdout
    assert "next_batch                    : none" in proc.stdout
    assert "Do not start Phase 23 until phase22-readiness and completion gate pass" in proc.stdout


def test_phase22_completion_gate_cli_is_read_only() -> None:
    proc = subprocess.run(
        [".venv/bin/python", "scripts/phase22_completion_gate.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "Phase 22 completion gate" in proc.stdout
    assert "status                        : PHASE22_COMPLETE_READY_FOR_PHASE23" in proc.stdout
    assert "can_advance_phase23           : true" in proc.stdout
    assert "current_next_batch            : none" in proc.stdout


def test_system_status_reports_phase22_component() -> None:
    r = client.get("/system/status")
    assert r.status_code == 200
    body = r.json()
    assert "Phase 27.126" in body["current_phase"]
    assert any(
        c["name"] == "phase22_readiness" and c["status"] == "active"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase22_collection_plan" and c["status"] == "active"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase22_next_batch" and c["status"] == "active"
        for c in body["components"]
    )
    assert any(
        c["name"] == "phase22_completion_gate" and c["status"] == "active"
        for c in body["components"]
    )
