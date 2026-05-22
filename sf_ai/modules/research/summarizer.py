"""RuleBasedSummarizer — extractive summarization without any LLM.

Algorithm (per article):
1. Segment into sentences (Arabic + English aware).
2. Build a token-frequency map across all sentences (after lowercasing
   ASCII and dropping stopwords).
3. Score each sentence as the sum of its tokens' frequencies, normalized
   by sentence length to avoid biasing toward long sentences.
4. Select top-K by score, then **re-order by original position** for
   readability.
5. Deduplicate sentences whose Jaccard similarity exceeds `dedup_threshold`.

Multi-article summarization: run per-article, then merge top sentences
from each, attributing every kept sentence back to its source URL.

Why this approach?
- 100% local, 100% rule-based.
- Deterministic; same input → same output.
- Auditable: the score for any sentence can be inspected.
- Compatible with citations: every output sentence has a `source_url`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from difflib import SequenceMatcher

from sf_ai.core.nlp._lexicons import load_lexicon
from sf_ai.core.semantic.lexical_similarity import (
    jaccard,
    normalized_simple,
    simple_tokenize,
)


# Sentence-end markers in Arabic + English; keep newlines as boundaries too.
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[\.!\?؟…])\s+|\n+")


@dataclass(frozen=True)
class ScoredSentence:
    text: str
    score: float
    source_url: str
    index_in_article: int


@dataclass(frozen=True)
class Summary:
    sentences: tuple[ScoredSentence, ...]
    per_source_counts: dict[str, int] = field(default_factory=dict)
    total_input_sentences: int = 0
    dedup_dropped: int = 0

    @property
    def text(self) -> str:
        return "\n".join(s.text for s in self.sentences)


def split_sentences(text: str) -> list[str]:
    """Crude but stable sentence segmentation for AR/EN."""
    if not text or not text.strip():
        return []
    parts = _SENTENCE_SPLIT_RE.split(text)
    out: list[str] = []
    for p in parts:
        s = p.strip()
        if not s:
            continue
        # Drop trivial "sentences" (single tokens) — they're usually headings.
        if len(s.split()) < 2:
            continue
        out.append(s)
    return out


class RuleBasedSummarizer:
    def __init__(
        self,
        *,
        max_sentences: int = 5,
        min_sentence_words: int = 4,
        dedup_threshold: float = 0.75,
        stopword_lang: tuple[str, ...] = ("ar", "en"),
    ) -> None:
        if max_sentences < 1:
            raise ValueError("max_sentences must be >= 1")
        if not (0.0 < dedup_threshold <= 1.0):
            raise ValueError("dedup_threshold must be in (0, 1]")
        self.max_sentences = max_sentences
        self.min_sentence_words = min_sentence_words
        self.dedup_threshold = dedup_threshold

        data = load_lexicon("stopwords_ar_en.yaml") or {}
        stops: set[str] = set()
        for lang in stopword_lang:
            stops.update(data.get(lang) or ())
        self._stopwords = frozenset(stops)

    # ----- scoring -----

    def _token_freq(self, sentences: list[str]) -> dict[str, int]:
        freq: dict[str, int] = {}
        for s in sentences:
            for tok in simple_tokenize(s):
                if tok in self._stopwords:
                    continue
                freq[tok] = freq.get(tok, 0) + 1
        return freq

    def _score(self, sentence: str, freq: dict[str, int]) -> float:
        tokens = [t for t in simple_tokenize(sentence) if t not in self._stopwords]
        if not tokens:
            return 0.0
        total = sum(freq.get(t, 0) for t in tokens)
        return total / len(tokens)

    # ----- core ops -----

    def summarize(self, text: str, *, source_url: str = "") -> Summary:
        """Summarize a single article."""
        sents = split_sentences(text)
        if not sents:
            return Summary(sentences=(), total_input_sentences=0)

        freq = self._token_freq(sents)
        scored = [
            ScoredSentence(
                text=s,
                score=self._score(s, freq),
                source_url=source_url,
                index_in_article=i,
            )
            for i, s in enumerate(sents)
            if len(s.split()) >= self.min_sentence_words
        ]
        # Pick top-K by score.
        scored.sort(key=lambda s: s.score, reverse=True)
        kept: list[ScoredSentence] = []
        dropped = 0
        for cand in scored:
            if len(kept) >= self.max_sentences:
                break
            if self._is_duplicate(cand, kept):
                dropped += 1
                continue
            kept.append(cand)
        # Restore original reading order.
        kept.sort(key=lambda s: s.index_in_article)
        return Summary(
            sentences=tuple(kept),
            per_source_counts={source_url: len(kept)} if source_url else {},
            total_input_sentences=len(sents),
            dedup_dropped=dropped,
        )

    def summarize_many(self, items: list[tuple[str, str]]) -> Summary:
        """Multi-article summary. `items` = [(text, source_url), ...].

        Strategy: run per-article, then merge by re-ranking sentences across
        all articles, applying dedup, and trimming to `max_sentences`.
        """
        if not items:
            return Summary(sentences=())

        all_sentences: list[ScoredSentence] = []
        total_input = 0
        for text, url in items:
            per = self.summarize(text, source_url=url)
            all_sentences.extend(per.sentences)
            total_input += per.total_input_sentences

        all_sentences.sort(key=lambda s: s.score, reverse=True)
        kept: list[ScoredSentence] = []
        dropped = 0
        for cand in all_sentences:
            if len(kept) >= self.max_sentences:
                break
            if self._is_duplicate(cand, kept):
                dropped += 1
                continue
            kept.append(cand)

        per_source: dict[str, int] = {}
        for s in kept:
            per_source[s.source_url] = per_source.get(s.source_url, 0) + 1

        # Keep insertion order by original article index when possible —
        # but cross-article ordering is ambiguous, so sort by source_url
        # then by index_in_article to be deterministic.
        kept.sort(key=lambda s: (s.source_url, s.index_in_article))
        return Summary(
            sentences=tuple(kept),
            per_source_counts=per_source,
            total_input_sentences=total_input,
            dedup_dropped=dropped,
        )

    # ----- helpers -----

    def _is_duplicate(self, candidate: ScoredSentence, kept: list[ScoredSentence]) -> bool:
        tokens_c = simple_tokenize(candidate.text)
        for k in kept:
            if jaccard(tokens_c, simple_tokenize(k.text)) >= self.dedup_threshold:
                return True
            ratio = SequenceMatcher(
                None,
                normalized_simple(candidate.text),
                normalized_simple(k.text),
            ).ratio()
            if ratio >= self.dedup_threshold:
                return True
        return False
