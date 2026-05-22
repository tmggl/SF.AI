# ROUTER.md

## Router Design — SF.AI

طبقة التوجيه في SF.AI تقرر **أين** تذهب رسالة المستخدم داخل النظام: أي مجال (domain) وأي نية (intent).

> الراوتر لا يستخدم أي نموذج لغوي ولا embeddings جاهزة. كل القرارات مبنية على قواعد محلية + مطابقة معجمية + similarity محلي.

---

## بنية الراوتر

```
text ─► DomainRouter ─► (domain, score, signals)
        │
        └── IntentRouter (داخل المجال المختار) ─► (intent, score, signals)
```

- **DomainRouter** ([sf_ai/core/router/domain_router.py](../sf_ai/core/router/domain_router.py)): يحسب نقاطًا لكل مجال في `CapabilityRegistry` ويختار الأعلى.
- **IntentRouter** ([sf_ai/core/router/intent_router.py](../sf_ai/core/router/intent_router.py)): يكرر نفس المنطق داخل intents المجال الفائز.
- **rules.py** ([sf_ai/core/router/rules.py](../sf_ai/core/router/rules.py)): يحدد أنواع الإشارات وأوزانها.

---

## نظام النقاط

| Signal Kind      | Weight | متى يُصدر |
|------------------|--------|----------|
| `phrase`         | **+5** | عبارة كاملة موجودة داخل النص بعد التطبيع |
| `keyword`        | **+3** | كلمة مفتاحية مفردة موجودة كـ token |
| `normalized`     | +2.5   | (Phase 3) مطابقة بعد التطبيع العربي |
| `dialect_alias`  | +2     | (Phase 3) مرادف لهجي |
| `typo_corrected` | +1.5   | (Phase 3) مطابقة بعد تصحيح إملائي |
| `fuzzy`          | +1     | تشابه `difflib.SequenceMatcher ≥ 0.85` |
| `hashing`        | +0.5   | cosine على hashing vector |
| `safety_term`    | 0      | يرفع safety flag فقط — لا يقرر المجال |

> **Phase 2 فعّال:** `phrase`, `keyword`, `fuzzy`, `hashing`.
> **Phase 3 سيُفعّل:** `normalized`, `dialect_alias`, `typo_corrected`.

### من النقاط إلى confidence

```python
confidence = score / (score + 2.0)
```

| Score | Confidence |
|-------|-----------|
| 0     | 0.00      |
| 1     | 0.33      |
| 3     | 0.60      |
| 5     | 0.71      |
| 8     | 0.80      |
| 13    | 0.87      |

محصور دائمًا في `[0, 1)`. لا يصل إلى 1.0 مهما كان (يحافظ على عدم اليقين).

---

## الـ Fallback

- لا signals يتعدى `MIN_DOMAIN_SCORE = 0.5` → استخدام `meta.fallback` من الـ registry.
- الافتراضي حاليًا: `domain=chat`, `intent=chat.general`, `style=arabic_formal`.

---

## شكل النتيجة

```python
RoutingResult(
    domain=str,
    score=float,
    confidence=float,
    matched_signals=tuple[RoutingSignal, ...],
    fallback_used=bool,
    route_reason=str,
)
```

`RoutingSignal.describe()` يطبع `phrase:مرحبا(+5.00)` للتشخيص.

---

## المجالات الحساسة

`legal, medical, finance, security, religion` تحمل `requires_safety=true`.
الـ Composer يرفع safety flag ويعطي رد آمن بدلًا من المحتوى المتخصص.

---

## نقاط التوسعة

1. **Phase 3:** ربط NLP pipeline → يُدخل `normalized/dialect_alias/typo_corrected` كإشارات إضافية.
2. **Phase 4:** الـ Orchestrator سيرسل الراوتر لـ ChatModule مباشرة بدل الـ Composer الافتراضي.
3. **Phase 6+:** استبدال hashing vector بـ SF custom embeddings مدرّبة من الصفر.
