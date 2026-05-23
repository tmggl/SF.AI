# PHASE27_6_SF10M_ASSISTANT_TARGET_REPORT.md

## SF.AI — Phase 27.6 SF-10M Assistant-Target Training

**Journey:** Phase 27.6 / 30
**Language track:** `msa + saudi` only
**Lexicon track:** `Saudi Seed v1`
**Tokenizer:** `artifacts/tokenizers/sf_bpe/v2`
**Status:** `COMPLETED_WITH_LIMITS_RUNTIME_BLOCKED`

## الهدف

Phase 27.5 جعل التدريب حواريًا، لكنه كان يحاسب النموذج على كل النص: علامات
الأدوار وسياق المستخدم ورد المساعد. Phase 27.6 أضاف هدفًا أدق:

```text
user/context/role markers → masked with -100
assistant reply tokens    → trained normally
```

أي أن السؤال يصبح سياقًا، والرد هو الهدف.

## ما تغير هندسيًا

- أضيف `--loss-scope assistant` إلى `train_tiny_lm`.
- أضيف نفس الخيار إلى `evaluate_tiny_lm`.
- أضيف `_encode_assistant_target_dialogue()` لبناء labels مقنّعة.
- بقي `--loss-scope full` متاحًا للمقارنة وعدم كسر تقارير v0.4.
- أضيفت اختبارات تثبت أن user/role markers لا تدخل في الخسارة وأن assistant
  content فقط يتعلم.

## التدريب

```text
model           : sf-10m
parameters      : 7,444,992
corpus          : 5143 records
stream_format   : dialogue
loss_scope      : assistant
steps           : 4000
epochs          : 8
seq_len         : 64
batch_size      : 4
device          : mps
first loss      : 8.4643
last loss       : 2.3513
checkpoint      : artifacts/checkpoints/sf_10m_v0_5/sf-10m-step4000
```

## التقييم

أفضل نتيجة مقاسة كانت عند step2000:

```text
checkpoint  : sf-10m-step2000
eval loss   : 6.5718
perplexity  : 714.65
prompt      : كيفك
output      : الزبدة: اطلب رر بخياها بخيا. ، وبخيا. ، بالموقت مطر: اكتب الز: قل الزبدة: اطلب رر ب
```

نتيجة step4000:

```text
eval loss   : 7.9360
perplexity  : 2796.09
prompt      : كيفك
output      : الجواب العملي: اذكر الطروت الهدوء. . . . خياريني الطف. . . . . خير. الهدوء. خير. الطويل. ك .
```

## القرار

```text
SF-10M v0.5: TRAINED_ASSISTANT_TARGET_BUT_RUNTIME_BLOCKED
```

تحسّن الهدف الهندسي، وبدأت الجمل تأخذ شكلًا عربيًا أكثر من v0.4، لكن الردود
لا تزال مكررة وغير مرتبطة كفاية بالسؤال. لذلك:

- لا يتم تفعيل `SF-10M v0.5` في الواجهة.
- لا يبدأ `SF-50M`.
- لا يبدأ Phase 28.
- الخطوة التالية ليست تكبيرًا، بل تحسين بيانات/تقسيم/تقييم التوليد قبل scaling.

## الاستنتاج الفني

Assistant-target وحده غير كافٍ. نحتاج الخطوة التالية:

1. فصل train/eval split ثابت بدل تقييم أول batches من نفس الترتيب.
2. عينات `gold` أكثر للردود القصيرة الاجتماعية: تحية، سؤال حال، متابعة، توضيح.
3. decoding guard أقوى للتكرار الصوتي والحروف المتكررة.
4. canary حقيقي يقيس الصلة بالسؤال قبل السماح للواجهة.
