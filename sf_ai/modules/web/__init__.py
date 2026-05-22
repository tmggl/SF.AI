"""sf_ai.modules.web — fetch + rank + structured response (Phase 7).

No search-engine API. Planner only handles user-provided URLs in Phase 7.
"""

from sf_ai.modules.web.module import WebModule, WebRequest, WebResult
from sf_ai.modules.web.web_response_builder import WebResponseBuilder
from sf_ai.modules.web.web_result_ranker import WebResultRanker
from sf_ai.modules.web.web_search_planner import WebSearchPlan, WebSearchPlanner

__all__ = [
    "WebModule",
    "WebRequest",
    "WebResponseBuilder",
    "WebResult",
    "WebResultRanker",
    "WebSearchPlan",
    "WebSearchPlanner",
]
