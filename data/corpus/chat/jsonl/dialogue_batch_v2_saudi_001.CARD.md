# dialogue_batch_v2_saudi_001

## Purpose

First Phase 22 Saudi dialogue batch for SF.AI Gold Dialogue Corpus v2.

This batch starts the Saudi coverage push after the MSA minimum reached
200 records. It uses practical, owner-delegated Saudi conversations about
project status, templates vs generator, corpus governance, direct agent-side
execution, testing, and next-step discipline.

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

- Source: `sf-ai-owner-delegated-agent-authored-saudi-v1`
- License: `owner-approved-for-sf-ai-training`
- Authoring mode: owner-delegated agent-authored

## Scope

The records cover:

- Natural Saudi next-step questions.
- Honest distinction between templates, UI testing, and native generation.
- Difference between lexicons and training data.
- Saudi dialogue authoring style without exaggeration.
- Phase 22 gates, corpus counts, and direct agent-side workflow.
- Provenance fields and user-scoped records.
- Handling correction, confusion, short commands, and status requests.

## Safety

- No medical, legal, finance, security, or religious advice.
- No external dataset copied.
- No pretrained model output.
- No raw SF-10M output included.

## Validation

Run:

```bash
.venv/bin/python scripts/validate_dataset.py data/corpus/chat/jsonl/dialogue_batch_v2_saudi_001.jsonl
make corpus-audit
make phase22-readiness
```
