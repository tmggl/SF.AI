"""Productivity domain skeleton — no task engine yet."""

from __future__ import annotations

from sf_ai.modules._skeleton import SkeletonDomainModule


class ProductivityModule(SkeletonDomainModule):
    domain = "productivity"
    limitations = (
        "does not create reminders, calendar events, or recurring tasks yet",
        "no hidden automation or external productivity API",
        "future activation must keep user review explicit",
    )
