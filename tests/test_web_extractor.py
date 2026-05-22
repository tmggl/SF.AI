"""Phase 7 — ArticleExtractor + HTMLExtractor + SourceMetadata + Crawler/Robots/RateLimiter."""

from __future__ import annotations

from pathlib import Path

import pytest

from sf_ai.tools.web import (
    Article,
    ArticleExtractor,
    CrawlerBase,
    CrawlerPermissionError,
    CrawlerRobotsError,
    HTMLExtractor,
    RateLimiter,
    RobotsPolicy,
    SourceMetadata,
    content_hash,
    domain_of,
)


FIXTURES = Path(__file__).resolve().parent / "fixtures"


# ---------- HTMLExtractor ----------

def test_html_extractor_strips_scripts_and_keeps_text() -> None:
    html = "<html><body><p>Hello</p><script>alert(1)</script></body></html>"
    page = HTMLExtractor().extract(html)
    assert "Hello" in page.text
    assert "alert" not in page.text


def test_html_extractor_handles_empty() -> None:
    page = HTMLExtractor().extract("")
    assert page.text == ""
    assert page.char_count == 0


# ---------- ArticleExtractor ----------

def test_article_extractor_full_fixture() -> None:
    html = (FIXTURES / "article_sample.html").read_text(encoding="utf-8")
    art, meta = ArticleExtractor().extract(html, url="https://example.org/ai-sovereign")
    assert "الذكاء الاصطناعي السيادي" in art.title
    assert "SF.AI" in art.author
    assert art.publish_date == "2026-05-22T10:00:00Z"
    assert "السيادي" in art.body_text
    # Navigation/footer/aside must be stripped.
    assert "النشرة" not in art.body_text
    assert "اقرأ أيضًا" not in art.body_text
    assert "جميع الحقوق محفوظة" not in art.body_text
    assert art.source_domain == "example.org"
    assert art.lang == "ar"
    # Metadata is filled.
    assert meta.url == "https://example.org/ai-sovereign"
    assert meta.title == art.title
    assert meta.author == art.author
    assert meta.content_length > 0
    assert meta.content_hash


def test_article_extractor_missing_fields_returns_empties() -> None:
    html = "<html><body><div>plain text</div></body></html>"
    art, meta = ArticleExtractor().extract(html, url="https://x.test/")
    assert art.title == ""
    assert art.author == ""
    assert art.publish_date == ""
    assert art.source_domain == "x.test"
    assert "plain text" in art.body_text


# ---------- SourceMetadata helpers ----------

def test_domain_of() -> None:
    assert domain_of("https://Example.ORG/path") == "example.org"


def test_content_hash_stable() -> None:
    a = content_hash("hello")
    b = content_hash("hello")
    c = content_hash("hello!")
    assert a == b
    assert a != c
    assert len(a) == 32   # blake2b-16 hex


# ---------- RobotsPolicy ----------

def test_robots_policy_allows_when_robots_permits() -> None:
    def fake_fetcher(url: str) -> str:
        return "User-agent: *\nDisallow: /private\n"
    policy = RobotsPolicy(fetcher=fake_fetcher)
    allowed, reason = policy.check("https://example.org/public")
    assert allowed is True
    assert reason == "allowed_by_robots"


def test_robots_policy_disallows_specific_path() -> None:
    def fake_fetcher(url: str) -> str:
        return "User-agent: *\nDisallow: /private\n"
    policy = RobotsPolicy(fetcher=fake_fetcher)
    allowed, reason = policy.check("https://example.org/private/file")
    assert allowed is False
    assert "disallow" in reason


def test_robots_policy_unreachable_treated_as_disallow() -> None:
    def boom(url: str) -> str:
        raise RuntimeError("no network in test")
    policy = RobotsPolicy(fetcher=boom)
    allowed, reason = policy.check("https://example.org/x")
    assert allowed is False
    assert "unreachable" in reason


def test_robots_policy_caches_per_domain() -> None:
    calls = {"n": 0}

    def counting_fetcher(url: str) -> str:
        calls["n"] += 1
        return "User-agent: *\nDisallow:\n"
    policy = RobotsPolicy(fetcher=counting_fetcher)
    policy.check("https://example.org/a")
    policy.check("https://example.org/b")
    assert calls["n"] == 1


# ---------- RateLimiter ----------

def test_rate_limiter_first_call_does_not_wait() -> None:
    waits: list[float] = []
    rl = RateLimiter(default_seconds=2.0, sleep=lambda s: waits.append(s),
                     clock=lambda: 100.0)
    rl.wait_for("https://example.org/a")
    assert waits == []


def test_rate_limiter_second_call_waits_remainder() -> None:
    now = {"t": 100.0}
    waits: list[float] = []

    def sleep(s: float) -> None:
        waits.append(s)
        now["t"] += s
    rl = RateLimiter(default_seconds=2.0, sleep=sleep, clock=lambda: now["t"])
    rl.wait_for("https://example.org/a")
    now["t"] += 0.5   # 0.5s elapsed
    rl.wait_for("https://example.org/a")
    assert pytest.approx(waits[-1], rel=1e-3) == 1.5


def test_rate_limiter_per_domain_isolation() -> None:
    now = {"t": 100.0}
    waits: list[float] = []
    rl = RateLimiter(default_seconds=2.0,
                     sleep=lambda s: waits.append(s),
                     clock=lambda: now["t"])
    rl.wait_for("https://a.test/x")
    rl.wait_for("https://b.test/y")    # different domain → no wait
    assert waits == []


# ---------- CrawlerBase ----------

def test_crawler_refuses_without_permission() -> None:
    c = CrawlerBase()
    with pytest.raises(CrawlerPermissionError):
        c.fetch("https://example.org")


def test_crawler_blocks_disallowed_by_robots() -> None:
    def fake_robots(url: str) -> str:
        return "User-agent: *\nDisallow: /\n"
    robots = RobotsPolicy(fetcher=fake_robots)
    rl = RateLimiter(default_seconds=0.0)
    c = CrawlerBase(permission_granted=True, robots=robots, rate_limiter=rl,
                    fetcher=lambda url, ua, t: (200, "body"))
    with pytest.raises(CrawlerRobotsError):
        c.fetch("https://example.org/anything")


def test_crawler_returns_fetch_result_with_metadata() -> None:
    def fake_robots(url: str) -> str:
        return "User-agent: *\nDisallow:\n"
    robots = RobotsPolicy(fetcher=fake_robots)
    rl = RateLimiter(default_seconds=0.0)

    def fake_fetcher(url, ua, timeout):
        assert ua.startswith("SF.AI")
        return 200, "<html><body>ok</body></html>"
    c = CrawlerBase(permission_granted=True, robots=robots, rate_limiter=rl,
                    fetcher=fake_fetcher)
    result = c.fetch("https://example.org/page")
    assert result.status == 200
    assert "ok" in result.body
    assert isinstance(result.metadata, SourceMetadata)
    assert result.metadata.source_domain == "example.org"
    assert result.metadata.fetched_with_user_permission is True
    assert result.metadata.fetcher == "urllib"


# ---------- Sanity: stubs raise ----------

def test_playwright_stub_raises() -> None:
    from sf_ai.tools.web.playwright_fetcher import PlaywrightFetcher
    with pytest.raises(NotImplementedError):
        PlaywrightFetcher()


def test_scrapy_stub_raises() -> None:
    from sf_ai.tools.web.scrapy_pipeline import ScrapyPipeline
    with pytest.raises(NotImplementedError):
        ScrapyPipeline()
