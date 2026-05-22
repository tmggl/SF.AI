"""WebResponseBuilder — short, structured response for the web domain.

Builds an Arabic-formal block listing each fetched article (title +
source domain + short snippet) and reminding the user that no search API
was used. Reuses CitationBuilder for the references.
"""

from __future__ import annotations

from dataclasses import dataclass

from sf_ai.modules.web.web_result_ranker import RankedArticle


@dataclass(frozen=True)
class BuiltWebReply:
    text: str
    article_count: int


_SNIPPET_CHARS = 240


class WebResponseBuilder:
    def __init__(self, *, snippet_chars: int = _SNIPPET_CHARS) -> None:
        if snippet_chars < 40:
            raise ValueError("snippet_chars must be >= 40")
        self.snippet_chars = snippet_chars

    def build(
        self,
        ranked: list[RankedArticle],
        *,
        skipped: list[tuple[str, str]] | None = None,
        query: str = "",
    ) -> BuiltWebReply:
        skipped = skipped or []
        if not ranked:
            lines: list[str] = []
            if query:
                lines.append(f"بحثت في المصادر التي زوّدتني بها عن: «{query}».")
            lines.append(
                "لم أحصل على مقالات صالحة لتلخيصها. "
                "Phase 7 لا تستخدم أي محرك بحث خارجي — أرسل لي روابط مباشرة."
            )
            if skipped:
                lines.append("")
                lines.append("روابط متجاوَزة:")
                for url, reason in skipped:
                    lines.append(f"• {url} — {reason}")
            return BuiltWebReply(text="\n".join(lines), article_count=0)

        lines = [f"نتائج البحث ({len(ranked)} مصدر):", ""]
        for i, r in enumerate(ranked, start=1):
            art = r.article
            snippet = art.body_text[: self.snippet_chars].rstrip()
            if len(art.body_text) > self.snippet_chars:
                snippet += "…"
            lines.append(f"[{i}] {art.title or '(بدون عنوان)'} — {art.source_domain}")
            if art.publish_date:
                lines.append(f"    تاريخ النشر: {art.publish_date}")
            if art.author:
                lines.append(f"    الكاتب: {art.author}")
            lines.append(f"    {snippet}")
            lines.append(f"    {art.url}")
            lines.append("")

        if skipped:
            lines.append("روابط متجاوَزة:")
            for url, reason in skipped:
                lines.append(f"• {url} — {reason}")

        return BuiltWebReply(text="\n".join(lines).rstrip(), article_count=len(ranked))
