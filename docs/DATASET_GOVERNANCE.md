# DATASET_GOVERNANCE.md

## Dataset Governance

هذه الوثيقة تثبت قواعد datasets قبل Phase 12.

## الحقول الإلزامية

كل سجل training يجب أن يحتوي:

```json
{
  "domain": "chat",
  "lang": "ar",
  "messages": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "provenance": {
    "source": "...",
    "license": "...",
    "language": "ar",
    "dialect": "msa أو saudi",
    "quality": "gold أو silver أو bronze",
    "training_allowed": true
  }
}
```

## قواعد القبول

- `source` إلزامي.
- `license` إلزامي.
- `quality` إلزامي.
- `training_allowed=true` إلزامي.
- `dialect` إلزامي.
- `language=ar` في corpus الأول.
- `domain=chat` في corpus الأول.
- وجود user وassistant إلزامي.

## مصدر مقبول: owner-delegated agent-authored

سامي أعطى تفويضًا صريحًا في محادثة المشروع بتاريخ 2026-05-23 بأن أي حوار
يؤلفه الوكيل لخدمة corpus يُعتمد ولا ينتظر تعميدًا إضافيًا. لذلك تقبل
Phase 22 سجلات `owner-delegated agent-authored` بشرط الشفافية الكاملة:

- `source` بصيغة مثل `sf-ai-owner-delegated-agent-authored-msa-v1`.
- `license=owner-approved-for-sf-ai-training`.
- `training_allowed=true`.
- `quality=silver` افتراضيًا، ولا تصبح `gold` إلا بمراجعة بشرية لاحقة.
- `dialect` صريح: `msa` أو `saudi` فقط حاليًا.
- `notes` تذكر أن المالك فوّض التأليف والاعتماد، وأن النص ليس من dataset
  خارجي ولا من أوزان/قاموس/tokenizer جاهز.

هذا لا يفتح الباب لبيانات LLM خارجية أو مصادر مجهولة؛ بل يثبت قناة تأليف
داخلية موثقة ومحدودة لمشروع SF.AI.

## الممنوع

- corpus مجهولة.
- synthetic LLM data من مصدر خارجي أو غير موثق.
- agent-authored data بلا تفويض مالك واضح وبلا provenance.
- بيانات بلا license.
- بيانات بلا إذن تدريب.
- بيانات حساسة شخصية.
- copy من مصادر محمية بلا إذن.
- خلط lexicon payload مع chat corpus مباشرة.

## فصل datasets عن lexicons

```text
data/corpus/                 training/eval datasets
resources/lexicons/          references/runtime lexicons
```

أي تحويل من lexicon إلى dataset يجب أن ينتج ملفًا جديدًا داخل `data/corpus/` مع:

- source يشير للمرجع.
- license.
- training_allowed.
- quality.
- notes تشرح التحويل.

## Reports

تقارير البيانات تكون في:

```text
data/corpus/**/reports/
```

أو docs إذا كانت تقريرًا عامًا لا يحتوي payload خاص.

## Git

الافتراضي أن corpus خاص ومهمَل في `.gitignore`.

لا يرفع ملف corpus إلا إذا:

- صغير.
- مقصود.
- موثق.
- لا يحتوي أسرارًا.
- لديه CARD/README عند الحاجة.
- وافق سامي أو طلبه صراحة.

## الحالة الحالية

يوجد seed صغير:

```text
data/corpus/chat/jsonl/first_dialogue_seed.jsonl
```

وحالته:

- 20 records.
- Saudi.
- gold.
- training_allowed=true.
- يمر `make corpus-audit`.

هذا لا يعني بدء التدريب.
