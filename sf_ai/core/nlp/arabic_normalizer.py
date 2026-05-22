"""ArabicNormalizer — light, lossless Arabic normalization.

Operations:
    1. Unicode NFC.
    2. Strip tashkeel + tatweel + zero-width marks.
    3. Unify alef forms (أ إ آ ٱ → ا) and yaa (ى → ي).
    4. Digit unification (Arabic-Indic / Eastern → ASCII).
    5. Whitespace collapse.

Reads its character tables from `resources/lexicons/arabic_normalization.yaml`
so rules are inspectable. The original text is never destroyed — the pipeline
keeps `original_text` separately on `NLPAnalysis`.
"""

from __future__ import annotations

import re
import unicodedata

from sf_ai.core.nlp._lexicons import load_lexicon

_WHITESPACE_RE = re.compile(r"\s+")


class ArabicNormalizer:
    def __init__(
        self,
        strip_chars: tuple[str, ...] | None = None,
        char_map: dict[str, str] | None = None,
        digit_map: dict[str, str] | None = None,
        fold_ta_marbuta: bool = False,
    ) -> None:
        if strip_chars is None or char_map is None or digit_map is None:
            data = load_lexicon("arabic_normalization.yaml")
            strip_chars = strip_chars or tuple(data.get("strip_chars") or ())
            char_map = char_map or dict(data.get("char_map") or {})
            digit_map = digit_map or dict(data.get("digit_map") or {})
            options = data.get("options") or {}
            fold_ta_marbuta = bool(options.get("fold_ta_marbuta", fold_ta_marbuta))

        self._strip_set = frozenset(strip_chars)
        self._char_map = char_map
        self._digit_map = digit_map
        self._fold_ta_marbuta = fold_ta_marbuta
        # Build a fast translation table at construction time.
        combined: dict[int, str | None] = {}
        for ch in self._strip_set:
            combined[ord(ch)] = None
        for src, dst in self._char_map.items():
            combined[ord(src)] = dst
        for src, dst in self._digit_map.items():
            combined[ord(src)] = dst
        if fold_ta_marbuta:
            combined[ord("ة")] = "ه"
        self._table = combined

    def normalize(self, text: str) -> str:
        if not text:
            return ""
        text = unicodedata.normalize("NFC", text)
        text = text.translate(self._table)
        text = _WHITESPACE_RE.sub(" ", text).strip()
        return text

    # Sometimes callers want a fold-everything variant for fuzzy matching.
    def normalize_aggressive(self, text: str) -> str:
        base = self.normalize(text)
        return base.replace("ة", "ه")
