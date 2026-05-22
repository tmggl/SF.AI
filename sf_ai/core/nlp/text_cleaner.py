"""TextCleaner — strips noise without destroying code.

Phase 3 cleaner only removes characters that are clearly not content:
zero-width marks, control chars (except newline/tab), exotic emoji-style
punctuation. Programming-relevant symbols `{} [] () ; : / \\ . _ - = + * < >`
are preserved because Phase 4+ chat and Phase 7 web summarizer must be able
to echo code/URLs faithfully.
"""

from __future__ import annotations

import re

# Preserve programming-relevant punctuation. Reject only:
#   - control chars (Cc) other than \n \t
#   - format chars (Cf): RLM/LRM/ZWNJ/ZWJ/BOM (the normalizer also handles these)
#   - exotic quote / dash sets (left as-is — they don't break routing)
_CONTROL_RE = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]")
_FORMAT_RE = re.compile(r"[​-‏‪-‮⁠-⁯﻿]")
_MULTI_NEWLINE_RE = re.compile(r"\n{3,}")


class TextCleaner:
    """Conservative cleaner. Returns a new string; never mutates input."""

    def clean(self, text: str) -> str:
        if not text:
            return ""
        text = _CONTROL_RE.sub("", text)
        text = _FORMAT_RE.sub("", text)
        text = _MULTI_NEWLINE_RE.sub("\n\n", text)
        return text.strip()
