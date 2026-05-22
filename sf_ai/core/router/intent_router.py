"""IntentRouter — chooses an intent within a domain.

Phase 3 upgrade: lens-aware scoring identical in spirit to DomainRouter.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from difflib import SequenceMatcher

from sf_ai.core.config import CONFIDENCE_SOFTENING, FUZZY_MATCH_THRESHOLD
from sf_ai.core.index import DomainManifest, IntentSpec
from sf_ai.core.nlp.types import NLPAnalysis
from sf_ai.core.router.rules import RoutingSignal, SignalKind, make_signal
from sf_ai.core.semantic.lexical_similarity import (
    contains_phrase,
    normalized_simple,
    simple_tokenize,
)


@dataclass(frozen=True)
class IntentResult:
    intent: str
    score: float
    confidence: float
    matched_signals: tuple[RoutingSignal, ...]
    fallback_used: bool

    @property
    def signal_descriptions(self) -> list[str]:
        return [s.describe() for s in self.matched_signals]


@dataclass
class _IntentScore:
    intent: IntentSpec
    score: float = 0.0
    signals: list[RoutingSignal] = field(default_factory=list)
    matched_keys: set[str] = field(default_factory=set)


def _confidence(score: float) -> float:
    if score <= 0.0:
        return 0.0
    return score / (score + CONFIDENCE_SOFTENING)


class IntentRouter:
    def __init__(self, fuzzy_threshold: float = FUZZY_MATCH_THRESHOLD) -> None:
        self.fuzzy_threshold = fuzzy_threshold

    # ----- public entrypoints -----

    def route(self, domain: DomainManifest, text: str) -> IntentResult:
        return self._route_lenses(
            domain,
            original=text,
            normalized=normalized_simple(text),
            corrected=text,
            canonical=normalized_simple(text),
        )

    def route_with_nlp(self, domain: DomainManifest, analysis: NLPAnalysis) -> IntentResult:
        return self._route_lenses(
            domain,
            original=analysis.original_text,
            normalized=analysis.normalized_text,
            corrected=analysis.corrected_text,
            canonical=analysis.canonical_text,
        )

    # ----- core -----

    def _route_lenses(
        self,
        domain: DomainManifest,
        *,
        original: str,
        normalized: str,
        corrected: str,
        canonical: str,
    ) -> IntentResult:
        if not domain.intents:
            return IntentResult(
                intent=f"{domain.name}.general",
                score=0.0,
                confidence=0.0,
                matched_signals=(),
                fallback_used=True,
            )

        norm_orig = normalized_simple(original)
        tokens_orig = set(simple_tokenize(norm_orig))
        tokens_norm = set(simple_tokenize(normalized))
        tokens_corr = set(simple_tokenize(corrected))
        tokens_canon = set(simple_tokenize(canonical))

        scored: list[_IntentScore] = []
        for intent in domain.intents:
            isc = _IntentScore(intent=intent)
            self._score_phrases(
                intent, isc,
                norm_orig=norm_orig,
                normalized=normalized,
                corrected=corrected,
                canonical=canonical,
            )
            self._score_keywords(
                intent, isc,
                tokens_orig=tokens_orig,
                tokens_norm=tokens_norm,
                tokens_corr=tokens_corr,
                tokens_canon=tokens_canon,
            )
            self._score_fuzzy(intent, isc, normalized=normalized)
            scored.append(isc)

        scored.sort(key=lambda s: s.score, reverse=True)
        top = scored[0] if scored else None
        if top is not None and top.score > 0.0:
            return IntentResult(
                intent=top.intent.name,
                score=top.score,
                confidence=_confidence(top.score),
                matched_signals=tuple(top.signals),
                fallback_used=False,
            )

        fb = domain.fallback_intent
        if fb is not None:
            return IntentResult(
                intent=fb.name,
                score=0.0,
                confidence=0.0,
                matched_signals=(),
                fallback_used=True,
            )

        return IntentResult(
            intent=f"{domain.name}.general",
            score=0.0,
            confidence=0.0,
            matched_signals=(),
            fallback_used=True,
        )

    # ----- per-lens scorers -----

    def _score_phrases(
        self,
        intent: IntentSpec,
        isc: _IntentScore,
        *,
        norm_orig: str,
        normalized: str,
        corrected: str,
        canonical: str,
    ) -> None:
        for phrase in intent.phrases:
            key = f"phrase:{phrase}"
            if key in isc.matched_keys:
                continue
            phrase_n = normalized_simple(phrase)
            if not phrase_n:
                continue
            if contains_phrase(norm_orig, phrase):
                isc.signals.append(make_signal(SignalKind.PHRASE, phrase, norm_orig))
                isc.score += 5.0
                isc.matched_keys.add(key)
                continue
            if phrase_n in normalized:
                isc.signals.append(make_signal(SignalKind.NORMALIZED, phrase, normalized))
                isc.score += 2.5
                isc.matched_keys.add(key)
                continue
            if phrase_n in canonical:
                isc.signals.append(make_signal(SignalKind.DIALECT_ALIAS, phrase, canonical))
                isc.score += 2.0
                isc.matched_keys.add(key)
                continue
            if phrase_n in corrected:
                isc.signals.append(make_signal(SignalKind.TYPO_CORRECTED, phrase, corrected))
                isc.score += 1.5
                isc.matched_keys.add(key)

    def _score_keywords(
        self,
        intent: IntentSpec,
        isc: _IntentScore,
        *,
        tokens_orig: set[str],
        tokens_norm: set[str],
        tokens_corr: set[str],
        tokens_canon: set[str],
    ) -> None:
        for keyword in intent.keywords:
            key = f"keyword:{keyword}"
            if key in isc.matched_keys:
                continue
            kw_tokens = simple_tokenize(keyword)
            if len(kw_tokens) != 1:
                continue
            kw = kw_tokens[0]
            if kw in tokens_orig:
                isc.signals.append(make_signal(SignalKind.KEYWORD, keyword, " ".join(tokens_orig)))
                isc.score += 3.0
                isc.matched_keys.add(key)
                continue
            if kw in tokens_norm:
                isc.signals.append(make_signal(SignalKind.NORMALIZED, keyword, " ".join(tokens_norm)))
                isc.score += 2.5
                isc.matched_keys.add(key)
                continue
            if kw in tokens_canon:
                isc.signals.append(make_signal(SignalKind.DIALECT_ALIAS, keyword, " ".join(tokens_canon)))
                isc.score += 2.0
                isc.matched_keys.add(key)
                continue
            if kw in tokens_corr:
                isc.signals.append(make_signal(SignalKind.TYPO_CORRECTED, keyword, " ".join(tokens_corr)))
                isc.score += 1.5
                isc.matched_keys.add(key)

    def _score_fuzzy(
        self, intent: IntentSpec, isc: _IntentScore, *, normalized: str
    ) -> None:
        if isc.signals:
            return
        for phrase in intent.phrases:
            ratio = SequenceMatcher(None, normalized, normalized_simple(phrase)).ratio()
            if ratio >= self.fuzzy_threshold:
                isc.signals.append(make_signal(SignalKind.FUZZY, phrase, normalized))
                isc.score += 1.0
                return
