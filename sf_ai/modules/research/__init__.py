"""sf_ai.modules.research — extract + summarize + cite (Phase 7).

Rule-based summarization. No LLM. No external API.
"""

from sf_ai.modules.research.citation_builder import Citation, CitationBuilder
from sf_ai.modules.research.module import ResearchModule, ResearchRequest, ResearchResult
from sf_ai.modules.research.response_organizer import OrganizedResponse, ResponseOrganizer
from sf_ai.modules.research.summarizer import RuleBasedSummarizer, Summary

__all__ = [
    "Citation",
    "CitationBuilder",
    "OrganizedResponse",
    "ResearchModule",
    "ResearchRequest",
    "ResearchResult",
    "ResponseOrganizer",
    "RuleBasedSummarizer",
    "Summary",
]
