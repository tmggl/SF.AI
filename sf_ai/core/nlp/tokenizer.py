"""LightTokenizer — Phase 3 placeholder tokenizer.

Not the SF-BPE tokenizer (that arrives in Phase 5.5 and trains from scratch
on SF.AI corpus). This is a deterministic whitespace + punctuation splitter
sufficient for routing & lexicon lookups.
"""

from __future__ import annotations

import re

from sf_ai.core.nlp._lexicons import load_lexicon

# Keep code-relevant chars attached to their token (so "main.py" stays one token).
# Strip Arabic + ASCII sentence punctuation.
_SPLIT_RE = re.compile(r"[\s،,؛;؟?!«»\"'\[\]\(\)\{\}…]+")


class LightTokenizer:
    def __init__(self, drop_stopwords: bool = False) -> None:
        self.drop_stopwords = drop_stopwords
        data = load_lexicon("stopwords_ar_en.yaml") or {}
        ar = set(data.get("ar") or ())
        en = set(data.get("en") or ())
        self._stopwords = ar | en

    def tokenize(self, text: str) -> list[str]:
        if not text:
            return []
        parts = (p for p in _SPLIT_RE.split(text) if p)
        if self.drop_stopwords:
            return [p for p in parts if p.lower() not in self._stopwords]
        return list(parts)

    @property
    def stopwords(self) -> frozenset[str]:
        return frozenset(self._stopwords)
