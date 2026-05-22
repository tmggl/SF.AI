"""sf_ai.core.nlp — Language Understanding Layer (Phase 3).

Pipeline:
    raw text
      ─► TextCleaner          (preserve code, drop noise)
      ─► ArabicNormalizer     (NFC, tashkeel, alef/yaa unification, digits)
      ─► ArabiziMapper        (shlon → شلون, keef → كيف …) — code-safe
      ─► DialectMapper        (dialect form → canonical MSA hint)
      ─► TypoCorrector        (typo patterns + bounded fuzzy)
      ─► Tokenizer            (whitespace + light Arabic-aware splits)
      ─► LanguageDetector     (ar / en / mixed / code)
      ─► IntentDetector       (hints — never decides alone)
      ─► NLPAnalysis

No pretrained model is touched anywhere in this layer. All decisions are
driven by local rules + YAML lexicons under `resources/lexicons/`.
"""

from sf_ai.core.nlp.arabic_normalizer import ArabicNormalizer
from sf_ai.core.nlp.arabizi_mapper import ArabiziMapper
from sf_ai.core.nlp.dialect_mapper import DialectMapper
from sf_ai.core.nlp.intent_detector import IntentDetector
from sf_ai.core.nlp.language_detector import LanguageDetector
from sf_ai.core.nlp.pipeline import NLPPipeline, get_default_pipeline
from sf_ai.core.nlp.text_cleaner import TextCleaner
from sf_ai.core.nlp.tokenizer import LightTokenizer
from sf_ai.core.nlp.typo_corrector import TypoCorrector
from sf_ai.core.nlp.types import (
    Correction,
    DialectSignal,
    IntentHint,
    NLPAnalysis,
)

__all__ = [
    "ArabicNormalizer",
    "ArabiziMapper",
    "Correction",
    "DialectMapper",
    "DialectSignal",
    "IntentDetector",
    "IntentHint",
    "LanguageDetector",
    "LightTokenizer",
    "NLPAnalysis",
    "NLPPipeline",
    "TextCleaner",
    "TypoCorrector",
    "get_default_pipeline",
]
