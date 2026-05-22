"""Social domain skeleton — no specialized social coach yet."""

from __future__ import annotations

from sf_ai.modules._skeleton import SkeletonDomainModule


class SocialModule(SkeletonDomainModule):
    domain = "social"
    limitations = (
        "does not provide specialized relationship or mental-health guidance",
        "general conversation remains handled by ChatModule",
        "no long-term user profiling",
    )
