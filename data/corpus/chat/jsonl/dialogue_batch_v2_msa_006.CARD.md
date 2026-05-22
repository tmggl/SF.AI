# dialogue_batch_v2_msa_006

## Purpose

Sixth Phase 22 MSA dialogue batch for SF.AI Gold Dialogue Corpus v2.

This batch adds practical MSA conversations about focused session authoring,
follow-up behavior, honest capability boundaries, testing discipline, endpoint
status, batch naming, and the remaining Phase 22 MSA/Saudi balance work.

## Counts

- Records: 25
- Domain: chat
- Language: Arabic
- Dialect: `msa`
- Quality: `silver`
- Training allowed: true
- User scope: `single_user`
- Owner user: `sami-local`
- Created by user: `sami-local`
- Target user: `sami-local`

## Provenance

- Source: `sf-ai-owner-delegated-agent-authored-msa-v6`
- License: `owner-approved-for-sf-ai-training`
- Authoring mode: owner-delegated agent-authored

## Scope

The records cover:

- Focused topic selection for reviewable sessions.
- Natural follow-up questions in MSA.
- Requesting clarification without overloading the user.
- Honest distinction between UI, templates, raw generator, and future model.
- Test-before-push discipline.
- Endpoint and local server status.
- Dialogue batch naming and card requirements.
- Phase 22 completion conditions.

## Safety

- No medical, legal, finance, security, or religious advice.
- No external dataset copied.
- No pretrained model output.
- No raw SF-10M output included.

## Validation

Run:

```bash
.venv/bin/python scripts/validate_dataset.py data/corpus/chat/jsonl/dialogue_batch_v2_msa_006.jsonl
make corpus-audit
make phase22-readiness
```
