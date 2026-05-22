# LANGUAGE_UNDERSTANDING.md

## SF.AI — Language Understanding Layer (Phase 3)

طبقة فهم اللغة هي **أول طبقة تلمس نص المستخدم** قبل الراوتر. تأخذ نصًا خامًا وتُرجِع تحليلًا منظمًا (`NLPAnalysis`) تستخدمه بقية مكونات النظام.

> **بدون أي نموذج لغوي مدرّب مسبقًا. بدون embeddings جاهزة. كل القرارات قواعد محلية + YAML lexicons.**

---

## التدفق

```
raw text
  │
  ▼ TextCleaner             — يحذف الـ control/format chars، يحافظ على أكواد/روابط
  ▼ ArabicNormalizer        — NFC + tashkeel + tatweel + alef/yaa + digits
  ▼ ArabiziMapper           — shlon→شلون, keef→كيف ...  (protected: python/docker/api/...)
  ▼ ArabicNormalizer        — إعادة تطبيع
  ▼ DialectMapper           — شلونك→كيف حالك (gulf/egyptian/levantine/iraqi)
  ▼ TypoCorrector           — بايثن→بايثون (patterns + bounded fuzzy)
  ▼ LightTokenizer          — split (Arabic-aware) — ليس BPE، BPE في Phase 5.5
  ▼ LanguageDetector        — ar / en / mixed / code / unknown
  ▼ SafetyScanner           — يرفع flags للمحتوى الحساس (medical/legal/finance/security/religion)
  ▼ IntentDetector          — يطرح hints (لا يقرر)
  │
  ▼ NLPAnalysis
```

---

## NLPAnalysis (العقد الموحد)

ملف: [sf_ai/core/nlp/types.py](../sf_ai/core/nlp/types.py)

| حقل | نوع | متى يُملأ |
|------|------|-----------|
| `original_text` | str | كما كتبه المستخدم |
| `cleaned_text` | str | بعد TextCleaner |
| `normalized_text` | str | بعد ArabicNormalizer |
| `corrected_text` | str | بعد TypoCorrector |
| `canonical_text` | str | بعد Arabizi + Dialect → canonical |
| `language` | str | ar/en/mixed/code/unknown |
| `detected_dialect` | str | msa/gulf/egyptian/levantine/iraqi/unknown |
| `tokens` | tuple[str] | من canonical عبر LightTokenizer |
| `corrections` | tuple[Correction] | typo_pattern \| fuzzy \| soft_hint |
| `aliases` | tuple[DialectSignal] | كل تحويل arabizi+dialect مع surface→canonical |
| `domain_hints` | tuple[str] | مجالات مرشحة من IntentHint |
| `intent_hints` | tuple[IntentHint] | top 3 |
| `safety_flags` | tuple[str] | "medical:ألم", "legal:عقد", ... |
| `confidence` | float | تقدير ناعم في [0,1) |

---

## السلوك التفصيلي

### ArabicNormalizer
- `strip_chars`: 8 tashkeel + tatweel + ZWNJ/ZWJ/BOM/RLM/LRM.
- `char_map`: أ/إ/آ/ٱ → ا، ى/ئ → ي، ؤ → و، چ → ج، گ → ك، پ → ب.
- `digit_map`: ٠١٢٣٤٥٦٧٨٩ → 0..9 (والإيرانية أيضًا).
- `ة` تُحفظ افتراضيًا — اختياريًا `fold_ta_marbuta: true` للـ fuzzy.
- المصدر: [resources/lexicons/arabic_normalization.yaml](../resources/lexicons/arabic_normalization.yaml).

### TextCleaner
- يحذف Cc و Cf فقط.
- **يحافظ** على `{} [] () ; : / \ . _ - = + * < >` لأن أكواد المستخدم وروابطه يجب أن تظل قابلة للعرض الحرفي.

### ArabiziMapper
- token-by-token على نطاق Latin.
- `protected_tokens`: python/django/api/json/docker/react/sql/http/... — لا تُحوَّل أبدًا.
- كل تحويل يخرج `DialectSignal(surface, canonical, dialect, confidence)`.

### DialectMapper
- ثلاث lexicons: gulf، egyptian، levantine، iraqi.
- longest-match-first (multi-word قبل tokens).
- `detect_dialect(signals)` يصوّت على اللهجة بالأوزان.
- لا يغيّر نص المستخدم في الرد النهائي — Phase 4 chat module يحترم أسلوب المستخدم.
- **Phase 3.5:** يمكن تفعيل قاموس سعودي موسَّع مستورد من معجم (mo3jam) عبر متغير البيئة `ENABLE_MO3JAM_SAUDI_LEXICON=true`. الإضافة تظل **خارج** `dialects_gulf.yaml` الأصلي لحفظ النسبة. التفاصيل في [SOURCE_DISCOVERY_MO3JAM.md](./SOURCE_DISCOVERY_MO3JAM.md). البيانات تحمل `credit_required=true` و `training_allowed=false` افتراضيًا.

