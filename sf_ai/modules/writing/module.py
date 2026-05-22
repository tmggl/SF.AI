"""Writing domain skeleton — no creative generation yet."""

from __future__ import annotations

from sf_ai.modules._skeleton import SkeletonDomainModule


class WritingModule(SkeletonDomainModule):
    domain = "writing"
    limitations = (
        "does not generate long-form writing or style rewrites yet",
        "no pretrained writing model or external AI API",
        "only skeleton metadata is available",
    )
