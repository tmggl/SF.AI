# PHASE12_PREFLIGHT_REPORT.md

## SF.AI — Phase 12 Preflight Report

**الحالة:** جاهز تقنيًا لبدء Phase 12، لكن التدريب لم يبدأ ولا يبدأ إلا بإذن صريح من سامي.

آخر توجيه حاكم:

> لا تبدأ Phase 12 قبل إذن صريح.

---

## 1. Corpus Readiness

الأمر:

```bash
make corpus-audit
```

النتيجة الحالية:

```text
total_records   : 30
training_ready  : 30
issues          : 0
dialects        : saudi: 30
quality         : gold: 30
status          : READY_FOR_PHASE_12_TOKENIZER_TRAINING
```

المصادر:

```text
sf-ai-saudi-seed-v1-derived-dialogue-seed       : 20
sf-ai-saudi-seed-v1-protected-terms-coverage   : 10
```

الملفات:

```text
data/corpus/chat/jsonl/first_dialogue_seed.jsonl
data/corpus/chat/jsonl/protected_terms_seed_v1.jsonl
```

كل سجل يحتوي:

- `source`
- `license`
- `language`
- `dialect`
- `quality`
- `training_allowed=true`

---

## 2. Tokenization Policy Readiness

الأمر:

```bash
make tokenization-audit ARGS="--show-missing"
```

النتيجة الحالية:

```text
protected_terms_total   : 30
protected_terms_covered : 30
coverage_ratio          : 100.00%
missing protected terms : none
status                  : READY_FOR_PHASE12_TOKENIZATION_PREFLIGHT
```

الموارد:

```text
resources/tokenization/protected_terms_saudi.txt
resources/tokenization/preferred_merges.txt
resources/tokenization/tokenization_rules.yaml
```

القواعد المثبتة:

- UTF-8 إلزامي.
- لا pretrained vocab.
- لا pretrained merges.
- tokenizer يتعلم من corpus السيادي فقط.
- الكلمات السعودية المحمية يجب أن تخضع لفحص splitting.

---

## 3. Source Inventory

الأمر:

```bash
make source-inventory
```

النتيجة الحالية:

```text
phase12_status          : READY_FOR_PHASE_12_TOKENIZER_TRAINING
source_count            : 4
chat_training_records   : 30
local_reference_records : 1548
```

المصادر:

| المصدر | الحالة | الاستخدام |
|--------|--------|-----------|
| `chat_training_jsonl` | ready | Corpus مباشر لPhase 12 |
| `saudi_dialect_training_tasks_seed_v1` | reference_ready | مرجع/مرشح تحويل لاحق |
| `saudi_seed_v1_lexicon_reference` | reference_ready | قاموس خاص، ليس corpus مباشر |
| `mo3jam_saudi_import_slot` | empty_permission_gated | مؤجل بإذن |

---

## 4. Server Status

الأمر:

```bash
make server-status
```

الحالة الحالية:

```text
127.0.0.1:8123 listening
GET /health → {"status":"ok","project":"SF.AI","phase":"Phase 11"}
```

قرار Phase 12 الموحّد:

```text
GET /system/phase12-readiness
preflight_pass=false
can_train_now=false
training_permission_granted=false
missing_required_dialects=["msa"]
required_confirmation_flag=--confirm-phase12-permission
```

والقرار نفسه متاح من الطرفية بدون restart للسيرفر:

```bash
make phase12-readiness
```

قاعدة التشغيل:

- لا توقف السيرفر إذا كان يعمل.
- لا تستخدم `pkill` أو restart إلا بطلب صريح.
- استخدم `make server-status` للفحص.
- استخدم `make server-start` فقط إذا كان السيرفر متوقفًا.

---

## 5. Training Boundary

لم يتم تشغيل:

```bash
make train-bpe
make train-lm
```

ولم تُكتب:

```text
artifacts/tokenizers/*/vocab.json
artifacts/tokenizers/*/merges.txt
artifacts/checkpoints/*
artifacts/logs/*
```

جاهزية preflight لا تعني بدء التدريب.

كما أن أمر التدريب نفسه مغلق ببوابة تنفيذية:

```text
--confirm-phase12-permission
```

بدون هذا العلم، يرفض `make train-bpe` و`scripts/train_bpe.py` البدء ولا يكتبان أي tokenizer artifacts.

---

## 6. Known Constraints

- corpus الحالي صغير جدًا: 30 سجلًا فقط.
- مناسب لاختبار pipeline وtokenizer smoke، وليس لبناء نموذج قوي.
- كل البيانات سعودية gold؛ لا توجد عينات MSA بعد في corpus الحالي.
- ملف مهام اللهجة السعودية 1032 سجل موجود كمرجع محلي، لكنه ليس LM corpus مباشرًا.
- قاموس Saudi Seed v1 موجود كمرجع خاص، ولا يرفع payload الكامل ولا يدخل كحوار مباشر.

---

## 7. Required Command If Sami Approves Phase 12 Later

لا تنفذ إلا بعد إذن صريح:

```bash
make train-bpe ARGS="--confirm-phase12-permission --corpus data/corpus/chat/jsonl --out artifacts/tokenizers/sf_bpe/v1"
```

بعد التدريب يجب إنشاء report مستقل يوضح:

- corpus المستخدم.
- tokenization rules المستخدمة.
- protected terms coverage بعد التدريب.
- vocab/merges provenance.
- `sf_origin=true`.
- عدم استخدام pretrained vocab/merges.

---

## 8. Decision

```text
Phase 12 corpus/tokenization preflight: PASS
Phase 12 language-balance gate: MISSING msa
Training permission: NOT GRANTED
Action now: STOP before training
```
