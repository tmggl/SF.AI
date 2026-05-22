"""Coding domain skeleton — no code generation or execution yet."""

from __future__ import annotations

from sf_ai.modules._skeleton import SkeletonDomainModule


class CodingModule(SkeletonDomainModule):
    domain = "coding"
    limitations = (
        "does not write, execute, debug, or modify code yet",
        "no runtime access to files, package managers, or shells through chat",
        "no pretrained coding model or external AI API",
    )
