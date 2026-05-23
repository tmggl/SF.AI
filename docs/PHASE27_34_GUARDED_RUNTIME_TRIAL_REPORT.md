# Phase 27.34 — Guarded Runtime Trial

## الهدف

ربط checkpoint الناجح من Phase 27.33 بمسار الواجهة/API كتجربة محروسة، بدون جعله runtime افتراضيًا مخفيًا.

## ما أُضيف

- حقل طلب جديد في `/chat/message`:

```json
{"generator_trial": true}
```

- زر في الواجهة باسم `مولّد تجريبي`.
- مسار Orchestrator منفصل للتجربة يستخدم:
  - tokenizer: `artifacts/tokenizers/sf_bpe/v4_min_lexical`
  - checkpoint: `artifacts/eval/phase27_33_advice_micro_stabilization/checkpoints/sf-10m-step9800`
  - generator metadata: `sf_10m_phase27_33`
- fallback واضح إلى `template` إذا فشل policy أو guard.
- استمرار الهوية والمجالات الحساسة على القوالب/المؤلف الآمن.

## نتيجة البوابة

```text
Phase 27.34 guarded runtime trial
passed: 9/9
status: PASSED_GUARDED_RUNTIME_TRIAL_READY_FOR_UI_TEST
```

| النوع | النتيجة |
|---|---:|
| generator prompts | 7/7 |
| template/safety controls | 2/2 |
| ui_test_allowed | true |
| sf50m_allowed | false |

## ماذا تستطيع تجربته الآن؟

افتح:

```text
http://127.0.0.1:8123/ui/chat
```

فعّل زر:

```text
مولّد تجريبي
```

ثم جرّب:

- `كيفك اليوم`
- `شكرًا لمساعدتك`
- `وجهني بخطوة بسيطة`
- `رتب لي يومي بسرعة`
- `توترت شوي وش اسوي`
- `وش المقصود بالاحترام`
- `القراية تفيدني بشي`

في التشخيص يجب أن يظهر:

```text
مولّد SF-10M Phase 27.33
```

أو `قالب ثابت` إذا حجب الحارس الرد.

## حدود المرحلة

- هذا ليس فتحًا عامًا للمولّد.
- لا يزال `SF-50M` محجوبًا.
- ردود raw generator لا تدخل corpus التدريب.
- أي export يحتوي `sf_10m_phase27_33` يبقى review evidence فقط.

## القرار

Phase 27.34 يفتح تجربة واجهة محلية محروسة لسامي فقط. المرحلة التالية:

```text
Phase 27.35 — live UI trial observations
```
