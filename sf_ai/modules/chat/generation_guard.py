"""Phase 25 guardrails for local native-generation canaries.

The guard is intentionally simple and deterministic. It does not judge
"intelligence"; it only blocks obvious bad output so a raw checkpoint cannot
pretend to be a useful assistant inside the chat UI.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_ARABIC_RE = re.compile(r"[\u0600-\u06FF]")
_TOKEN_RE = re.compile(r"[\w\u0600-\u06FF]+", re.UNICODE)
_BROKEN_CHARS = ("�", "\x00")
_CORPUS_ARTIFACTS = (
    "corpus",
    "tokenizer",
    "phase",
    "Phase",
    "training",
    "النموذج",
    "تدريب",
    "دفعة",
    "الدفعة",
    "المعنى:",
    "وأين",
)
_MODEL_ARTIFACT_FRAGMENTS = (
    # Observed in SF-10M v0.6 canary samples: Arabic-looking fragments that
    # are not stable words and should never surface in runtime chat.
    "الطرو",
    "حارين",
    "استعجه",
    "مستمستم",
    "بالمو",
    "رتنا",
    # Observed in SF-10M v0.7 after short-response repair.
    "الدعج",
    "صعج",
    "عجه",
    "حياذكر",
    "بععجه",
    "آالطف",
    "الموقت",
    "تقللا",
    "وازعج",
    "لللم",
    "خياهر",
    "موعد عج",
    "تزعريف",
    "الزعج",
    # Observed in SF-10M v0.8 after boundary/EOS + dialect conditioning.
    "اشكرتزذر",
    "خيازذر",
    "خياار",
    "بخمين",
    "حيرتزعلك",
    "بهادقتزم",
    "بالموعد",
    "بالأالأثر",
    "الأالأثر",
    "همن",
    "عجهادئة",
    "نحاستمب",
    "أخرفين",
    "يرتزعلك",
    "بالمومن",
    "عادئة",
    "منزياولت",
    "هادقف",
    "التصمن",
    "ياذكر",
    "هوياستمرغم",
    # Observed in SF-10M v0.10 after social/lexical curriculum.
    "الصوري ين",
    "روري",
    "مة مك",
    "المفاجعليك",
    "تخيارين",
    "خياروح",
    "يارين",
    # Observed in Phase 27.17 prompt-answer micro-probe.
    "وعليكأهلًا",
    "التعاعاون",
    "القراد. ءة",
    "تحتاججج",
    "ججبعيادة",
    "هوش تحتاجججبعيادة",
)
_BROKEN_PREFIX_RE = re.compile(r"^\s*[\u0600-\u06FF]\s*[؟?]")
_REPEATED_ARABIC_BIGRAM_RE = re.compile(r"([\u0600-\u06FF]{2})\1")
_REPEATED_SHORT_PHRASE_RE = re.compile(
    r"\b([\w\u0600-\u06FF]{2,}(?:\s+[\w\u0600-\u06FF]{2,}){0,2})\b"
    r"(?:\s+\1\b){2,}",
    re.IGNORECASE,
)

_SOCIAL_PROMPT_RULES: tuple[tuple[tuple[str, ...], tuple[str, ...], str], ...] = (
    (
        ("كيفك", "كيف حالك", "وشلونك", "شلونك", "علومك"),
        ("بخير", "تمام", "الحمد", "أنا"),
        "social_smalltalk_mismatch",
    ),
    (
        ("السلام عليكم", "سلام عليكم"),
        ("وعليكم", "أهل", "حياك"),
        "greeting_mismatch",
    ),
    (
        ("شكرا", "شكرًا", "مشكور", "يعطيك العافية", "تسلم"),
        ("العفو", "حياك", "تسلم", "الله يعافيك"),
        "thanks_mismatch",
    ),
    (
        ("سعودي", "بالسعودي", "لهجة سعودية"),
        ("سعودي", "السعودية", "اللهجة", "أبشر", "حياك"),
        "saudi_preference_mismatch",
    ),
)


@dataclass(frozen=True)
class GenerationGuardVerdict:
    allowed: bool
    reason: str
    repetition_ratio: float
    arabic_ratio: float


@dataclass(frozen=True)
class GenerationGuard:
    """Block repetitive, fragmented, or corpus-artifact output."""

    min_chars: int = 18
    max_repetition_ratio: float = 0.36
    min_arabic_ratio: float = 0.45
    max_slash_count: int = 2

    def inspect(self, text: str) -> GenerationGuardVerdict:
        cleaned = " ".join((text or "").split())
        if len(cleaned) < self.min_chars:
            return self._verdict(False, "too_short", cleaned)
        if _BROKEN_PREFIX_RE.search(cleaned):
            return self._verdict(False, "broken_prefix", cleaned)
        if any(ch in cleaned for ch in _BROKEN_CHARS):
            return self._verdict(False, "broken_characters", cleaned)
        if _has_malformed_token(cleaned):
            return self._verdict(False, "malformed_token", cleaned)
        if cleaned.count("/") > self.max_slash_count:
            return self._verdict(False, "too_fragmented", cleaned)
        if any(marker in cleaned for marker in _CORPUS_ARTIFACTS):
            return self._verdict(False, "corpus_artifact", cleaned)
        if any(marker in cleaned for marker in _MODEL_ARTIFACT_FRAGMENTS):
            return self._verdict(False, "model_artifact_fragment", cleaned)
        if _REPEATED_SHORT_PHRASE_RE.search(cleaned):
            return self._verdict(False, "repeated_phrase", cleaned)

        repetition = _repetition_ratio(cleaned)
        arabic = _arabic_ratio(cleaned)
        if repetition > self.max_repetition_ratio:
            return GenerationGuardVerdict(False, "repetition", repetition, arabic)
        if arabic < self.min_arabic_ratio:
            return GenerationGuardVerdict(False, "low_arabic_ratio", repetition, arabic)
        return GenerationGuardVerdict(True, "passed", repetition, arabic)

    def inspect_for_prompt(self, prompt: str, text: str) -> GenerationGuardVerdict:
        """Inspect generated text and require obvious social prompt alignment.

        The native model is still immature. A generic Arabic-looking sentence is
        not enough for runtime: common social prompts must receive a recognisable
        social answer, otherwise templates remain safer for the single-user UI.
        """

        verdict = self.inspect(text)
        if not verdict.allowed:
            return verdict

        p = _normalize_surface(prompt)
        t = _normalize_surface(text)
        for triggers, expected_terms, reason in _SOCIAL_PROMPT_RULES:
            if any(trigger in p for trigger in triggers) and not any(
                term in t for term in expected_terms
            ):
                return GenerationGuardVerdict(
                    allowed=False,
                    reason=reason,
                    repetition_ratio=verdict.repetition_ratio,
                    arabic_ratio=verdict.arabic_ratio,
                )
        return verdict

    def _verdict(self, allowed: bool, reason: str, text: str) -> GenerationGuardVerdict:
        return GenerationGuardVerdict(
            allowed=allowed,
            reason=reason,
            repetition_ratio=_repetition_ratio(text),
            arabic_ratio=_arabic_ratio(text),
        )


def _repetition_ratio(text: str) -> float:
    tokens = _TOKEN_RE.findall(text)
    if not tokens:
        return 1.0
    counts: dict[str, int] = {}
    for token in tokens:
        t = token.lower()
        counts[t] = counts.get(t, 0) + 1
    repeated = sum(count - 1 for count in counts.values() if count > 1)
    return repeated / max(1, len(tokens))


def _arabic_ratio(text: str) -> float:
    letters = [ch for ch in text if ch.isalpha()]
    if not letters:
        return 0.0
    arabic = sum(1 for ch in letters if _ARABIC_RE.match(ch))
    return arabic / len(letters)


def _has_malformed_token(text: str) -> bool:
    for token in _TOKEN_RE.findall(text):
        if len(token) >= 6 and _REPEATED_ARABIC_BIGRAM_RE.search(token):
            return True
    return False


def _normalize_surface(text: str) -> str:
    return (
        (text or "")
        .replace("أ", "ا")
        .replace("إ", "ا")
        .replace("آ", "ا")
        .replace("ى", "ي")
        .replace("ة", "ه")
        .strip()
        .lower()
    )
