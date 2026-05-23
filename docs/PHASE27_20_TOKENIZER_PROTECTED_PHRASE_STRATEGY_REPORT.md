# Phase 27.20 — Tokenizer/Protected-Phrase Strategy

## القرار

```text
COMPLETED_PROTECTED_PHRASE_STRATEGY_READY_FOR_TOKENIZER_V3
```

هذه المرحلة لم تفعّل المولد في الواجهة، ولم تبدأ `SF-50M`.

هدفها كان إصلاح سبب محدد ظهر في Phase 27.18 وPhase 27.19: عبارات طبيعية
تتجزأ بقوة داخل tokenizer v2 ثم تظهر آثارها في توليد مشوه.

## ما أضيف

- أضيف دعم `protected_terms` داخل `TokenizerConfig`.
- أصبح `BPETokenizer` قادرًا على حماية عبارات متعددة الكلمات عبر joiner داخلي
  محفوظ في `meta.json`.
- أضيف مسار CLI لتدريب tokenizer لاحقًا مع ملف protected terms:

```bash
make train-bpe ARGS="... --protected-terms resources/tokenization/protected_phrases_phase27_20.txt"
```

- أضيف ملف:

```text
resources/tokenization/protected_phrases_phase27_20.txt
```

- أضيف تقرير آلي:

```text
artifacts/reports/phase27_20_tokenizer_strategy_report.json
```

- أضيف هدف:

```bash
make phase27-tokenizer-strategy
```

## العبارات المحمية

```text
وعليكم السلام
نفسًا هادئًا
نشتغل سوا
القراءة تفيد
تقدّر الناس
```

هذه العبارات جاءت من فشل Phase 27.17/27.18/27.19، وليست vocabulary
مستوردة أو pretrained.

## نتيجة القياس

Tokenizer v2 الحالي:

```text
max_pieces = 8
```

استراتيجية protected phrase الجديدة:

```text
max_pieces = 1
all_single_piece = true
all_roundtrip_ok = true
```

أي أن العبارة التي كانت تتجزأ إلى 5–8 قطع يمكن حفظها كوحدة واحدة في
tokenizer v3 القادم.

## هل صار المولد جاهزًا للواجهة؟

لا.

هذه مرحلة tokenizer strategy فقط. هي تزيل عائقًا مهمًا، لكنها لا تثبت أن
النموذج نفسه صار يرد بردود مقنعة.

## لماذا runtime ما زال محجوبًا؟

لأن الواجهة يجب ألا تعرض المولد إلا بعد:

- تدريب tokenizer v3 بهذه السياسة.
- تدريب/Probe على tokenizer v3.
- اجتياز micro-probe.
- اجتياز generation-quality canary.
- غياب الكسور والتكرار والردود غير المرتبطة بالسؤال.

## القرار العملي

```text
runtime_allowed = false
sf50m_allowed   = false
```

## التالي

```text
Phase 27.21 — Tokenizer v3 protected-phrase retrain + micro-probe
```

هدف Phase 27.21:

- تدريب tokenizer v3 سيادي مع protected phrases.
- إعادة تشغيل prompt-answer micro-probe.
- قياس هل اختفت كسور العبارات الخمس.
- عدم تفعيل الواجهة إلا إذا نجح canary.
