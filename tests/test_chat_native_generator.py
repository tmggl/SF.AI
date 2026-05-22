"""Phase 15 — native generator adapter safety and metadata tests."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from sf_ai.core.nlp import get_default_pipeline
from sf_ai.modules.chat import (
    ChatModule,
    GenerationPolicy,
    NativeGenerationResult,
    NativeGenerator,
    NativeGeneratorConfig,
)


class _FakeGenerator:
    def generate(self, prompt: str, **_: object) -> NativeGenerationResult:
        return NativeGenerationResult(
            used=True,
            text=f"رد مولد تجريبي على: {prompt}",
            generator="sf_10m_v0_1",
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
    policy = GenerationPolicy.from_env()
    assert policy.enabled is True
    assert policy.experimental_runtime is True


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


def test_generation_policy_allows_high_confidence_safe_chat() -> None:
    decision = GenerationPolicy(enabled=True).decide(
        domain="chat",
        intent="chat.smalltalk",
        confidence=0.95,
        domain_status="active",
        requires_safety=False,
        fallback_used=False,
    )
    assert decision.allowed is True
    assert decision.generator == "sf_10m_v0_1"


def test_native_generator_status_checks_sovereign_artifact_locations() -> None:
    status = NativeGenerator().status()
    assert status.generator == "sf_10m_v0_1"
    assert status.tokenizer_exists is True
    # Checkpoint state is intentionally ignored by git, so CI or a fresh clone
    # may only have metadata. The status surface must report both facts.
    assert isinstance(status.checkpoint_meta_exists, bool)
    assert isinstance(status.checkpoint_state_exists, bool)


def test_native_generator_returns_missing_checkpoint_without_throwing(tmp_path: Path) -> None:
    gen = NativeGenerator(
        NativeGeneratorConfig(
            checkpoints_root=tmp_path / "missing_checkpoints",
            checkpoint_name="missing",
        )
    )
    out = gen.generate("مرحبا")
    assert out.used is False
    assert out.generator == "sf_10m_v0_1"
    assert out.reason == "missing_checkpoint"


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
        generation_policy=GenerationPolicy(enabled=True, experimental_runtime=True),
        native_generator=_FakeGenerator(),  # type: ignore[arg-type]
    )
    analysis = pipe.analyze_user_text("اكتب رد قصير")
    out = mod.handle(analysis, intent="chat.general", session_id="phase15-exp")
    assert out.text == "رد مولد تجريبي على: اكتب رد قصير"
    assert "generator:sf_10m_v0_1" in out.notes
    assert "native_generator:experimental_runtime" in out.notes


def test_chat_module_keeps_pinned_identity_on_template_when_experimental() -> None:
    pipe = get_default_pipeline()
    mod = ChatModule(
        generation_policy=GenerationPolicy(enabled=True, experimental_runtime=True),
        native_generator=_FakeGenerator(),  # type: ignore[arg-type]
    )
    analysis = pipe.analyze_user_text("من أنت")
    out = mod.handle(analysis, intent="chat.identity", session_id="phase15-pinned")
    assert "SF.AI" in out.text
    assert "generator:template" in out.notes
    assert "native_generator:pinned_identity_capability_intent" in out.notes


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
