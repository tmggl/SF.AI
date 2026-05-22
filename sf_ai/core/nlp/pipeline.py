"""NLPPipeline — orchestrates the Language Understanding Layer.

Order of operations:
    1. TextCleaner.clean        → cleaned_text
    2. ArabicNormalizer.normalize → normalized_text (from cleaned)
    3. ArabiziMapper.transform   → latin chat → Arabic + arabizi signals
    4. ArabicNormalizer.normalize → re-normalize after arabizi rewrite
    5. DialectMapper.map_text    → canonical_text + dialect signals
    6. TypoCorrector.correct     → corrected_text + corrections
    7. LightTokenizer.tokenize   → tokens (from canonical)
    8. LanguageDetector.detect   → language label
    9. SafetyScanner.scan        → safety_flags (across all lenses)
   10. IntentDetector.detect     → intent_hints (across all lenses)

The output NLPAnalysis is purely informative — downstream components decide.
"""

from __future__ import annotations

from functools import lru_cache

from sf_ai.core.nlp._safety import SafetyScanner
from sf_ai.core.nlp.arabic_normalizer import ArabicNormalizer
from sf_ai.core.nlp.arabizi_mapper import ArabiziMapper
from sf_ai.core.nlp.dialect_mapper import DialectMapper
from sf_ai.core.nlp.intent_detector import IntentDetector
from sf_ai.core.nlp.language_detector import LanguageDetector
from sf_ai.core.nlp.text_cleaner import TextCleaner
from sf_ai.core.nlp.tokenizer import LightTokenizer
from sf_ai.core.nlp.typo_corrector import TypoCorrector
from sf_ai.core.nlp.types import DialectSignal, NLPAnalysis


def _confidence_from_signals(*scores: float) -> float:
    """Combine boolean confidences into a soft estimate in [0,1)."""
    if not scores:
        return 0.0
    total = sum(scores)
    return total / (total + 2.0)


class NLPPipeline:
    def __init__(
        self,
        cleaner: TextCleaner | None = None,
        normalizer: ArabicNormalizer | None = None,
        arabizi: ArabiziMapper | None = None,
        dialect: DialectMapper | None = None,
        corrector: TypoCorrector | None = None,
        tokenizer: LightTokenizer | None = None,
        language: LanguageDetector | None = None,
        intent: IntentDetector | None = None,
        safety: SafetyScanner | None = None,
    ) -> None:
        self.cleaner = cleaner or TextCleaner()
        self.normalizer = normalizer or ArabicNormalizer()
        self.arabizi = arabizi or ArabiziMapper()
        self.dialect = dialect or DialectMapper()
        self.corrector = corrector or TypoCorrector()
        self.tokenizer = tokenizer or LightTokenizer()
        self.language = language or LanguageDetector()
        self.intent = intent or IntentDetector()
        self.safety = safety or SafetyScanner()

    def analyze_user_text(self, text: str) -> NLPAnalysis:
        original = text or ""

        cleaned = self.cleaner.clean(original)
        normalized = self.normalizer.normalize(cleaned)

        # Arabizi rewrite (Latin → Arabic), then re-normalize.
        arabizi_out, arabizi_signals = self.arabizi.transform(normalized)
        canonical_after_arabizi = self.normalizer.normalize(arabizi_out)

        # Dialect → canonical hint.
        canonical, dialect_signals = self.dialect.map_text(canonical_after_arabizi)

        # Typo correction operates on the canonical form.
        corrected, corrections = self.corrector.correct(canonical)

        # Tokens taken from canonical (downstream lexicon lookups expect canonical-ish).
        tokens = tuple(self.tokenizer.tokenize(canonical))

        # Language detected on the original (untouched) text.
        language = self.language.detect(original)

        # Dialect verdict from signal votes.
        all_signals: tuple[DialectSignal, ...] = arabizi_signals + dialect_signals
        detected_dialect = self.dialect.detect_dialect(all_signals)

        safety_flags = self.safety.scan(
            original, normalized, canonical, corrected
        )

        intent_hints = self.intent.detect(
            normalized, canonical, corrected
        )

        domain_hints: tuple[str, ...] = tuple(
            dict.fromkeys(h.domain_hint for h in intent_hints)
        )

        confidence = _confidence_from_signals(
            float(bool(cleaned)),
            float(bool(normalized)),
            float(bool(all_signals)) * 0.5,
            float(bool(intent_hints)),
        )

        return NLPAnalysis(
            original_text=original,
            cleaned_text=cleaned,
            normalized_text=normalized,
            corrected_text=corrected,
            canonical_text=canonical,
            language=language,
            detected_dialect=detected_dialect,
            tokens=tokens,
            corrections=corrections,
            aliases=all_signals,
            domain_hints=domain_hints,
            intent_hints=intent_hints,
            safety_flags=safety_flags,
            confidence=confidence,
        )


@lru_cache(maxsize=1)
def get_default_pipeline() -> NLPPipeline:
    return NLPPipeline()
