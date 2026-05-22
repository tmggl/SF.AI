"""Medical domain skeleton — safety-gated, no diagnosis."""

from __future__ import annotations

from sf_ai.modules._skeleton import SkeletonDomainModule


class MedicalModule(SkeletonDomainModule):
    domain = "medical"
    requires_safety = True
    limitations = (
        "does not diagnose, prescribe, or triage medical issues",
        "must route to safe ResponseComposer messaging while skeleton_only",
        "future activation requires medical safety and source policy",
    )
