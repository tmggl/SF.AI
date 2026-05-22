"""HTMLExtractor — generic HTML → clean text + basic metadata.

Used by ArticleExtractor as the first stage. Strips scripts/styles/svg,
collapses whitespace, returns title + lang + visible text.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from bs4 import BeautifulSoup


_WS_RE = re.compile(r"[ \t\f\v]+")
_NL_RE = re.compile(r"\n{2,}")


@dataclass(frozen=True)
class ExtractedPage:
    title: str
    lang: str
    text: str
    char_count: int


_DROP_TAGS = ("script", "style", "noscript", "svg", "iframe", "form")


class HTMLExtractor:
    def extract(self, html: str) -> ExtractedPage:
        if not html:
            return ExtractedPage(title="", lang="", text="", char_count=0)
        soup = BeautifulSoup(html, "lxml")

        for tag_name in _DROP_TAGS:
            for tag in soup.find_all(tag_name):
                tag.decompose()

        title = (soup.title.get_text(strip=True) if soup.title else "")
        html_tag = soup.find("html")
        lang = ""
        if html_tag is not None:
            lang = html_tag.get("lang", "") or html_tag.get("xml:lang", "")

        body = soup.body or soup
        text = body.get_text("\n", strip=True)
        text = _WS_RE.sub(" ", text)
        text = _NL_RE.sub("\n\n", text).strip()
        return ExtractedPage(
            title=title.strip(),
            lang=lang.strip(),
            text=text,
            char_count=len(text),
        )
