"""Lexical similarity primitives — pure Python, no external models.

These functions are the foundation Phase 2 routing uses. They are intentionally
simple so Phase 3 can layer richer normalization (typo correction, dialect
aliases, Arabizi) on top without changing this code.
"""

from __future__ import annotations

import re
import unicodedata

_WHITESPACE_RE = re.compile(r"\s+")
# Punctuation kept light: strip common separators (incl. Arabic ones) but
# keep code-relevant chars like {} [] () ; : / \ . _ - = + * < > intentionally
# out of this regex — Phase 3 cleaner will handle that nuance.
_PUNCT_RE = re.compile(r"[،,.;:!?؟؛٫٬\"'\(\)\[\]\{\}«»…]+")


def normalized_simple(text: str) -> str:
    """Light-weight normalization shared by Phase 2 routing.

    - Unicode NFC.
    - Lower-case ASCII.
    - Strip a small punctuation set.
    - Collapse whitespace.

    Phase 3 will provide a real ArabicNormalizer (alef/yaa/ta-marbuta etc.).
    """
    text = unicodedata.normalize("NFC", text)
    text = text.lower()
    text = _PUNCT_RE.sub(" ", text)
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text


def simple_tokenize(text: str) -> list[str]:
    """Tokenize on whitespace after light normalization."""
    if not text:
        return []
    return [t for t in normalized_simple(text).split(" ") if t]


def overlap_count(tokens_a: list[str], tokens_b: list[str]) -> int:
    """Number of tokens of `tokens_b` that appear in `tokens_a` (multiset-safe)."""
    if not tokens_a or not tokens_b:
        return 0
    pool = list(tokens_a)
    matched = 0
    for tok in tokens_b:
        if tok in pool:
            pool.remove(tok)
            matched += 1
    return matched


def jaccard(tokens_a: list[str], tokens_b: list[str]) -> float:
    """Set Jaccard similarity over tokens. 0.0 when either side is empty."""
    set_a = set(tokens_a)
    set_b = set(tokens_b)
    if not set_a or not set_b:
        return 0.0
    inter = len(set_a & set_b)
    union = len(set_a | set_b)
    return inter / union if union else 0.0


def contains_phrase(text: str, phrase: str) -> bool:
    """Whole-substring match over normalized text."""
    if not phrase:
        return False
    return normalized_simple(phrase) in normalized_simple(text)
