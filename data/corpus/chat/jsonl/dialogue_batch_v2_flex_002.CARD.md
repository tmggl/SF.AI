# dialogue_batch_v2_flex_002

## Purpose

Second flexible Phase 22 dialogue batch for SF.AI Gold Dialogue Corpus v2.

This batch continues the post-minimum flexible collection stage after both
current language tracks passed their minimum coverage. It adds 25 reviewed
dialogue records toward the 500-record Phase 22 target.

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

- Source: `sf-ai-owner-delegated-agent-authored-flex-v2`
- License: `owner-approved-for-sf-ai-training`
- Authoring mode: owner-delegated agent-authored

## Scope

The records cover:

- Natural social dialogue rather than stiff status reports.
- Honest distinction between UI templates and native generation.
- Repetition/hallucination awareness without treating raw model output as data.
- Continuation commands such as "اكمل" and "التالي".
- Runtime vs training vs corpus readiness.
- MSA + Saudi-only policy and Saudi Seed v1 as reference.
- Server continuity and push-only-after-success workflow.

## Safety

- No medical, legal, finance, security, or religious advice.
- No external dataset copied.
- No pretrained model output.
- No raw SF-10M output included.

## Validation

Run:

```bash
.venv/bin/python scripts/validate_dataset.py data/corpus/chat/jsonl/dialogue_batch_v2_flex_002.jsonl
make corpus-audit
make phase22-readiness
```
