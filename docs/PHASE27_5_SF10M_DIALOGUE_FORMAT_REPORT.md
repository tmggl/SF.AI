# PHASE27_5_SF10M_DIALOGUE_FORMAT_REPORT.md

## SF.AI — Phase 27.5 SF-10M Dialogue-Format Repair

**Journey:** Phase 27.5 / 30
**Language track:** `msa + saudi` only
**Lexicon track:** `Saudi Seed v1`
**Tokenizer:** `artifacts/tokenizers/sf_bpe/v2`
**Status:** `COMPLETED_WITH_LIMITS_RUNTIME_BLOCKED`

## الهدف

بعد اكتمال corpus gate في Phase 27 عند `5143` سجلًا طبيعيًا، تبيّن أن تدريب
النموذج كتيار رسائل منفصلة لا يعلّمه علاقة:

```text
المستخدم يسأل → المساعد يجيب
```

هذه المرحلة أصلحت صيغة التدريب والتقييم لتستخدم حوارًا كاملًا بعلامات أدوار
عربية واضحة، ثم اختبرت `SF-10M v0.4`.

## ما تغيّر هندسيًا

- أضيف `ChatDataset.iter_dialogue_texts()` ليبث كل عينة كحوار كامل:
  `المستخدم: ...` ثم `المساعد: ...`.
- أصبح `train_tiny_lm` يستخدم `--stream-format dialogue` افتراضيًا، مع إبقاء
  `messages` كخيار تشخيصي.
- أصبح `evaluate_tiny_lm` يدعم `--chat-prompt` لتغليف prompt بصيغة الحوار.
- أضيف استخراج مضبوط لرد المساعد عبر `extract_dialogue_reply()` حتى لا يختلط
  prompt المستخدم برد النموذج.
- بقي runtime الواسع محجوبًا؛ الواجهة المستقرة لا تتحول إلى النموذج الخام.

## التدريب

```text
model           : sf-10m
parameters      : 7,444,992
corpus          : 5143 records
stream_format   : dialogue
steps           : 4000
epochs          : 8
seq_len         : 64
batch_size      : 4
device          : mps
first loss      : 8.4662
last loss       : 1.4070
checkpoint      : artifacts/checkpoints/sf_10m_v0_4/sf-10m-step4000
```

## التقييم

بعد إصلاح استخراج الرد:

```text
eval batches : 20
loss         : 5.8267
perplexity   : 339.24
```

عينات توليد:

```text
prompt: كيفك
output: لا، الاعتذار الطرف الآخر.

prompt: السلام عليكم
output: لا، الجواب العملي: ابدأ بتحية بسيطًا.

prompt: اشرح لي الماء
output: لا، الاعتذار الطرف الآخر.
```

## القرار

```text
SF-10M v0.4: TRAINED_AND_MEASURED_BUT_RUNTIME_BLOCKED
```

النتيجة أفضل من ناحية التعلم الداخلي: النموذج صار يتعلم بنية الأدوار، والخسارة
التدريبية انخفضت بقوة. لكن الردود القصيرة لا تزال غير مناسبة للسؤال ولا تصل
إلى "حوار مولّد مقنع".

لذلك:

- لا يتم تفعيل `SF-10M v0.4` كمولّد افتراضي في الواجهة.
- لا ننتقل إلى `SF-50M` قبل إصلاح جودة الردود على `SF-10M`.
- لا ننتقل إلى Phase 28 لأن شرط `SF-50M` لم يتحقق.

## البوابة التالية

الخطوة التالية يجب أن تكون إصلاحًا نوعيًا لا تكبيرًا:

1. تدريب/تقييم بأسلوب assistant-target أو loss masking حتى يركز النموذج على رد
   المساعد لا تكرار سياق الحوار كله.
2. تحسين decoding/canary لقياس الصلة بالسؤال والتكرار.
3. تشغيل eval حواري صغير على النموذج الحقيقي، لا على القوالب.
4. السماح بالواجهة فقط إذا أنتج النموذج ردودًا مفهومة ومرتبطة بالسؤال.

## الملفات الداعمة

- `artifacts/reports/sf_10m_v0_4_dialogue_format_report.json`
- `artifacts/samples/sf_10m_v0_4_generations.md`
