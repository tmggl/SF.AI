"""ArticleExtractor — extract article-shaped content from HTML.

Heuristics:
- Title: <h1> > <meta og:title> > <title>
- Author: <meta name="author"> > <meta property="article:author"> > .byline / .author
- Publish date: <meta property="article:published_time"> > <meta name="date"> > <time datetime=...>
- Body: <article> > <main> > <body>, with nav/header/footer/aside removed

Returns an `Article` dataclass with a paired `SourceMetadata` candidate.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from bs4 import BeautifulSoup

from sf_ai.tools.web.html_extractor import HTMLExtractor
from sf_ai.tools.web.source_metadata import (
    SourceMetadata,
    content_hash,
    domain_of,
    now_utc,
)


_DROP_NAV_TAGS = ("nav", "header", "footer", "aside")
_WS_RE = re.compile(r"[ \t\f\v]+")


@dataclass(frozen=True)
class Article:
    title: str
    author: str
    publish_date: str
    body_text: str
    body_html: str          # cleaned article fragment (for citations)
    lang: str
    url: str
    source_domain: str


class ArticleExtractor:
    def __init__(self) -> None:
        self._html = HTMLExtractor()

    # ---- low-level metadata helpers ----

    @staticmethod
    def _meta(soup: BeautifulSoup, *, name: str | None = None, prop: str | None = None) -> str:
        if name is not None:
            tag = soup.find("meta", attrs={"name": re.compile(rf"^{re.escape(name)}$", re.I)})
            if tag and tag.get("content"):
                return str(tag["content"]).strip()
        if prop is not None:
            tag = soup.find("meta", attrs={"property": re.compile(rf"^{re.escape(prop)}$", re.I)})
            if tag and tag.get("content"):
                return str(tag["content"]).strip()
        return ""

    def _title(self, soup: BeautifulSoup) -> str:
        for selector in ("h1",):
            node = soup.select_one(selector)
            if node:
                txt = node.get_text(" ", strip=True)
                if txt:
                    return txt
        og = self._meta(soup, prop="og:title")
        if og:
            return og
        if soup.title:
            return soup.title.get_text(strip=True)
        return ""

    def _author(self, soup: BeautifulSoup) -> str:
        for candidate in (
            self._meta(soup, name="author"),
            self._meta(soup, prop="article:author"),
        ):
            if candidate:
                return candidate
        for selector in (".byline", ".author", '[itemprop="author"]'):
            node = soup.select_one(selector)
            if node:
                return node.get_text(" ", strip=True)
        return ""

    def _publish_date(self, soup: BeautifulSoup) -> str:
        for prop in ("article:published_time", "og:published_time"):
            v = self._meta(soup, prop=prop)
            if v:
                return v
        for name in ("date", "pubdate"):
            v = self._meta(soup, name=name)
            if v:
                return v
        time_tag = soup.find("time", attrs={"datetime": True})
        if time_tag is not None:
            return str(time_tag["datetime"]).strip()
        return ""

    def _body(self, soup: BeautifulSoup) -> tuple[str, str]:
        for selector in ("article", "main"):
            node = soup.select_one(selector)
            if node is not None:
                self._strip_nav(node)
                txt = node.get_text("\n", strip=True)
                return _WS_RE.sub(" ", txt).strip(), str(node)
        if soup.body is not None:
            self._strip_nav(soup.body)
            txt = soup.body.get_text("\n", strip=True)
            return _WS_RE.sub(" ", txt).strip(), str(soup.body)
        return "", ""

    @staticmethod
    def _strip_nav(node) -> None:  # type: ignore[no-untyped-def]
        for tag_name in _DROP_NAV_TAGS:
            for n in node.find_all(tag_name):
                n.decompose()
        for tag_name in ("script", "style", "noscript", "svg", "iframe", "form"):
            for n in node.find_all(tag_name):
                n.decompose()

    # ---- public ----

    def extract(self, html: str, *, url: str) -> tuple[Article, SourceMetadata]:
        soup = BeautifulSoup(html, "lxml")
        title = self._title(soup)
        author = self._author(soup)
        publish_date = self._publish_date(soup)
        body_text, body_html = self._body(soup)

        html_tag = soup.find("html")
        lang = ""
        if html_tag is not None:
            lang = html_tag.get("lang", "") or html_tag.get("xml:lang", "")

        article = Article(
            title=title,
            author=author,
            publish_date=publish_date,
            body_text=body_text,
            body_html=body_html,
            lang=lang.strip(),
            url=url,
            source_domain=domain_of(url),
        )
        meta = SourceMetadata(
            url=url,
            source_domain=domain_of(url),
            fetch_time=now_utc(),
            fetch_status=200,
            fetcher="parsed_html",
            title=title,
            author=author,
            publish_date=publish_date,
            content_length=len(body_text),
            content_hash=content_hash(body_text),
            fetched_with_user_permission=False,  # caller sets True for live fetches
        )
        return article, meta
