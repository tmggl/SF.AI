# Phase 27.38 — Targeted Topic Curriculum/Probe

## الهدف

بناء probe تدريبي صغير لـ `SF-10M` على الموضوعات المحجوبة بعد Phase 27.37:

- `الصداقة`
- `الصدق`
- `التنظيم`
- `الهدوء`

هذه ليست مرحلة تكبير نموذج. لا `SF-50M` ولا Phase 28.

## ما حدث

دُرّب checkpoint تجريبي محدود:

```text
checkpoint: sf-10m-step2400
candidate_generator: sf_10m_phase27_38
training_scope: targeted SF-10M probe only
```

## النتيجة

```text
status     : PARTIAL_TARGETED_TOPIC_CURRICULUM_KEEP_CURRENT_RUNTIME
cases      : 6/20
regression : 6/8
new_topic  : 0/8
heldout    : 0/4
```

## التشخيص

المرشح الجديد لم ينجح في فتح الموضوعات المحجوبة. ظهر **topic collapse**:

- أسئلة `الصداقة` و`التنظيم` انجرفت إلى ردود `الاحترام`.
- أسئلة `الصدق` انجرفت إلى دعم/تهدئة أو عبارات عامة.
- أسئلة `الهدوء` انجرفت إلى `الاحترام` أو `القراءة`.
- regression خسر `التعاون` و`الصبر`.

لذلك:

```text
runtime_switch_allowed = false
```

## القرار

لا نبدّل مولّد الواجهة. يبقى runtime التجريبي على checkpoint السابق
`sf_10m_phase27_33` مع فتح `الصبر` من Phase 27.37 فقط.

## المرحلة التالية

```text
Phase 27.39 — repair failed targeted topics
```

التركيز التالي:

- تقليل خلط `الاحترام` مع بقية التعريفات.
- فصل كل موضوع بتوازن أعلى وعدسات تقييم أدق.
- عدم فتح أي موضوع جديد في الواجهة قبل اجتياز new_topic + heldout.

## artifacts

- `artifacts/reports/phase27_38_targeted_topic_curriculum_probe_report.json`
- `artifacts/samples/phase27_38_targeted_topic_curriculum_probe.md`
