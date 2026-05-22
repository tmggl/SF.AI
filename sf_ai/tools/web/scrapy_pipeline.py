"""Scrapy pipeline — stub.

Scrapy is reserved for larger crawls where backpressure, retries, and a
pipeline of extract/transform/load steps justify the dependency. Phase 7
needs neither. When you need it later:

    pip install scrapy

Then write a Scrapy `Spider` that respects the same robots / rate-limit
policy as CrawlerBase and emits `SourceMetadata`-shaped items.
"""

from __future__ import annotations


class ScrapyPipeline:
    def __init__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        raise NotImplementedError(
            "ScrapyPipeline is not implemented in Phase 7. "
            "Install scrapy and add a real implementation when needed."
        )
