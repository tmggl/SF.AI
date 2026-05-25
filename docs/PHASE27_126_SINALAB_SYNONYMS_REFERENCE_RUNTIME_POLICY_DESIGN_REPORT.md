# Phase 27.126 — Synonyms Reference Runtime Policy Design

## الخلاصة

تم تصميم سياسة runtime مستقبلية فقط. لا تفعيل lookup، لا ChatModule،
لا واجهة، لا corpus/tokenizer/training.

## القرار

```text
PHASE27_126_SINALAB_SYNONYMS_REFERENCE_RUNTIME_POLICY_DESIGN_DECISION
ALLOW_PHASE27_127_SYNONYMS_REFERENCE_RUNTIME_POLICY_ENFORCEMENT_NO_ACTIVATION
```

## Runtime Policy

- default mode: `disabled`
- allowed future output: `aggregate_signal_only`
- raw term display allowed: `False`
- query row display allowed: `False`
- fallback template masking allowed: `False`

## Logging Policy

- logs may contain raw query: `False`
- logs may contain raw terms: `False`
- logs may contain query rows: `False`
- logs may contain hashes/counts: `True`

## الممنوع

- runtime lookup activation.
- chat module integration.
- raw terms/query rows in git.
- UI term display.
- data/corpus writes.
- tokenizer vocab/merges.
- training.
- SF-50M transition.

## الملفات

- `resources/external_sources/phase27_126_sinalab_synonyms_reference_runtime_policy.json`
- `resources/external_sources/phase27_126_sinalab_synonyms_reference_runtime_policy_design_gate.json`
- `artifacts/reports/phase27_126_sinalab_synonyms_reference_runtime_policy_design_report.json`
- `artifacts/reports/PHASE27_126_SINALAB_SYNONYMS_REFERENCE_RUNTIME_POLICY_DESIGN_DECISION.json`

## التالي

```text
Phase 27.127 — Synonyms Reference Runtime Policy Enforcement, no activation
```
