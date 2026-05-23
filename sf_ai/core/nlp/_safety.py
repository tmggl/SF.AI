"""Internal safety-term scanner used by the NLP pipeline."""

from __future__ import annotations

import re

from sf_ai.core.nlp._lexicons import load_lexicon


_TOKEN_RE = re.compile(r"[\w\u0600-\u06FF]+", re.UNICODE)

_BENEFIT_NON_FINANCE_CONTEXT = {
    "قراءة",
    "القراءة",
    "قراية",
    "القراية",
    "تعلم",
    "التعلم",
    "دراسة",
    "الدراسة",
    "رياضة",
    "الرياضة",
}


def _tokenize_for_safety(text: str) -> tuple[str, ...]:
    return tuple(match.group(0) for match in _TOKEN_RE.finditer(text))


def _contains_safety_term(variant: str, term: str) -> bool:
    term_lower = term.lower()
    tokens = {token for token in _tokenize_for_safety(variant)}
    tokens_lower = {token.lower() for token in tokens}
    if " " not in term_lower:
        return term in tokens or term_lower in tokens_lower

    padded_variant = " ".join(_tokenize_for_safety(variant.lower()))
    return f" {term_lower} " in f" {padded_variant} "


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
            for domain, terms in self._flags.items():
                for term in terms:
                    if _is_contextual_false_positive(variant, domain, term):
                        continue
                    if _contains_safety_term(variant, term):
                        flag = f"{domain}:{term}"
                        if flag not in hits:
                            hits.append(flag)
        return tuple(hits)


def _is_contextual_false_positive(variant: str, domain: str, term: str) -> bool:
    """Avoid treating everyday "benefit of reading" phrases as finance.

    The finance flag keeps `فائدة` for loan/bank contexts, but common
    educational questions like "ما فائدة القراءة؟" should not block the
    generator as financial advice.
    """
    if domain != "finance" or term not in {"فائدة", "فائده"}:
        return False
    tokens = {token.lower() for token in _tokenize_for_safety(variant)}
    return bool(tokens & _BENEFIT_NON_FINANCE_CONTEXT)
