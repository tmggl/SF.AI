"""Phase 7 — RuleBasedSummarizer + CitationBuilder + ResponseOrganizer + modules."""

from __future__ import annotations

from pathlib import Path

import pytest

from sf_ai.modules.research import (
    CitationBuilder,
    OrganizedResponse,
    ResearchModule,
    ResearchRequest,
    ResponseOrganizer,
    RuleBasedSummarizer,
    Summary,
)
from sf_ai.modules.research.summarizer import ScoredSentence, split_sentences
from sf_ai.modules.web import WebModule, WebRequest, WebSearchPlanner
from sf_ai.tools.web import ArticleExtractor


FIXTURES = Path(__file__).resolve().parent / "fixtures"


# ---------- split_sentences ----------

def test_split_sentences_handles_arabic_and_english() -> None:
    text = "هذه الجملة الأولى. وهذه الثانية! وثالثة؟\nسطر جديد here."
    parts = split_sentences(text)
    assert len(parts) >= 3


def test_split_sentences_drops_one_word_fragments() -> None:
    parts = split_sentences("hi.\nthis is a real sentence.\nworld")
    assert all(len(p.split()) >= 2 for p in parts)


# ---------- RuleBasedSummarizer (single article) ----------

def test_summarizer_returns_at_most_max_sentences() -> None:
    text = " ".join([f"الجملة رقم {i} عن الذكاء الاصطناعي." for i in range(20)])
    summ = RuleBasedSummarizer(max_sentences=3)
    result = summ.summarize(text, source_url="https://x.test/")
    assert len(result.sentences) <= 3
    assert all(isinstance(s, ScoredSentence) for s in result.sentences)


def test_summarizer_dedups_near_identical_sentences() -> None:
    text = (
        "الذكاء الاصطناعي السيادي يهم.\n"
        "الذكاء الاصطناعي السيادي يهم.\n"
        "الذكاء الاصطناعي السيادي يهم.\n"
        "نموذج صغير من الصفر هو نقطة البداية.\n"
        "التدريب بدون أوزان جاهزة قرار طويل المدى.\n"
    )
    summ = RuleBasedSummarizer(max_sentences=5, dedup_threshold=0.7)
    result = summ.summarize(text, source_url="https://x.test/")
    assert result.dedup_dropped >= 1
    texts = [s.text for s in result.sentences]
    # The duplicates should appear at most once.
    assert texts.count("الذكاء الاصطناعي السيادي يهم.") == 1


def test_summarizer_preserves_reading_order_for_kept_sentences() -> None:
    text = "الجملة الأولى عن أ.\nالجملة الثانية عن ب.\nالجملة الثالثة عن أ ب أ ب."
    summ = RuleBasedSummarizer(max_sentences=3, min_sentence_words=2)
    result = summ.summarize(text, source_url="u")
    indices = [s.index_in_article for s in result.sentences]
    assert indices == sorted(indices)


def test_summarizer_empty_input() -> None:
    summ = RuleBasedSummarizer()
    result = summ.summarize("")
    assert result.sentences == ()
    assert result.total_input_sentences == 0


# ---------- RuleBasedSummarizer (multi-article) ----------

def test_summarize_many_attributes_each_sentence() -> None:
    summ = RuleBasedSummarizer(max_sentences=4)
    items = [
        ("الذكاء الاصطناعي السيادي يبدأ من الصفر. لا أوزان جاهزة هنا.",
         "https://a.test/"),
        ("التلخيص rule-based في SF.AI. لا LLM في طبقة البحث.",
         "https://b.test/"),
    ]
    result = summ.summarize_many(items)
    urls = {s.source_url for s in result.sentences}
    assert urls.issubset({"https://a.test/", "https://b.test/"})
    assert sum(result.per_source_counts.values()) == len(result.sentences)


# ---------- CitationBuilder ----------

def test_citation_builder_numbers_sources_deterministically() -> None:
    sents = (
        ScoredSentence(text="a", score=1.0, source_url="u1", index_in_article=0),
        ScoredSentence(text="b", score=0.5, source_url="u2", index_in_article=0),
        ScoredSentence(text="c", score=0.4, source_url="u1", index_in_article=1),
    )
    cited = CitationBuilder().build(Summary(sentences=sents))
    assert "[1]" in cited.body
    assert "[2]" in cited.body
    assert len(cited.citations) == 2
    nums = [c.number for c in cited.citations]
    assert nums == [1, 2]
    urls = [c.source_url for c in cited.citations]
    assert urls == ["u1", "u2"]


