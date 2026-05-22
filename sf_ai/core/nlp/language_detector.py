"""LanguageDetector — character-class voting.

Labels: ar | en | mixed | code | unknown.

`code` is reported when at least 30% of characters are code-specific symbols
or token shape suggests a code snippet (presence of `def `, `class `, `=>`,
fenced blocks, `;` line terminator density).
"""

from __future__ import annotations

import re

_AR_RANGE = re.compile(r"[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]")
_EN_RANGE = re.compile(r"[A-Za-z]")
_CODE_HINTS = re.compile(
    r"(\bdef\s|\bclass\s|=>|->|::|\bimport\s|\bfrom\s|"
    r"^\s*#include|\bSELECT\s|\bINSERT\s|\bUPDATE\s|"
    r"\b(public|private|static|void)\s|"
    r"```|\b(let|const|var)\s)",
    re.IGNORECASE | re.MULTILINE,
)
_CODE_SYMBOLS = re.compile(r"[{}\[\];=<>+*/\\|`~]")


class LanguageDetector:
    def detect(self, text: str) -> str:
        if not text or not text.strip():
            return "unknown"

        ar_count = len(_AR_RANGE.findall(text))
        en_count = len(_EN_RANGE.findall(text))
        total_letters = ar_count + en_count

        if _CODE_HINTS.search(text):
            return "code"

        sym_count = len(_CODE_SYMBOLS.findall(text))
        density = sym_count / max(len(text), 1)
        if density >= 0.3 and total_letters < sym_count * 1.5:
            return "code"

        if total_letters == 0:
            return "unknown"

        ar_ratio = ar_count / total_letters
        if ar_ratio >= 0.85:
            return "ar"
        if ar_ratio <= 0.15:
            return "en"
        return "mixed"
