"""ResearchModule — extract → summarize → cite → organize.

Phase 7 contract:

    request: ResearchRequest(html_sources=[...], url_sources=[...])
    result:  ResearchResult(response_text, summary, citations, organized)

`html_sources` is the offline path: callers pass already-fetched HTML +
the URL it came from. The module never reaches out by itself.

`url_sources` is the online path: when the caller has a configured
`crawler` (with permission_granted=True), the module uses it. Without a
crawler, url_sources are recorded as "not fetched" notes — Phase 7 keeps
this conservative on purpose.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sf_ai.modules.research.citation_builder import Citation, CitationBuilder, CitedText
from sf_ai.modules.research.response_organizer import OrganizedResponse, ResponseOrganizer
from sf_ai.modules.research.summarizer import RuleBasedSummarizer, Summary
from sf_ai.tools.web.article_extractor import Article, ArticleExtractor
from sf_ai.tools.web.crawler_base import (
    CrawlerBase,
    CrawlerPermissionError,
    CrawlerRobotsError,
)
from sf_ai.tools.web.source_metadata import SourceMetadata


@dataclass(frozen=True)
class ResearchRequest:
    html_sources: tuple[tuple[str, str], ...] = ()   # (url, html_text)
    url_sources: tuple[str, ...] = ()
    max_sentences: int = 5
    note: str = ""


@dataclass
class ResearchResult:
    response_text: str
    organized: OrganizedResponse
    cited: CitedText
    summary: Summary
    articles: list[Article] = field(default_factory=list)
    sources: dict[str, SourceMetadata] = field(default_factory=dict)
    skipped: list[tuple[str, str]] = field(default_factory=list)   # (url, reason)


class ResearchModule:
    domain = "research"

    def __init__(
        self,
        *,
        extractor: ArticleExtractor | None = None,
        summarizer: RuleBasedSummarizer | None = None,
        citation_builder: CitationBuilder | None = None,
        organizer: ResponseOrganizer | None = None,
        crawler: CrawlerBase | None = None,
    ) -> None:
        self.extractor = extractor or ArticleExtractor()
        self.summarizer = summarizer or RuleBasedSummarizer()
        self.citation_builder = citation_builder or CitationBuilder()
        self.organizer = organizer or ResponseOrganizer()
        self.crawler = crawler

    def handle(self, request: ResearchRequest) -> ResearchResult:
        articles: list[Article] = []
        sources: dict[str, SourceMetadata] = {}
        skipped: list[tuple[str, str]] = []

        # 1. Offline path: caller supplied HTML directly.
        for url, html in request.html_sources:
            try:
                art, meta = self.extractor.extract(html, url=url)
            except Exception as e:
                skipped.append((url, f"extract_error:{type(e).__name__}"))
                continue
            if not art.body_text.strip():
                skipped.append((url, "empty_body"))
                continue
            articles.append(art)
            sources[url] = meta

        # 2. Online path: only if a crawler is wired AND permissioned.
        if request.url_sources:
            if self.crawler is None:
                for url in request.url_sources:
                    skipped.append((url, "no_crawler_configured"))
            else:
                for url in request.url_sources:
                    try:
                        fetched = self.crawler.fetch(url)
                    except CrawlerPermissionError:
                        skipped.append((url, "crawler_permission_denied"))
                        continue
                    except CrawlerRobotsError as e:
                        skipped.append((url, str(e)))
                        continue
                    except Exception as e:
                        skipped.append((url, f"fetch_error:{type(e).__name__}"))
                        continue
                    try:
                        art, meta = self.extractor.extract(fetched.body, url=url)
                    except Exception as e:
                        skipped.append((url, f"extract_error:{type(e).__name__}"))
                        continue
                    if not art.body_text.strip():
                        skipped.append((url, "empty_body"))
                        continue
                    # Prefer the live SourceMetadata (status + hash) over the parser's.
                    sources[url] = SourceMetadata(
                        url=url,
                        source_domain=fetched.metadata.source_domain,
                        fetch_time=fetched.metadata.fetch_time,
                        fetch_status=fetched.metadata.fetch_status,
                        fetcher=fetched.metadata.fetcher,
                        title=art.title,
                        author=art.author,
                        publish_date=art.publish_date,
                        content_length=fetched.metadata.content_length,
                        content_hash=fetched.metadata.content_hash,
                        fetched_with_user_permission=True,
                        notes=fetched.metadata.notes,
                    )
                    articles.append(art)

        # 3. Summarize across whatever articles we obtained.
        summary = self.summarizer.summarize_many(
            [(a.body_text, a.url) for a in articles]
        )

        # 4. Cite + organize.
        cited = self.citation_builder.build(summary, sources)
        organized = self.organizer.organize(cited)

        return ResearchResult(
            response_text=organized.text,
            organized=organized,
            cited=cited,
            summary=summary,
            articles=articles,
            sources=sources,
            skipped=skipped,
        )
