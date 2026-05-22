"""TypoCorrector — rule-based + bounded fuzzy.

Two sources of fixes:
1. `patterns` from `typo_patterns.yaml` — applied automatically when
   confidence ≥ `apply_threshold` (default 0.7).
2. `soft_hints` — reported on NLPAnalysis.corrections but NOT applied to
   `corrected_text`. The chat module may surface them to the user.

Fuzzy fallback is intentionally limited: only triggered against a small
known-good vocabulary (e.g. domain keywords) to avoid mangling rare names.
"""

from __future__ import annotations

import re
from difflib import SequenceMatcher

from sf_ai.core.nlp._lexicons import load_lexicon
from sf_ai.core.nlp.types import Correction

_TOKEN_RE = re.compile(r"\S+")


class TypoCorrector:
    def __init__(
        self,
        apply_threshold: float = 0.7,
        fuzzy_threshold: float = 0.9,
    ) -> None:
        data = load_lexicon("typo_patterns.yaml")
        raw_patterns = data.get("patterns") or {}
        raw_soft = data.get("soft_hints") or {}

        self._patterns: dict[str, tuple[str, float, str]] = {
            k: (str(v.get("correct", k)), float(v.get("conf", 0.7)), str(v.get("reason", "")))
            for k, v in raw_patterns.items()
        }
        self._soft: dict[str, tuple[str, float, str]] = {
            k: (str(v.get("correct", k)), float(v.get("conf", 0.5)), str(v.get("reason", "")))
            for k, v in raw_soft.items()
        }
        self.apply_threshold = apply_threshold
        self.fuzzy_threshold = fuzzy_threshold

    def correct(self, text: str) -> tuple[str, tuple[Correction, ...]]:
        """Return (corrected_text, corrections)."""
        if not text:
            return "", ()

        corrections: list[Correction] = []

        def _replace(match: re.Match[str]) -> str:
            tok = match.group(0)
            lower = tok.lower()
            pattern_hit = self._patterns.get(lower) or self._patterns.get(tok)
            if pattern_hit is not None:
                correct, conf, reason = pattern_hit
                corrections.append(
                    Correction(
                        original=tok,
                        corrected=correct,
                        confidence=conf,
                        reason=reason or "typo_pattern",
                    )
                )
                if conf >= self.apply_threshold:
                    return correct
                return tok

            soft_hit = self._soft.get(lower) or self._soft.get(tok)
            if soft_hit is not None:
                correct, conf, reason = soft_hit
                corrections.append(
                    Correction(
                        original=tok,
                        corrected=correct,
                        confidence=conf,
                        reason=reason or "soft_hint",
                    )
                )
            return tok

        corrected = _TOKEN_RE.sub(_replace, text)
        return corrected, tuple(corrections)

    def fuzzy_against(self, token: str, vocabulary: list[str]) -> Correction | None:
        """Bounded fuzzy correction against a known-good vocabulary."""
        if not token or not vocabulary:
            return None
        best_word: str | None = None
        best_ratio = 0.0
        for cand in vocabulary:
            ratio = SequenceMatcher(None, token.lower(), cand.lower()).ratio()
            if ratio > best_ratio:
                best_word, best_ratio = cand, ratio
        if best_word is None or best_ratio < self.fuzzy_threshold:
            return None
        if best_word == token:
            return None
        return Correction(
            original=token,
            corrected=best_word,
            confidence=best_ratio,
            reason="fuzzy",
        )
