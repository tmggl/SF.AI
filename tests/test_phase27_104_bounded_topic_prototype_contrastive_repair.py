"""Phase 27.104 — bounded topic-prototype contrastive repair coverage."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/reports/phase27_104_bounded_topic_prototype_contrastive_repair_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_104_BOUNDED_TOPIC_PROTOTYPE_CONTRASTIVE_REPAIR_DECISION.json"
SAMPLES = ROOT / "artifacts/samples/phase27_104_bounded_topic_prototype_contrastive_repair.md"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase27_104_training_improves_topic_but_blocks_runtime() -> None:
    report = _json(REPORT)
    decision = _json(DECISION)

    assert report["phase"] == "Phase 27.104"
    assert report["status"] == "PHASE27_104_TRAINED_RUNTIME_BLOCKED_DIAGNOSIS_REQUIRED"
    assert report["decision"] == decision
    assert report["training_started"] is True
    assert report["training_completed"] is True
    assert report["runtime_changed"] is False
    assert decision["engineering_decision"] == (
        "BLOCK_RUNTIME_DIAGNOSE_TOPIC_PROTOTYPE_REPAIR_RESULT"
    )
    assert decision["runtime_release_allowed"] is False
    assert decision["ui_release_allowed"] is False
    assert decision["heldout_runtime_gate_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["tokenizer_retrain_allowed"] is False
    assert decision["next_phase"].startswith("Phase 27.105")


def test_phase27_104_best_checkpoint_passes_topic_gates_not_all_family() -> None:
    report = _json(REPORT)
    decision = report["decision"]

    assert decision["best_checkpoint"] == "sf-10m-step1200"
    assert decision["prototype_canary"] == "16/16"
    assert decision["prototype_observed_wrong_topic_count"] == 0
    assert decision["known_topic"] == "16/16"
    assert decision["fresh_topic"] == "9/10"
    assert decision["topic_family"] == "9/10"
    assert decision["all_family"] == "30/50"
    assert decision["required_gates"]["all_family"] == "45/50"


def test_phase27_104_training_view_uses_phase27_103_schedule() -> None:
    report = _json(REPORT)
    view = report["training_view"]
    config = report["train_config"]

    assert view["records"] == 192
    assert view["adjacent_same_topic_count"] == 0
    assert view["source_pack"].endswith("dialogue_batch_v12_topic_prototype_contrastive_012.jsonl")
    assert config["curriculum_view"] == "phase27_103_topic_dialect_round_robin_schedule_v1"
    assert config["steps"] == 1200
    assert config["lr"] == 8e-05


def test_phase27_104_samples_capture_regression_reason() -> None:
    text = SAMPLES.read_text(encoding="utf-8")
    assert "Prototype Canary Failures" in text
    assert "All Family Failures" in text
    assert "expected_terms_missing" in text
