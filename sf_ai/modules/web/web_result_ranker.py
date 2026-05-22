"""WebResultRanker — order fetched articles by relevance + freshness.

Score per article (no learned model — all rule-based):
- recency: more recent publish_date → small positive bonus
- title overlap with the user query: token overlap
- body length: very short bodies are demoted (likely error pages)
- duplicate domain: second hit from the same domain is penalized
"""

from __future__ import annotations

from dataclasses import dataclass

from sf_ai.core.semantic.lexical_similarity import simple_tokenize
from sf_ai.tools.web.article_extractor import Article


@dataclass(frozen=True)
class RankedArticle:
    article: Article
    score: float
    breakdown: dict[str, float]


class WebResultRanker:
    def __init__(
        self,
        *,
        recency_weight: float = 0.2,
        title_weight: float = 1.0,
        length_weight: float = 0.2,
        same_domain_penalty: float = 0.5,
        min_body_chars: int = 200,
    ) -> None:
        self.recency_weight = recency_weight
        self.title_weight = title_weight
        self.length_weight = length_weight
        self.same_domain_penalty = same_domain_penalty
        self.min_body_chars = min_body_chars

    def rank(self, articles: list[Article], query: str) -> list[RankedArticle]:
        if not articles:
            return []
        q_tokens = set(simple_tokenize(query)) if query else set()
        seen_domains: dict[str, int] = {}
        ranked: list[RankedArticle] = []
        for art in articles:
            title_score = 0.0
            if q_tokens:
                overlap = len(q_tokens & set(simple_tokenize(art.title)))
                title_score = self.title_weight * (overlap / max(len(q_tokens), 1))
            length_score = self.length_weight * (
                1.0 if len(art.body_text) >= self.min_body_chars else -1.0
            )
            recency_score = self.recency_weight * (1.0 if art.publish_date else 0.0)
            domain_penalty = self.same_domain_penalty * seen_domains.get(art.source_domain, 0)
            seen_domains[art.source_domain] = seen_domains.get(art.source_domain, 0) + 1
            score = title_score + length_score + recency_score - domain_penalty
            ranked.append(
                RankedArticle(
                    article=art,
                    score=score,
                    breakdown={
                        "title": title_score,
                        "length": length_score,
                        "recency": recency_score,
                        "domain_penalty": -domain_penalty,
                    },
                )
            )
        ranked.sort(key=lambda r: r.score, reverse=True)
        return ranked
