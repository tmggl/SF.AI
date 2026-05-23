# PHASE27_DIALOGUE_EVAL_V2_REPORT.md

## SF.AI — Phase 27 Dialogue Evaluation v2 + Corpus Expansion Plan

**Journey:** Phase 27 / 30  
**Language track:** `msa + saudi` only  
**Lexicon track:** Saudi Seed v1 + local Saudi/Gulf runtime seed  
**Status:** `COMPLETED_DIALOGUE_EVAL_V2_BASELINE_PASS_CORPUS_GATE_PASSED`

## الهدف

Phase 27 لا تدرّب نموذجًا ولا تفعّل مولدًا. هدفها:

1. اختبار الحوار متعدد الأدوار بدل prompt واحد.
2. التأكد أن runtime الحالي لا يكذب على سامي بأنه مولد ذكي.
3. تحويل قرار Phase 26 إلى خطة corpus دقيقة قبل أي `SF-50M`.

## نتيجة التقييم

```text
scenarios       : 7
turns           : 19/19
pass_rate       : 100%
generator_modes : {"template": 19}
open_generator_ready : false
can_start_phase28    : false
```

المعنى العملي:

- التوجيه والردود القالبية نجحت كـ baseline.
- هذا ليس حوارًا مولدًا مقنعًا.
- كل الردود لا تزال `template`.
- Phase 28 محجوبة حتى ينجح `SF-50M` أولًا، و`SF-50M` نفسه محجوب حتى نصلح جودة `SF-10M` وcanary.

## خطة توسيع corpus

```text
current_records   : 5143
target_records    : 5000
remaining_records : 0
needed_msa        : 0
needed_saudi      : 0
batch_size        : 1500
batches_total     : 0
gold_target       : 1000
needed_gold       : 969
needed_silver     : 0
```

فئات البيانات المطلوبة:

- social_smalltalk
- everyday_question_answer
- msa_daily_explanation
- saudi_daily_dialogue
- context_followup
- clarification_repair
- everyday_decisions
- polite_disagreement_and_apology
- feelings_and_reassurance

ممنوع في توسعة corpus: أي حوار عن إدارة المشروع، مراحل البناء، تشغيل
الوكيل، التدريب، tokenizer، أو أي نقاش هندسي داخلي. هذه الأنماط أصبحت
`training_forbidden_operational_internal_dialogue`.

## ما أُضيف

- `eval/prompts/dialogue_v2.json`
- `sf_ai/evaluation/phase27.py`
- `scripts/phase27_dialogue_eval.py`
- `make phase27-dialogue-eval`
- `GET /system/phase27-dialogue-eval`
- `eval/reports/dialogue_eval_v2.json`
- `artifacts/reports/phase27_dialogue_eval_v2_report.json`

## القرار

لا نبدأ `SF-50M` الآن، ولا نبدأ Phase 28. المسار الصحيح:

1. corpus gate اكتمل: الحالة الحالية `5143` داخل `msa + saudi`.
2. إعادة `corpus-audit` عند أي إضافة لاحقة.
3. إعادة تدريب/تحسين `SF-10M` على corpus الحالي.
4. إعادة canary.
5. إعادة `make phase26-readiness`.
6. فتح `SF-50M` فقط إذا اختفت blockers.
