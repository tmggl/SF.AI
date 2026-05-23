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
_BROKEN_PREFIX_RE = re.compile(r"^\s*[\u0600-\u06FF]\s*[؟?]")
_REPEATED_ARABIC_BIGRAM_RE = re.compile(r"([\u0600-\u06FF]{2})\1")


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

        repetition = _repetition_ratio(cleaned)
        arabic = _arabic_ratio(cleaned)
        if repetition > self.max_repetition_ratio:
            return GenerationGuardVerdict(False, "repetition", repetition, arabic)
        if arabic < self.min_arabic_ratio:
            return GenerationGuardVerdict(False, "low_arabic_ratio", repetition, arabic)
        return GenerationGuardVerdict(True, "passed", repetition, arabic)

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
