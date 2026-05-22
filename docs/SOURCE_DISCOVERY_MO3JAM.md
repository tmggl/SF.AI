# SOURCE_DISCOVERY_MO3JAM.md

## مصدر بيانات اللهجة السعودية لـ SF.AI (Phase 3.5)

> **مصدر اللهجات السعودية:**
> **معجم — اللهجة السعودية**
> **https://ar.mo3jam.com/dialect/Saudi**

---

## معلومات المصدر

- **اسم المصدر:** معجم — اللهجة السعودية
- **الرابط:** https://ar.mo3jam.com/dialect/Saudi
- **عدد المصطلحات المتوقع:** 3139 (مأخوذ من ترويسة الصفحة الرئيسية: "عدد المصطلحات: 3139 مصطلح")
- **حالة الإذن:** `allowed_with_user_confirmed_permission`
- **ملاحظة الإذن:** أكّد المستخدم أنه **تواصل معهم هاتفيًا** وأن المسؤولين عن الموقع **لا مانع لديهم** من استخدام البيانات داخل SF.AI، بشرط ذكر المصدر دائمًا.
- **شرط داخلي إلزامي:** يجب ذكر المصدر دائمًا عند:
  - تخزين البيانات في النظام.
  - استخدام البيانات في ردود المستخدم.
  - عرض المعنى أو الأمثلة.
  - أي ناتج يستند إلى هذه البيانات.

### صيغة النسبة المطلوبة

```
مصدر اللهجات السعودية:
معجم — اللهجة السعودية
https://ar.mo3jam.com/dialect/Saudi
```

---

## السياسة العملية للزحف

| العنصر | القيمة |
|--------|--------|
| User-Agent | `SF.AI Research Importer - permission confirmed by user` |
| Rate limit الافتراضي | **2.0 ثانية** بين كل طلبين |
| Parallelism | **لا parallel crawl** — تتابع متسلسل فقط |
| Resume | مدعوم: يتجاوز URLs المسجَّلة في الـ JSONL الحالي |
| robots.txt | يُفحص قبل أول طلب live |
| Failed URLs | تُحفظ في `data/corpus/dialects/saudi/reports/mo3jam_failed_urls.txt` |

### نتيجة فحص robots.txt (2026-05-22)

```
User-agent: *
Disallow: /home
Disallow: /profile
Disallow: /search
```

→ `/dialect/Saudi`, `/dialect/Saudi/all/{letter}`, `/term/{X}` كلها **مسموحة**.

---

## بنية المصدر (مُلاحظة من فحص واحد)

### صفحة اللهجة الرئيسية
`https://ar.mo3jam.com/dialect/Saudi`

تعرض ترويسة بعدد المصطلحات (3139) وفهرسة بالحروف.

### صفحات الحروف
نمط الرابط:
```
/dialect/Saudi/all/{LETTER}#{LETTER}
```

مثال:
- `/dialect/Saudi/all/أ#أ`
- `/dialect/Saudi/all/ب#ب`
- `/dialect/Saudi/all/ي#ي`

كل صفحة حرف تحتوي قائمة `<li><a href="/term/X#Saudi">X</a></li>` بدون pagination. ينتقل المستخدم بين الحروف عبر الفهرس العلوي.

### صفحات المصطلح
نمط الرابط:
```
/term/{TERM_TEXT}#Saudi
```

> **ملاحظة مهمة على الـ parser:** أثناء بناء هذه المرحلة، تم منع الـ WebFetch على صفحة مصطلح فردي بواسطة classifier السلامة في بيئة Claude Code (تحت Auto Mode). لم نُجبَر classifier — هذا قرار مقصود للحد من mass-crawling غير المُتحقَّق من الإذن. لذا parser صفحة المصطلح يستخدم heuristics:
>
> 1. ابحث عن `<a href="/dialect/Saudi">` أو نص "السعودية".
> 2. ارتفع إلى أقرب `<li>/<section>/<article>/<div>` كـ "Saudi block".
> 3. داخل الـ block: ابحث عن `p.definition` ثم أي `<p>` كأكبر نص → التعريف.
> 4. ابحث عن class يحتوي `example/usage/mathal` → المثال.
> 5. ابحث عن class يحتوي `spelling/variants/writing` → variants.
> 6. ابحث عن كلمات: حجازي/نجدي/قصيمي/شمالي/جنوبي → subdialect.
>
> أي parsing غير ناجح يُسجَّل في `parser_warnings` على السجل + يُحفظ raw HTML للمراجعة. **عند تشغيل المستخدم الفعلي للسكربت، أول 10–20 مصطلح يُفترض مراجعتها يدويًا قبل إكمال 3139.**

