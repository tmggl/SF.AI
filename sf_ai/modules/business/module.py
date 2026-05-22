"""Business domain skeleton — no strategic advisory engine yet."""

from __future__ import annotations

from sf_ai.modules._skeleton import SkeletonDomainModule


class BusinessModule(SkeletonDomainModule):
    domain = "business"
    limitations = (
        "does not provide business strategy, forecasting, or operational plans yet",
        "no external market data or AI API",
        "only skeleton metadata is available",
    )
