"""Response style enum for the Composer."""

from __future__ import annotations

from enum import Enum


class ResponseStyle(str, Enum):
    ARABIC_FORMAL = "arabic_formal"
    ARABIC_CASUAL = "arabic_casual"
    ENGLISH_FORMAL = "english_formal"