### كيف ينصح المستخدم بالتشغيل

```bash
# 1) Dry-run — يطبع الخطة بدون أي شبكة.
python scripts/import_mo3jam_saudi.py --dry-run

# 2) Sample صغير live — للتحقق من الـ parser على بيانات حقيقية.
python scripts/import_mo3jam_saudi.py \
    --no-dry-run --confirm-user-permission \
    --rate-limit 2.0 --limit 10

# 3) راجِع الـ 10 سجلات في الـ JSONL يدويًا.
# 4) إن كانت سليمة، أكمل بقية الـ 3139 (سيعمل resume تلقائيًا):
python scripts/import_mo3jam_saudi.py \
    --no-dry-run --confirm-user-permission \
    --rate-limit 2.0 --resume
```

⚠️ **الزمن المتوقع للزحف الكامل:** 3139 طلبًا × 2 ثانية = حوالي **105 دقيقة**.

---

## ما لا نفعله

- ❌ **لا نستخدم البيانات للتدريب الآن.** الحقل `training_allowed: false` على كل سجل في الـ YAML.
- ❌ **لا نخلطها مع `dialects_gulf.yaml` الأصلي.** الـ Mo3jam lexicon يعيش في `resources/lexicons/imported/mo3jam/` ويُحمَّل فقط عند `ENABLE_MO3JAM_SAUDI_LEXICON=true`.
- ❌ **لا parallel crawling.** تتابع واحد فقط مع rate limit صريح.
- ❌ **لا نتجاوز robots.txt.** robots.txt يُفحص قبل أول طلب.
- ❌ **لا نستخدم أي LLM** لتفسير المحتوى — كل parsing rule-based.
- ❌ **لا نستخدم أي API خارجي.** urllib + BeautifulSoup فقط.

---

## ما نفعله دائمًا

- ✅ **نحفظ المصدر** على كل سجل JSONL (`source_name`, `source_url`, `source_root`).
- ✅ **نسجل `credit_required: true`** على كل مدخل.
- ✅ **نحفظ raw HTML** قبل أي parse — يمكن إعادة المعالجة لاحقًا.
- ✅ **نحسب blake2b hash** على كل ملف raw للتوثيق.
- ✅ **نحفظ failed URLs** في تقرير منفصل.
- ✅ **نُولِّد report Markdown** بالإحصائيات الكاملة بعد كل run.
- ✅ **نضع شعار النسبة** في كل artifact ناتج (JSONL header، YAML metadata، report).

---

## القرار: لماذا هذه البيانات سيادية رغم أنها خارجية

- المصدر **بيانات لغوية** (لهجة) — وليس نموذج ذكاء.
- لا أوزان مدرَّبة، لا embeddings، لا decision boundary خارجية.
- الـ definitions نصوص بشرية كتبها مساهمو الموقع، يقابلها إذن مكتوب/شفهي.
- استخدامها لتحسين فهم النص العربي السعودي = مكافئ لمعجم ورقي تستفيد منه.
- الـ **shortcut الممنوع** هو استيراد عقل (LLM/weights/embeddings). أما هذا فاستيراد **معجم لغوي مع إذن** — أداة، لا عقل.

اقرأ [PROJECT_PRINCIPLES.md](../PROJECT_PRINCIPLES.md) و [SOVEREIGN_ACCELERATION.md](./SOVEREIGN_ACCELERATION.md) للفروق الكاملة.
