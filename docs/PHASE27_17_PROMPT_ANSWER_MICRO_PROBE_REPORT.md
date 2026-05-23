# Phase 27.17 — Prompt-to-Answer Micro-Probe

## القرار

```text
FAILED_PROMPT_ANSWER_MICRO_PROBE_BLOCK_RUNTIME
```

هذه المرحلة ليست تدريبًا واسعًا ولا تفعيلًا للواجهة. الهدف كان إثبات أن
المسار السيادي يستطيع تعلم أزواج قصيرة من نوع:

```text
سؤال المستخدم → جواب المساعد
```

قبل أي محاولة لتكبير النموذج.

## الإعداد

```text
language_track = msa + saudi
lexicon_track  = Saudi Seed v1
records        = 32
msa            = 16
saudi          = 16
model          = SF-10M
steps          = 2400
packing_mode   = sample_isolated
loss_scope     = assistant
```

البيانات بقيت داخل `artifacts/eval/phase27_17_prompt_answer_micro_probe/`
ولا تُعد توسعة corpus عامة.

## النتيجة

```text
passed       = 27/32
exact_clean  = 28/32
semantic     = 29/32
guard_passed = 29/32
```

هذا أول تحسن واضح في prompt-to-answer mapping. النموذج لم يكتف بنص عربي
عام؛ في أغلب العينات أرجع الجواب الصحيح أو قريبًا منه.

## الفشل المتبقي

الفشل ليس فقدًا كاملًا للمعنى، بل كسور لفظية/حروفية في كلمات محددة:

```text
وعليكأهلًا السم، أهلًا بك.
التعاعاون يعني أن ننجز معًا بدل الانفراد.
القراد. ءة توسع الفهم وتزيد المفردات.
هوش تحتاجججبعيادة.
```

هذا يعني أن المشكلة التالية ليست زيادة حجم النموذج، بل:

- tokenizer/decoding hygiene.
- حماية الكلمات الشائعة من الكسر.
- probe خاص للكسور اللفظية قبل التدريب الواسع.

## القرار العملي

- لا تفعيل للمولد في `/ui/chat`.
- لا تدريب `SF-50M`.
- لا انتقال إلى Phase 28.
- الانتقال التالي: Phase 27.18 — Tokenization/Decoding Hygiene Repair.

## الملفات

- `scripts/phase27_17_prompt_answer_micro_probe.py`
- `artifacts/reports/phase27_17_prompt_answer_micro_probe_report.json`
- `artifacts/samples/phase27_17_prompt_answer_micro_probe_generations.md`
