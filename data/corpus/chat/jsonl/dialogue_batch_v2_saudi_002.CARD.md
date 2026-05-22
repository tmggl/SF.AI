# dialogue_batch_v2_saudi_002

## Purpose

Second Phase 22 Saudi dialogue batch for SF.AI Gold Dialogue Corpus v2.

This batch continues the Saudi coverage push after `saudi_001`. It focuses on
natural Saudi follow-up behavior, honest generator status, corpus governance,
project tracking, and practical user-agent workflow.

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

- Source: `sf-ai-owner-delegated-agent-authored-saudi-v2`
- License: `owner-approved-for-sf-ai-training`
- Authoring mode: owner-delegated agent-authored

## Scope

The records cover:

- Saudi next-step and status questions.
- Honest separation of UI, templates, and future native generation.
- Why raw SF-10M output must not enter quality corpus.
- Saudi conversational repair, clarification, and follow-up.
- Testing, secret scanning, and push discipline.
- MSA + Saudi language policy and Saudi Seed reference status.

## Safety

- No medical, legal, finance, security, or religious advice.
- No external dataset copied.
- No pretrained model output.
- No raw SF-10M output included.

## Validation

Run:

```bash
.venv/bin/python scripts/validate_dataset.py data/corpus/chat/jsonl/dialogue_batch_v2_saudi_002.jsonl
make corpus-audit
make phase22-readiness
```
