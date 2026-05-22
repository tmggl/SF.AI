"""DomainRouter — picks the domain that best explains the user's message.

Phase 3 upgrade: routes via NLPAnalysis "lenses" — original / normalized /
corrected / canonical — and tags each match with the appropriate SignalKind:
    - phrase / keyword         → original (or normalized) lens
    - normalized               → only normalized lens, not original
    - typo_corrected           → only corrected lens, not original/normalized
    - dialect_alias            → only canonical lens (after dialect rewrite)
    - fuzzy                    → fallback similarity on normalized lens

`route()` keeps a raw-text entry point for callers that don't (yet) have an
NLPAnalysis — internally it builds a minimal analysis on the fly.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from difflib import SequenceMatcher

from sf_ai.core.config import CONFIDENCE_SOFTENING, FUZZY_MATCH_THRESHOLD, MIN_DOMAIN_SCORE
from sf_ai.core.index import CapabilityRegistry, DomainManifest
from sf_ai.core.nlp.types import NLPAnalysis
from sf_ai.core.router.rules import RoutingSignal, SignalKind, make_signal
from sf_ai.core.semantic.lexical_similarity import (
    contains_phrase,
    normalized_simple,
    simple_tokenize,
)


@dataclass(frozen=True)
class RoutingResult:
    domain: str
    score: float
    confidence: float
    matched_signals: tuple[RoutingSignal, ...]
    fallback_used: bool
    route_reason: str

    @property
    def signal_descriptions(self) -> list[str]:
        return [s.describe() for s in self.matched_signals]


@dataclass
class _DomainScore:
    domain: DomainManifest
    score: float = 0.0
    signals: list[RoutingSignal] = field(default_factory=list)
    matched_keys: set[str] = field(default_factory=set)


def _confidence(score: float) -> float:
    if score <= 0.0:
        return 0.0
    return score / (score + CONFIDENCE_SOFTENING)


def _status_rank(status: str) -> int:
    return {"active": 3, "skeleton_only": 2, "planned": 1, "disabled": 0}.get(status, 0)


class DomainRouter:
    """Score every domain in the registry against an NLP analysis."""

    def __init__(
        self,
        registry: CapabilityRegistry,
        fuzzy_threshold: float = FUZZY_MATCH_THRESHOLD,
    ) -> None:
        self.registry = registry
        self.fuzzy_threshold = fuzzy_threshold

    # ----- public entrypoints -----

    def route(self, text: str) -> RoutingResult:
        """Raw-text entrypoint. Builds a minimal analysis-like view internally."""
        if not text or not text.strip():
            return self._fallback("empty input")
        return self._route_lenses(
            original=text,
            normalized=normalized_simple(text),
            corrected=text,
            canonical=normalized_simple(text),
        )

    def route_with_nlp(self, analysis: NLPAnalysis) -> RoutingResult:
        if not analysis.original_text.strip():
            return self._fallback("empty input")
        return self._route_lenses(
            original=analysis.original_text,
            normalized=analysis.normalized_text,
            corrected=analysis.corrected_text,
            canonical=analysis.canonical_text,
        )

    # ----- core scoring -----

    def _route_lenses(
        self,
        *,
        original: str,
        normalized: str,
        corrected: str,
        canonical: str,
    ) -> RoutingResult:
        # Pre-tokenize each lens once.
        norm_orig = normalized_simple(original)
        tokens_orig = set(simple_tokenize(norm_orig))
        tokens_norm = set(simple_tokenize(normalized))
        tokens_corr = set(simple_tokenize(corrected))
        tokens_canon = set(simple_tokenize(canonical))

        scored: list[_DomainScore] = []
        for domain in self.registry.all_domains():
            ds = _DomainScore(domain=domain)
            self._score_phrases(
                domain, ds,
                norm_orig=norm_orig,
                normalized=normalized,
                corrected=corrected,
                canonical=canonical,
            )
            self._score_keywords(
                domain, ds,
                tokens_orig=tokens_orig,
                tokens_norm=tokens_norm,
                tokens_corr=tokens_corr,
                tokens_canon=tokens_canon,
            )
            self._score_fuzzy(domain, ds, normalized=normalized)
            scored.append(ds)

        scored.sort(
            key=lambda s: (s.score, _status_rank(s.domain.status)),
            reverse=True,
        )
        top = scored[0] if scored else None
        if top is None or top.score < MIN_DOMAIN_SCORE:
            return self._fallback("no signals matched threshold")

        return RoutingResult(
            domain=top.domain.name,
            score=top.score,
            confidence=_confidence(top.score),
            matched_signals=tuple(top.signals),
            fallback_used=False,
            route_reason=f"top score={top.score:.2f}, signals={len(top.signals)}",
        )

    # ----- per-lens scorers -----

    def _score_phrases(
        self,
        domain: DomainManifest,
        ds: _DomainScore,
        *,
        norm_orig: str,
        normalized: str,
        corrected: str,
        canonical: str,
    ) -> None:
        for phrase in domain.phrases:
            key = f"phrase:{phrase}"
            if key in ds.matched_keys:
                continue
            phrase_n = normalized_simple(phrase)
            if not phrase_n:
                continue

            # Order matters: highest-weight lens first; stop at first hit.
            if contains_phrase(norm_orig, phrase):
                ds.signals.append(make_signal(SignalKind.PHRASE, phrase, norm_orig))
                ds.score += 5.0
                ds.matched_keys.add(key)
                continue
            if phrase_n in normalized:
                ds.signals.append(make_signal(SignalKind.NORMALIZED, phrase, normalized))
                ds.score += 2.5
                ds.matched_keys.add(key)
                continue
            if phrase_n in canonical:
                ds.signals.append(make_signal(SignalKind.DIALECT_ALIAS, phrase, canonical))
                ds.score += 2.0
                ds.matched_keys.add(key)
                continue
            if phrase_n in corrected:
                ds.signals.append(make_signal(SignalKind.TYPO_CORRECTED, phrase, corrected))
                ds.score += 1.5
                ds.matched_keys.add(key)

    def _score_keywords(
        self,
        domain: DomainManifest,
        ds: _DomainScore,
        *,
        tokens_orig: set[str],
        tokens_norm: set[str],
        tokens_corr: set[str],
        tokens_canon: set[str],
    ) -> None:
        for keyword in domain.keywords:
            key = f"keyword:{keyword}"
            if key in ds.matched_keys:
                continue
            kw_tokens = simple_tokenize(keyword)
            if len(kw_tokens) != 1:
                continue
            kw = kw_tokens[0]

            if kw in tokens_orig:
                ds.signals.append(make_signal(SignalKind.KEYWORD, keyword, " ".join(tokens_orig)))
                ds.score += 3.0
                ds.matched_keys.add(key)
                continue
            if kw in tokens_norm:
                ds.signals.append(make_signal(SignalKind.NORMALIZED, keyword, " ".join(tokens_norm)))
                ds.score += 2.5
                ds.matched_keys.add(key)
                continue
            if kw in tokens_canon:
                ds.signals.append(make_signal(SignalKind.DIALECT_ALIAS, keyword, " ".join(tokens_canon)))
                ds.score += 2.0
                ds.matched_keys.add(key)
                continue
            if kw in tokens_corr:
                ds.signals.append(make_signal(SignalKind.TYPO_CORRECTED, keyword, " ".join(tokens_corr)))
                ds.score += 1.5
                ds.matched_keys.add(key)

    def _score_fuzzy(
        self, domain: DomainManifest, ds: _DomainScore, *, normalized: str
    ) -> None:
        if ds.signals:
            return  # already explained — no need for fuzzy
        for phrase in domain.phrases:
            ratio = SequenceMatcher(None, normalized, normalized_simple(phrase)).ratio()
            if ratio >= self.fuzzy_threshold:
                ds.signals.append(make_signal(SignalKind.FUZZY, phrase, normalized))
                ds.score += 1.0
                return

    # ----- fallback -----

    def _fallback(self, reason: str) -> RoutingResult:
        fb = self.registry.fallback
        return RoutingResult(
            domain=fb.domain,
            score=0.0,
            confidence=0.0,
            matched_signals=(),
            fallback_used=True,
            route_reason=f"fallback: {reason}",
        )
