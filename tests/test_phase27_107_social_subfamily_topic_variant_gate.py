"""Phase 27.107 — social subfamily/topic variant gate."""

from __future__ import annotations

import json
from pathlib import Path

from sf_ai.datasets.chat_dataset import (
    SOCIAL_SUBFAMILY_CONDITION_LABELS,
    canonical_topic_from_text,
    render_dialogue_text,
)
from sf_ai.datasets.schemas import StructuredSample
from sf_ai.models.tokenizer import BPETokenizer
from sf_ai.training.train_tiny_lm import _encode_training_text

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/reports/phase27_107_social_subfamily_topic_variant_gate_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_107_SOCIAL_SUBFAMILY_TOPIC_VARIANT_GATE_DECISION.json"
CANARY = ROOT / "artifacts/reports/phase27_107_social_subfamily_topic_variant_canary.json"
DOC = ROOT / "docs/PHASE27_107_SOCIAL_SUBFAMILY_TOPIC_VARIANT_GATE_REPORT.md"


def _report() -> dict:
    return json.loads(REPORT.read_text(encoding="utf-8"))


def test_phase27_107_gate_allows_data_pack_only() -> None:
    report = _report()
    decision = json.loads(DECISION.read_text(encoding="utf-8"))

    assert report["phase"] == "Phase 27.107"
    assert report["status"] == "PHASE27_107_GATE_PASSED_DATA_PACK_ALLOWED_NO_TRAINING"
    assert report["gate_passed"] is True
    assert report["training_started"] is False
    assert report["decision"] == decision
    assert decision["data_pack_authoring_allowed"] is True
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert "Phase 27.108" in decision["next_phase"]


def test_phase27_107_canary_covers_social_and_topic_variants() -> None:
    canary = json.loads(CANARY.read_text(encoding="utf-8"))
    prompts = {row["id"]: row for row in canary["prompts"]}

    assert len(prompts) == 7
    assert prompts["greeting_saudi_01"]["subfamily"] == "greeting"
    assert prompts["smalltalk_msa_01"]["subfamily"] == "smalltalk"
    assert prompts["open_chat_saudi_01"]["subfamily"] == "open_chat"
    assert prompts["identity_msa_01"]["subfamily"] == "identity"
    assert prompts["capability_saudi_01"]["subfamily"] == "capability"
    assert prompts["topic_variant_friendship_01"]["canonical_topic"] == "الصداقة"
    assert prompts["topic_variant_brotherhood_01"]["canonical_topic"] == "الأخوة"


def test_phase27_107_renderer_and_masking_gate() -> None:
    sample = StructuredSample(
        domain="chat",
        lang="ar",
        messages=[
            {"role": "user", "content": "كيف الحال"},
            {"role": "assistant", "content": "بخير، الحمد لله. وأنت كيفك؟"},
        ],
        provenance={
            "dialect": "saudi",
            "dialogue_family": "open_social",
            "dialogue_subfamily": "smalltalk",
        },
    )

    text = render_dialogue_text(sample)
    assert "عائلة الحوار: سوالف\nنوع السوالف: سؤال حال\n" in text

    tokenizer = BPETokenizer.load(ROOT / "artifacts/tokenizers/sf_bpe/v9_phase27_76")
    _ids, labels = _encode_training_text(
        tokenizer,
        text,
        stream_format="dialogue",
        loss_scope="assistant",
    )
    masked_prefix = (
        len(tokenizer.encode("النطاق: سعودي"))
        + len(tokenizer.encode("عائلة الحوار: سوالف"))
        + len(tokenizer.encode("نوع السوالف: سؤال حال"))
        + len(tokenizer.encode("المستخدم: كيف الحال"))
        + len(tokenizer.encode("المساعد:"))
    )
    assert all(label == -100 for label in labels[:masked_prefix])
    assert any(label != -100 for label in labels[masked_prefix:])


def test_phase27_107_topic_variant_gate() -> None:
    assert canonical_topic_from_text("الصداقه") == "الصداقة"
    assert canonical_topic_from_text("الاخوه") == "الأخوة"

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
    assert "الموضوع المطلوب: الأخوة" in text


def test_phase27_107_docs_and_report_name_next_phase() -> None:
    report = _report()
    doc = DOC.read_text(encoding="utf-8")

    assert report["social_subfamily_labels"] == SOCIAL_SUBFAMILY_CONDITION_LABELS
    assert report["next_data_pack_requirements"]["minimum_gold_records"] == 420
    assert "Phase 27.108" in doc
