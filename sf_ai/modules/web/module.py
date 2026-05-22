"""WebModule — fetch + rank + structured response (Phase 7).

Sister to ResearchModule: web focuses on "show me the source pages" while
research focuses on "summarize across sources". They share the same
ArticleExtractor + CrawlerBase but produce different responses.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sf_ai.modules.web.web_response_builder import BuiltWebReply, WebResponseBuilder
from sf_ai.modules.web.web_result_ranker import RankedArticle, WebResultRanker
from sf_ai.modules.web.web_search_planner import WebSearchPlan, WebSearchPlanner
from sf_ai.tools.web.article_extractor import Article, ArticleExtractor
from sf_ai.tools.web.crawler_base import (
    CrawlerBase,
    CrawlerPermissionError,
    CrawlerRobotsError,
)
from sf_ai.tools.web.source_metadata import SourceMetadata


@dataclass(frozen=True)
class WebRequest:
    query: str = ""
    html_sources: tuple[tuple[str, str], ...] = ()  # (url, html)
    url_sources: tuple[str, ...] = ()


@dataclass
class WebResult:
    response_text: str
    plan: WebSearchPlan
    ranked: list[RankedArticle] = field(default_factory=list)
    skipped: list[tuple[str, str]] = field(default_factory=list)
    sources: dict[str, SourceMetadata] = field(default_factory=dict)


class WebModule:
    domain = "web"

    def __init__(
        self,
        *,
        planner: WebSearchPlanner | None = None,
        extractor: ArticleExtractor | None = None,
        ranker: WebResultRanker | None = None,
        builder: WebResponseBuilder | None = None,
        crawler: CrawlerBase | None = None,
    ) -> None:
        self.planner = planner or WebSearchPlanner()
        self.extractor = extractor or ArticleExtractor()
        self.ranker = ranker or WebResultRanker()
        self.builder = builder or WebResponseBuilder()
        self.crawler = crawler

    def handle(self, request: WebRequest) -> WebResult:
        plan = self.planner.plan(request.query)
        # Combine planner-extracted URLs with caller-provided ones, dedup.
        all_urls = tuple(dict.fromkeys(plan.urls + request.url_sources))

        articles: list[Article] = []
        sources: dict[str, SourceMetadata] = {}
        skipped: list[tuple[str, str]] = []

        # Offline path.
        for url, html in request.html_sources:
            art, meta = self.extractor.extract(html, url=url)
            if not art.body_text.strip():
                skipped.append((url, "empty_body"))
                continue
            articles.append(art)
            sources[url] = meta

        # Online path.
        if all_urls:
            if self.crawler is None:
                for url in all_urls:
                    skipped.append((url, "no_crawler_configured"))
            else:
                for url in all_urls:
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
                    art, meta = self.extractor.extract(fetched.body, url=url)
                    if not art.body_text.strip():
                        skipped.append((url, "empty_body"))
                        continue
                    articles.append(art)
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

        ranked = self.ranker.rank(articles, query=request.query)
        reply: BuiltWebReply = self.builder.build(
            ranked, skipped=skipped, query=request.query
        )
        return WebResult(
            response_text=reply.text,
            plan=plan,
            ranked=ranked,
            skipped=skipped,
            sources=sources,
        )
