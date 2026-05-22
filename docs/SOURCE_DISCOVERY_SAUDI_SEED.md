# SOURCE_DISCOVERY_SAUDI_SEED.md

## مصدر: SF.AI Saudi Dialect Seed v1 (تأليف المستخدم)

> **هذا قاموس أصلي مؤلَّف من المستخدم. غير منسوخ من معجم (Mo3jam).** بذرة منظَّمة بـ 516 مدخل تخص اللهجة السعودية بفروعها.

---

## معلومات الحزمة

- **اسم الحزمة:** `saudi_dialect_lexicon_full_seed_v1`
- **عدد المداخل:** **516**
- **مساره داخل SF.AI:** `resources/lexicons/imported/saudi_seed_v1/`
- **تاريخ الإنتاج:** `2026-05-22` (من `validation_summary.json`)
- **حالة الإذن:** المستخدم نفسه هو المؤلف. لا إذن خارجي مطلوب.
- **`source_basis` على كل مدخل:** `original_compilation_not_copied_from_mo3jam`.

### الملفات المنقولة

```
resources/lexicons/imported/saudi_seed_v1/
├── saudi_dialect_lexicon_full_seed_v1.json    (~ 580 KB)
├── saudi_dialect_lexicon_full_seed_v1.jsonl   (~ 420 KB) ← المصدر التشغيلي
├── saudi_dialect_lexicon_full_seed_v1.csv     (~ 165 KB)
├── validation_summary.json
├── AGENT_INSTRUCTIONS_AR.txt
└── README_AR.md
```

ومهام التدريب الجاهزة (متوافقة مع Phase 5 format):

```
data/corpus/dialects/saudi/jsonl/saudi_dialect_training_tasks_seed_v1.jsonl
```

---

## بنية المدخل

```json
{
  "id": "sa-lex-...",
  "term": "وش",
  "normalized_term": "وش",
  "variants": ["وشو"],
  "kind": "word",
  "category": "question",
  "dialect_labels": ["saudi_general", "najdi"],
  "dialect_names_ar": ["سعودي عام", "نجدي"],
  "used_in_places": ["عموم السعودية", "الرياض", "..."],
  "meaning_msa": "ماذا / ما",
  "english_gloss": null,
  "example_saudi": "وش تبي من السوق؟",
  "register": "neutral",
  "dialectality": "high",
  "confidence": "high | medium | low",
  "requires_native_review": false,
  "safety": {
    "sensitive_or_profane": false,
    "allow_for_generation": true,
    "recommended_use": ["dialect_identification", "lexicon_lookup", "normalization", "RAG_context"]
  },
  "source_basis": "original_compilation_not_copied_from_mo3jam"
}
```

---

## الإحصاءات (من `validation_summary.json`)

| المقياس | القيمة |
|---------|--------|
| إجمالي المداخل | **516** |
| مداخل فريدة بعد التطبيع | 514 (مكررتان: "ايش"، "سنع") |
| `confidence=high` | **441** |
| `confidence=medium` | 69 |
| `confidence=low` | 6 |
| `sensitive_or_profane=true` | 3 |
| `requires_native_review=true` | 144 |

### التوزيع حسب اللهجة

| اللهجة | العدد |
|--------|--------|
| saudi_general | 389 |
| najdi | 130 |
| hijazi_urban | 78 |
| bedouin_tribal | 76 |
| eastern_shargawi | 46 |
| southern_asiri_bahawi | 35 |
| jizani_tihami | 27 |
| northern_shamali | 21 |
| najrani | 3 |

---

## سياسة الاستخدام داخل SF.AI

### Runtime (DialectMapper)

تُحمَّل المداخل فقط عند:

```bash
ENABLE_SAUDI_SEED_V1_LEXICON=true
```

والمداخل المُحمَّلة تخضع لـ **safety filter** صارم:
- `confidence == "high"` فقط (441 مدخل).
- `sensitive_or_profane == false` (يُستثنى 3 مداخل).
- `allow_for_generation == true`.
- `requires_native_review == false` (يُستثنى 144).

النتيجة الفعلية: ~300 مدخل آمن للوقت الحقيقي (تختلف بحسب التداخلات).

### Confidence → mapping confidence

