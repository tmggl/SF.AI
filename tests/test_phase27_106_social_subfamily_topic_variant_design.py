"""Phase 27.106 — social subfamily and topic variant objective design."""

from __future__ import annotations

import json
from pathlib import Path

from sf_ai.datasets.chat_dataset import (
    SOCIAL_SUBFAMILY_CONDITION_LABELS,
    TOPIC_VARIANT_CANONICALS,
    canonical_topic_from_text,
    render_dialogue_text,
)
from sf_ai.datasets.schemas import StructuredSample

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/reports/phase27_106_social_subfamily_topic_variant_design_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_106_SOCIAL_SUBFAMILY_TOPIC_VARIANT_DESIGN_DECISION.json"
DOC = ROOT / "docs/PHASE27_106_SOCIAL_SUBFAMILY_TOPIC_VARIANT_DESIGN_REPORT.md"


def _report() -> dict:
    return json.loads(REPORT.read_text(encoding="utf-8"))


def test_phase27_106_design_blocks_training_but_allows_gate_encoding() -> None:
    report = _report()
    decision = json.loads(DECISION.read_text(encoding="utf-8"))

    assert report["phase"] == "Phase 27.106"
    assert report["status"] == "PHASE27_106_DESIGN_READY_GATE_ENCODING_NO_TRAINING"
    assert report["training_started"] is False
    assert report["official_runtime_release_allowed"] is False
    assert report["decision"] == decision
    assert decision["new_training_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["pretrained_allowed"] is False
    assert "Phase 27.107" in decision["next_phase"]


def test_social_subfamily_labels_are_explicit_and_rendered() -> None:
    assert SOCIAL_SUBFAMILY_CONDITION_LABELS == {
        "greeting": "تحية",
        "smalltalk": "سؤال حال",
        "open_chat": "فتح سالفة",
        "thanks": "شكر",
        "identity": "هوية",
        "capability": "قدرات",
    }

    sample = StructuredSample(
        domain="chat",
        lang="ar",
        messages=[
            {"role": "user", "content": "السلام عليكم"},
            {"role": "assistant", "content": "وعليكم السلام، حيّاك الله."},
        ],
        provenance={
            "dialect": "saudi",
            "dialogue_family": "open_social",
            "dialogue_subfamily": "greeting",
        },
    )

    text = render_dialogue_text(sample)
    assert text.startswith(
        "النطاق: سعودي\n"
        "عائلة الحوار: سوالف\n"
        "نوع السوالف: تحية\n"
    )
    assert "المساعد: وعليكم السلام، حيّاك الله. <eos>" in text


def test_topic_variants_map_to_canonical_requested_topic() -> None:
    assert TOPIC_VARIANT_CANONICALS["الصداقه"] == "الصداقة"
    assert TOPIC_VARIANT_CANONICALS["الاخوه"] == "الأخوة"
    assert canonical_topic_from_text("الصداقه") == "الصداقة"
    assert canonical_topic_from_text("حدثني عن الاخوه") == "الأخوة"

    sample = StructuredSample(
        domain="chat",
        lang="ar",
        messages=[
            {"role": "user", "content": "الاخوه"},
            {"role": "assistant", "content": "الأخوة قرب ومساندة واحترام."},
        ],
        provenance={"dialect": "msa", "dialogue_family": "topic"},
    )

    text = render_dialogue_text(sample)
    assert text.startswith(
        "النطاق: فصحى\n"
        "عائلة الحوار: موضوع\n"
        "الموضوع المطلوب: الأخوة\n"
    )


def test_phase27_106_report_names_success_metrics_and_blocked_actions() -> None:
    report = _report()
    doc = DOC.read_text(encoding="utf-8")

    assert "greeting" in report["social_subfamilies"]
    assert "الأخوة" in report["topic_variant_policy"]["canonical_topics"]
    assert "renderer emits social subfamily line" in report["canary_design"]["required_before_training"]
    assert "No SF-50M transition." in report["blocked_actions"]
    assert "نوع السوالف" in doc
    assert "Phase 27.107" in doc
