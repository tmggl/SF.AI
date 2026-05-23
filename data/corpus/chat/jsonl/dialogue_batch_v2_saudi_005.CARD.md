# dialogue_batch_v2_saudi_005

## Purpose

Fifth Phase 22 Saudi dialogue batch for SF.AI Gold Dialogue Corpus v2.

This batch teaches SF.AI the user's standing instruction that "اكمل" and
"التالي" mean continue the correct project line according to the gates. It
also expands Saudi conversational examples around honesty, generator status,
project management, corpus governance, and agent autonomy.

## Counts

- Records: 25
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

- Source: `sf-ai-owner-delegated-agent-authored-saudi-v5`
- License: `owner-approved-for-sf-ai-training`
- Authoring mode: owner-delegated agent-authored

## Scope

The records cover:

- Interpreting "اكمل" and "التالي" as delegated continuation.
- Saudi project-following language for Phase 22 gates.
- Honest separation of current templates from future generation.
- User trust, frustration repair, and concise progress reporting.
- Corpus governance, source/license discipline, and secret scanning.
- MSA + Saudi-only runtime/training scope.

## Safety

- No medical, legal, finance, security, or religious advice.
- No external dataset copied.
- No pretrained model output.
- No raw SF-10M output included.

## Validation

Run:

```bash
.venv/bin/python scripts/validate_dataset.py data/corpus/chat/jsonl/dialogue_batch_v2_saudi_005.jsonl
make corpus-audit
make phase22-readiness
```
