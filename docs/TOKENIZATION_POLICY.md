# TOKENIZATION_POLICY.md

## سياسة Tokenization في SF.AI

هذه السياسة تحكم Phase 12 قبل تدريب SF-BPE tokenizer.

## المبادئ

- UTF-8 إلزامي.
- لا pretrained vocab.
- لا pretrained merges.
- tokenizer يتعلم من corpus السيادي فقط.
- الكلمات السعودية الشائعة لا تُكسر aggressively.
- protected terms مدعومة.
- preferred merges مدعومة.

## الموارد

```text
resources/tokenization/
├── protected_terms_saudi.txt
├── protected_terms_msa_candidate.txt
├── preferred_merges.txt
├── preferred_merges_msa_candidate.txt
└── tokenization_rules.yaml
```

## Protected Terms

protected terms هي كلمات أو عبارات يجب أن يحاول tokenizer الحفاظ عليها كقطع مستقرة.

أمثلة:

- `وش`
- `وشلون`
- `تكفى`
- `لا هنت`
- `الله لا يهينك`

هذه ليست vocab جاهزًا خارجيًا. هي policy محلية مشتقة من مرجع سعودي يملكه المشروع.

أضيفت أيضًا قائمة مرشحة للفصحى:

- `protected_terms_msa_candidate.txt`
- حجمها الحالي: 138 مصطلحًا/عبارة فصيحة.
- ليست active protected terms بعد.
- ليست corpus ولا vocab pretrained.
- تُفعّل تدريجيًا فقط عندما تغطيها دفعات corpus السيادية وتنجح audit.

## Preferred Merges

preferred merges هي أزواج أو سلاسل يُفضّل تعلمها مبكرًا إذا ظهرت في corpus.

هي توجيه سيادي، وليست merges pretrained.

أضيفت قائمة مرشحة للفصحى:

- `preferred_merges_msa_candidate.txt`
- لا تُرقّى إلى merges نشطة إلا إذا دعمها corpus السيادي.

لا تُستخدم إذا لم تكن مدعومة في implementation. عند إضافتها للتنفيذ يجب:

- اختبارها.
- توثيقها.
- حفظها في tokenizer provenance.

## منع splitting السيء

التقسيم السيء يعني مثلًا:

```text
وشلون → و ش ل و ن
تكفى → ت ك ف ى
```

هذا مقبول كمرحلة أولية قبل التعلم، لكنه غير مقبول كـ artifact نهائي إذا كانت الكلمة شائعة ومحمية.

Phase 12 يجب أن ينتج audit يراجع:

- protected terms token counts.
- average pieces per protected term.
- Saudi examples round-trip.
- MSA examples round-trip.

قبل Phase 12، شغّل preflight read-only:

```bash
make tokenization-audit
```

هذا يفحص:

- وجود قواعد YAML.
- وجود protected terms.
- وجود preferred merges.
- تغطية protected terms داخل corpus الحالي.
- عدم وجود pretrained policy.

ولا يدرّب tokenizer ولا يكتب artifacts.

## سياسة corpus

tokenizer يتعلم من:

- `data/corpus/...`
- سجلات تمر governance.

ولا يتعلم من:

- `resources/lexicons/...` مباشرة.
- docs.
- tests.
- external tokenizer.

إذا استُخدم lexicon كمرجع، يجب تحويله إلى corpus مشتق مع provenance.

## مخرجات tokenizer

المخرجات داخل:

```text
artifacts/tokenizers/
```

يجب أن تحتوي provenance يثبت:

- `sf_origin=true`.
- corpus path.
- tokenization rules hash أو path.
- protected terms path.
- candidate protected/preferred paths إن استُخدمت في audit.
- no pretrained vocab.

## تغيير السياسة

لا تغيّر:

- protected terms.
- preferred merges.
- tokenization rules.

إلا مع:

- تحديث docs.
- تحديث tests.
- ذكر السبب في commit.
