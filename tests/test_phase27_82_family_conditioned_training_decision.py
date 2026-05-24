"""Phase 27.82 — family-conditioned training decision coverage."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_report() -> dict:
    return json.loads(
        (
            ROOT
            / "artifacts/reports/phase27_82_family_conditioned_training_decision_report.json"
        ).read_text(encoding="utf-8")
    )


def test_phase27_82_allows_only_bounded_sf10m_training() -> None:
    report = _load_report()

    assert report["phase"] == "Phase 27.82"
    assert report["strategy"] == "Sovereign Practical Acceleration Strategy v2"
    assert report["sovereignty_mode"] == "SF-native only"
    assert report["status"] == "PHASE27_82_ALLOW_PHASE27_83_BOUNDED_TRAINING"
    assert report["training_started"] is False
    assert report["tokenizer_training_started"] is False
    assert report["runtime_changed"] is False

    decision = report["decision"]
    assert decision["decision_id"] == "PHASE27_82_FAMILY_CONDITIONED_TRAINING_DECISION"
    assert decision["engineering_decision"] == "ALLOW_PHASE27_83_BOUNDED_SF10M_REPAIR_TRAINING"
    assert decision["new_training_allowed"] is True
    assert decision["training_allowed_phase"] == "Phase 27.83"
    assert decision["tokenizer_retrain_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_justified_transition"] is False


def test_phase27_82_prerequisites_and_artifacts_are_sovereign() -> None:
    report = _load_report()

    assert report["prerequisites"] == {
        "phase27_80_gates_passed": True,
        "phase27_81_pack_ready": True,
        "corpus_ready": True,
        "tokenizer_ready": True,
        "init_checkpoint_ready": True,
    }
    assert report["corpus"]["training_ready"] == 8443
    assert report["corpus"]["issues"] == 0
    assert report["tokenizer"]["path"] == "artifacts/tokenizers/sf_bpe/v9_phase27_76"
    assert report["tokenizer"]["sf_origin"] is True
    assert report["init_checkpoint"]["name"] == "sf-10m-step6200"
    assert report["init_checkpoint"]["sf_origin"] is True


def test_phase27_82_training_plan_is_family_conditioned_and_no_runtime_release() -> None:
    report = _load_report()
    plan_path = ROOT / report["artifacts"]["training_plan"]
    plan = json.loads(plan_path.read_text(encoding="utf-8"))

    assert plan["phase"] == "Phase 27.83"
    assert plan["objective"] == "assistant_answer_only_with_family_conditioned_records"
    assert plan["curriculum"]["view"] == "explicit_balanced_family_view"
    assert plan["curriculum"]["families"] == {
        "open_social": 500,
        "followup": 500,
        "planning": 500,
        "support": 500,
        "topic": 500,
    }
    assert plan["curriculum"]["dialect_per_family"] == {"msa": 250, "saudi": 250}
    assert plan["release_rules"]["runtime_release_allowed_by_training"] is False
    assert "sample_isolated" in plan["training_command"][2]
    assert "--loss-scope assistant" in plan["training_command"][2]
