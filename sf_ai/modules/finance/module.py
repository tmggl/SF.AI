"""Finance domain skeleton — safety-gated, no financial advice."""

from __future__ import annotations

from sf_ai.modules._skeleton import SkeletonDomainModule


class FinanceModule(SkeletonDomainModule):
    domain = "finance"
    requires_safety = True
    limitations = (
        "does not provide investment, tax, or personal finance advice",
        "must route to safe ResponseComposer messaging while skeleton_only",
        "future activation requires financial safety policy",
    )
