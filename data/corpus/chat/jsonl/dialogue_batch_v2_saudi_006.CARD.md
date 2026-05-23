# dialogue_batch_v2_saudi_006

## Purpose

Sixth Phase 22 Saudi dialogue batch for SF.AI Gold Dialogue Corpus v2.

This batch continues Saudi minimum coverage after `saudi_005`. It focuses on
gate-driven continuation, short user commands, honest generator status,
runtime vs training boundaries, and provenance-aware corpus work.

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

- Source: `sf-ai-owner-delegated-agent-authored-saudi-v6`
- License: `owner-approved-for-sf-ai-training`
- Authoring mode: owner-delegated agent-authored

## Scope

The records cover:

- Continuing Phase 22 through `saudi_006` without jumping phases.
- Explaining Saudi shortfall and remaining corpus counts.
- Reinforcing that current UI templates are not a convincing generator.
- Agent autonomy under documented gates.
- Corpus validation, server checks, and push discipline.
- User-scoped provenance for future multi-user separation.

## Safety

- No medical, legal, finance, security, or religious advice.
- No external dataset copied.
- No pretrained model output.
- No raw SF-10M output included.

## Validation

Run:

```bash
.venv/bin/python scripts/validate_dataset.py data/corpus/chat/jsonl/dialogue_batch_v2_saudi_006.jsonl
make corpus-audit
make phase22-readiness
```
