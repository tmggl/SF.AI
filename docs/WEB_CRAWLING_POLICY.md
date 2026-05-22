# WEB_CRAWLING_POLICY.md

## SF.AI — Web Crawling Policy

هذه السياسة تنطبق على **كل** access ويب يقوم به SF.AI، سواء عبر `CrawlerBase` العامة، أو الـ importers الخاصة (مثل Mo3jam في Phase 3.5).

---

## القواعد الإلزامية

| القاعدة | التفاصيل |
|---------|----------|
| **User-Agent ظاهر** | `SF.AI Research Crawler - permission-gated` أو مشتقاتها. لا تخفّي. |
| **robots.txt إلزامي** | كل URL يُفحص قبل الـ GET. خطأ في جلب robots = معاملة كـ disallow. |
| **rate-limit صارم** | 2.0 ثانية افتراضيًا بين طلبين على نفس الـ domain. قابل للضبط. |
| **لا parallelism** | تتابع متسلسل فقط. لا threads، لا async، لا concurrent requests. |
| **permission_granted** | `CrawlerBase(permission_granted=True)` إلزامي قبل أول fetch. بدون ذلك يرفع `CrawlerPermissionError`. |
| **توثيق المصدر** | كل fetch ينتج `SourceMetadata` يحفظ url, domain, fetch_time, status, hash. |
| **لا search APIs** | Phase 7 لا يستخدم Google/Bing/أي search API. روابط من المستخدم فقط. |
| **لا playwright/scrapy** | stubs فقط في Phase 7. تفعيل أي منهما = phase منفصل. |
| **resume** | للـ importers (Mo3jam): URLs الموجودة سابقًا تُتجاوز. |
| **failed URLs** | تُحفظ في report خاص. |

---

## ما لا يفعله SF.AI

- ❌ **لا fetch بدون إذن مكتوب أو مؤكَّد للمصدر.** Mo3jam مثال: المستخدم تواصل هاتفيًا. أي مصدر آخر يحتاج إذنًا مماثلًا.
- ❌ **لا تجاوز robots.txt.** حتى لو "كنا متأكدين من الإذن."
- ❌ **لا يجلب صفحة بدون تسجيل metadata.** كل بيانات الـ corpus مُتتَبّع مصدرها.
- ❌ **لا يلوّن نفسه بـ User-Agent متصفح حقيقي** لتجاوز قيود.
- ❌ **لا يحاول تجاوز CAPTCHA، login walls، أو paywalls.**
- ❌ **لا يحفظ ملفات وسائط** (صور، فيديو، مرفقات) إلا في phase مستقل بإذن.
- ❌ **لا يستخدم synthetic data مولّدة من LLM خارجي** كبديل عن fetching حقيقي.

---

## السياسة العامة عبر السنوات

عند نمو SF.AI:

1. **مصادر جديدة → سياسة جديدة.** كل مصدر جديد يحتاج وثيقة `SOURCE_DISCOVERY_*.md` مثل Mo3jam.
2. **تغيير الـ User-Agent** يحتاج تحديث هذه الوثيقة + اختبار.
3. **زيادة الـ parallelism** يحتاج Phase خاص + مراجعة.
4. **الانتقال إلى Playwright** = إعادة تقييم سطح الهجوم (JS execution).
5. **استخدام search API لاحقًا** = phase مستقل بإذن صريح من المستخدم.

---

## التطبيق التقني

### في الكود

```python
from sf_ai.tools.web import CrawlerBase

# لن يعمل — يرفع CrawlerPermissionError
crawler = CrawlerBase()
crawler.fetch("https://example.org")  # ❌

# يعمل — لكن يحترم robots + rate-limit
crawler = CrawlerBase(permission_granted=True)
result = crawler.fetch("https://example.org")  # ✅
print(result.metadata)
```

### في الـ Orchestrator

WebModule و ResearchModule يأخذان crawler عبر الـ constructor:

```python
from sf_ai.modules.web import WebModule
from sf_ai.tools.web import CrawlerBase

# Offline:
mod = WebModule()  # crawler=None → روابط المستخدم تُحفظ كـ "no_crawler_configured"

# Online (Phase 7.5 إن فُعّل):
crawler = CrawlerBase(permission_granted=True)
mod = WebModule(crawler=crawler)
```

افتراضيًا في `get_default_orchestrator()` لا crawler مسجَّل. التفعيل قرار صريح يحتاج phase منفصل أو env flag.

---

## مراجعة دورية

كل مرة نضيف مصدرًا جديدًا أو يتغير سلوك مصدر موجود:

1. أعد قراءة هذه الوثيقة.
2. أعد فحص robots.txt للمصدر.
3. اختبر rate-limit على عينة صغيرة.
4. سجّل أي مشكلة في `data/corpus/*/reports/*.md`.
5. حدّث `SOURCE_DISCOVERY_*.md` للمصدر.

---

## الشفافية كمسؤولية

SF.AI يجلب البيانات **علنًا** بـ User-Agent يقول من نحن. هذا فلسفة ليس إكراه قانوني فقط:

- إن استطعت أن تشرح كل request للمالك، فأنت تفعل الصواب.
- إن احتجت إخفاء نفسك لتفعل ما تفعل، فأنت تفعل خطأ.

نختار الشفافية حتى لو كلّفت أكثر.
