"""WebSearchPlanner — turn a user request into a fetch plan.

Phase 7 does NOT call any search-engine API. The planner:
1. Extracts any URLs the user explicitly typed.
2. (Future) consults a user-curated allowlist of sources for a given topic.

Without an explicit URL, the planner returns an empty plan so the module
responds with "no sources provided" rather than guessing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


_URL_RE = re.compile(
    r"\bhttps?://[\w\-]+(?:\.[\w\-]+)+(?:/[^\s\"')]*)?",
    re.UNICODE,
)


@dataclass(frozen=True)
class WebSearchPlan:
    urls: tuple[str, ...]
    rationale: str
    used_search_api: bool = False


class WebSearchPlanner:
    def plan(self, user_text: str) -> WebSearchPlan:
        urls = tuple(_URL_RE.findall(user_text or ""))
        if urls:
            return WebSearchPlan(
                urls=urls,
                rationale=f"extracted {len(urls)} URL(s) directly from user text",
                used_search_api=False,
            )
        return WebSearchPlan(
            urls=(),
            rationale=(
                "no URL found in request; Phase 7 does not use external "
                "search APIs. Provide a URL or wait for Phase 8 RAG."
            ),
            used_search_api=False,
        )
