"""Scoring rules for the router.

The weights below are the canonical Phase 3 scoring scale. Phase 2 only emits
`phrase` / `keyword` / `fuzzy` / `hashing` signals; Phase 3 will start emitting
`normalized`, `dialect_alias`, `typo_corrected`. The router is already wired
to handle all of them.

Reference scale (from EXECUTION_PLAN.md):
    phrase        : +5
    keyword       : +3
    normalized    : +2.5
    dialect_alias : +2
    typo_corrected: +1.5
    fuzzy         : +1
    safety_term   : 0 — raises safety flag only, never decides the domain.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SignalKind(str, Enum):
    PHRASE = "phrase"
    KEYWORD = "keyword"
    NORMALIZED = "normalized"
    DIALECT_ALIAS = "dialect_alias"
    TYPO_CORRECTED = "typo_corrected"
    FUZZY = "fuzzy"
    HASHING = "hashing"
    SAFETY_TERM = "safety_term"


_WEIGHTS: dict[SignalKind, float] = {
    SignalKind.PHRASE: 5.0,
    SignalKind.KEYWORD: 3.0,
    SignalKind.NORMALIZED: 2.5,
    SignalKind.DIALECT_ALIAS: 2.0,
    SignalKind.TYPO_CORRECTED: 1.5,
    SignalKind.FUZZY: 1.0,
    SignalKind.HASHING: 0.5,
    SignalKind.SAFETY_TERM: 0.0,
}


def signal_weight(kind: SignalKind) -> float:
    return _WEIGHTS[kind]


@dataclass(frozen=True)
class RoutingSignal:
    """One contributing signal toward a domain/intent score."""

    kind: SignalKind
    matched_value: str   # the phrase/keyword/etc. that matched
    source_text: str     # what we found it in (already normalized)
    score: float

    def describe(self) -> str:
        return f"{self.kind.value}:{self.matched_value}({self.score:+.2f})"


def make_signal(kind: SignalKind, matched_value: str, source_text: str) -> RoutingSignal:
    return RoutingSignal(
        kind=kind,
        matched_value=matched_value,
        source_text=source_text,
        score=signal_weight(kind),
    )
