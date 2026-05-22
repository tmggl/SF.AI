"""Data-analysis domain skeleton — no dataframe/file execution yet."""

from __future__ import annotations

from sf_ai.modules._skeleton import SkeletonDomainModule


class DataModule(SkeletonDomainModule):
    domain = "data"
    limitations = (
        "does not load, clean, or analyze datasets yet",
        "no pandas/openpyxl runtime path through chat",
        "no external analytics or AI API",
    )