| `confidence` | مَن يُحمَّل افتراضيًا؟ | الـ DialectMapper conf |
|--------------|-----------------------|------------------------|
| `high` | ✅ نعم | 0.95 |
| `medium` | ❌ لا (تتطلب مراجعة بشرية) | 0.7 |
| `low` | ❌ لا | 0.5 |

### Training (Phase 5+ / Phase 6+)

- المداخل `confidence=high` + `not sensitive` → **مرشحة للتدريب التوليدي**.
- المداخل `medium`/`low` أو التي تحتاج مراجعة → **inspection only**، لا تدريب.
- `allow_for_generation=false` → **لا** تُستخدم لأي توليد.
- `requires_native_review=true` → تنتظر مراجعة ناطق محلي قبل أي استخدام إنتاجي.

---

## التكامل البرمجي

### تحميل آمن من Python

```python
from sf_ai.datasets import load_saudi_seed, saudi_seed_stats

safe_entries = load_saudi_seed(safe_only=True)
print(len(safe_entries), "entries safe for runtime")

stats = saudi_seed_stats()
print(stats)
```

### تفعيل في DialectMapper

```python
import os
os.environ["ENABLE_SAUDI_SEED_V1_LEXICON"] = "true"

from sf_ai.core.nlp.dialect_mapper import DialectMapper
mapper = DialectMapper()
out, signals = mapper.map_text("ترى يا اخوي")
# signals يحتوي على dialect='saudi'
```

---

## النسبة المطلوبة

```
مصدر قاموس اللهجات السعودية:
saudi_dialect_lexicon_full_seed_v1 — تأليف مستخدم SF.AI.
غير منسوخ من Mo3jam.
```

> **مهم:** عند توسيع القاموس لاحقًا بمدخلات من Mo3jam، يجب وضع إسناد منفصل لكل مدخل من تلك المدخلات:
> ```
> المصدر: معجم — اللهجة السعودية
> https://ar.mo3jam.com/dialect/Saudi
> ```

---

## مقارنة مع Mo3jam (Phase 3.5)

| الجانب | Saudi Seed v1 (Phase 3.6) | Mo3jam (Phase 3.5) |
|--------|----------------------------|---------------------|
| المؤلف | المستخدم نفسه | فريق معجم |
| التحقق من الإذن | غير مطلوب — ملكية المستخدم | مكالمة هاتفية أكدها المستخدم |
| الإسناد | داخلي (تأليف المستخدم) | إلزامي عند العرض |
| credit_required | لا (يكفي ذكر التأليف الذاتي) | **نعم على كل مدخل** |
| training_allowed افتراضيًا | true لـ `confidence=high` فقط | false (يحتاج قرارًا صريحًا لاحقًا) |
| الاسم البرمجي | `ENABLE_SAUDI_SEED_V1_LEXICON` | `ENABLE_MO3JAM_SAUDI_LEXICON` |
| المسار | `resources/lexicons/imported/saudi_seed_v1/` | `resources/lexicons/imported/mo3jam/` |
| العدد | 516 | 3139 (إذا اكتمل الاستيراد) |

كلاهما يبقى **معزولًا** عن قواميس SF.AI الأصلية (`dialects_gulf.yaml` ...) حفاظًا على وضوح الإسناد.

---

## ما لم يُنفَّذ بعد (مقصود)

- ❌ تدريب فعلي من بيانات `saudi_dialect_training_tasks_seed_v1.jsonl` — ينتظر اكتمال Phase 6 + قرار صريح.
- ❌ تكامل في `WebModule`/`ResearchModule` كـ Phase 7 context — يأتي مع Phase 8 RAG.
- ❌ معالجة المداخل `medium`/`low` — تنتظر مراجعة بشرية.

---

## الاختبارات

```
tests/test_saudi_seed.py — 15 passed
```

التغطية:
- وجود الملف في المسار الصحيح.
- تحميل 516 مدخل.
- إحصاءات تطابق `validation_summary.json` (441 high، 69 medium، 6 low، 3 sensitive).
- safety filter يستثني sensitive/low/medium/review-required.
- مرونة الـ loader أمام JSON تالف أو مفاتيح ناقصة.
- DialectMapper بدون flag لا يُحمِّل القاموس.
- DialectMapper مع flag يُصدر `saudi` signal لمصطلح حصري للسعودية.
- مرونة الـ DialectMapper أمام ملف غير موجود.
