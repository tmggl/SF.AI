"""Generation policy for the local sovereign generator.

The default runtime stays explicit: generation is enabled by flags and safety
domains keep their gates. Sami's lab mode can route non-sensitive skeleton
prompts through ChatModule so the raw generator can be stress-tested without
pretending the model is mature.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


def _env_true(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class GenerationDecision:
    allowed: bool
    reason: str
    generator: str = "template"


@dataclass(frozen=True)
class GenerationPolicy:
    enabled: bool = False
    experimental_runtime: bool = False
    min_confidence: float = 0.80
    max_new_tokens: int = 48
    temperature: float = 0.20
    top_k: int = 0

    @classmethod
    def from_env(cls) -> "GenerationPolicy":
        return cls(
            enabled=_env_true("SF_ENABLE_NATIVE_GENERATOR"),
            experimental_runtime=_env_true("SF_NATIVE_GENERATOR_EXPERIMENTAL"),
        )

    def decide(
        self,
        *,
        domain: str,
        intent: str,
        confidence: float,
        domain_status: str,
        requires_safety: bool,
        fallback_used: bool,
    ) -> GenerationDecision:
        if not self.enabled:
            return GenerationDecision(False, "native_generator_disabled")
        if domain != "chat":
            return GenerationDecision(False, "domain_not_chat")
        if domain_status != "active":
            return GenerationDecision(False, "domain_not_active")
        if requires_safety:
            return GenerationDecision(False, "safety_blocked")
        if fallback_used:
            return GenerationDecision(False, "fallback_route")
        if confidence < self.min_confidence:
            return GenerationDecision(False, "low_confidence")
        if intent in {"chat.identity", "chat.who_made_you", "chat.capability"}:
            return GenerationDecision(False, "pinned_identity_capability_intent")
        return GenerationDecision(True, "allowed", generator="sf_10m_v0_1")
