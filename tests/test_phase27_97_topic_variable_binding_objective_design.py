"""Phase 27.97 — topic variable-binding objective design coverage."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.phase27_97_topic_variable_binding_objective_design import (
    DEFAULT_REPORT,
    TOPIC_TERMS,
    build_report,
    parse_args,
)

ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "artifacts/reports/PHASE27_97_TOPIC_VARIABLE_BINDING_OBJECTIVE_DESIGN_DECISION.json"
SPEC = ROOT / "artifacts/reports/phase27_97_topic_variable_binding_objective_spec.json"


def test_phase27_97_design_allows_gate_encoding_but_blocks_training() -> None:
    report, spec = build_report(parse_args([]))
    decision = report["decision"]

    assert report["phase"] == "Phase 27.97"
    assert report["status"] == "PHASE27_97_TOPIC_BINDING_OBJECTIVE_DESIGN_READY_NO_TRAINING"
    assert report["training_started"] is False
    assert report["runtime_changed"] is False
    assert report["design_ready"] is True
    assert spec["objective_name"] == "topic_copy_contrastive_binding_objective_v1"

    assert decision["topic_binding_gate_encoding_allowed"] is True
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["tokenizer_retrain_allowed"] is False
    assert "Phase 27.98" in decision["next_phase"]


def test_phase27_97_spec_requires_copy_anchor_and_contrastive_controls() -> None:
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    contract = spec["assistant_target_contract"]

    assert "first 12 visible Arabic characters" in contract["copy_anchor"]
    assert any(
        template.startswith("معنى <topic_term>:")
        for template in contract["prefix_templates"]
    )
    assert spec["canary_design"]["contrastive_wrong_topic_max"] == 0
    assert spec["canary_design"]["copy_anchor_min"] == "26/26"
    assert len(spec["contrastive_controls"]) == len(TOPIC_TERMS)
    assert {row["requested_topic"] for row in spec["contrastive_controls"]} == set(TOPIC_TERMS)


def test_phase27_97_decision_artifact_matches_report() -> None:
    report = json.loads(Path(DEFAULT_REPORT).read_text(encoding="utf-8"))
    decision = json.loads(DECISION.read_text(encoding="utf-8"))

    assert report["decision"] == decision
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_98_TOPIC_BINDING_GATE_ENCODING_NO_TRAINING"
    )
    gates = report["objective_spec"]["phase27_98_required_gates"]
    assert any("explicit topic_term" in gate for gate in gates)
    assert any("per-topic round-robin" in gate for gate in gates)