def test_citation_builder_handles_empty() -> None:
    cited = CitationBuilder().build(Summary(sentences=()))
    assert cited.body == ""
    assert cited.citations == ()


def test_citation_references_block_formats_lines() -> None:
    sents = (ScoredSentence(text="x", score=1.0, source_url="https://u.test/",
                             index_in_article=0),)
    cited = CitationBuilder().build(Summary(sentences=sents))
    block = cited.references_block()
    assert "المصادر:" in block
    assert "https://u.test/" in block


# ---------- ResponseOrganizer ----------

def test_organizer_formats_bullets_and_includes_references() -> None:
    sents = (
        ScoredSentence(text="جملة مفيدة جدًا.", score=1.0,
                       source_url="https://x.test/", index_in_article=0),
    )
    cited = CitationBuilder().build(Summary(sentences=sents))
    out = ResponseOrganizer().organize(cited)
    assert isinstance(out, OrganizedResponse)
    assert out.bullet_count == 1
    assert out.citation_count == 1
    assert "ملخص" in out.text
    assert "المصادر:" in out.text


def test_organizer_handles_empty_summary() -> None:
    cited = CitationBuilder().build(Summary(sentences=()))
    out = ResponseOrganizer().organize(cited)
    assert out.bullet_count == 0
    assert "لم أجد محتوى" in out.text


# ---------- ResearchModule end-to-end ----------

def test_research_module_offline_pipeline() -> None:
    html = (FIXTURES / "article_sample.html").read_text(encoding="utf-8")
    mod = ResearchModule(summarizer=RuleBasedSummarizer(max_sentences=3))
    result = mod.handle(
        ResearchRequest(
            html_sources=(("https://example.org/sovereign", html),),
        )
    )
    assert result.articles
    assert "ملخص" in result.response_text
    assert "[1]" in result.response_text
    assert "example.org" in result.response_text or "example.org" in str(result.sources)
    assert result.sources["https://example.org/sovereign"].title


def test_research_module_url_without_crawler_records_skip() -> None:
    mod = ResearchModule()
    result = mod.handle(ResearchRequest(url_sources=("https://example.org",)))
    reasons = {r for _, r in result.skipped}
    assert "no_crawler_configured" in reasons
    assert result.articles == []


def test_research_module_skips_invalid_html() -> None:
    mod = ResearchModule()
    result = mod.handle(
        ResearchRequest(
            html_sources=(("https://example.org/empty", "<html></html>"),),
        )
    )
    assert ("https://example.org/empty", "empty_body") in result.skipped


# ---------- WebModule + Planner + Ranker + Builder ----------

def test_web_search_planner_extracts_urls() -> None:
    plan = WebSearchPlanner().plan("ابحث لي عن https://a.test و https://b.test/path")
    assert "https://a.test" in plan.urls
    assert any(u.startswith("https://b.test") for u in plan.urls)
    assert plan.used_search_api is False


def test_web_search_planner_no_urls_yields_empty_plan() -> None:
    plan = WebSearchPlanner().plan("ابحث لي عن الذكاء الاصطناعي")
    assert plan.urls == ()
    assert "Phase 8" in plan.rationale


def test_web_module_offline_returns_structured_reply() -> None:
    html = (FIXTURES / "article_sample.html").read_text(encoding="utf-8")
    mod = WebModule()
    result = mod.handle(
        WebRequest(
            query="الذكاء الاصطناعي السيادي",
            html_sources=(("https://example.org/sovereign", html),),
        )
    )
    assert "نتائج البحث" in result.response_text
    assert "example.org" in result.response_text
    assert result.sources["https://example.org/sovereign"].title


def test_web_module_no_urls_no_html_reports_no_crawler() -> None:
    mod = WebModule()
    result = mod.handle(WebRequest(query="ابحث عن شيء"))
    assert "Phase 7" in result.response_text
    assert result.ranked == []


def test_web_module_with_query_url_uses_crawler_path_without_crawler() -> None:
    mod = WebModule()
    result = mod.handle(WebRequest(query="ابحث في https://a.test/path"))
    reasons = {r for _, r in result.skipped}
    assert "no_crawler_configured" in reasons
