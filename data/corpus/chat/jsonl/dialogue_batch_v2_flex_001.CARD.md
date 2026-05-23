# dialogue_batch_v2_flex_001

## Purpose

First flexible Phase 22 dialogue batch for SF.AI Gold Dialogue Corpus v2.

This batch starts the post-minimum flexible collection stage after both current
language tracks reached their minimum coverage:

- `msa=200`
- `saudi=200`

The batch adds 25 reviewed dialogue records toward the 500-record Phase 22
target.

## Counts

- Records: 25
- Domain: chat
- Language: Arabic
- Dialects: `msa`, `saudi`
- MSA records: 12
- Saudi records: 13
- Quality: `silver`
- Training allowed: true
- User scope: `single_user`
- Owner user: `sami-local`
- Created by user: `sami-local`
- Target user: `sami-local`

## Provenance

- Source: `sf-ai-owner-delegated-agent-authored-flex-v1`
- License: `owner-approved-for-sf-ai-training`
- Authoring mode: owner-delegated agent-authored

## Scope

The records cover:

- Phase 22 status reporting after dialect balance completion.
- Honest runtime vs training vs generator expectations.
- MSA + Saudi-only language policy.
- Corpus governance and user ownership fields.
- Protected terms and tokenization policy basics.
- Progressive scaling and no-jump model growth.
- Agent workflow: continue, test, document, and push only successful work.

## Safety

- No medical, legal, finance, security, or religious advice.
- No external dataset copied.
- No pretrained model output.
- No raw SF-10M output included.

## Validation

Run:

```bash
.venv/bin/python scripts/validate_dataset.py data/corpus/chat/jsonl/dialogue_batch_v2_flex_001.jsonl
make corpus-audit
make phase22-readiness
```
