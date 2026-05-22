"""Phase 17 — Local Memory/RAG bridge into ChatModule."""

from __future__ import annotations

from fastapi.testclient import TestClient

from apps.api.main import app
from sf_ai.core.index import load_default_registry
from sf_ai.core.nlp import get_default_pipeline
from sf_ai.core.orchestrator import Orchestrator, UserMessage
from sf_ai.memory import Document, HybridRetriever, RetrievalConfig
from sf_ai.modules.chat import (
    ChatModule,
    ChatRagBridge,
    ContextBuilder,
    GenerationPolicy,
    NativeGenerationResult,
    RagBridgeConfig,
)


class _FakeGenerator:
    def generate(self, prompt: str, **_: object) -> NativeGenerationResult:
        return NativeGenerationResult(
            used=True,
            text=f"generated: {prompt}",
            generator="sf_10m_v0_1",
            reason="generated",
        )


def _retriever_with_local_memory() -> HybridRetriever:
    retriever = HybridRetriever(config=RetrievalConfig(top_k=3))
    retriever.add_document(
        Document(
            doc_id="sfai-local-policy",
            title="سياسة SF.AI المحلية",
            source_url="local://sfai/policy",
            language="ar",
            text=(
                "SF.AI يركز حاليًا على العربية الفصحى واللهجة السعودية فقط. "
                "مختبر سامي المحلي يستطيع اختبار التوليد الخام، والمسار اليومي يعتمد على التقييم."
            ),
            metadata={"scope": "local_test"},
        )
    )
    return retriever


def test_context_builder_formats_local_memory_with_source() -> None:
    retriever = _retriever_with_local_memory()
    hits = retriever.search("ما لغة SF.AI الحالية؟", top_k=2)
    built = ContextBuilder().build(hits)
    assert built.used is True
    assert "من الذاكرة المحلية" in built.text
    assert "المصدر:" in built.text
    assert "سياسة SF.AI المحلية" in built.text


def test_rag_bridge_uses_local_retriever_for_general_chat() -> None:
    bridge = ChatRagBridge(
        _retriever_with_local_memory(),
        config=RagBridgeConfig(top_k=2, min_score=0.0),
    )
    context = bridge.maybe_build_context(
        "ما اللغة الحالية في SF.AI؟",
        intent="chat.general",
    )
    assert context.used is True
    assert "العربية الفصحى" in context.text
    assert "اللهجة السعودية" in context.text
    assert "rag:used" in context.notes


def test_rag_bridge_skips_pinned_identity_intent() -> None:
    bridge = ChatRagBridge(
        _retriever_with_local_memory(),
        config=RagBridgeConfig(top_k=2, min_score=0.0),
    )
    context = bridge.maybe_build_context("من أنت؟", intent="chat.identity")
    assert context.used is False
    assert "rag:pinned_intent" in context.notes


def test_chat_module_distinguishes_local_memory_response() -> None:
    pipe = get_default_pipeline()
    bridge = ChatRagBridge(
        _retriever_with_local_memory(),
        config=RagBridgeConfig(top_k=2, min_score=0.0),
    )
    mod = ChatModule(rag_bridge=bridge)
    analysis = pipe.analyze_user_text("ما اللغة الحالية في SF.AI؟")
    out = mod.handle(analysis, intent="chat.general", session_id="rag-1")
    assert "من الذاكرة المحلية" in out.text
    assert "المصدر:" in out.text
    assert "rag:used" in out.notes
    assert "generator:template" in out.notes


def test_chat_module_prefers_local_memory_over_experimental_generation() -> None:
    pipe = get_default_pipeline()
    bridge = ChatRagBridge(
        _retriever_with_local_memory(),
        config=RagBridgeConfig(top_k=2, min_score=0.0),
    )
    mod = ChatModule(
        rag_bridge=bridge,
        generation_policy=GenerationPolicy(enabled=True, experimental_runtime=True),
        native_generator=_FakeGenerator(),  # type: ignore[arg-type]
    )
    analysis = pipe.analyze_user_text("ما اللغة الحالية في SF.AI؟")
    out = mod.handle(analysis, intent="chat.general", session_id="rag-gen-1")
    assert "من الذاكرة المحلية" in out.text
    assert "generated:" not in out.text
    assert "rag:used" in out.notes
    assert "native_generator:skipped_rag_used" in out.notes


def test_orchestrator_surfaces_rag_debug_metadata() -> None:
    bridge = ChatRagBridge(
        _retriever_with_local_memory(),
        config=RagBridgeConfig(top_k=2, min_score=0.0),
    )
    orch = Orchestrator(
        registry=load_default_registry(),
        modules={"chat": ChatModule(rag_bridge=bridge)},
    )
    result = orch.process(UserMessage(text="ما اللغة الحالية في SF.AI؟", session_id="rag-2"))
    assert result.domain == "chat"
    assert result.debug["rag"] == "used"
    assert "سياسة SF.AI المحلية" in result.debug["rag_sources"]
    assert "من الذاكرة المحلية" in result.response


def test_default_api_reports_rag_not_used() -> None:
    client = TestClient(app)
    r = client.post("/chat/message", json={"message": "مرحبا", "session_id": "rag-api"})
    assert r.status_code == 200
    body = r.json()
    assert body["rag"] == "not_used"
    assert body["debug"]["rag"] == "not_used"
