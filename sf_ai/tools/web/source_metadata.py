"""Source metadata — uniform record for any fetched URL.

Every byte SF.AI pulls from the web goes through one of these. Citations,
audit logs, and the research module all consume `SourceMetadata` so we
never lose track of where content came from.
"""

from __future__ import annotations

import hashlib
import urllib.parse
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class SourceMetadata:
    url: str
    source_domain: str
    fetch_time: str        # ISO 8601 UTC
    fetch_status: int      # HTTP status (-1 for "not yet fetched")
    fetcher: str           # "urllib" | "playwright" | "scrapy" | "test"
    title: str = ""
    author: str = ""
    publish_date: str = ""
    content_length: int = 0
    content_hash: str = ""
    fetched_with_user_permission: bool = False
    notes: tuple[str, ...] = field(default_factory=tuple)

    def describe(self) -> str:
        return (
            f"{self.title or '(no title)'} — {self.source_domain} — "
            f"{self.publish_date or self.fetch_time}"
        )


def domain_of(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    return parsed.netloc.lower()


def content_hash(body: bytes | str) -> str:
    if isinstance(body, str):
        body = body.encode("utf-8")
    return hashlib.blake2b(body, digest_size=16).hexdigest()


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()
