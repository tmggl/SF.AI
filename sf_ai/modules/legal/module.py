"""Legal domain skeleton — safety-gated, no legal advice."""

from __future__ import annotations

from sf_ai.modules._skeleton import SkeletonDomainModule


class LegalModule(SkeletonDomainModule):
    domain = "legal"
    requires_safety = True
    limitations = (
        "does not provide legal opinions, advice, or document interpretation",
        "must route to safe ResponseComposer messaging while skeleton_only",
        "future activation requires source and jurisdiction policy",
    )
