# dialogue_batch_v2_saudi_007

## Purpose

Seventh Phase 22 Saudi dialogue batch for SF.AI Gold Dialogue Corpus v2.

This is the final Saudi-minimum batch in Phase 22. It adds the last 20 Saudi
records needed to reach the current dialect minimum (`saudi=200`) while
keeping the project honest about the remaining total-record target.

## Counts

- Records: 20
- Domain: chat
- Language: Arabic
- Dialect: `saudi`
- Quality: `silver`
- Training allowed: true
- User scope: `single_user`
- Owner user: `sami-local`
- Created by user: `sami-local`
- Target user: `sami-local`

## Provenance

- Source: `sf-ai-owner-delegated-agent-authored-saudi-v7`
- License: `owner-approved-for-sf-ai-training`
- Authoring mode: owner-delegated agent-authored

## Scope

The records cover:

- Completing Saudi minimum coverage.
- Explaining why Phase 22 still needs 500 total records after dialect balance.
- Transition logic from Saudi batches to flex batches.
- Clear user-facing status reports for "وين وصلنا", "اختصر", and "فصل".
- Runtime/training honesty and no-generator-before-time messaging.
- MSA + Saudi-only language policy.

## Safety

- No medical, legal, finance, security, or religious advice.
- No external dataset copied.
- No pretrained model output.
- No raw SF-10M output included.

## Validation

Run:

```bash
.venv/bin/python scripts/validate_dataset.py data/corpus/chat/jsonl/dialogue_batch_v2_saudi_007.jsonl
make corpus-audit
make phase22-readiness
```