### TypoCorrector
- `patterns` (auto-apply عند `conf ≥ 0.7`).
- `soft_hints` (تُرفع كملاحظات فقط).
- `fuzzy_against(token, vocab)` للاستخدام التحكمي.
- يقبل reasons قابلة للقراءة: `missing_waw`, `hamza_drop`, `letter_swap`, ...

### LanguageDetector
- خوارزمية بسيطة: عدّ Arabic range vs Latin، + قواعد code (`def`, `class`, `=>`, fenced blocks).
- ar إذا ≥ 85% عربي، en إذا ≤ 15%، إلا فـ mixed.

### SafetyScanner
- يفحص جميع lenses (original/normalized/canonical/corrected).
- يصدر flags بصيغة `<domain>:<term>`.
- مصدر: [resources/lexicons/safety_terms.yaml](../resources/lexicons/safety_terms.yaml).

### IntentDetector
- يطرح **hints فقط**، لا يقرر.
- المصدر: [resources/lexicons/intents.yaml](../resources/lexicons/intents.yaml).

---

## الـ Lexicons (Phase 3 seed)

| ملف | الحجم/الجودة | استخدام |
|------|---------------|---------|
| `arabic_normalization.yaml` | جداول كاملة | ArabicNormalizer |
| `arabizi_map.yaml` | ~40 mapping + protected list | ArabiziMapper |
| `dialects_gulf.yaml` | ~25 | DialectMapper |
| `dialects_common_arabic.yaml` | ~30 (egyptian+levantine+iraqi) | DialectMapper |
| `typo_patterns.yaml` | ~25 + soft_hints | TypoCorrector |
| `safety_terms.yaml` | 5 مجالات × ~10 terms | SafetyScanner |
| `stopwords_ar_en.yaml` | ar+en قصيرة | LightTokenizer |
| `intents.yaml` | ~18 intent | IntentDetector |
| `domains.yaml` | overlay مجالات | IntentDetector |
| `programming_terms.yaml` | بذرة coding | Phase 4+ |
| `data_terms.yaml` | بذرة data | Phase 4+ |
| `files_terms.yaml` | بذرة files | Phase 4+ |
| `web_terms.yaml` | بذرة web | Phase 7 |
| `legal_terms.yaml` | بذرة legal (sensitive) | Phase 4+ |
| `medical_terms.yaml` | بذرة medical (sensitive) | Phase 4+ |
| `finance_terms.yaml` | بذرة finance (sensitive) | Phase 4+ |
| `education_terms.yaml` | بذرة education | Phase 4+ |
| `social_terms.yaml` | بذرة social | Phase 4+ |

> **مبدأ:** جودة قبل الكمية. ممنوع حشو الـ lexicons بمدخلات عشوائية لمجرد الوصول إلى رقم.

---

## كيف يستخدم الراوتر NLPAnalysis

[ROUTER.md](./ROUTER.md) يصف الجدول الكامل، لكن باختصار:

كل phrase/keyword في domain يُجرَّب على **lenses** بترتيب القوة:
1. **original** (norm_simple) → `phrase` (+5) / `keyword` (+3)
2. **normalized_text** → `normalized` (+2.5)
3. **canonical_text** (بعد arabizi+dialect) → `dialect_alias` (+2)
4. **corrected_text** → `typo_corrected` (+1.5)
5. fuzzy على normalized → `fuzzy` (+1)

أول lens تطابق تربح، ولا يُحسب نفس phrase/keyword مرتين.

---

## مبدأ مهم: لا تتجاوز السيادة

- **لا** `langdetect` library تستخدم بيانات إحصائية مدربة → كتبنا detector محلي بسيط بدلًا منها.
- **لا** `nltk.stopwords` → ملف YAML سيادي.
- **لا** `pyarabic.araby` (مع أنها قواعد فقط) — نكتب القواعد بأنفسنا في YAML قابل للمراجعة.
- **لا** `polyglot` / `spacy` نماذج لغوية.
- **لا** embeddings لتحديد التشابه — استخدمنا fuzzy + hashing.

أي تحسين في الجودة لاحقًا يأتي من:
1. Lexicons أوسع (يضيفها المستخدم بإذنه).
2. SF Native Encoder (Phase 6+).
3. SF Native LM (Phase 6).
