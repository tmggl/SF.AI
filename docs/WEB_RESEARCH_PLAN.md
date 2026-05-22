# WEB_RESEARCH_PLAN.md

## SF.AI — Web Research Plan (Phase 7)

> **القاعدة:** في Phase 7 لا يوجد محرك بحث خارجي ولا LLM. المستخدم يعطي روابط، SF.AI يجلبها ضمن سياسة صارمة ويُلخّصها بقواعد محلية.

---

## الفلسفة

1. **الويب أداة استرجاع، ليست خلفية تدريب.** المعرفة المتخصصة تُسترجَع من صفحات معروفة، ولا تُحفر في أوزان النموذج.
2. **كل صفحة لها مصدر.** كل سجل ناتج يحمل `SourceMetadata` مع url + domain + fetch_time + status + hash.
3. **لا zalim.** لا parallelism، لا ضغط، rate-limit صارم، robots.txt إلزامي.
4. **توليد التلخيص rule-based.** لا نموذج تلخيص جاهز، لا OpenAI/Claude، لا LLM داخلي قبل Phase 6+ ينضج.
5. **استشهاد منمَّق.** كل جملة في الـ summary لها [n] يشير إلى References block.

---

## التدفق الكامل

```
user: "لخّص لي هذين المقالين عن X: <URL1> <URL2>"
   │
   ▼ Orchestrator → domain=research (or web)
   │
   ▼ Planner: extracts URLs from text (no search API)
   │
   ▼ For each URL:
   │   • RobotsPolicy.check(url) — must allow
   │   • RateLimiter.wait_for(url) — per-domain
   │   • CrawlerBase.fetch(url)    — single GET, User-Agent visible
   │   • ArticleExtractor.extract — title / author / date / body
   │   • SourceMetadata.created   — url, domain, fetch_time, status, hash
   │
   ▼ RuleBasedSummarizer.summarize_many(articles)
   │   • sentence split (AR + EN aware)
   │   • token-frequency scoring (skip stopwords)
   │   • top-K with Jaccard/SequenceMatcher dedup
   │   • re-order by article position
   │
   ▼ CitationBuilder.build(summary, sources)
   │   • numbered references, deterministic order
   │
   ▼ ResponseOrganizer.organize(cited)
   │   • bullet list + references block + disclaimer
   │
   ▼ orchestrator response
```

---

## مكونات `sf_ai/tools/web/`

| ملف | المسؤولية |
|-----|-----------|
| `source_metadata.py` | `SourceMetadata` dataclass + `domain_of` + `content_hash` + `now_utc` |
| `robots_policy.py` | `RobotsPolicy.check(url)` يرجع `(allowed, reason)`. cache 24h |
| `rate_limiter.py` | `RateLimiter.wait_for(url)` per-domain، sequential |
| `crawler_base.py` | `CrawlerBase.fetch(url)` يجمعهم. يرفض بدون `permission_granted=True` |
| `html_extractor.py` | تنظيف HTML عام (scripts/style/svg out) |
| `article_extractor.py` | عنوان/كاتب/تاريخ/body بعد heuristics |
| `playwright_fetcher.py` | **stub** — يرفع NotImplementedError |
| `scrapy_pipeline.py` | **stub** — يرفع NotImplementedError |
| `mo3jam_importer.py` | Phase 3.5 (موجود سابقًا، يستخدم نفس البنية) |

---

## مكونات `sf_ai/modules/web/`

| ملف | المسؤولية |
|-----|-----------|
| `web_search_planner.py` | يستخرج URLs من نص المستخدم. لا search API |
| `web_result_ranker.py` | rule-based: title overlap + recency + length + domain dedup |
| `web_response_builder.py` | block منظَّم لكل مقال مع snippet + مصدر |
| `module.py` | `WebModule.handle(WebRequest)` → `WebResult` |
| `manifest.yaml` | metadata domain=web |

---

## مكونات `sf_ai/modules/research/`

| ملف | المسؤولية |
|-----|-----------|
| `summarizer.py` | `RuleBasedSummarizer.summarize` + `summarize_many` |
| `citation_builder.py` | `CitationBuilder.build(summary, sources)` → `CitedText` |
| `response_organizer.py` | تنسيق نهائي بـ headline + bullets + references |
| `module.py` | `ResearchModule.handle(ResearchRequest)` → `ResearchResult` |
| `manifest.yaml` | metadata domain=research |

---

## سياسة الجلب (مختصرة — التفاصيل في WEB_CRAWLING_POLICY.md)

- **User-Agent ظاهر:** `SF.AI Research Crawler - permission-gated`
- **rate-limit افتراضي:** 2.0 ثانية بين كل طلبين على نفس الـ domain
- **robots.txt:** إلزامي. أي خطأ في جلبه → معاملته كـ disallow.
- **permission_granted:** يجب أن يكون True عند إنشاء CrawlerBase. الـ Orchestrator لا يمرر crawler إلى الـ module افتراضيًا.
- **لا parallelism.** لا threads، لا async.
- **لا playwright/scrapy.** stubs فقط.

---

## كيف يستخدم الـ Orchestrator هذه المجالات

في Phase 7 تبقى حالة `web` و `research` في الـ registry **skeleton_only**. الكود جاهز وقابل للاختبار، لكن الـ Orchestrator يمر عبر Composer الذي يرد:
> "هذا المجال محجوز ولم يُفعَّل بعد."

لتفعيلها عمليًا، الخطوات (لاحقًا، بعد قرار صريح من المستخدم):

1. تغيير `status: skeleton_only` → `status: active` في `default_registry.yaml` للمجالين.
2. تسجيل `WebModule` و `ResearchModule` في `Orchestrator.modules`.
3. تكوين `CrawlerBase(permission_granted=True)` عند الانطلاق إذا أراد المستخدم crawl حي.
4. إعادة تشغيل الاختبارات الكاملة + سيناريو يدوي بـ 1-2 URL.

هذا قرار **منفصل** عن Phase 7 ويستحق "Phase 7.5" لو فُعّل لاحقًا.

---

## مثال استدعاء برمجي

### Offline (لا شبكة)
```python
from sf_ai.modules.research import ResearchModule, ResearchRequest

mod = ResearchModule()
result = mod.handle(
    ResearchRequest(
        html_sources=[
            ("https://example.org/a", open("samples/a.html").read()),
            ("https://example.org/b", open("samples/b.html").read()),
        ],
        max_sentences=4,
    )
)
print(result.response_text)
```

### Online (يحتاج إذنًا صريحًا من المستخدم)
```python
from sf_ai.tools.web import CrawlerBase
from sf_ai.modules.research import ResearchModule, ResearchRequest

crawler = CrawlerBase(permission_granted=True)
mod = ResearchModule(crawler=crawler)
result = mod.handle(
    ResearchRequest(
        url_sources=("https://example.org/article-1",),
    )
)
print(result.response_text)
```

---

## الحدود الواضحة لـ Phase 7

- ✅ بنية الـ crawler + extractor + summarizer + citation + organizer.
- ✅ tests على offline fixtures.
- ✅ rule-based summarization تعمل على نصوص عربية وإنجليزية.
- ❌ لا crawling حي تلقائيًا.
- ❌ لا تفعيل المجالين في الـ Orchestrator بعد.
- ❌ لا playwright/scrapy.
- ❌ لا search API.
- ❌ لا LLM-based summarization (لا في Phase 7 ولا قبل تأكد جودة Phase 6).
