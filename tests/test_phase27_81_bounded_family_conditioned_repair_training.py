"""Phase 27.81 — bounded SF-10M family-conditioned repair training."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/reports/phase27_81_bounded_family_conditioned_repair_training_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_81_BOUNDED_FAMILY_CONDITIONED_REPAIR_TRAINING_DECISION.json"
DOC = ROOT / "docs/PHASE27_81_BOUNDED_FAMILY_CONDITIONED_REPAIR_TRAINING_REPORT.md"
SAMPLES = ROOT / "artifacts/samples/phase27_81_bounded_family_conditioned_repair_training.md"


def _report() -> dict:
    return json.loads(REPORT.read_text(encoding="utf-8"))


def test_phase27_81_training_completed_but_runtime_blocked() -> None:
    report = _report()
    decision = json.loads(DECISION.read_text(encoding="utf-8"))

    assert report["phase"] == "Phase 27.81"
    assert report["status"] == "PHASE27_81_TRAINED_RUNTIME_BLOCKED_DIAGNOSIS_REQUIRED"
    assert report["decision"] == decision
    assert report["training_started"] is True
    assert report["training_completed"] is True
    assert report["runtime_changed"] is False
    assert decision["engineering_decision"] == "BLOCK_RUNTIME_DIAGNOSE_PHASE27_81_RESULT"
    assert decision["runtime_release_allowed"] is False
    assert decision["ui_release_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["tokenizer_retrain_allowed"] is False
    assert decision["next_phase"].startswith("Phase 27.82")


def test_phase27_81_best_checkpoint_improves_all_family_but_misses_gate() -> None:
    report = _report()
    decision = report["decision"]

    assert decision["best_checkpoint"] == "sf-10m-step2000"
    assert decision["all_family"] == "42/50"
    assert decision["prototype_canary"] == "16/16"
    assert decision["known_topic"] == "16/16"
    assert decision["fresh_topic"] == "9/10"
    assert decision["topic_family"] == "10/10"
    assert decision["required_gates"]["all_family"] == "45/50"

    best = next(row for row in report["checkpoints"] if row["checkpoint"] == "sf-10m-step2000")
    families = best["all_family_summary"]["family_summary"]
    assert families["open_social"]["passed"] == 9
    assert families["planning"]["passed"] == 10
    assert families["topic"]["passed"] == 10
    assert families["followup"]["passed"] == 7
    assert families["support"]["passed"] == 6
    assert best["all_family_summary"]["reason_counts"]["expected_terms_missing"] == 8


def test_phase27_81_uses_sovereign_family_round_robin_training() -> None:
    report = _report()
    config = report["train_config"]

    assert report["source_decision"]["decision_id"] == (
        "PHASE27_80_BOUNDED_FAMILY_CONDITIONED_REPAIR_GATE_DECISION"
    )
    assert report["objective"] == "family_conditioned_assistant_only_objective_v2"
    assert report["split_order"] == "family_round_robin"
    assert config["loss_scope"] == "assistant"
    assert config["packing_mode"] == "sample_isolated"
    assert config["amp_enabled"] is False
    assert report["init_checkpoint"].endswith("sf-10m-step1200")


def test_phase27_81_docs_and_samples_exist() -> None:
    doc = DOC.read_text(encoding="utf-8")
    samples = SAMPLES.read_text(encoding="utf-8")

    assert "all-family: `42/50`" in doc
    assert "لا تفعيل للواجهة" in doc
    assert "Best checkpoint: `sf-10m-step2000`" in samples
