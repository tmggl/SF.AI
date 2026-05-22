"""Per-domain rate limiter. Sequential by design — no parallelism."""

from __future__ import annotations

import time
from threading import Lock

from sf_ai.tools.web.source_metadata import domain_of


class RateLimiter:
    def __init__(
        self,
        default_seconds: float = 2.0,
        per_domain: dict[str, float] | None = None,
        clock=time.monotonic,                 # type: ignore[no-untyped-def]
        sleep=time.sleep,                     # type: ignore[no-untyped-def]
    ) -> None:
        if default_seconds < 0:
            raise ValueError("default_seconds must be >= 0")
        self.default_seconds = default_seconds
        self._per_domain = dict(per_domain or {})
        self._last_at: dict[str, float] = {}
        self._lock = Lock()
        self._clock = clock
        self._sleep = sleep

    def configure(self, domain: str, seconds: float) -> None:
        with self._lock:
            self._per_domain[domain.lower()] = float(seconds)

    def wait_for(self, url: str) -> float:
        """Block until the next allowed fetch time for `url`. Returns slept seconds."""
        domain = domain_of(url)
        per_domain = self._per_domain.get(domain, self.default_seconds)
        with self._lock:
            now = self._clock()
            last = self._last_at.get(domain, 0.0)
            elapsed = now - last
            wait = max(0.0, per_domain - elapsed)
            self._last_at[domain] = now + wait
        if wait > 0:
            self._sleep(wait)
        return wait

    def reset(self, domain: str | None = None) -> None:
        with self._lock:
            if domain is None:
                self._last_at.clear()
            else:
                self._last_at.pop(domain.lower(), None)
