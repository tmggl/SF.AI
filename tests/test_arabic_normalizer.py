"""Phase 3 — ArabicNormalizer + TextCleaner + LightTokenizer + LanguageDetector."""

from __future__ import annotations

from sf_ai.core.nlp import ArabicNormalizer, LanguageDetector, LightTokenizer, TextCleaner


def test_normalizer_strips_tashkeel() -> None:
    n = ArabicNormalizer()
    assert n.normalize("مَرْحَبًا") == "مرحبا"


def test_normalizer_strips_tatweel() -> None:
    n = ArabicNormalizer()
    assert n.normalize("مرحــــبا") == "مرحبا"


def test_normalizer_unifies_alef_forms() -> None:
    n = ArabicNormalizer()
    assert n.normalize("أهلاً") == "اهلا"
    assert n.normalize("إيراد") == "ايراد"
    assert n.normalize("آمنة") == "امنه" or n.normalize("آمنة") == "امنة"


def test_normalizer_yaa() -> None:
    n = ArabicNormalizer()
    assert n.normalize("على") == "علي"


def test_normalizer_digits() -> None:
    n = ArabicNormalizer()
    assert n.normalize("سنة ٢٠٢٦") == "سنة 2026"


def test_normalizer_whitespace_collapse() -> None:
    n = ArabicNormalizer()
    assert n.normalize("   مرحبا    كيف   ") == "مرحبا كيف"


def test_text_cleaner_preserves_code_chars() -> None:
    c = TextCleaner()
    code = "def f(x): return {y: x + 1}"
    assert c.clean(code) == code


def test_text_cleaner_strips_control_chars() -> None:
    c = TextCleaner()
    out = c.clean("ab\x00cd\x07ef")
    assert out == "abcdef"


def test_tokenizer_splits_arabic_punctuation() -> None:
    t = LightTokenizer()
    assert t.tokenize("مرحبا، كيف الحال؟") == ["مرحبا", "كيف", "الحال"]


def test_tokenizer_keeps_code_tokens() -> None:
    t = LightTokenizer()
    assert "main.py" in t.tokenize("افتح main.py please")


def test_tokenizer_stopwords_optional() -> None:
    t = LightTokenizer(drop_stopwords=True)
    assert "في" not in t.tokenize("ابحث في الانترنت")


def test_language_detector_arabic() -> None:
    d = LanguageDetector()
    assert d.detect("مرحبا كيف الحال") == "ar"


def test_language_detector_english() -> None:
    d = LanguageDetector()
    assert d.detect("hello how are you today") == "en"


def test_language_detector_mixed() -> None:
    d = LanguageDetector()
    assert d.detect("ابي اشغل docker على الجهاز") == "mixed"


def test_language_detector_code() -> None:
    d = LanguageDetector()
    assert d.detect("def hello():\n    return 1") == "code"


def test_language_detector_unknown() -> None:
    d = LanguageDetector()
    assert d.detect("") == "unknown"
