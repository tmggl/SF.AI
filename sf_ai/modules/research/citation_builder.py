"""CitationBuilder — attach citations to summary sentences.

Each citation is a numbered reference [1], [2], ... mapping to a
SourceMetadata. The builder produces:
- inline-cited text (each sentence followed by [n])
- a references block, ordered, with title + url + author + date

Phase 7 keeps the format simple and human-readable. JSON / BibTeX exports
can be added later from the same `Citation` dataclass.
"""

from __future__ import annotations

from dataclasses import dataclass

from sf_ai.modules.research.summarizer import ScoredSentence, Summary
from sf_ai.tools.web.source_metadata import SourceMetadata


@dataclass(frozen=True)
class Citation:
    number: int
    source_url: str
    title: str
    author: str = ""
    publish_date: str = ""


@dataclass(frozen=True)
class CitedText:
    body: str
    citations: tuple[Citation, ...]

    def references_block(self) -> str:
        if not self.citations:
            return ""
        lines = ["", "المصادر:"]
        for c in self.citations:
            line = f"[{c.number}] {c.title or c.source_url}"
            if c.author:
                line += f" — {c.author}"
            if c.publish_date:
                line += f" — {c.publish_date}"
            line += f"\n    {c.source_url}"
            lines.append(line)
        return "\n".join(lines)


class CitationBuilder:
    def build(
        self,
        summary: Summary,
        sources: dict[str, SourceMetadata] | None = None,
    ) -> CitedText:
        if not summary.sentences:
            return CitedText(body="", citations=())

        sources = sources or {}
        url_to_number: dict[str, int] = {}
        citations: list[Citation] = []
        body_lines: list[str] = []

        def _cite(url: str) -> int:
            if url not in url_to_number:
                n = len(url_to_number) + 1
                url_to_number[url] = n
                meta = sources.get(url)
                citations.append(
                    Citation(
                        number=n,
                        source_url=url,
                        title=(meta.title if meta else "") or url,
                        author=meta.author if meta else "",
                        publish_date=meta.publish_date if meta else "",
                    )
                )
            return url_to_number[url]

        for sent in summary.sentences:
            if sent.source_url:
                num = _cite(sent.source_url)
                body_lines.append(f"{sent.text} [{num}]")
            else:
                body_lines.append(sent.text)

        return CitedText(body="\n".join(body_lines), citations=tuple(citations))
