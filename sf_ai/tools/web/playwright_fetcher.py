"""Playwright fetcher — stub.

Playwright is not wired into Phase 7. It is reserved for sites that need
JS rendering. When the user wants it:

    pip install playwright
    playwright install chromium

Then implement `PlaywrightFetcher.fetch(url)` here and route the
CrawlerBase to use it via the `fetcher=` injection.

Refusing to ship a half-baked browser automation in Phase 7. JS rendering
opens a much larger attack surface and needs a dedicated review pass.
"""

from __future__ import annotations


class PlaywrightFetcher:
    def __init__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        raise NotImplementedError(
            "PlaywrightFetcher is not implemented in Phase 7. "
            "Install playwright and add a real implementation when needed."
        )
