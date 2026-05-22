"""ArabiziMapper — converts Latin-script Arabic chat into Arabic letters.

Operates token-by-token so protected tokens (programming/tech terms like
`python`, `docker`, `api`) are preserved as-is. Each mapping carries a
dialect tag and a confidence.
"""

from __future__ import annotations

import re

from sf_ai.core.nlp._lexicons import load_lexicon
from sf_ai.core.nlp.types import DialectSignal

_LATIN_TOKEN_RE = re.compile(r"[A-Za-z0-9]+")


class ArabiziMapper:
    def __init__(self) -> None:
        data = load_lexicon("arabizi_map.yaml")
        raw = data.get("mappings") or {}
        self._map: dict[str, dict[str, object]] = {k.lower(): v for k, v in raw.items()}
        self._protected: frozenset[str] = frozenset(
            (t.lower() for t in (data.get("protected_tokens") or ()))
        )

    def is_protected(self, token: str) -> bool:
        return token.lower() in self._protected

    def map_token(self, token: str) -> DialectSignal | None:
        if not token:
            return None
        lower = token.lower()
        if lower in self._protected:
            return None
        entry = self._map.get(lower)
        if entry is None:
            return None
        return DialectSignal(
            surface=token,
            canonical=str(entry.get("ar", token)),
            dialect=str(entry.get("dialect", "arabizi")),
            confidence=float(entry.get("conf", 0.7)),
        )

    def transform(self, text: str) -> tuple[str, tuple[DialectSignal, ...]]:
        """Rewrite Latin tokens to Arabic where confident. Returns (new_text, signals)."""
        if not text:
            return "", ()

        signals: list[DialectSignal] = []

        def _sub(match: re.Match[str]) -> str:
            tok = match.group(0)
            signal = self.map_token(tok)
            if signal is None:
                return tok
            signals.append(signal)
            return signal.canonical

        new_text = _LATIN_TOKEN_RE.sub(_sub, text)
        return new_text, tuple(signals)
