"""Phase 25 — generated chat canary guardrails."""

from __future__ import annotations

from sf_ai.modules.chat import GenerationGuard, GenerationPolicy


def test_phase25_generation_guard_allows_simple_arabic_reply() -> None:
    verdict = GenerationGuard().inspect(
        "أفهم طلبك. الخطوة التالية هي أن نختبر الرد بهدوء ثم نقيس التكرار."
    )
    assert verdict.allowed is True
    assert verdict.reason == "passed"
    assert verdict.arabic_ratio > 0.80


def test_phase25_generation_guard_blocks_corpus_artifacts() -> None:
    verdict = GenerationGuard().inspect(
        "المعنى: المعنى: corpus Phase tokenizer / / /"
    )
    assert verdict.allowed is False
    assert verdict.reason in {"corpus_artifact", "too_fragmented"}


def test_phase25_generation_guard_blocks_real_v02_style_fragment() -> None:
    verdict = GenerationGuard().inspect(
        "ر؟ لا. قدة. هل هذا مهم؟ لأن النموذج يتعلم يكون كل شيء "
        "وولا تدريب النموذج السلابنوايها بنعلعل."
    )
    assert verdict.allowed is False
    assert verdict.reason in {"broken_prefix", "corpus_artifact", "malformed_token"}


def test_phase25_generation_guard_blocks_repetition() -> None:
    verdict = GenerationGuard().inspect(
        "تمام تمام تمام تمام تمام تمام تمام تمام تمام"
    )
    assert verdict.allowed is False
    assert verdict.reason == "repetition"


def test_phase25_policy_requires_all_three_flags() -> None:
    base = dict(
        domain="chat",
        intent="chat.general",
        confidence=0.95,
        domain_status="active",
        requires_safety=False,
        fallback_used=False,
    )
    assert GenerationPolicy(enabled=True).decide(**base).allowed is False
    assert GenerationPolicy(enabled=True, experimental_runtime=True).decide(
        **base
    ).reason == "canary_disabled"

    allowed = GenerationPolicy(
        enabled=True,
        experimental_runtime=True,
        canary=True,
    ).decide(**base)
    assert allowed.allowed is True
    assert allowed.generator == "sf_10m_v0_2"
