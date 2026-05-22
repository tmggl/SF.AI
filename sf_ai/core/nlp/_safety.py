"""Internal safety-term scanner used by the NLP pipeline."""

from __future__ import annotations

from sf_ai.core.nlp._lexicons import load_lexicon


class SafetyScanner:
    def __init__(self) -> None:
        data = load_lexicon("safety_terms.yaml") or {}
        flags = data.get("flags") or {}
        self._flags: dict[str, tuple[str, ...]] = {
            domain: tuple(terms or ()) for domain, terms in flags.items()
        }

    def scan(self, *text_variants: str) -> tuple[str, ...]:
        if not self._flags:
            return ()
        hits: list[str] = []
        for variant in text_variants:
            if not variant:
                continue
            lowered = variant.lower()
            tokens = set(variant.split()) | set(lowered.split())
            for domain, terms in self._flags.items():
                for term in terms:
                    if term in tokens or term.lower() in tokens or term in variant:
                        flag = f"{domain}:{term}"
                        if flag not in hits:
                            hits.append(flag)
        return tuple(hits)
