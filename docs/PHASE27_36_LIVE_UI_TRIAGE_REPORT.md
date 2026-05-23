# Phase 27.36 — Live UI Triage

## الهدف

جمع ملاحظات حية أوسع من واجهة/API المحادثة بعد فتح زر `مولّد تجريبي`، ثم
تصنيف ما يجب أن يذهب للمولّد وما يجب أن يبقى template حتى لا يرى سامي ردودًا
عشوائية.

هذه المرحلة لم تبدأ تدريبًا جديدًا، ولم تضف corpus.

## ما تغيّر

- أضيفت بوابة جودة داخل `ChatModule` للتجربة المحروسة:
  - تمنع raw `chat.general` من الذهاب للمولّد.
  - تمنع موضوعات التعريف غير المثبتة من الذهاب للمولّد.
  - تبقي المسارات المثبتة فقط على `sf_10m_phase27_33`.
- أضيفت تغطية routing لـ `الحمدلله`/`الحمد لله`/`بخير` حتى لا تذهب كـ general.
- أضيف أمر:

```text
make phase27-live-ui-triage
```

## نتيجة الاختبار الحي

```text
status        : PASSED_LIVE_UI_TRIAGE_QUALITY_FLOOR_ACTIVE
health_phase  : Phase 27.36
cases         : 27/27
generated     : 18/18
quality_floor : 5/5
controls      : 4/4
```

## المسارات التي يسمح لها بالمولّد الآن

- smalltalk
- thanks
- advice
- planning
- support
- definition: `الاحترام`
- definition: `التعاون`
- definition: `القراءة`

## المسارات التي حُجبت عمدًا

- raw `chat.general`
- تعريف موضوعات غير مثبتة مثل `الصبر`/`الصداقة`/`الصدق`
- الهوية والقدرات وشرح مراحل المشروع
- المجالات الحساسة مثل الطب

## قرار المرحلة

يظل زر `مولّد تجريبي` متاحًا لسامي، لكن داخل نطاقات مثبتة فقط. الافتراضي
يبقى template. لا `SF-50M` ولا Phase 28 حتى نوسع نوايا/موضوعات المولّد
ونعيد اختبارات الواجهة.

المرحلة التالية:

```text
Phase 27.37 — expand supported generator intents/topics before SF-50M
```

## artifacts

- `artifacts/reports/phase27_36_live_ui_triage_report.json`
- `artifacts/samples/phase27_36_live_ui_triage.md`
