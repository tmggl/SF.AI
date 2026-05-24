"""Phase 27.93 — topic-objective gate encoding tests."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.phase27_93_topic_objective_gate_encoding import build_report, parse_args
from sf_ai.datasets.chat_dataset import render_dialogue_text
from sf_ai.datasets.schemas import StructuredSample

ROOT = Path(__file__).resolve().parents[1]


def test_topic_family_renderer_emits_requested_topic_line() -> None:
    sample = StructuredSample(
        domain="chat",
        lang="ar",
        messages=[
            {"role": "user", "content": "وش يعني الوفاء؟"},
            {"role": "assistant", "content": "الوفاء ثبات وصدق في العلاقة."},
        ],
        provenance={
            "dialect": "saudi",
            "dialogue_family": "topic",
            "topic_term": "الوفاء",
        },
    )

    text = render_dialogue_text(sample)
    assert text.startswith(
        "النطاق: سعودي\n"
        "عائلة الحوار: موضوع\n"
        "الموضوع المطلوب: الوفاء\n"
    )
    assert "المستخدم: وش يعني الوفاء؟" in text
    assert "المساعد: الوفاء ثبات وصدق في العلاقة." in text


def test_non_topic_family_does_not_emit_requested_topic_line() -> None:
    sample = StructuredSample(
        domain="chat",
        lang="ar",
        messages=[
            {"role": "user", "content": "وش الأخبار؟"},
            {"role": "assistant", "content": "طيبة، وش ودك نسولف عنه؟"},
        ],
        provenance={"dialect": "saudi", "dialogue_family": "open_social"},
    )

    text = render_dialogue_text(sample)
    assert "عائلة الحوار: سوالف" in text
    assert "الموضوع المطلوب:" not in text


def test_phase27_93_gate_passes_dry_run_but_blocks_training_for_data_gap(tmp_path: Path) -> None:
    args = parse_args(
        [
            "--report",
            str(tmp_path / "report.json"),
            "--decision",
            str(tmp_path / "decision.json"),
            "--canary",
            str(tmp_path / "canary.json"),
            "--doc",
            str(tmp_path / "report.md"),
        ]
    )
    report, canary = build_report(args)
    decision = report["decision"]

    assert report["phase"] == "Phase 27.93"
    assert report["dry_run_passed"] is True
    assert report["training_data_ready"] is False
    assert report["status"] == "PHASE27_93_TOPIC_OBJECTIVE_GATE_PASSED_DATA_PACK_REQUIRED_NO_TRAINING"
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_94_TOPIC_OBJECTIVE_DATA_PACK_AUTHORING_NO_TRAINING"
    )
    assert decision["new_training_allowed"] is False
    assert decision["data_pack_authoring_allowed"] is True
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["tokenizer_retrain_allowed"] is False
    assert "الوفاء" in report["corpus_topic_coverage"]["shortfalls"]
    assert canary["coverage"]["prompt_count"] == 16
    assert canary["coverage"]["all_terms_covered"] is True
    assert canary["coverage"]["all_dialects_covered"] is True


def test_phase27_93_artifacts_match_decision_and_canary() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/phase27_93_topic_objective_gate_encoding_report.json")
        .read_text(encoding="utf-8")
    )
    decision = json.loads(
        (ROOT / "artifacts/reports/PHASE27_93_TOPIC_OBJECTIVE_GATE_ENCODING_DECISION.json")
        .read_text(encoding="utf-8")
    )
    canary = json.loads(
        (ROOT / "eval/prompts/phase27_93_topic_objective_canary.json")
        .read_text(encoding="utf-8")
    )

    assert report["decision"] == decision
    assert report["canary_manifest_path"] == "eval/prompts/phase27_93_topic_objective_canary.json"
    assert canary["suite_id"] == "phase27_93_topic_objective_canary"
    assert decision["new_training_allowed"] is False
    assert decision["next_phase"].startswith("Phase 27.94")
