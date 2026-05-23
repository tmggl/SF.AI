# dialogue_batch_v2_saudi_003

## Purpose

Third Phase 22 Saudi dialogue batch for SF.AI Gold Dialogue Corpus v2.

This batch continues Saudi minimum coverage after `saudi_001` and `saudi_002`.
It focuses on project-following language, honest generator status, corpus
governance, Saudi user instructions, and practical agent execution behavior.

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

- Source: `sf-ai-owner-delegated-agent-authored-saudi-v3`
- License: `owner-approved-for-sf-ai-training`
- Authoring mode: owner-delegated agent-authored

## Scope

The records cover:

- Saudi next-step and phase-tracking dialogue.
- Difference between templates, corpus, tokenizer, and future generation.
- Honest correction when current runtime is not a convincing generator.
- Owner-delegated corpus authoring and provenance requirements.
- Saudi follow-up, clarification, objection, and concise/detail mode.
- MSA + Saudi language-scope discipline.

## Safety

- No medical, legal, finance, security, or religious advice.
- No external dataset copied.
- No pretrained model output.
- No raw SF-10M output included.

## Validation

Run:

```bash
.venv/bin/python scripts/validate_dataset.py data/corpus/chat/jsonl/dialogue_batch_v2_saudi_003.jsonl
make corpus-audit
make phase22-readiness
```
