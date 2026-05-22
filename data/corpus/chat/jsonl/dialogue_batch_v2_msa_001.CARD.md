# dialogue_batch_v2_msa_001

## Purpose

First Phase 22 MSA dialogue batch for SF.AI Gold Dialogue Corpus v2.

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

- Source: `sf-ai-owner-delegated-agent-authored-msa-v1`
- License: `owner-approved-for-sf-ai-training`
- Authoring mode: owner-delegated agent-authored
- Owner instruction: Sami explicitly delegated agent authoring and approval in project chat on 2026-05-23.

## Scope

The records cover:

- Runtime versus training.
- Template replies versus model generation.
- Corpus provenance.
- Phase 22 readiness gates.
- Tokenization policy.
- Saudi/MSA language scope.
- Progressive scaling and evaluation.

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
