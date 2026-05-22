"""SemanticExplorer — picks the most plausible match against a candidate list.

Combines three local signals:
1. Phrase containment (exact, on normalized text).
2. Token overlap / Jaccard.
3. Fuzzy similarity (difflib SequenceMatcher).

No pretrained model is involved. The score returned by `best_match` is in
[0.0, 1.0] and reflects only lexical evidence. Phase 3 will inject the NLP
pipeline (typo correction, dialect mapping) before this layer is consulted.
"""

from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher

from sf_ai.core.config import FUZZY_MATCH_THRESHOLD
from sf_ai.core.semantic.hashing_vectorizer import HashingVectorizer, cosine_sparse
from sf_ai.core.semantic.lexical_similarity import (
    contains_phrase,
    jaccard,
    normalized_simple,
    simple_tokenize,
)


@dataclass(frozen=True)
class SignalMatch:
    candidate: str
    score: float
    signal: str  # phrase | token | fuzzy | hashing


class SemanticExplorer:
    """Pure local similarity over a candidate string list."""

    def __init__(
        self,
        fuzzy_threshold: float = FUZZY_MATCH_THRESHOLD,
        hashing: HashingVectorizer | None = None,
    ) -> None:
        self.fuzzy_threshold = fuzzy_threshold
        self.hashing = hashing or HashingVectorizer()

    def score_candidate(self, text: str, candidate: str) -> SignalMatch:
        """Score a single candidate string against `text`. Picks the strongest signal."""
        norm_text = normalized_simple(text)
        norm_cand = normalized_simple(candidate)
        if not norm_cand:
            return SignalMatch(candidate=candidate, score=0.0, signal="none")

        if contains_phrase(norm_text, norm_cand):
            return SignalMatch(candidate=candidate, score=1.0, signal="phrase")

        text_tokens = simple_tokenize(norm_text)
        cand_tokens = simple_tokenize(norm_cand)
        jacc = jaccard(text_tokens, cand_tokens)
        if jacc >= 0.5:
            return SignalMatch(candidate=candidate, score=jacc, signal="token")

        ratio = SequenceMatcher(None, norm_text, norm_cand).ratio()
        if ratio >= self.fuzzy_threshold:
            return SignalMatch(candidate=candidate, score=ratio, signal="fuzzy")

        # Hashing cosine as a soft fallback.
        cos = cosine_sparse(self.hashing.transform(norm_text), self.hashing.transform(norm_cand))
        if cos > 0.0:
            return SignalMatch(candidate=candidate, score=cos, signal="hashing")

        return SignalMatch(candidate=candidate, score=0.0, signal="none")

    def best_match(self, text: str, candidates: list[str]) -> SignalMatch | None:
        """Return the highest-scoring SignalMatch across `candidates`, or None."""
        best: SignalMatch | None = None
        for cand in candidates:
            match = self.score_candidate(text, cand)
            if match.score <= 0.0:
                continue
            if best is None or match.score > best.score:
                best = match
        return best
