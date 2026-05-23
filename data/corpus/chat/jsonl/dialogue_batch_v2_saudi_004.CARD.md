# dialogue_batch_v2_saudi_004

## Purpose

Fourth Phase 22 Saudi dialogue batch for SF.AI Gold Dialogue Corpus v2.

This batch continues Saudi minimum coverage after `saudi_003`. It focuses on
clear project status, honest generator/runtime boundaries, data governance,
Saudi follow-up instructions, and the practical workflow Sami expects from the
agent.

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

- Source: `sf-ai-owner-delegated-agent-authored-saudi-v4`
- License: `owner-approved-for-sf-ai-training`
- Authoring mode: owner-delegated agent-authored

## Scope

The records cover:

- Current Phase 22 status and Saudi shortfall.
- Runtime vs training explanations in Saudi Arabic.
- Honest template/generator boundaries.
- Quality-focused corpus collection before tokenizer/model work.
- Saudi-style short/detail commands and project-following language.
- User-scoped provenance and agent-side execution responsibility.

## Safety

- No medical, legal, finance, security, or religious advice.
- No external dataset copied.
- No pretrained model output.
- No raw SF-10M output included.

## Validation

Run:

```bash
.venv/bin/python scripts/validate_dataset.py data/corpus/chat/jsonl/dialogue_batch_v2_saudi_004.jsonl
make corpus-audit
make phase22-readiness
```
