"""ResponseOrganizer — formats summary + citations into a final response.

Returns Arabic-formal text with sections:
- (optional) headline
- bullet-point summary
- references block

The Composer in Phase 2 still owns "default reply style"; this organizer
adds research-specific structure. It produces a string ready for the
orchestrator's `OrchestratorResult.response`.
"""

from __future__ import annotations

from dataclasses import dataclass

from sf_ai.modules.research.citation_builder import CitedText


@dataclass(frozen=True)
class OrganizedResponse:
    text: str
    bullet_count: int
    citation_count: int


class ResponseOrganizer:
    def __init__(
        self,
        *,
        headline: str = "ملخص",
        bullet_marker: str = "• ",
        include_disclaimer: bool = True,
    ) -> None:
        self.headline = headline
        self.bullet_marker = bullet_marker
        self.include_disclaimer = include_disclaimer

    def organize(self, cited: CitedText) -> OrganizedResponse:
        if not cited.body.strip():
            return OrganizedResponse(
                text=(
                    "لم أجد محتوى كافٍ للتلخيص في المصادر المعطاة. "
                    "تحقق من الروابط، ثم أعد الطلب."
                ),
                bullet_count=0,
                citation_count=0,
            )

        bullets: list[str] = []
        for line in cited.body.splitlines():
            line = line.strip()
            if not line:
                continue
            bullets.append(f"{self.bullet_marker}{line}")

        sections: list[str] = []
        sections.append(self.headline)
        sections.append("")
        sections.extend(bullets)
        refs_block = cited.references_block()
        if refs_block:
            sections.append(refs_block)
        if self.include_disclaimer:
            sections.append("")
            sections.append(
                "ملاحظة: التلخيص مبني على قواعد لغوية محلية (rule-based) — "
                "ليس توليدًا من نموذج. راجع المصادر الأصلية للتحقق."
            )
        return OrganizedResponse(
            text="\n".join(sections).strip(),
            bullet_count=len(bullets),
            citation_count=len(cited.citations),
        )
