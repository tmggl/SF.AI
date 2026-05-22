"""sf_ai.tools.web — controlled web access for SF.AI.

Phase 3.5 shipped the Mo3jam Saudi-dialect importer. Phase 7 generalizes
the building blocks so any future research/web module can reuse them.

All web access here:
- requires `permission_granted=True` on the crawler
- respects robots.txt (RobotsPolicy)
- rate-limits per-domain (RateLimiter)
- emits SourceMetadata for every fetch
- writes attribution into downstream artifacts
"""

from sf_ai.tools.web.article_extractor import Article, ArticleExtractor
from sf_ai.tools.web.crawler_base import (
    CrawlerBase,
    CrawlerPermissionError,
    CrawlerRobotsError,
    FetchResult,
)
from sf_ai.tools.web.html_extractor import ExtractedPage, HTMLExtractor
from sf_ai.tools.web.mo3jam_importer import (
    Mo3jamImporter,
    Mo3jamImportConfig,
    Mo3jamImportReport,
    Mo3jamTerm,
)
from sf_ai.tools.web.rate_limiter import RateLimiter
from sf_ai.tools.web.robots_policy import RobotsPolicy
from sf_ai.tools.web.source_metadata import (
    SourceMetadata,
    content_hash,
    domain_of,
    now_utc,
)

__all__ = [
    "Article",
    "ArticleExtractor",
    "CrawlerBase",
    "CrawlerPermissionError",
    "CrawlerRobotsError",
    "ExtractedPage",
    "FetchResult",
    "HTMLExtractor",
    "Mo3jamImportConfig",
    "Mo3jamImportReport",
    "Mo3jamImporter",
    "Mo3jamTerm",
    "RateLimiter",
    "RobotsPolicy",
    "SourceMetadata",
    "content_hash",
    "domain_of",
    "now_utc",
]
