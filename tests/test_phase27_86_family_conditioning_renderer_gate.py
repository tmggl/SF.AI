"""Phase 27.86 — family-conditioning renderer gate coverage."""

from __future__ import annotations

import json
from pathlib import Path

from sf_ai.datasets.chat_dataset import (
    FAMILY_CONDITION_LABELS,
    render_dialogue_text,
)
from sf_ai.datasets.schemas import StructuredSample
from sf_ai.models.tokenizer import BPETokenizer
from sf_ai.training.train_tiny_lm import _encode_training_text

ROOT = Path(__file__).resolve().parents[1]


def _report() -> dict:
    return json.loads(
        (
            ROOT
            / "artifacts/reports/phase27_86_family_conditioning_renderer_gate_report.json"
        ).read_text(encoding="utf-8")
    )


def test_phase27_86_gate_passes_and_allows_only_next_training() -> None:
    report = _report()

    assert report["phase"] == "Phase 27.86"
    assert report["status"] == "PHASE27_86_RENDERER_GATE_PASSED_TRAINING_ALLOWED_NEXT_NO_RUNTIME"
    assert report["training_started"] is False
    assert report["runtime_changed"] is False
    assert report["gate_passed"] is True

    decision = report["decision"]
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_87_BOUNDED_FAMILY_CONDITIONED_SF10M_REPAIR_TRAINING"
    )
    assert decision["new_training_allowed"] is True
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["tokenizer_retrain_allowed"] is False
    assert "Phase 27.87" in decision["next_phase"]


def test_phase27_86_provenance_keeps_dialogue_family_fields() -> None:
    sample = StructuredSample(
        domain="chat",
        lang="ar",
        messages=[
            {"role": "user", "content": "كيف أرتب يومي؟"},
            {"role": "assistant", "content": "ابدأ بثلاث مهام واضحة."},
        ],
        provenance={
            "dialect": "saudi",
            "dialogue_family": "planning",
            "prompt_family": "planning",
            "answer_family": "planning",
        },
    )

    assert sample.provenance is not None
    assert sample.provenance.dialogue_family == "planning"
    assert sample.provenance.prompt_family == "planning"
    assert sample.provenance.answer_family == "planning"


def test_phase27_86_render_dialogue_text_emits_arabic_family_line() -> None:
    sample = StructuredSample(
        domain="chat",
        lang="ar",
        messages=[
            {"role": "user", "content": "كيف أرتب يومي؟"},
            {"role": "assistant", "content": "ابدأ بثلاث مهام واضحة."},
        ],
        provenance={"dialect": "saudi", "dialogue_family": "planning"},
    )

    text = render_dialogue_text(sample)
    assert text.startswith("النطاق: سعودي\nعائلة الحوار: تنظيم\n")
    assert "المستخدم: كيف أرتب يومي؟" in text
    assert "المساعد: ابدأ بثلاث مهام واضحة. <eos>" in text


def test_phase27_86_all_family_labels_render_distinctly() -> None:
    assert FAMILY_CONDITION_LABELS == {
        "open_social": "سوالف",
        "followup": "متابعة",
        "planning": "تنظيم",
        "support": "دعم",
        "topic": "موضوع",
    }
    rendered_lines = {
        row["expected_family_line"]
        for row in _report()["render_probes"].values()
    }
    assert rendered_lines == {
        "عائلة الحوار: سوالف",
        "عائلة الحوار: متابعة",
        "عائلة الحوار: تنظيم",
        "عائلة الحوار: دعم",
        "عائلة الحوار: موضوع",
    }


def test_phase27_86_conditioning_lines_are_masked_from_assistant_loss() -> None:
    tokenizer = BPETokenizer.load(ROOT / "artifacts/tokenizers/sf_bpe/v9_phase27_76")
    text = (
        "النطاق: سعودي\n"
        "عائلة الحوار: تنظيم\n"
        "المستخدم: كيف أرتب يومي؟\n"
        "المساعد: ابدأ بثلاث مهام واضحة. <eos>\n"
    )
    _ids, labels = _encode_training_text(
        tokenizer,
        text,
        stream_format="dialogue",
        loss_scope="assistant",
    )

    condition_and_user_token_count = sum(
        len(tokenizer.encode(line))
        for line in [
            "النطاق: سعودي",
            "عائلة الحوار: تنظيم",
            "المستخدم: كيف أرتب يومي؟",
            "المساعد:",
        ]
    )
    assert all(label == -100 for label in labels[:condition_and_user_token_count])
    assert any(label != -100 for label in labels[condition_and_user_token_count:])


def test_phase27_86_streaming_paths_both_emit_family_line() -> None:
    stream = _report()["stream_probe"]
    assert stream["no_split_has_family_line"] is True
    assert stream["split_train_has_family_line"] is True
    assert "عائلة الحوار:" in stream["no_split_preview"]
    assert "عائلة الحوار:" in stream["split_train_preview"]
