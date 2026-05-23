# PHASE24_SF10M_V0_2_REPORT.md

## SF.AI — Phase 24 SF-10M v0.2 Quality Training

**Journey:** Phase 24 / 30  
**Language track:** `msa + saudi` only  
**Tokenizer:** `artifacts/tokenizers/sf_bpe/v2`  
**Status:** `COMPLETED_WITH_LIMITS_RUNTIME_BLOCKED`

## الهدف

Phase 24 هي أول محاولة تدريب جودة مفيدة بعد اكتمال corpus المتوازن
`500/500` وتدريب tokenizer v2. الهدف لم يكن جعل الواجهة ترد بذكاء كامل، بل
قياس هل صار `SF-10M` أقل تكرارًا وأكثر قابلية للتحسين.

## Preflight

قبل التدريب تم تشغيل البوابات:

```text
corpus-audit             : 500/500, msa=250, saudi=250, issues=0
phase23-tokenizer-audit  : COMPLETED_READY_FOR_PHASE24
tokenization-audit       : protected_terms 30/30
```

## الأمر المستخدم

```bash
make train-lm ARGS="--tokenizer artifacts/tokenizers/sf_bpe/v2 --corpus data/corpus/chat/jsonl --size sf-10m --seq-len 64 --batch-size 4 --steps 2000 --epochs 25 --warmup 50 --save-every 500 --checkpoints artifacts/checkpoints/sf_10m_v0_2 --seed 20260523"
```

## نتيجة التدريب

```text
device          : mps
model           : sf-10m
parameters      : 7,444,992
requested steps : 2000
completed steps : 2000
first loss      : 8.4751
last loss       : 2.8256
checkpoint      : artifacts/checkpoints/sf_10m_v0_2/sf-10m-step2000
```

ملفات checkpoint محلية وغير مرفوعة إلى git حسب سياسة المشروع:

```text
artifacts/checkpoints/**/*
```

## التقييم

```text
batches     : 20
loss        : 2.5779
perplexity  : 13.17
generation  : non-empty, UTF-8 valid, still incoherent
```

مقارنة توجيهية مع Phase 14:

```text
SF-10M v0.1 perplexity : 59.01
SF-10M v0.2 perplexity : 13.17
```

ليست مقارنة مثالية لأن corpus/tokenizer تغيرا، لكنها تثبت اتجاهًا إيجابيًا.

## عينات التوليد

العينات محفوظة في:

```text
artifacts/samples/sf_10m_v0_2_generations.md
```

الخلاصة: النموذج لم يعد عالقًا بنفس تكرار `المعنى/وأين` مثل v0.1، لكنه ما
زال يخلط عبارات عربية ومقاطع corpus بطريقة غير مقنعة.

## القرار

```text
Phase 24 SF-10M v0.2: COMPLETED_WITH_LIMITS_RUNTIME_BLOCKED
Suitable for runtime chat: NO
Recommended next: Phase 25 canary only, with strict fallback
```

لا يتم تفعيل `SF-10M v0.2` كمسار رد واسع في الواجهة. المرحلة التالية يجب أن
تبني canary صغيرًا يقيس التكرار/التماسك ويعيد الرد إلى القوالب عند الفشل.
