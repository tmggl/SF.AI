"""RobotsPolicy — per-domain robots.txt cache and check.

`check(url)` returns `(allowed, reason)`. Failure to fetch robots.txt is
treated conservatively: **not allowed**. Cache TTL defaults to 24h.
"""

from __future__ import annotations

import time
import urllib.parse
import urllib.robotparser
from dataclasses import dataclass
from threading import Lock


DEFAULT_USER_AGENT = "SF.AI Research Crawler - permission-gated"
DEFAULT_CACHE_TTL = 24 * 60 * 60   # 24h


@dataclass
class _CacheEntry:
    parser: urllib.robotparser.RobotFileParser | None
    fetched_at: float
    fetch_ok: bool


class RobotsPolicy:
    def __init__(
        self,
        user_agent: str = DEFAULT_USER_AGENT,
        cache_ttl: int = DEFAULT_CACHE_TTL,
        fetcher=None,  # type: ignore[no-untyped-def]
    ) -> None:
        self.user_agent = user_agent
        self.cache_ttl = cache_ttl
        self._cache: dict[str, _CacheEntry] = {}
        self._lock = Lock()
        # Injectable fetcher for tests; signature: fetcher(robots_url) -> str
        self._fetcher = fetcher

    def _robots_url(self, url: str) -> tuple[str, str]:
        parsed = urllib.parse.urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"invalid url: {url!r}")
        scheme = parsed.scheme
        netloc = parsed.netloc
        return f"{scheme}://{netloc}/robots.txt", netloc.lower()

    def _load(self, robots_url: str) -> _CacheEntry:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        ok = True
        try:
            if self._fetcher is not None:
                text = self._fetcher(robots_url)
                rp.parse(text.splitlines())
            else:
                rp.read()
        except Exception:
            ok = False
            rp = None
        return _CacheEntry(parser=rp, fetched_at=time.time(), fetch_ok=ok)

    def _get(self, robots_url: str, key: str) -> _CacheEntry:
        with self._lock:
            entry = self._cache.get(key)
            if entry is not None and (time.time() - entry.fetched_at) < self.cache_ttl:
                return entry
            entry = self._load(robots_url)
            self._cache[key] = entry
            return entry

    def check(self, url: str) -> tuple[bool, str]:
        robots_url, key = self._robots_url(url)
        entry = self._get(robots_url, key)
        if not entry.fetch_ok or entry.parser is None:
            return False, "robots_unreachable_treated_as_disallow"
        try:
            allowed = entry.parser.can_fetch(self.user_agent, url)
        except Exception:
            return False, "robots_parse_error_treated_as_disallow"
        return (allowed, "allowed_by_robots" if allowed else "disallowed_by_robots")

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()
