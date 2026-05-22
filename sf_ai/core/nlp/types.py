"""Dataclasses for the Language Understanding Layer.

`NLPAnalysis` is the contract every downstream component (Router, Composer,
ChatModule) consumes. Once a field exists here it should remain stable; new
information can be added but existing fields should not be removed silently.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Correction:
    """A single typo / fix recommendation."""

    original: str
    corrected: str
    confidence: float
    reason: str  # "typo_pattern" | "fuzzy" | "norm_variant"

    def describe(self) -> str:
        return f"{self.original}→{self.corrected}({self.confidence:.2f}/{self.reason})"


@dataclass(frozen=True)
class DialectSignal:
    """One dialect / arabizi term and its canonical Arabic form."""

    surface: str           # what the user wrote
    canonical: str         # canonical MSA-ish form used downstream
    dialect: str           # "gulf" | "egyptian" | "levantine" | "iraqi" | "arabizi" | "msa"
    confidence: float

    def describe(self) -> str:
        return f"{self.surface}→{self.canonical}({self.dialect},{self.confidence:.2f})"


@dataclass(frozen=True)
class IntentHint:
    """Hint emitted by IntentDetector. The Router decides, not this."""

    intent: str
    domain_hint: str
    confidence: float
    matched_terms: tuple[str, ...]


@dataclass(frozen=True)
class NLPAnalysis:
    """Output of `NLPPipeline.analyze_user_text(text)`."""

    original_text: str
    cleaned_text: str
    normalized_text: str
    corrected_text: str
    canonical_text: str        # after arabizi + dialect → canonical
    language: str              # "ar" | "en" | "mixed" | "code" | "unknown"
    detected_dialect: str      # "msa" | "gulf" | "egyptian" | "levantine" | "iraqi" | "unknown"
    tokens: tuple[str, ...]
    corrections: tuple[Correction, ...] = field(default_factory=tuple)
    aliases: tuple[DialectSignal, ...] = field(default_factory=tuple)
    domain_hints: tuple[str, ...] = field(default_factory=tuple)
    intent_hints: tuple[IntentHint, ...] = field(default_factory=tuple)
    safety_flags: tuple[str, ...] = field(default_factory=tuple)
    confidence: float = 1.0

    @property
    def lenses(self) -> dict[str, str]:
        """All text variants the Router can score against."""
        return {
            "original": self.original_text,
            "cleaned": self.cleaned_text,
            "normalized": self.normalized_text,
            "corrected": self.corrected_text,
            "canonical": self.canonical_text,
        }
