"""sf_ai.core.router — domain & intent routing with explicit signals."""

from sf_ai.core.router.domain_router import DomainRouter, RoutingResult
from sf_ai.core.router.intent_router import IntentResult, IntentRouter
from sf_ai.core.router.rules import RoutingSignal, SignalKind, signal_weight

__all__ = [
    "DomainRouter",
    "IntentResult",
    "IntentRouter",
    "RoutingResult",
    "RoutingSignal",
    "SignalKind",
    "signal_weight",
]
