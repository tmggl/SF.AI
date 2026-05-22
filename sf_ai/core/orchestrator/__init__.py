"""sf_ai.core.orchestrator — wires NLP / Router / Modules / Composer together.

Phase 2 builds the end-to-end path with Router and Composer only. Phase 3
will insert the NLP pipeline before the Router; Phase 4 will dispatch active
domains to their Module instead of relying on the Composer's stock replies.
"""

from sf_ai.core.orchestrator.orchestrator import Orchestrator, get_default_orchestrator
from sf_ai.core.orchestrator.types import OrchestratorResult, UserMessage

__all__ = [
    "Orchestrator",
    "OrchestratorResult",
    "UserMessage",
    "get_default_orchestrator",
]
