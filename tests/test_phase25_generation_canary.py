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


def test_phase27_8_generation_guard_blocks_v06_fragment() -> None:
    verdict = GenerationGuard().inspect(
        "ابدأ بهالفكرة: اطلب الطروسبب حارين وسبب حاستعجه على بنير."
    )
    assert verdict.allowed is False
    assert verdict.reason == "model_artifact_fragment"


def test_phase27_10_generation_guard_blocks_v07_fragment() -> None:
    verdict = GenerationGuard().inspect(
        "ابدأ بهالفكرة: اطلب الوضوح وحياذكر السبب بععجه بوضوح."
    )
    assert verdict.allowed is False
    assert verdict.reason == "model_artifact_fragment"


def test_phase27_13_generation_guard_blocks_v08_fragment() -> None:
    verdict = GenerationGuard().inspect(
        "قل: عادئة عة، أو استخدم إني منزياولت ثم أل ته."
    )
    assert verdict.allowed is False
    assert verdict.reason == "model_artifact_fragment"


def test_phase25_generation_guard_blocks_repetition() -> None:
    verdict = GenerationGuard().inspect(
        "تمام تمام تمام تمام تمام تمام تمام تمام تمام"
    )
    assert verdict.allowed is False
    assert verdict.reason in {"repetition", "repeated_phrase"}


def test_phase25_generation_guard_blocks_repeated_short_phrase() -> None:
    verdict = GenerationGuard().inspect(
        "المعنى واضح المعنى واضح المعنى واضح وأحتاج صياغة أفضل."
    )
    assert verdict.allowed is False
    assert verdict.reason == "repeated_phrase"


def test_phase27_22_generation_guard_allows_valid_tanween_words() -> None:
    verdict = GenerationGuard().inspect(
        "اخرج مبكرًا واترك وقتًا إضافيًا."
    )
    assert verdict.allowed is True
    assert verdict.reason == "passed"


def test_phase25_generation_guard_requires_social_prompt_alignment() -> None:
    verdict = GenerationGuard().inspect_for_prompt(
        "كيفك",
        "أفهم طلبك. الخطوة التالية أن نرتب السؤال ونجيب عليه بوضوح.",
    )
    assert verdict.allowed is False
    assert verdict.reason == "social_smalltalk_mismatch"


def test_phase25_generation_guard_allows_aligned_social_reply() -> None:
    verdict = GenerationGuard().inspect_for_prompt(
        "كيفك",
        "أنا بخير الحمد لله، وأنت كيف حالك؟",
    )
    assert verdict.allowed is True
    assert verdict.reason == "passed"


def test_phase27_42_generation_guard_blocks_misaligned_akhbarak() -> None:
    verdict = GenerationGuard(min_chars=4).inspect_for_prompt(
        "وش اخبارك",
        "ابدأ بشي بسيط ولا تكثرها.",
    )
    assert verdict.allowed is False
    assert verdict.reason == "social_smalltalk_mismatch"


def test_phase27_42_generation_guard_blocks_misaligned_planning() -> None:
    verdict = GenerationGuard(min_chars=4).inspect_for_prompt(
        "نظم وقتي",
        "أهلًا بك.",
    )
    assert verdict.allowed is False
    assert verdict.reason == "planning_mismatch"


def test_phase27_42_generation_guard_allows_aligned_planning() -> None:
    verdict = GenerationGuard(min_chars=4).inspect_for_prompt(
        "كيف ارتب مهامي",
        "اكتب ثلاث مهام وابدأ بالأهم.",
    )
    assert verdict.allowed is True
    assert verdict.reason == "passed"


def test_generation_guard_does_not_treat_bilsaudi_definition_as_language_preference() -> None:
    verdict = GenerationGuard(min_chars=4).inspect_for_prompt(
        "فسر التعاون بالسعودي",
        "التعاون إنك تساعد غيرك وتنجزون سوا.",
    )
    assert verdict.allowed is True
    assert verdict.reason == "passed"


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
    assert allowed.generator == "sf_10m_phase27_33"
