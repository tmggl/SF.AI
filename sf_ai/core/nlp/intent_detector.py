"""IntentDetector — produces IntentHint records.

This component **does not decide** the final intent. Its job is to surface
"these intents look plausible" so the Router can either confirm or override.
Phase 4's ChatModule can also consume hints directly without re-routing.

Signals are scored with the same scale as the router (phrase +5, keyword +3,
fuzzy +1), then normalized into confidence with the same softening formula.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from difflib import SequenceMatcher

from sf_ai.core.config import CONFIDENCE_SOFTENING, FUZZY_MATCH_THRESHOLD
from sf_ai.core.nlp._lexicons import load_lexicon
from sf_ai.core.nlp.types import IntentHint


@dataclass(frozen=True)
class _IntentDef:
    intent: str
    domain: str
    phrases: tuple[str, ...]
    keywords: tuple[str, ...]


def _confidence(score: float) -> float:
    if score <= 0.0:
        return 0.0
    return score / (score + CONFIDENCE_SOFTENING)


@dataclass
class _Score:
    intent: _IntentDef
    score: float = 0.0
    matched: list[str] = field(default_factory=list)


class IntentDetector:
    def __init__(self, fuzzy_threshold: float = FUZZY_MATCH_THRESHOLD) -> None:
        data = load_lexicon("intents.yaml") or {}
        raw = data.get("intents") or {}
        intents: list[_IntentDef] = []
        for name, body in raw.items():
            if not isinstance(body, dict):
                continue
            intents.append(
                _IntentDef(
                    intent=name,
                    domain=str(body.get("domain", "chat")),
                    phrases=tuple(body.get("phrases") or ()),
                    keywords=tuple(body.get("keywords") or ()),
                )
            )
        self._intents = tuple(intents)
        self.fuzzy_threshold = fuzzy_threshold

    def detect(self, *text_variants: str) -> tuple[IntentHint, ...]:
        """Score each intent against any of the provided text lenses.

        Pass the original/normalized/canonical/corrected lenses — the highest
        score across them wins. Empty variants are ignored.
        """
        candidates = [v for v in text_variants if v and v.strip()]
        if not candidates:
            return ()

        scores: list[_Score] = []
        for intent in self._intents:
            sc = _Score(intent=intent)
            for variant in candidates:
                lowered = variant.lower()
                # Phrase containment.
                for phrase in intent.phrases:
                    if phrase and phrase in variant:
                        sc.score += 5.0
                        sc.matched.append(phrase)
                # Keyword token containment.
                v_tokens = set(variant.split())
                for kw in intent.keywords:
                    if kw and kw in v_tokens:
                        sc.score += 3.0
                        sc.matched.append(kw)
                    elif kw and kw.lower() in lowered.split():
                        sc.score += 3.0
                        sc.matched.append(kw)
                # Fuzzy: only against phrases, capped at 1 hit per variant.
                if not sc.matched:
                    for phrase in intent.phrases:
                        ratio = SequenceMatcher(None, variant, phrase).ratio()
                        if ratio >= self.fuzzy_threshold:
                            sc.score += 1.0
                            sc.matched.append(phrase)
                            break
            if sc.score > 0:
                scores.append(sc)

        scores.sort(key=lambda s: s.score, reverse=True)

        # Keep top-3 hints; dedupe matched terms within each.
        out: list[IntentHint] = []
        for sc in scores[:3]:
            seen: set[str] = set()
            unique: list[str] = []
            for m in sc.matched:
                if m not in seen:
                    unique.append(m)
                    seen.add(m)
            out.append(
                IntentHint(
                    intent=sc.intent.intent,
                    domain_hint=sc.intent.domain,
                    confidence=_confidence(sc.score),
                    matched_terms=tuple(unique),
                )
            )
        return tuple(out)
