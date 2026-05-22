"""Tokenization policy audit — read-only preflight before Phase 12."""

from __future__ import annotations

import json
from pathlib import Path

from sf_ai.models.tokenizer.policy_audit import (
    audit_tokenization_policy,
    load_plain_terms,
)


def test_load_plain_terms_ignores_comments_and_blanks(tmp_path: Path) -> None:
    terms = tmp_path / "terms.txt"
    terms.write_text("# comment\n\nوش\nتكفى\n", encoding="utf-8")
    assert load_plain_terms(terms) == ["وش", "تكفى"]


def test_tokenization_policy_audit_counts_protected_terms(tmp_path: Path) -> None:
    corpus = tmp_path / "data/corpus/chat/jsonl"
    corpus.mkdir(parents=True)
    (corpus / "seed.jsonl").write_text(
        json.dumps(
            {
                "domain": "chat",
                "lang": "ar",
                "messages": [
                    {"role": "user", "content": "وش معنى تكفى؟"},
                    {"role": "assistant", "content": "تكفى تعني رجاء بطلب مؤكد."},
                ],
                "provenance": {
                    "source": "test",
                    "license": "user-provided",
                    "language": "ar",
                    "dialect": "saudi",
                    "quality": "gold",
                    "training_allowed": True,
                },
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    protected = tmp_path / "protected.txt"
    preferred = tmp_path / "preferred.txt"
    rules = tmp_path / "rules.yaml"
    protected.write_text("وش\nتكفى\nلا هنت\n", encoding="utf-8")
    preferred.write_text("ت كفى\nلا هنت\n", encoding="utf-8")
    rules.write_text(
        """
encoding: utf-8
scope:
  current_dialects: [msa, saudi]
sovereignty:
  no_pretrained_vocab: true
  no_pretrained_merges: true
  learn_from_sovereign_corpus_only: true
normalization:
  arabizi_has_separate_normalization: true
  code_is_separate_from_dialogue: true
protected_terms:
  policy: avoid_aggressive_splitting
artifact_requirements:
  require_sf_origin: true
""".strip(),
        encoding="utf-8",
    )

    report = audit_tokenization_policy(
        corpus=corpus,
        protected_terms_path=protected,
        preferred_merges_path=preferred,
        rules_path=rules,
    )

    assert report.corpus_files == 1
    assert report.messages_seen == 2
    assert report.protected_terms_total == 3
    assert report.protected_terms_covered == 2
    assert {hit.term: hit.count for hit in report.protected_hits} == {
        "وش": 1,
        "تكفى": 2,
    }
    assert "لا هنت" in report.missing_terms
    assert report.status == "READY_FOR_PHASE12_TOKENIZATION_PREFLIGHT"


def test_real_tokenization_policy_audit_sees_current_seed() -> None:
    report = audit_tokenization_policy()
    assert report.corpus_files >= 1
    assert report.messages_seen >= 20
    assert report.protected_terms_total >= 20
    assert report.protected_terms_covered >= 10
    assert "وش" in {hit.term for hit in report.protected_hits}
    assert report.rules["sovereignty"]["no_pretrained_vocab"] is True
