# dialogue_batch_v2_msa_002

## Purpose

Second Phase 22 MSA dialogue batch for SF.AI Gold Dialogue Corpus v2.

This batch also locks the operational rule that Sami does not need to save,
export, or manually approve corpus dialogues during Phase 22. The agent authors,
reviews, approves, validates, documents, and pushes successful work.

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

- Source: `sf-ai-owner-delegated-agent-authored-msa-v2`
- License: `owner-approved-for-sf-ai-training`
- Authoring mode: owner-delegated agent-authored

## Scope

The records cover:

- Agent-side autonomous execution.
- No user-side save/export workflow requirement.
- User-scoped corpus ownership.
- Phase 22 batch progress.
- Template versus generator honesty.
- Corpus quality, audit, and completion gates.

## Safety

- No medical, legal, finance, security, or religious advice.
- No external dataset copied.
- No pretrained model output.
- No raw SF-10M output included.

## Validation

Run:

```bash
make corpus-audit
make phase22-readiness
```
