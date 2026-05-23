# dialogue_batch_v2_flex_003

## Purpose

Third flexible Phase 22 dialogue batch for SF.AI Gold Dialogue Corpus v2.

This batch focuses on natural user-facing dialogue: frustration, trust,
short continuation commands, honest generator status, and concise progress
updates. It adds 25 reviewed dialogue records toward the 500-record Phase 22
target.

## Counts

- Records: 25
- Domain: chat
- Language: Arabic
- Dialects: `msa`, `saudi`
- MSA records: 13
- Saudi records: 12
- Quality: `silver`
- Training allowed: true
- User scope: `single_user`
- Owner user: `sami-local`
- Created by user: `sami-local`
- Target user: `sami-local`

## Provenance

- Source: `sf-ai-owner-delegated-agent-authored-flex-v3`
- License: `owner-approved-for-sf-ai-training`
- Authoring mode: owner-delegated agent-authored

## Scope

The records cover:

- Natural social responses to frustration and urgency.
- Honest "not ready yet" generator messaging.
- Short commands such as "اكمل", "طيب", and "اختصر".
- Avoiding false claims about model quality.
- Refusing to train on raw broken model output.
- MSA + Saudi-only policy.
- Phase 22 acceptance criteria and next-step reporting.

## Safety

- No medical, legal, finance, security, or religious advice.
- No external dataset copied.
- No pretrained model output.
- No raw SF-10M output included.

## Validation

Run:

```bash
.venv/bin/python scripts/validate_dataset.py data/corpus/chat/jsonl/dialogue_batch_v2_flex_003.jsonl
make corpus-audit
make phase22-readiness
```
