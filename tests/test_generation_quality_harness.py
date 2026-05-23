"""Phase 27.9 — native generation quality canary tests."""

from __future__ import annotations

import json
from pathlib import Path

from sf_ai.evaluation import (
    load_generation_prompts,
    run_generation_quality_eval,
)
from sf_ai.modules.chat import NativeGenerationResult


class _GoodGenerator:
    def generate(self, prompt: str, **_: object) -> NativeGenerationResult:
        if "السلام" in prompt:
            text = "وعليكم السلام، أهلًا بك."
        elif "كيفك" in prompt:
            text = "أنا بخير الحمد لله، وأنت كيف حالك؟"
        elif "شكرا" in prompt:
            text = "العفو، حياك الله، وشاكر لك لطفك."
        elif "سعودي" in prompt:
            text = "أبشر، نتكلم باللهجة السعودية الواضحة."
        else:
            text = "خذ خطوة صغيرة وواضحة، ثم كررها بهدوء."
        return NativeGenerationResult(True, text, "fake_good", "generated")


class _BadGenerator:
    def generate(self, prompt: str, **_: object) -> NativeGenerationResult:
        return NativeGenerationResult(
            True,
            "ابدأ بهالفكرة: اطلب الطروسبب حارين وسبب حاستعجه على بنير.",
            "fake_bad",
            "generated",
        )


def test_generation_quality_suite_is_msa_saudi_only() -> None:
    prompts = load_generation_prompts("eval/prompts/generation_quality_v1.json")
    assert len(prompts) == 10
    assert {prompt.dialect for prompt in prompts} <= {"msa", "saudi"}
    assert any(prompt.required_terms for prompt in prompts)
    assert all("phase" not in prompt.prompt.lower() for prompt in prompts)


def test_generation_quality_passes_good_generator() -> None:
    report = run_generation_quality_eval(
        suite_path="eval/prompts/generation_quality_v1.json",
        generator=_GoodGenerator(),
        checkpoint_name="fake",
        generator_name="fake_good",
    )
    assert report.status == "PASSED_GENERATION_QUALITY_CANARY"
    assert report.runtime_allowed is True
    assert report.passed_prompts == report.total_prompts == 10
    assert report.blockers == ()


def test_generation_quality_blocks_model_artifacts() -> None:
    report = run_generation_quality_eval(
        suite_path="eval/prompts/generation_quality_v1.json",
        generator=_BadGenerator(),
        checkpoint_name="fake",
        generator_name="fake_bad",
    )
    assert report.status == "BLOCKED_GENERATION_QUALITY_CANARY"
    assert report.runtime_allowed is False
    assert report.failed_prompts == 10
    assert report.guard_reason_counts["model_artifact_fragment"] == 10
    assert "model_artifact_fragments" in report.blockers


def test_generation_quality_report_json_shape(tmp_path: Path) -> None:
    report = run_generation_quality_eval(
        suite_path="eval/prompts/generation_quality_v1.json",
        generator=_BadGenerator(),
        checkpoint_name="fake",
        generator_name="fake_bad",
    )
    out = tmp_path / "report.json"
    out.write_text(json.dumps(report.to_json(), ensure_ascii=False), encoding="utf-8")
    loaded = json.loads(out.read_text(encoding="utf-8"))
    assert loaded["language_track"] == ["msa", "saudi"]
    assert loaded["results"][0]["guard_reason"] == "model_artifact_fragment"
