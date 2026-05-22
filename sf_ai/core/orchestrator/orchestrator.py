"""Orchestrator — entry point for end-to-end message processing.

Phase 4 flow:
    UserMessage
       └─► NLPPipeline.analyze_user_text  ─► NLPAnalysis
              └─► DomainRouter.route_with_nlp
                     └─► IntentRouter.route_with_nlp
                            ├─► if domain is active and has a module
                            │     → Module.handle(analysis, intent, session_id)
                            └─► else
                                  → ResponseComposer.compose(...)
       ─► OrchestratorResult

Module registry is keyed by domain name. Phase 4 ships one entry: `chat` →
ChatModule. Later phases register `web`, `research`, etc.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Callable, Protocol

from sf_ai.core.composer import ResponseComposer
from sf_ai.core.index import CapabilityRegistry, load_default_registry
from sf_ai.core.logging import get_logger
from sf_ai.core.nlp import NLPPipeline, get_default_pipeline
from sf_ai.core.nlp.types import NLPAnalysis
from sf_ai.core.orchestrator.types import OrchestratorResult, UserMessage
from sf_ai.core.planner import Planner
from sf_ai.core.router import DomainRouter, IntentRouter
from sf_ai.modules.chat import ChatModule, get_default_chat_module

logger = get_logger("sf_ai.orchestrator")


class _ModuleProtocol(Protocol):
    domain: str

    def handle(
        self,
        analysis: NLPAnalysis,
        *,
        intent: str,
        session_id: str | None,
    ): ...


class Orchestrator:
    def __init__(
        self,
        registry: CapabilityRegistry,
        nlp: NLPPipeline | None = None,
        domain_router: DomainRouter | None = None,
        intent_router: IntentRouter | None = None,
        composer: ResponseComposer | None = None,
        planner: Planner | None = None,
        modules: dict[str, _ModuleProtocol] | None = None,
        chat_module_factory: Callable[[], ChatModule] = get_default_chat_module,
    ) -> None:
        self.registry = registry
        self.nlp = nlp or get_default_pipeline()
        self.domain_router = domain_router or DomainRouter(registry)
        self.intent_router = intent_router or IntentRouter()
        self.composer = composer or ResponseComposer()
        self.planner = planner or Planner()
        if modules is None:
            modules = {"chat": chat_module_factory()}
        self.modules = modules

    # ----- public API -----

    def process(self, message: UserMessage) -> OrchestratorResult:
        text = message.text or ""
        analysis = self.nlp.analyze_user_text(text)

        domain_result = self.domain_router.route_with_nlp(analysis)
        domain = self.registry.get_domain(domain_result.domain)
        if domain is None:
            logger.error("Routed to unknown domain: %s", domain_result.domain)
            return self._fail_safe(reason=f"unknown_domain:{domain_result.domain}")

        intent_result = self.intent_router.route_with_nlp(domain, analysis)

        # Planner stub stays in the loop for future expansion.
        self.planner.plan(goal=text, domain=domain.name, intent=intent_result.intent)

        combined_signals = (
            domain_result.signal_descriptions + intent_result.signal_descriptions
        )
        confidence = max(domain_result.confidence, intent_result.confidence)

        debug = self._build_debug(message, analysis, domain_result, intent_result)

        # Dispatch decision.
        response_text, dispatch_kind, extra_notes = self._produce_response(
            domain_name=domain.name,
            domain_status=domain.status,
            domain_requires_safety=domain.requires_safety,
            intent=intent_result.intent,
            analysis=analysis,
            session_id=message.session_id,
        )
        debug["dispatch"] = dispatch_kind
        if extra_notes:
            debug["module_notes"] = ",".join(extra_notes)
            generator = self._extract_note_value(extra_notes, prefix="generator:")
            if generator:
                debug["generator"] = generator
        debug.setdefault("generator", "template")

        return OrchestratorResult(
            domain=domain.name,
            intent=intent_result.intent,
            confidence=confidence,
            matched_signals=tuple(combined_signals),
            route_reason=domain_result.route_reason,
            response=response_text,
            requires_safety=domain.requires_safety or bool(analysis.safety_flags),
            status=domain.status,
            fallback_used=domain_result.fallback_used or intent_result.fallback_used,
            debug=debug,
        )

    # ----- internals -----

    def _produce_response(
        self,
        *,
        domain_name: str,
        domain_status: str,
        domain_requires_safety: bool,
        intent: str,
        analysis: NLPAnalysis,
        session_id: str | None,
    ) -> tuple[str, str, tuple[str, ...]]:
        """Return (response_text, dispatch_kind, extra_notes)."""
        # Safety-flagged domains and skeleton-only domains still go through
        # the Composer's stock replies — we want one consistent voice for
        # "this isn't ready" and "this is sensitive".
        if domain_requires_safety or domain_status != "active":
            domain = self.registry.get_domain(domain_name)
            # `domain` will not be None here — registry already vetted it.
            reply = self.composer.compose(
                domain,  # type: ignore[arg-type]
                intent,
                intent_fallback=False,
                domain_fallback=False,
            )
            return reply.text, "composer", ()

        module = self.modules.get(domain_name)
        if module is None:
            # Active domain without a registered module — fall back to composer.
            domain = self.registry.get_domain(domain_name)
            reply = self.composer.compose(
                domain,  # type: ignore[arg-type]
                intent,
                intent_fallback=False,
                domain_fallback=False,
            )
            return reply.text, "composer_no_module", ()

        module_result = module.handle(
            analysis,
            intent=intent,
            session_id=session_id,
        )
        return module_result.text, f"module:{module.domain}", module_result.notes

    def _build_debug(
        self,
        message: UserMessage,
        analysis: NLPAnalysis,
        domain_result,
        intent_result,
    ) -> dict[str, str]:
        return {
            "domain_score": f"{domain_result.score:.2f}",
            "intent_score": f"{intent_result.score:.2f}",
            "session_id": message.session_id or "",
            "language": analysis.language,
            "dialect": analysis.detected_dialect,
            "corrections": ";".join(c.describe() for c in analysis.corrections),
            "aliases": ";".join(a.describe() for a in analysis.aliases),
            "safety_flags": ",".join(analysis.safety_flags),
            "intent_hints": ",".join(h.intent for h in analysis.intent_hints),
        }

    def _extract_note_value(self, notes: tuple[str, ...], *, prefix: str) -> str:
        for note in notes:
            if note.startswith(prefix):
                return note[len(prefix):]
        return ""

    def _fail_safe(self, reason: str) -> OrchestratorResult:
        return OrchestratorResult(
            domain="chat",
            intent="chat.general",
            confidence=0.0,
            matched_signals=(),
            route_reason=f"fail_safe:{reason}",
            response="حدث خطأ داخلي أثناء توجيه رسالتك. أعد المحاولة لاحقًا.",
            requires_safety=False,
            status="active",
            fallback_used=True,
            debug={"reason": reason},
        )


@lru_cache(maxsize=1)
def get_default_orchestrator() -> Orchestrator:
    return Orchestrator(registry=load_default_registry())
