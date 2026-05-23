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


_TEMPLATE_FIRST_INTENTS: frozenset[str] = frozenset(
    {
        "chat.greeting",
        "chat.smalltalk",
        "chat.presence",
        "chat.understanding",
        "chat.identity",
        "chat.who_made_you",
        "chat.capability",
        "chat.language_preference",
        "chat.clarification",
        "chat.dialogue_test",
        "chat.next_step",
        "chat.training_activation_difference",
        "chat.help",
        "chat.confused",
        "chat.thanks",
        "chat.affirmation",
        "chat.negation",
        "chat.farewell",
    }
)


@dataclass(frozen=True)
class GenerationDecision:
    allowed: bool
    reason: str
    generator: str = "template"


@dataclass(frozen=True)
class GenerationPolicy:
    enabled: bool = False
    experimental_runtime: bool = False
    canary: bool = False
    guarded_runtime_trial: bool = False
    min_confidence: float = 0.80
    max_new_tokens: int = 24
    temperature: float = 1.0
    top_k: int = 0
    candidate_generator: str = "sf_10m_phase27_33"

    @classmethod
    def from_env(cls) -> GenerationPolicy:
        return cls(
            enabled=_env_true("SF_ENABLE_NATIVE_GENERATOR"),
            experimental_runtime=_env_true("SF_NATIVE_GENERATOR_EXPERIMENTAL"),
            canary=_env_true("SF_GENERATOR_CANARY"),
            guarded_runtime_trial=_env_true("SF_GUARDED_RUNTIME_TRIAL"),
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
        if intent in _TEMPLATE_FIRST_INTENTS and not (
            self.guarded_runtime_trial and intent in _GUARDED_TRIAL_SOCIAL_INTENTS
        ):
            return GenerationDecision(False, "template_first_social_intent")
        if not self.canary:
            return GenerationDecision(False, "canary_disabled")
        if intent in _TEMPLATE_FIRST_INTENTS and not self.guarded_runtime_trial:
            return GenerationDecision(False, "guarded_runtime_trial_disabled")
        return GenerationDecision(True, "allowed", generator=self.candidate_generator)


_GUARDED_TRIAL_SOCIAL_INTENTS: frozenset[str] = frozenset(
    {
        "chat.greeting",
        "chat.smalltalk",
        "chat.thanks",
    }
)
