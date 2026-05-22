"""Type containers for the orchestrator layer."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class UserMessage:
    text: str
    session_id: str | None = None


@dataclass(frozen=True)
class OrchestratorResult:
    domain: str
    intent: str
    confidence: float
    matched_signals: tuple[str, ...]
    route_reason: str
    response: str
    requires_safety: bool = False
    status: str = "active"  # status of the matched domain
    fallback_used: bool = False
    debug: dict[str, str] = field(default_factory=dict)
