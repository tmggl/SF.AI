"""Education domain skeleton — no tutoring engine yet."""

from __future__ import annotations

from sf_ai.modules._skeleton import SkeletonDomainModule


class EducationModule(SkeletonDomainModule):
    domain = "education"
    limitations = (
        "does not generate full lessons, quizzes, or curricula yet",
        "no learner model or long-term study plan engine",
        "no external education AI API",
    )
