"""Translation domain skeleton — no translation engine yet."""

from __future__ import annotations

from sf_ai.modules._skeleton import SkeletonDomainModule


class TranslationModule(SkeletonDomainModule):
    domain = "translation"
    limitations = (
        "does not translate sentences or documents yet",
        "DialectMapper aliases are not a translation engine",
        "no pretrained translation model or external AI API",
    )
