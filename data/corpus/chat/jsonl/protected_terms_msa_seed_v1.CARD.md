# protected_terms_msa_seed_v1

## Purpose

MSA protected-terms coverage seed for SF.AI tokenization policy and Phase 22
corpus balance.

This seed converts a small set of project-authored MSA operational terms into
governed chat records. It is corpus data, unlike the candidate term banks under
`resources/tokenization/`.

## Counts

- Records: 22
- Domain: chat
- Language: Arabic
- Dialect: `msa`
- Quality: `gold`
- Training allowed: true
- User scope: `single_user`
- Owner user: `sami-local`
- Created by user: `sami-local`
- Target user: `sami-local`

## Provenance

- Source: `sf-ai-owner-delegated-agent-authored-msa-tokenization-terms-v1`
- License: `owner-approved-for-sf-ai-training`
- Authoring mode: owner-delegated agent-authored

## Scope

The records cover MSA operational terms such as:

- مرحلة / خطة / بوابة / جاهزية
- حوكمة / مصدر / رخصة / جودة
- تدريب / تفعيل / تشغيل
- نموذج لغوي / نموذج سيادي
- قالب ثابت / توليد مقنع
- سيادة معرفية / corpus سيادي / tokenizer v2

## Safety

- No medical, legal, finance, security, or religious advice.
- No external dataset copied.
- No pretrained model output.
- No raw SF-10M output included.

## Validation

Run:

```bash
.venv/bin/python scripts/validate_dataset.py data/corpus/chat/jsonl/protected_terms_msa_seed_v1.jsonl
make corpus-audit
make tokenization-audit
```
