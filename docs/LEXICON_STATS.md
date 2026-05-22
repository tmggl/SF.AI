# LEXICON_STATS.md

## SF.AI — إحصائيات قواميس اللغة

هذا الملف يُحدَّث بعد كل تغيير في `resources/lexicons/`.

---

## القواميس الأصلية (SF.AI seed — Phase 3)

| ملف | نوع | عدد العناصر التقريبي |
|------|-----|----------------------|
| `arabic_normalization.yaml` | قواعد تطبيع | ~30 char rules + 20 digit rules |
| `arabizi_map.yaml` | mappings | ~40 entry + ~70 protected tokens |
| `dialects_gulf.yaml` | mappings | ~25 |
| `dialects_common_arabic.yaml` | mappings | ~30 (egyptian + levantine + iraqi) |
| `typo_patterns.yaml` | patterns | ~25 + soft hints |
| `safety_terms.yaml` | flags | 5 مجالات × ~10 terms |
| `stopwords_ar_en.yaml` | stopwords | ar + en قصيرة |
| `intents.yaml` | intents | ~18 |
| `domains.yaml` | overlay | ~11 مجال + extras |
| `programming_terms.yaml` | seed | ~30 keyword + 7 phrase |
| `data_terms.yaml` | seed | ~25 |
| `files_terms.yaml` | seed | ~17 |
| `web_terms.yaml` | seed | ~18 |
| `legal_terms.yaml` | seed | ~17 (sensitive) |
| `medical_terms.yaml` | seed | ~20 (sensitive) |
| `finance_terms.yaml` | seed | ~17 (sensitive) |
| `education_terms.yaml` | seed | ~15 |
| `social_terms.yaml` | seed | ~12 |

---

## القواميس المستوردة

### SF.AI Saudi Seed v1 (Phase 3.6 — تأليف المستخدم)

- **المؤلف:** المستخدم نفسه. أصلي، غير منسوخ من Mo3jam.
- **عدد المداخل:** **516** (validation_summary.json).
- **التوزيع:** 441 high / 69 medium / 6 low. 3 sensitive. 144 يحتاج مراجعة بشرية.
- **اللهجات:** saudi_general 389، najdi 130، hijazi_urban 78، bedouin_tribal 76، eastern_shargawi 46، southern_asiri_bahawi 35، jizani_tihami 27، northern_shamali 21، najrani 3.
- **التحميل في DialectMapper:** فقط عند `ENABLE_SAUDI_SEED_V1_LEXICON=true`.
- **safety filter:** runtime-safe ≈ 300 مدخل (high + not sensitive + not review-required).
- **مكان الـ JSONL:** `resources/lexicons/imported/saudi_seed_v1/saudi_dialect_lexicon_full_seed_v1.jsonl`.
- **مهام التدريب:** `data/corpus/dialects/saudi/jsonl/saudi_dialect_training_tasks_seed_v1.jsonl`.

التفاصيل في [SOURCE_DISCOVERY_SAUDI_SEED.md](./SOURCE_DISCOVERY_SAUDI_SEED.md).

### Mo3jam Saudi Dialect (Phase 3.5)

- **المصدر:** معجم — اللهجة السعودية
- **الرابط:** https://ar.mo3jam.com/dialect/Saudi
- **عدد المصطلحات المتوقع:** 3139
- **عدد المصطلحات المستوردة فعلًا:** _(يُحدَّث بعد تشغيل المستخدم لـ `scripts/import_mo3jam_saudi.py --confirm-user-permission`)_
- **الحالة:** بنية الاستيراد جاهزة، الزحف لم يبدأ بعد
- **credit_required:** **true** على كل سجل
- **training_allowed:** **false** افتراضيًا
- **التحميل في DialectMapper:** فقط عند `ENABLE_MO3JAM_SAUDI_LEXICON=true`
- **مكان JSONL الناتج:** `data/corpus/dialects/saudi/jsonl/mo3jam_saudi_terms.jsonl`
- **مكان YAML الناتج:** `resources/lexicons/imported/mo3jam/saudi_dialect_terms.yaml`
- **مكان raw HTML:** `data/corpus/dialects/saudi/raw/mo3jam/{listing,term}/`
- **مكان report:** `data/corpus/dialects/saudi/reports/mo3jam_import_report.md`

#### النسبة الإلزامية (يجب أن تظهر في كل ناتج)

```
مصدر اللهجات السعودية:
معجم — اللهجة السعودية
https://ar.mo3jam.com/dialect/Saudi
```

---

## القواعد العامة

- **جودة قبل الكمية.** لا حشو عشوائي.
- **مصدر دائم.** أي بيانات مستوردة تحمل `source_url` و `source_name` و `credit_required: true`.
- **سيادة.** لا أوزان جاهزة، لا embeddings، لا LLM. القواميس بيانات لغوية فقط.
- **خطة التدريب.** القواميس تخدم NLP الآن. أي قرار باستخدامها في training يحتاج إذن صريح من المستخدم.
