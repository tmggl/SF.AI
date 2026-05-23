"""Phase 15 — native generator adapter safety and metadata tests."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from sf_ai.core.index import load_default_registry
from sf_ai.core.nlp import get_default_pipeline
from sf_ai.core.orchestrator import Orchestrator, UserMessage
from sf_ai.modules.chat import (
    ChatModule,
    GenerationPolicy,
    NativeGenerationResult,
    NativeGenerator,
    NativeGeneratorConfig,
)
from sf_ai.modules.chat.native_generator import extract_dialogue_reply


class _FakeGenerator:
    def generate(self, prompt: str, **_: object) -> NativeGenerationResult:
        return NativeGenerationResult(
            used=True,
            text=f"رد مولد تجريبي على: {prompt}",
            generator="sf_10m_v0_2",
            reason="generated",
        )


class _BadGenerator:
    def generate(self, prompt: str, **_: object) -> NativeGenerationResult:
        return NativeGenerationResult(
            used=True,
            text="المعنى: المعنى: corpus Phase tokenizer / / /",
            generator="sf_10m_v0_2",
            reason="generated",
        )


class _MisalignedSocialGenerator:
    def generate(self, prompt: str, **_: object) -> NativeGenerationResult:
        return NativeGenerationResult(
            used=True,
            text="أفهم طلبك. أستطيع ترتيب الفكرة وشرحها بخطوات قصيرة.",
            generator="sf_10m_v0_2",
            reason="generated",
        )


def test_generation_policy_disabled_by_default() -> None:
    decision = GenerationPolicy(enabled=False).decide(
        domain="chat",
        intent="chat.smalltalk",
        confidence=0.95,
        domain_status="active",
        requires_safety=False,
        fallback_used=False,
    )
    assert decision.allowed is False
    assert decision.generator == "template"
    assert decision.reason == "native_generator_disabled"


def test_generation_policy_reads_experimental_runtime_flags(monkeypatch) -> None:
    monkeypatch.setenv("SF_ENABLE_NATIVE_GENERATOR", "true")
    monkeypatch.setenv("SF_NATIVE_GENERATOR_EXPERIMENTAL", "true")
    monkeypatch.setenv("SF_GENERATOR_CANARY", "true")
    policy = GenerationPolicy.from_env()
    assert policy.enabled is True
    assert policy.experimental_runtime is True
    assert policy.canary is True


def test_generation_policy_blocks_sensitive_and_unready_paths() -> None:
    policy = GenerationPolicy(enabled=True)
    blocked = [
        policy.decide(
            domain="medical",
            intent="medical.general",
            confidence=0.95,
            domain_status="skeleton_only",
            requires_safety=True,
            fallback_used=False,
        ),
        policy.decide(
            domain="chat",
            intent="chat.general",
            confidence=0.95,
            domain_status="skeleton_only",
            requires_safety=False,
            fallback_used=False,
        ),
        policy.decide(
            domain="chat",
            intent="chat.general",
            confidence=0.10,
            domain_status="active",
            requires_safety=False,
            fallback_used=False,
        ),
        policy.decide(
            domain="chat",
            intent="chat.identity",
            confidence=0.95,
            domain_status="active",
            requires_safety=False,
            fallback_used=False,
        ),
    ]
    assert all(decision.allowed is False for decision in blocked)


def test_generation_policy_requires_canary_before_freeform_chat() -> None:
    decision = GenerationPolicy(enabled=True, experimental_runtime=True).decide(
        domain="chat",
        intent="chat.general",
        confidence=0.95,
        domain_status="active",
        requires_safety=False,
        fallback_used=False,
    )
    assert decision.allowed is False
    assert decision.reason == "canary_disabled"


def test_generation_policy_allows_canary_high_confidence_freeform_chat() -> None:
    decision = GenerationPolicy(enabled=True, experimental_runtime=True, canary=True).decide(
        domain="chat",
        intent="chat.general",
        confidence=0.95,
        domain_status="active",
        requires_safety=False,
        fallback_used=False,
    )
    assert decision.allowed is True
    assert decision.generator == "sf_10m_v0_2"


def test_generation_policy_keeps_social_intents_on_templates() -> None:
    policy = GenerationPolicy(enabled=True, experimental_runtime=True)

    for intent in (
        "chat.greeting",
        "chat.smalltalk",
        "chat.presence",
        "chat.understanding",
        "chat.language_preference",
    ):
        decision = policy.decide(
            domain="chat",
            intent=intent,
            confidence=0.95,
            domain_status="active",
            requires_safety=False,
            fallback_used=False,
        )
        assert decision.allowed is False
        assert decision.reason == "template_first_social_intent"


def test_native_generator_status_checks_sovereign_artifact_locations() -> None:
    status = NativeGenerator().status()
    assert status.generator == "sf_10m_v0_2"
    assert status.tokenizer_exists is True
    # Checkpoint state is intentionally ignored by git, so CI or a fresh clone
    # may only have metadata. The status surface must report both facts.
    assert isinstance(status.checkpoint_meta_exists, bool)
    assert isinstance(status.checkpoint_state_exists, bool)


def test_native_generator_default_decoding_controls_are_enabled() -> None:
    cfg = NativeGeneratorConfig()
    assert cfg.no_repeat_ngram_size == 3
    assert cfg.repetition_penalty > 1.0


def test_native_generator_returns_missing_checkpoint_without_throwing(tmp_path: Path) -> None:
    gen = NativeGenerator(
        NativeGeneratorConfig(
            checkpoints_root=tmp_path / "missing_checkpoints",
            checkpoint_name="missing",
        )
    )
    out = gen.generate("مرحبا")
    assert out.used is False
    assert out.generator == "sf_10m_v0_2"
    assert out.reason == "missing_checkpoint"


def test_native_generator_formats_dialect_conditioned_prompt() -> None:
    gen = NativeGenerator()
    assert gen._format_prompt("مرحبا", dialect="msa") == "النطاق: فصحى\nالمستخدم: مرحبا\nالمساعد:"
    assert gen._format_prompt("هلا", dialect="saudi") == "النطاق: سعودي\nالمستخدم: هلا\nالمساعد:"
    assert gen._format_prompt("شلونك", dialect="gulf") == "النطاق: سعودي\nالمستخدم: شلونك\nالمساعد:"


def test_extract_dialogue_reply_prefers_assistant_segment() -> None:
    prompt = "المستخدم: كيفك\nالمساعد:"
    decoded = "المستخدم: كيفك\nالمساعد: بخير الحمد لله.\nالمستخدم: ممتاز"
    assert extract_dialogue_reply(decoded, prompt) == "بخير الحمد لله."


def test_extract_dialogue_reply_handles_tokenizer_spacing() -> None:
    prompt = "المستخدم: كيفك\nالمساعد:"
    decoded = " المستخدم: كيفك \n المساعد: تمام، وأنت؟ المستخدم: بخير"
    assert extract_dialogue_reply(decoded, prompt) == "تمام، وأنت؟"


def test_chat_module_exposes_template_generator_metadata() -> None:
    pipe = get_default_pipeline()
    mod = ChatModule(generation_policy=GenerationPolicy(enabled=False))
    analysis = pipe.analyze_user_text("مرحبا")
    out = mod.handle(analysis, intent="chat.greeting", session_id="phase15")
    assert "generator:template" in out.notes
    assert "native_generator:disabled" in out.notes


def test_chat_module_uses_native_generator_in_explicit_experimental_mode() -> None:
    pipe = get_default_pipeline()
    mod = ChatModule(
        generation_policy=GenerationPolicy(enabled=True, experimental_runtime=True, canary=True),
        native_generator=_FakeGenerator(),  # type: ignore[arg-type]
    )
    analysis = pipe.analyze_user_text("اكتب رد قصير")
    out = mod.handle(analysis, intent="chat.general", session_id="phase15-exp")
    assert out.text == "رد مولد تجريبي على: اكتب رد قصير"
    assert "generator:sf_10m_v0_2" in out.notes
    assert "native_generator:canary_passed" in out.notes


def test_chat_module_blocks_bad_canary_output_and_keeps_template() -> None:
    pipe = get_default_pipeline()
    mod = ChatModule(
        generation_policy=GenerationPolicy(enabled=True, experimental_runtime=True, canary=True),
        native_generator=_BadGenerator(),  # type: ignore[arg-type]
    )
    analysis = pipe.analyze_user_text("اكتب رد قصير")
    out = mod.handle(analysis, intent="chat.general", session_id="phase25-bad")
    assert "رد مولد تجريبي" not in out.text
    assert "generator:template" in out.notes


def test_chat_module_blocks_prompt_misaligned_social_generation() -> None:
    pipe = get_default_pipeline()
    mod = ChatModule(
        generation_policy=GenerationPolicy(enabled=True, experimental_runtime=True, canary=True),
        native_generator=_MisalignedSocialGenerator(),  # type: ignore[arg-type]
    )
    analysis = pipe.analyze_user_text("كيفك")
    out = mod.handle(analysis, intent="chat.general", session_id="phase27-guard")
    assert out.text != "أفهم طلبك. أستطيع ترتيب الفكرة وشرحها بخطوات قصيرة."
    assert "generator:template" in out.notes
    assert "generation_guard:social_smalltalk_mismatch" in out.notes
    assert "native_generator:canary_blocked" in out.notes
    assert any(note.startswith("generation_guard:") for note in out.notes)


def test_chat_module_keeps_pinned_identity_on_template_when_experimental() -> None:
    pipe = get_default_pipeline()
    mod = ChatModule(
        generation_policy=GenerationPolicy(enabled=True, experimental_runtime=True, canary=True),
        native_generator=_FakeGenerator(),  # type: ignore[arg-type]
    )
    analysis = pipe.analyze_user_text("من أنت")
    out = mod.handle(analysis, intent="chat.identity", session_id="phase15-pinned")
    assert "SF.AI" in out.text
    assert "generator:template" in out.notes
    assert "native_generator:template_first_social_intent" in out.notes


def test_chat_module_keeps_smalltalk_on_template_when_experimental() -> None:
    pipe = get_default_pipeline()
    mod = ChatModule(
        generation_policy=GenerationPolicy(enabled=True, experimental_runtime=True, canary=True),
        native_generator=_FakeGenerator(),  # type: ignore[arg-type]
    )
    analysis = pipe.analyze_user_text("كيفك")
    out = mod.handle(analysis, intent="chat.smalltalk", session_id="phase15-social")
    assert "كيف حالك" in out.text
    assert "generator:template" in out.notes
    assert "native_generator:template_first_social_intent" in out.notes


def test_chat_api_response_includes_generator_metadata() -> None:
    client = TestClient(app)
    r = client.post(
        "/chat/message",
        json={"message": "مرحبا", "session_id": "phase15-api"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["generator"] == "template"
    assert body["debug"]["generator"] == "template"


def test_lab_generation_can_cover_non_sensitive_skeleton_domains(monkeypatch) -> None:
    monkeypatch.setenv("SF_LAB_GENERATION_FOR_NON_SENSITIVE", "true")
    pipe = get_default_pipeline()
    fake_chat = ChatModule(
        generation_policy=GenerationPolicy(enabled=True, experimental_runtime=True, canary=True),
        native_generator=_FakeGenerator(),  # type: ignore[arg-type]
    )
    orch = Orchestrator(
        registry=load_default_registry(),
        nlp=pipe,
        modules={"chat": fake_chat},
    )

    result = orch.process(UserMessage(text="ابي اسوي كود", session_id="lab-skeleton"))

    assert result.domain == "coding"
    assert result.debug["dispatch"] == "module:chat_lab"
    assert result.debug["generator"] == "sf_10m_v0_2"
    assert "رد مولد تجريبي" in result.response
    assert "lab_domain:coding" in result.debug["module_notes"]


def test_lab_generation_keeps_sensitive_domains_on_composer(monkeypatch) -> None:
    monkeypatch.setenv("SF_LAB_GENERATION_FOR_NON_SENSITIVE", "true")
    fake_chat = ChatModule(
        generation_policy=GenerationPolicy(enabled=True, experimental_runtime=True, canary=True),
        native_generator=_FakeGenerator(),  # type: ignore[arg-type]
    )
    orch = Orchestrator(registry=load_default_registry(), modules={"chat": fake_chat})

    result = orch.process(UserMessage(text="عندي ألم في الراس", session_id="lab-sensitive"))

    assert result.domain == "medical"
    assert result.debug["dispatch"] == "composer"
    assert result.debug["generator"] == "template"
