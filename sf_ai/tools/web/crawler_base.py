"""CrawlerBase — composes RobotsPolicy + RateLimiter + fetcher.

This is the only place in SF.AI that performs outbound HTTP for research.
Every fetch is gated by:
1. `permission_granted=True` on the crawler (set by caller).
2. robots.txt allow check.
3. Per-domain rate limit.

No parallelism. No background fetches. Each call to `fetch()` is one HTTP
GET, synchronous, with a clear User-Agent.

The implementation here uses `urllib`. Heavier fetchers (Playwright for JS,
Scrapy for scale) are stubs in `playwright_fetcher.py` / `scrapy_pipeline.py`
and require a separate phase to wire in.
"""

from __future__ import annotations

import urllib.request
from dataclasses import dataclass

from sf_ai.tools.web.rate_limiter import RateLimiter
from sf_ai.tools.web.robots_policy import (
    DEFAULT_USER_AGENT,
    RobotsPolicy,
)
from sf_ai.tools.web.source_metadata import SourceMetadata, content_hash, domain_of, now_utc


class CrawlerPermissionError(RuntimeError):
    """Raised when fetch() is called without explicit user permission."""


class CrawlerRobotsError(RuntimeError):
    """Raised when robots.txt disallows the URL."""


@dataclass(frozen=True)
class FetchResult:
    url: str
    status: int
    body: str
    metadata: SourceMetadata


class CrawlerBase:
    def __init__(
        self,
        *,
        user_agent: str = DEFAULT_USER_AGENT,
        permission_granted: bool = False,
        timeout: float = 20.0,
        robots: RobotsPolicy | None = None,
        rate_limiter: RateLimiter | None = None,
        fetcher=None,                                # type: ignore[no-untyped-def]
    ) -> None:
        self.user_agent = user_agent
        self.permission_granted = bool(permission_granted)
        self.timeout = timeout
        self.robots = robots or RobotsPolicy(user_agent=user_agent)
        self.rate_limiter = rate_limiter or RateLimiter(default_seconds=2.0)
        self._fetcher = fetcher  # for tests; signature: fetcher(url, ua, timeout) -> (status, body)

    # ----- internals -----

    def _do_get(self, url: str) -> tuple[int, str]:
        if self._fetcher is not None:
            return self._fetcher(url, self.user_agent, self.timeout)
        req = urllib.request.Request(
            url,
            headers={"User-Agent": self.user_agent, "Accept-Language": "ar,en;q=0.9"},
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:  # nosec: B310
            raw = resp.read()
            charset = resp.headers.get_content_charset() or "utf-8"
            status = getattr(resp, "status", 200)
        return int(status), raw.decode(charset, errors="replace")

    # ----- public -----

    def fetch(self, url: str) -> FetchResult:
        if not self.permission_granted:
            raise CrawlerPermissionError(
                "SF.AI crawler refuses to fetch without explicit user permission. "
                "Construct with permission_granted=True after confirming the user has "
                "obtained permission from the source."
            )
        allowed, reason = self.robots.check(url)
        if not allowed:
            raise CrawlerRobotsError(f"{url} blocked: {reason}")

        self.rate_limiter.wait_for(url)
        status, body = self._do_get(url)

        meta = SourceMetadata(
            url=url,
            source_domain=domain_of(url),
            fetch_time=now_utc(),
            fetch_status=status,
            fetcher="urllib",
            content_length=len(body),
            content_hash=content_hash(body),
            fetched_with_user_permission=True,
            notes=(reason,),
        )
        return FetchResult(url=url, status=status, body=body, metadata=meta)
