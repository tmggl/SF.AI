# Phase 27.37 — Supported Topic Expansion

## الهدف

توسيع تجربة المولّد المحروسة بإضافة موضوع جديد فقط إذا كان ينجح دلاليًا،
مع إبقاء الموضوعات غير المستقرة خلف القالب.

هذه المرحلة لم تبدأ تدريبًا جديدًا، ولم تضف corpus.

## ما تغيّر

- أضيف موضوع `الصبر` إلى مسار definition المحروس.
- أضيف semantic topic guard بعد التوليد:
  - إذا كان الرد لا يحمل مفردات/معنى الموضوع، يُحجب ويرجع `template`.
  - السبب يظهر في التشخيص: `generation_guard:definition_topic_mismatch`.
- بقيت الموضوعات التالية محجوبة لأنها انحرفت عند القياس:
  - `الصداقة`
  - `الصدق`
  - `التنظيم`
  - `الهدوء`

## نتيجة الاختبار الحي

```text
status        : PASSED_SUPPORTED_TOPIC_EXPANSION_QUALITY_GATED
health_phase  : Phase 27.37
cases         : 21/21
generated     : 10/10
new_topic     : 3/3
quality_floor : 5/5
controls      : 3/3
```

## أمثلة مسموحة الآن للمولّد

```text
ما معنى الصبر
الصبر وش يعني
وش المقصود بالصبر
```

## أمثلة محجوبة عمدًا

```text
عرف الصبر
اشرح لي الصبر ببساطة
وش معنى الصداقة
اشرح الصدق
موضوع مفتوح
```

## القرار

يستمر زر `مولّد تجريبي`، وتضاف له قدرة محدودة جديدة: تعريف `الصبر`
بصيغ مثبتة. لا يزال `SF-50M` وPhase 28 محجوبين.

المرحلة التالية:

```text
Phase 27.38 — targeted topic curriculum/probe for blocked definitions
```

## artifacts

- `artifacts/reports/phase27_37_supported_topic_expansion_report.json`
- `artifacts/samples/phase27_37_supported_topic_expansion.md`
