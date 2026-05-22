"""Religion domain skeleton — safety-gated, no fatwa."""

from __future__ import annotations

from sf_ai.modules._skeleton import SkeletonDomainModule


class ReligionModule(SkeletonDomainModule):
    domain = "religion"
    requires_safety = True
    limitations = (
        "does not issue fatwas or religious rulings",
        "must route to safe ResponseComposer messaging while skeleton_only",
        "future activation requires trusted-source policy",
    )
