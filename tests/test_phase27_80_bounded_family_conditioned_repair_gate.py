"""Phase 27.80 — executable gates before bounded family-conditioned training."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/reports/phase27_80_bounded_family_conditioned_repair_gate_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_80_BOUNDED_FAMILY_CONDITIONED_REPAIR_GATE_DECISION.json"
DOC = ROOT / "docs/PHASE27_80_BOUNDED_FAMILY_CONDITIONED_REPAIR_GATE_REPORT.md"


def _report() -> dict:
    return json.loads(REPORT.read_text(encoding="utf-8"))


def test_phase27_80_gate_passes_without_starting_training() -> None:
    report = _report()
    decision = report["decision"]
    assert report["phase"] == "Phase 27.80"
    assert report["training_started"] is False
    assert report["runtime_changed"] is False
    assert decision["decision_id"] == "PHASE27_80_BOUNDED_FAMILY_CONDITIONED_REPAIR_GATE_DECISION"
    assert decision["all_gates_passed"] is True
    assert decision["bounded_training_allowed_next"] is True
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_allowed"] is False
    assert decision["tokenizer_retrain_allowed"] is False


def test_phase27_80_renderer_gate_uses_visible_eos_and_masks_context() -> None:
    gates = {gate["gate"]: gate for gate in _report()["gates"]}
    renderer = gates["objective_renderer_assistant_loss_mask"]
    assert renderer["passed"] is True
    assert "النطاق: سعودي" in renderer["rendered_preview"]
    assert "عائلة الحوار: تنظيم" in renderer["rendered_preview"]
    assert "المساعد: اكتب ثلاث مهام، وابدأ بالأهم لمدة قصيرة. <eos>" in renderer["rendered_preview"]
    assert renderer["context_masked"] is True
    assert renderer["assistant_supervised"] is True
    assert renderer["non_masked_label_count"] > 0


def test_phase27_80_round_robin_window_balances_all_families() -> None:
    gates = {gate["gate"]: gate for gate in _report()["gates"]}
    sampler = gates["stratified_round_robin_window_balance"]
    assert sampler["passed"] is True
    assert sampler["window_size"] == 500
    assert sampler["missing_families"] == []
    assert set(sampler["family_counts"]) == {
        "open_social",
        "followup",
        "planning",
        "support",
        "topic",
    }
    assert all(0.16 <= share <= 0.24 for share in sampler["family_shares"].values())


def test_phase27_80_policy_selector_logging_and_amp_gates() -> None:
    gates = {gate["gate"]: gate for gate in _report()["gates"]}
    policy = gates["decoding_eval_selector_logging_artifacts"]
    canaries = gates["heldout_contrastive_canary_inventory"]
    amp = gates["mps_amp_smoke"]
    assert policy["passed"] is True
    assert policy["decoding_policy"].endswith("decoding_policy_v2.json")
    assert policy["checkpoint_selector"].endswith("checkpoint_selector_v2.json")
    assert policy["metrics_template"].endswith("metrics_template.csv")
    assert canaries["passed"] is True
    assert amp["passed"] is True
    assert amp["amp_enabled_for_training"] is False


def test_phase27_80_doc_and_decision_match_report() -> None:
    report = _report()
    decision = json.loads(DECISION.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")
    assert decision == report["decision"]
    assert "GATES_PASSED_BOUNDED_TRAINING_CAN_BE_SCHEDULED" in doc
    assert "runtime release" in doc
