"""Dataclasses describing a single domain and its intents.

Phase 2 keeps a minimal vocabulary directly inside the registry YAML so the
router can demonstrate end-to-end routing. Phase 3 will move richer lexicons
to `resources/lexicons/*.yaml`, leaving the registry as a thin index.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class IntentSpec:
    """One intent inside a domain."""

    name: str
    description: str = ""
    phrases: tuple[str, ...] = ()
    keywords: tuple[str, ...] = ()
    fallback: bool = False


@dataclass(frozen=True)
class DomainManifest:
    """One domain entry in the global capability registry."""

    name: str
    description: str = ""
    status: str = "skeleton_only"  # active | skeleton_only | disabled | planned
    requires_safety: bool = False
    phrases: tuple[str, ...] = ()
    keywords: tuple[str, ...] = ()
    intents: tuple[IntentSpec, ...] = ()
    allowed_tools: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    notes: str = ""

    def get_intent(self, name: str) -> IntentSpec | None:
        for intent in self.intents:
            if intent.name == name:
                return intent
        return None

    @property
    def fallback_intent(self) -> IntentSpec | None:
        for intent in self.intents:
            if intent.fallback:
                return intent
        return None


@dataclass(frozen=True)
class RegistryFallback:
    domain: str = "chat"
    intent: str = "chat.general"
    response_style: str = "arabic_formal"


@dataclass(frozen=True)
class RegistryMeta:
    version: str = "0.2"
    schema_version: str = "phase2"
    generated_at: str = ""
    fallback: RegistryFallback = field(default_factory=RegistryFallback)
