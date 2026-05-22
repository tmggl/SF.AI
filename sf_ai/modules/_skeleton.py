"""Shared base for Phase 10 skeleton-only domain modules.

These modules are declarative placeholders. They must not perform domain work,
call tools, crawl, train, or produce specialist advice. The Orchestrator should
continue to route skeleton domains to ResponseComposer until a future phase
explicitly promotes a domain.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SkeletonRequest:
    text: str = ""
    intent: str = ""


@dataclass(frozen=True)
class SkeletonResponse:
    domain: str
    status: str
    requires_safety: bool
    text: str
    allowed_tools: tuple[str, ...] = field(default_factory=tuple)
    limitations: tuple[str, ...] = field(default_factory=tuple)


class SkeletonDomainModule:
    """Non-executing module contract for domains planned after chat."""

    domain = "unknown"
    status = "skeleton_only"
    requires_safety = False
    allowed_tools: tuple[str, ...] = ()
    limitations: tuple[str, ...] = (
        "skeleton_only: no runtime domain execution",
        "no external AI APIs or pretrained models",
    )

    def handle(self, request: SkeletonRequest | None = None) -> SkeletonResponse:
        _ = request
        return SkeletonResponse(
            domain=self.domain,
            status=self.status,
            requires_safety=self.requires_safety,
            allowed_tools=self.allowed_tools,
            limitations=self.limitations,
            text=(
                f"{self.domain} is registered as skeleton_only. "
                "It is not active in the Orchestrator yet."
            ),
        )
