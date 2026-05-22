"""Tokenization policy audit before Phase 12.

This is a preflight report only. It does not train a tokenizer, write
artifacts, or learn merges.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from sf_ai.datasets.chat_dataset import ChatDataset


@dataclass(frozen=True)
class ProtectedTermHit:
    term: str
    count: int


@dataclass(frozen=True)
class TokenizationPolicyAuditReport:
    corpus: Path
    protected_terms_path: Path
    preferred_merges_path: Path
    rules_path: Path
    corpus_files: int
    messages_seen: int
    protected_terms_total: int
    protected_terms_covered: int
    protected_hits: tuple[ProtectedTermHit, ...] = ()
    missing_terms: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    rules: dict[str, Any] = field(default_factory=dict)

    @property
    def coverage_ratio(self) -> float:
        if self.protected_terms_total == 0:
            return 0.0
        return self.protected_terms_covered / self.protected_terms_total

    @property
    def status(self) -> str:
        if self.warnings:
            return "READY_WITH_WARNINGS"
        return "READY_FOR_PHASE12_TOKENIZATION_PREFLIGHT"


def load_plain_terms(path: str | Path) -> list[str]:
    """Load UTF-8 term list, ignoring blank lines and comments."""
    p = Path(path)
    terms: list[str] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        term = line.strip()
        if not term or term.startswith("#"):
            continue
        terms.append(term)
    return terms


def load_tokenization_rules(path: str | Path) -> dict[str, Any]:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("tokenization rules must be a YAML mapping")
    return raw


def _validate_rules(rules: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    if rules.get("encoding") != "utf-8":
        warnings.append("encoding must be utf-8")

    sovereignty = rules.get("sovereignty") or {}
    if sovereignty.get("no_pretrained_vocab") is not True:
        warnings.append("no_pretrained_vocab must be true")
    if sovereignty.get("no_pretrained_merges") is not True:
        warnings.append("no_pretrained_merges must be true")
    if sovereignty.get("learn_from_sovereign_corpus_only") is not True:
        warnings.append("learn_from_sovereign_corpus_only must be true")

    scope = rules.get("scope") or {}
    if scope.get("current_dialects") != ["msa", "saudi"]:
        warnings.append("current_dialects must be exactly ['msa', 'saudi']")

    normalization = rules.get("normalization") or {}
    if normalization.get("arabizi_has_separate_normalization") is not True:
        warnings.append("Arabizi must have separate normalization")
    if normalization.get("code_is_separate_from_dialogue") is not True:
        warnings.append("code must stay separate from dialogue")

    return warnings


def audit_tokenization_policy(
    *,
    corpus: str | Path = "data/corpus/chat/jsonl",
    protected_terms_path: str | Path = "resources/tokenization/protected_terms_saudi.txt",
    preferred_merges_path: str | Path = "resources/tokenization/preferred_merges.txt",
    rules_path: str | Path = "resources/tokenization/tokenization_rules.yaml",
) -> TokenizationPolicyAuditReport:
    corpus_path = Path(corpus)
    protected_path = Path(protected_terms_path)
    preferred_path = Path(preferred_merges_path)
    rules_file = Path(rules_path)

    protected_terms = load_plain_terms(protected_path)
    preferred_merges = load_plain_terms(preferred_path)
    rules = load_tokenization_rules(rules_file)
    warnings = _validate_rules(rules)

    if not protected_terms:
        warnings.append("protected terms list is empty")
    if not preferred_merges:
        warnings.append("preferred merges list is empty")

    dataset = ChatDataset(corpus_path)
    files = dataset.jsonl_files()
    counts = {term: 0 for term in protected_terms}
    messages_seen = 0
    for message in dataset.iter_messages(clean=False):
        messages_seen += 1
        text = message.content
        for term in protected_terms:
            if term in text:
                counts[term] += text.count(term)

    hits = tuple(
        ProtectedTermHit(term=term, count=count)
        for term, count in counts.items()
        if count > 0
    )
    missing = tuple(term for term, count in counts.items() if count == 0)

    if not files:
        warnings.append("corpus has no JSONL files")
    if messages_seen == 0:
        warnings.append("corpus has no messages")
    if not hits:
        warnings.append("none of the protected terms appear in the corpus")

    return TokenizationPolicyAuditReport(
        corpus=corpus_path,
        protected_terms_path=protected_path,
        preferred_merges_path=preferred_path,
        rules_path=rules_file,
        corpus_files=len(files),
        messages_seen=messages_seen,
        protected_terms_total=len(protected_terms),
        protected_terms_covered=len(hits),
        protected_hits=hits,
        missing_terms=missing,
        warnings=tuple(warnings),
        rules=rules,
    )
